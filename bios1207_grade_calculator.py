#!/usr/bin/env python3
"""
BIOS 1207 (Fall 2026) grade calculator.

Implements the grading policy from the course syllabus:

    In-class exams (4 midterms)        40%
    Final exam                         20%
    Incoming Knowledge Evals (IKEs)     5%
    Team In-Class Activities (TICAs)    5%
    Homework                           10%
    Group project                      20%
    Other writing assignments           5%
                                      ----
                                      105%  (5% built-in extra credit, capped at 100%)

Drop rules:
    - IKE + TICA sessions count equally; the 4 lowest (across both) are dropped.
    - Homework: lowest score dropped.
    - Writing assignments (6 total): lowest score dropped.

Normalization: raw composite / mean of the top 5% of the class (only ever helps,
capped at 100%). Letter cutoffs: A >= 90, B >= 80, C >= 70, D >= 60.

Usage:
    python3 bios1207_grade_calculator.py --template      # writes my_bios_grades.json
    python3 bios1207_grade_calculator.py my_bios_grades.json
    python3 bios1207_grade_calculator.py my_bios_grades.json --top5 96.5

All scores are percentages (0-100). A score may also be written as a string
"earned/possible", e.g. "18/20".
"""

import argparse
import json
import sys

WEIGHTS = {
    "midterms": 40.0,
    "final": 20.0,
    "ike": 5.0,
    "tica": 5.0,
    "homework": 10.0,
    "project": 20.0,
    "writing": 5.0,
}

LABELS = {
    "midterms": "Midterm exams (4)",
    "final": "Final exam",
    "ike_tica": "IKEs + TICAs",
    "homework": "Homework",
    "project": "Group project",
    "writing": "Writing assignments",
}

CUTOFFS = [("A", 90.0), ("B", 80.0), ("C", 70.0), ("D", 60.0)]
NUM_MIDTERMS = 4
IKE_TICA_DROPS = 4
HOMEWORK_DROPS = 1
WRITING_DROPS = 1

TEMPLATE = {
    "_help": "Scores are percentages (0-100) or 'earned/possible' strings. "
             "Leave a list empty / value null if not graded yet.",
    "midterms": [],
    "final": None,
    "ike": [],
    "tica": [],
    "homework": [],
    "project": None,
    "writing": [],
}


def parse_score(value):
    if isinstance(value, str) and "/" in value:
        earned, possible = value.split("/", 1)
        return 100.0 * float(earned) / float(possible)
    return float(value)


def mean_after_drops(scores, drops):
    """Average of scores after dropping the `drops` lowest (never drops everything)."""
    if not scores:
        return None
    kept = sorted(scores)[min(drops, len(scores) - 1):]
    return sum(kept) / len(kept)


def category_averages(data):
    """Return {category: (average or None, weight)} for the graded categories."""
    def lst(key):
        return [parse_score(v) for v in (data.get(key) or [])]

    def one(key):
        v = data.get(key)
        return None if v is None else parse_score(v)

    midterms = lst("midterms")
    if len(midterms) > NUM_MIDTERMS:
        sys.exit(f"Expected at most {NUM_MIDTERMS} midterm scores, got {len(midterms)}.")

    return {
        "midterms": (sum(midterms) / len(midterms) if midterms else None, WEIGHTS["midterms"]),
        "final": (one("final"), WEIGHTS["final"]),
        "ike_tica": (mean_after_drops(lst("ike") + lst("tica"), IKE_TICA_DROPS),
                     WEIGHTS["ike"] + WEIGHTS["tica"]),
        "homework": (mean_after_drops(lst("homework"), HOMEWORK_DROPS), WEIGHTS["homework"]),
        "project": (one("project"), WEIGHTS["project"]),
        "writing": (mean_after_drops(lst("writing"), WRITING_DROPS), WEIGHTS["writing"]),
    }


def composite(cats, fill=None):
    """Raw composite (capped at 100). Ungraded categories use `fill` (or are skipped)."""
    total = 0.0
    for avg, weight in cats.values():
        score = avg if avg is not None else fill
        if score is not None:
            total += weight * score / 100.0
    return min(total, 100.0)


def letter(score):
    for grade, cutoff in CUTOFFS:
        if score >= cutoff:
            return grade
    return "F"


def normalize(raw, top5):
    if not top5:
        return raw
    return min(100.0, max(raw, 100.0 * raw / top5))


def needed_on_final(cats, assume, top5):
    """Final-exam score needed for each letter grade, with other gaps filled by `assume`."""
    others = dict(cats)
    others["final"] = (None, WEIGHTS["final"])
    base = 0.0
    for key, (avg, weight) in others.items():
        if key == "final":
            continue
        score = avg if avg is not None else assume
        base += weight * score / 100.0
    scale = (top5 / 100.0) if top5 else 1.0
    results = []
    for grade, cutoff in CUTOFFS:
        target = cutoff * scale
        need = 100.0 * (target - base) / WEIGHTS["final"]
        results.append((grade, need))
    return results


def report(data, top5):
    cats = category_averages(data)

    print("\nBIOS 1207 — Fall 2026 grade estimate")
    print("=" * 52)
    print(f"{'Category':<24}{'Weight':>8}{'Average':>10}{'Points':>10}")
    print("-" * 52)
    graded_weight = 0.0
    for key, (avg, weight) in cats.items():
        if avg is None:
            print(f"{LABELS[key]:<24}{weight:>7.0f}%{'—':>10}{'—':>10}")
        else:
            graded_weight += weight
            print(f"{LABELS[key]:<24}{weight:>7.0f}%{avg:>9.1f}%{weight * avg / 100:>10.2f}")
    print("-" * 52)

    if graded_weight == 0:
        print("No scores entered yet.")
        return

    earned = composite(cats)
    current_avg = 100.0 * sum(w * a / 100 for a, w in cats.values() if a is not None) / graded_weight
    all_graded = graded_weight == sum(WEIGHTS.values())

    if all_graded:
        print(f"Raw composite (max 100):   {earned:6.2f}%")
        final = normalize(earned, top5)
        if top5:
            print(f"Normalized (top 5% = {top5:.1f}): {final:6.2f}%")
        print(f"Final letter grade:         {letter(final)}")
        return

    print(f"Points banked so far:       {earned:6.2f} of {graded_weight:.0f} graded")
    print(f"Current average on graded work: {current_avg:6.2f}%  ({letter(current_avg)})")
    projected = normalize(composite(cats, fill=current_avg), top5)
    print(f"Projected final grade if you keep this average: {projected:6.2f}%  ({letter(projected)})")
    print("  (includes the 5% built-in extra credit"
          + (f" and normalization to {top5:.1f}%" if top5 else "") + ")")

    if cats["final"][0] is None:
        print("\nScore needed on the FINAL EXAM"
              " (other ungraded work assumed at your current average):")
        for grade, need in needed_on_final(cats, current_avg, top5):
            if need <= 0:
                msg = "already locked in"
            elif need > 100:
                msg = f"{need:.1f}%  (not reachable on the final alone)"
            else:
                msg = f"{need:.1f}%"
            print(f"  {grade}: {msg}")


def main():
    parser = argparse.ArgumentParser(description="BIOS 1207 Fall 2026 grade calculator")
    parser.add_argument("scores", nargs="?", help="JSON file with your scores")
    parser.add_argument("--template", action="store_true",
                        help="write a blank my_bios_grades.json to fill in")
    parser.add_argument("--top5", type=float, default=None,
                        help="mean score of the top 5%% of the class, if announced")
    args = parser.parse_args()

    if args.template:
        with open("my_bios_grades.json", "w") as f:
            json.dump(TEMPLATE, f, indent=2)
        print("Wrote my_bios_grades.json — fill in your scores and rerun.")
        return
    if not args.scores:
        parser.print_help()
        return

    with open(args.scores) as f:
        data = json.load(f)
    report(data, args.top5)


if __name__ == "__main__":
    main()

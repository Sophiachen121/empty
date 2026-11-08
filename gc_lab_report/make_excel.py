"""Build the Excel workbook for the GC post-lab report.

Usage:
    python make_excel.py                 # blank template
    python make_excel.py my_run.csv      # load the Vernier Mini GC export

Sheet "Chromatogram": time/response data + a native Excel scatter chart (Figure 1).
Sheet "Peak Table":   enter retention time, area, and whether each peak is a
                      starting material (Y/N); % area and % starting material
                      are calculated with Excel formulas.
Sheet "Density":      three density trials with mean and standard deviation.
"""
import csv
import sys
from openpyxl import Workbook
from openpyxl.chart import ScatterChart, Reference, Series
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
bold = Font(bold=True)
fill = PatternFill("solid", fgColor="FFF2CC")  # yellow = cells you fill in

# --- Chromatogram -----------------------------------------------------------
ws = wb.active
ws.title = "Chromatogram"
ws.append(["Retention time (min)", "Detector response (mV)"])
for c in ws[1]:
    c.font = bold
rows = []
if len(sys.argv) > 1:
    with open(sys.argv[1], newline="", encoding="utf-8-sig") as f:
        for r in csv.reader(f):
            try:
                rows.append((float(r[0]), float(r[1])))
            except (ValueError, IndexError):
                continue  # skip header / blank lines
for r in rows:
    ws.append(r)
n = max(len(rows), 2) + 1
chart = ScatterChart()
chart.title = "Figure 1. Gas chromatogram of the unknown ester product"
chart.style = 13
chart.x_axis.title = "Retention time (min)"
chart.y_axis.title = "Detector response (mV)"
chart.legend = None
s = Series(Reference(ws, min_col=2, min_row=2, max_row=n),
           Reference(ws, min_col=1, min_row=2, max_row=n), title="Product sample")
s.marker.symbol = "none"
s.smooth = False
chart.series.append(s)
chart.x_axis.delete = False
chart.y_axis.delete = False
chart.height, chart.width = 9, 17
ws.add_chart(chart, "D2")
ws.column_dimensions["A"].width = 20
ws.column_dimensions["B"].width = 24

# --- Peak table -------------------------------------------------------------
pt = wb.create_sheet("Peak Table")
pt.append(["Peak", "Retention time (min)", "Peak area", "Assignment",
           "Starting material? (Y/N)", "% of total area"])
for c in pt[1]:
    c.font = bold
    c.alignment = Alignment(wrap_text=True)
for i in range(1, 7):
    r = i + 1
    pt.append([i, None, None, None, None, f'=IF(C{r}="","",C{r}/$C$9*100)'])
    for col in "BCDE":
        pt[f"{col}{r}"].fill = fill
pt["B9"], pt["C9"] = "Total area", "=SUM(C2:C7)"
pt["B10"], pt["C10"] = "Starting-material area", '=SUMIF(E2:E7,"Y",C2:C7)'
pt["B11"], pt["C11"] = "% starting material", "=IF(C9=0,\"\",C10/C9*100)"
for c in ("B9", "B10", "B11"):
    pt[c].font = bold
pt["C11"].number_format = "0.0"
for r in range(2, 8):
    pt[f"F{r}"].number_format = "0.0"
for col, w in zip("ABCDEF", (6, 20, 14, 22, 16, 14)):
    pt.column_dimensions[col].width = w

# --- Density ----------------------------------------------------------------
d = wb.create_sheet("Density")
d.append(["Trial", "Volume (mL)", "Mass (g)", "Density (g/mL)"])
for c in d[1]:
    c.font = bold
for i in range(1, 4):
    r = i + 1
    d.append([i, None, None, f'=IF(OR(B{r}="",C{r}=""),"",C{r}/B{r})'])
    d[f"B{r}"].fill = fill
    d[f"C{r}"].fill = fill
    d[f"D{r}"].number_format = "0.000"
d["C6"], d["D6"] = "Mean", "=AVERAGE(D2:D4)"
d["C7"], d["D7"] = "Std. dev.", "=STDEV(D2:D4)"
d["D6"].number_format = d["D7"].number_format = "0.000"
for col, w in zip("ABCD", (8, 14, 12, 16)):
    d.column_dimensions[col].width = w

out = "GC_ester_data.xlsx"
wb.save(out)
print(f"Saved {out} ({len(rows)} data points loaded)")

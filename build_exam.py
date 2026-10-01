from reportlab.lib.pagesizes import letter
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image, KeepTogether,
                                PageBreak, Table, TableStyle)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from PIL import Image as PILImage

FIG = "figs/"
ss = getSampleStyleSheet()
Q = ParagraphStyle("Q", parent=ss["Normal"], fontName="Helvetica", fontSize=10.5, leading=14,
                   leftIndent=18, firstLineIndent=-18, spaceBefore=4)
OPT = ParagraphStyle("O", parent=Q, leftIndent=48, firstLineIndent=-16, spaceBefore=0)
H = ParagraphStyle("H", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=13, alignment=1, leading=17)
C = ParagraphStyle("C", parent=ss["Normal"], fontName="Helvetica", fontSize=11, alignment=1, leading=15)
N = ParagraphStyle("N", parent=ss["Normal"], fontName="Helvetica", fontSize=10.5, leading=14)
BUL = ParagraphStyle("B", parent=N, leftIndent=18, bulletIndent=6)
KEY = ParagraphStyle("K", parent=N, fontSize=9.5, leading=12.5, leftIndent=22, firstLineIndent=-22, spaceAfter=4)
HDR = ParagraphStyle("HDR", parent=N, fontName="Helvetica-Bold", fontSize=10.5, spaceBefore=8, spaceAfter=4)

def tbl(rows):
    t = Table(rows, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.6, colors.black),
                           ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                           ("FONTSIZE", (0, 0), (-1, -1), 9.5),
                           ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6)]))
    return t

# Each item: (stem, options, answer_letter, explanation, extras) ; extras = fig name, width, or table rows
QS = [
("If the government places the same per-unit tax on insulin and on restaurant meals, then holding all other factors equal, how will the deadweight loss in each market compare?",
 ["The deadweight losses are equal.", "Neither has a deadweight loss due to the tax.", "Insulin has a larger deadweight loss.", "Restaurant meals have a larger deadweight loss."],
 "d", "Demand for insulin is very inelastic (few substitutes), so the tax barely reduces quantity. Restaurant meals have many substitutes (cooking at home), so demand is more elastic and the quantity falls more. More elastic means larger deadweight loss.", None),
("Priya and Marco are bakers. The table shows how many cakes or pies each can bake in one hour. Priya should specialize in baking _____, and Marco should specialize in baking _____.",
 ["cakes; pies", "pies; cakes", "cakes; cakes", "pies; pies"],
 "b", "Priya: 1 cake costs 3/6 = 0.5 pie. Marco: 1 cake costs 1/4 = 0.25 pie. Marco has the lower opportunity cost of cakes, so he bakes cakes. Priya's cost of 1 pie is 2 cakes vs. Marco's 4 cakes, so Priya bakes pies.",
 ("table", [["", "Cakes per hour", "Pies per hour"], ["Priya", "6", "3"], ["Marco", "4", "1"]])),
("The graphs show production possibilities for Countries A, B, C, and D. If A and B trade with each other, and C and D trade with each other, which countries would export computers?",
 ["A and C would export computers.", "A and D would export computers.", "B and D would export computers.", "B and C would export computers."],
 "c", "Opportunity cost of 1 computer (in tons of wheat): A = 30/10 = 3, B = 20/40 = 0.5, C = 40/20 = 2, D = 10/30 = 0.33. In each pair, the lower-cost country exports computers: B (vs. A) and D (vs. C).", ("fig", "q03", 5.6)),
("Why is the world unlikely to ever literally run out of lithium (used in batteries)?",
 ["As cheap-to-mine lithium is used up, its price will rise, encouraging conservation, recycling, new exploration, and the development of substitutes.",
  "There is an unlimited supply of lithium.", "The demand for lithium is not very high.", "As the demand for lithium increases, the supply of lithium increases as well."],
 "a", "Rising prices signal scarcity. Higher prices reduce quantity demanded, make costlier sources worth extracting, and reward inventing substitutes, all long before the resource literally runs out.", None),
("A flight from New York to Miami costs $450 and takes 3 hours. A train ticket costs $150 and takes 28 hours. Other things equal, what is the minimum value of time that would lead a rational traveler to fly rather than take the train?",
 ["$10 per hour", "$12 per hour", "$25 per hour", "$150 per hour"],
 "b", "Flying costs $300 more but saves 25 hours. $300 / 25 hours = $12 per hour. Anyone who values their time above $12/hour should fly.", None),
("When there is a surplus in a market, competition will:",
 ["drive the price up to the equilibrium price.", "cause the demand curve to shift right.", "drive the price down to the equilibrium price.", "cause the supply curve to increase.", "cause buyers to boycott sellers."],
 "c", "In a surplus, quantity supplied is greater than quantity demanded. Sellers with unsold goods compete by cutting prices until the market reaches equilibrium. The curves themselves do not shift.", None),
("At a price of $10, consumers buy 400 movie tickets per week. When the price falls to $8, consumers buy 600 tickets per week. Using the midpoint method, what is the price elasticity of demand? Is demand elastic or inelastic?",
 ["0.56; inelastic", "1.8; inelastic", "1.0; unit elastic", "1.8; elastic", "2.0; elastic"],
 "d", "%change in Q = 200 / 500 = 40%. %change in P = 2 / 9 = 22.2%. Elasticity = 40 / 22.2 = 1.8. Since 1.8 > 1, demand is elastic.", None),
("In a competitive market, sellers compete with other sellers, which tends to _____ prices, and buyers compete with other buyers, which tends to _____ prices.",
 ["raise; lower", "raise; raise", "lower; lower", "lower; raise", "have no effect on; have no effect on"],
 "d", "Sellers compete for customers by offering lower prices. Buyers compete for limited goods by offering higher prices. Together these forces push the market to equilibrium.", None),
("What are the total gains from trade (consumer surplus + producer surplus) at the free-market equilibrium?",
 ["$720", "$1,080", "$1,440", "$2,160", "$2,880"],
 "c", "Total surplus is the triangle between demand and supply up to Q = 120: ½ × 120 × ($30 - $6) = $1,440. (CS = ½ × 120 × 12 = $720; PS = ½ × 120 × 12 = $720.)", ("fig", "q09", 3.4)),
("Which statement is true?",
 ["The gains from trade are maximized at 16 units of output.", "A free market is likely to produce more than 10 units of output.",
  "Consumer surplus at the free-market equilibrium is $500.", "Buyers are willing to pay $80 for the 16th unit, and it costs sellers $20 to produce that unit.",
  "At 4 units of output, there are unexploited gains from trade."],
 "e", "At Q = 4, buyers value the unit at $80 but it costs only $20 to produce, so gains from trade are left on the table. Equilibrium is Q = 10, P = $50. CS = ½ × 10 × ($100 - $50) = $250. At Q = 16, the numbers are reversed (WTP $20, cost $80).", ("fig", "q10", 3.4)),
("Jake values his mountain bike at $300, and Nina values her surfboard at $400. Suppose Jake voluntarily trades his bike for Nina's surfboard.",
 ["This trade makes Nina worse off by $100.", "This trade makes Jake better off by $100.",
  "Jake must value the surfboard at $300 or more, and Nina must value the bike at $400 or more.",
  "This trade decreases total value by moving the bike and surfboard away from the people who valued them most."],
 "c", "A voluntary trade happens only if each person values what they get at least as much as what they give up. We don't know each person's exact gain, only these lower limits.", None),
("If these figures represent the market for tea, which figure shows the effect of an increase in the price of coffee?",
 ["Figure A", "Figure B", "Figure C", "Figure D"],
 "a", "Coffee and tea are substitutes. A higher coffee price increases demand for tea (demand shifts right), which is Figure A.", ("fig", "q12", 4.6)),
("A gym charges $40 per month for unlimited visits. What is the marginal fee for the 20th visit in a month?",
 ["$2.00", "$40.00", "$1.33", "$0"],
 "d", "The $40 is paid regardless of how many visits are made. One more visit adds nothing to what you pay, so the marginal fee is $0.", None),
("After a major snowstorm, the price of snow shovels in the affected town doubles. According to economists:",
 ["this is a clear example of sellers exploiting consumers.",
  "the higher price signals scarcity, encouraging buyers to economize and giving sellers an incentive to bring more shovels into the area.",
  "the higher price will lead firms to ship fewer shovels to the town.",
  "the increase in demand should cause the price of shovels to fall."],
 "b", "Prices carry information and incentives. A high price sends shovels to their highest-valued uses and draws more supply into the area.", None),
("You won a free ticket to see Taylor Swift (it cannot be resold). Beyoncé is performing the same night and is your next-best alternative. Beyoncé tickets cost $200, and you would be willing to pay up to $350 to see her. There are no other costs. What is the opportunity cost of seeing Taylor Swift?",
 ["$0", "$200", "$350", "$150", "$550"],
 "d", "By choosing Taylor Swift, you give up the net value of seeing Beyoncé: $350 (value) - $200 (price you'd have paid) = $150.", None),
("You must recommend one of two taxes to raise revenue. A $1 per pack cigarette tax would reduce the quantity sold from 2,200,000 to 2,000,000 packs. A $50,000 luxury tax on private jets would reduce the quantity sold from 80 to 40 jets. Both raise $2,000,000. If efficiency were your only goal, which tax would you recommend?",
 ["The cigarette tax, as it causes a smaller deadweight loss.", "The jet tax, as it causes a smaller deadweight loss.",
  "Neither, as they both cause the same deadweight loss.", "There is not enough information to determine which causes the smaller deadweight loss."],
 "a", "DWL = ½ × tax × change in Q. Cigarettes: ½ × $1 × 200,000 = $100,000. Jets: ½ × $50,000 × 40 = $1,000,000. The cigarette tax is far more efficient because cigarette demand is less elastic.", None),
("During the oil shocks of the 1970s, gasoline prices rose sharply. Soon after, car makers began producing much more fuel-efficient cars. Why was this probably not a coincidence?",
 ["Large cars went out of fashion for unrelated reasons.", "The opportunity cost of building fuel-efficient cars rose.",
  "Car makers lacked any incentive to change their designs.", "Higher gasoline prices created an incentive to develop and buy cars that use less fuel."],
 "d", "Higher prices reward innovation that saves the scarce resource. Fuel efficiency became more valuable to buyers, so firms profited by supplying it.", None),
("A voluntary trade between two people occurs only when:",
 ["both people expect to be better off.", "both people will be worse off.", "one person gains exactly what the other person loses.", "the government approves the terms."],
 "a", "People agree to a voluntary trade only if each expects to gain. Trade creates value; it is not a zero-sum game.", None),
("A tax is imposed on sellers of pizza slices, shown as the shift from S<sub>1</sub> to S<sub>2</sub>. Sellers pay _____ of the tax per slice, and buyers pay _____.",
 ["$0.25; $0.75", "$0.75; $0.25", "$0; $1.00", "$0.50; $0.50"],
 "a", "The tax is $1.00 (the vertical gap between S<sub>1</sub> and S<sub>2</sub>). Buyers' price rises from $3.00 to $3.75 (+$0.75). Sellers keep $2.75, down $0.25 from $3.00.", ("fig", "q19", 3.5)),
("Each demand curve shows demand for landline phone service in a different year: 1995 (before cell phones were common), 2005 (cell phones widespread), and 2020 (smartphones and internet calling widespread). Assuming the only change is the number of available substitutes, which curve matches each year?",
 ["A: 2020, B: 2005, C: 1995", "A: 1995, B: 2005, C: 2020", "A: 2005, B: 1995, C: 2020", "A: 1995, B: 2020, C: 2005", "A: 2020, B: 1995, C: 2005"],
 "b", "More substitutes make demand more elastic (flatter). In 1995 there were few substitutes, so demand was steepest (A). By 2020 there were the most substitutes, so demand was flattest (C).", ("fig", "q20", 3.4)),
("Which area represents total consumer surplus at the free-market equilibrium?",
 ["Triangle AGM", "Triangle CGL", "Triangle EGM", "Triangle AEG"],
 "d", "Consumer surplus is the area below demand and above the equilibrium price (E), up to the equilibrium quantity (G): triangle AEG. EGM is producer surplus, and AGM is total surplus.", ("fig", "q21", 3.4)),
("A binding price ceiling on gasoline is MOST likely to result in:",
 ["long lines and wasted time searching for gas.", "a surplus of gasoline.", "higher-quality gasoline and better service at stations.", "more gas stations opening.", "a decrease in quantity demanded."],
 "a", "A binding ceiling causes a shortage (Qd > Qs). Without price to ration it, buyers waste time in lines and searching, and sellers have little reason to keep up quality.", None),
("In the table, a surplus occurs at a price _____, and a shortage occurs at a price _____.",
 ["of $16; above $16", "below $16; above $16", "above $16; below $16", "of $20; below $18", "above $14; below $20"],
 "c", "Equilibrium is $16 (Qd = Qs = 80). Above $16, Qs > Qd (surplus). Below $16, Qd > Qs (shortage).",
 ("table", [["Price per unit", "Quantity demanded", "Quantity supplied"], ["$20", "60", "95"], ["18", "70", "85"], ["16", "80", "80"], ["14", "90", "72"]])),
("If a price ceiling is set at $4 per pound of coffee, how big is the shortage or surplus?",
 ["40,000 pounds in shortage", "60,000 pounds in surplus", "80,000 pounds in shortage", "60,000 pounds in shortage"],
 "d", "At $4, quantity demanded is 80,000 and quantity supplied is 20,000, a shortage of 60,000 pounds. (Equilibrium is $6 at 60,000, so a $4 ceiling is binding.)", ("fig", "q24", 3.5)),
("With 1 unit of labor, Japan can produce 8 TVs or 4 cars, and Mexico can produce 3 TVs or 3 cars. If Mexico can trade only with Japan, comparative advantage suggests that Mexico should:",
 ["specialize in producing cars and import TVs from Japan.", "specialize in producing TVs and import cars from Japan.",
  "import both TVs and cars from Japan.", "produce both goods and import nothing from Japan."],
 "a", "Opportunity cost of 1 car: Japan = 2 TVs, Mexico = 1 TV. Mexico has the comparative advantage in cars (even though Japan has an absolute advantage in both), so Mexico specializes in cars and imports TVs.", None),
("Suppose a good has an income elasticity of demand of -0.5. Which best describes the good?",
 ["It is a normal good.", "It is an inferior good.", "It is a luxury good.", "It is a substitute.", "It is a complement."],
 "b", "A negative income elasticity means demand falls as income rises, which defines an inferior good.", None),
("After an earthquake, the prices of many goods rise. How might the government BEST help poor households afford goods and services?",
 ["Impose price controls at pre-earthquake prices.", "Give poor households cash or debit cards for essential purchases, but leave prices unregulated.",
  "Freeze wages to keep production costs from rising.", "Set prices at zero so everyone can get what they need."],
 "b", "Cash transfers help the poor while keeping prices free to signal scarcity and draw in more supply. Price controls would create shortages.", None),
("When the price of a good increases, the supply of the good will:",
 ["increase.", "decrease.", "be unaffected.", "depend on the corresponding change in demand."],
 "c", "A change in the good's own price causes a movement along the supply curve (a change in quantity supplied), not a shift in supply.", None),
("The table shows each buyer's maximum willingness to pay for one concert ticket. If the market price is $28, what is total consumer surplus? (Hint: use the definition of consumer surplus. Do not draw a demand curve.)",
 ["$72.25", "$53.50", "$44.25", "$62.75"],
 "b", "Only buyers with WTP  at least  $28 buy: A gets $45 - $28 = $17, B gets $30 - $28 = $2, C gets $62.50 - $28 = $34.50. D ($18.75) does not buy. Total = $53.50.",
 ("table", [["Buyer", "Maximum willingness to pay"], ["Buyer A", "$45.00"], ["Buyer B", "$30.00"], ["Buyer C", "$62.50"], ["Buyer D", "$18.75"]])),
("If the price of gaming consoles decreases, what will happen in the market for video games?",
 ["Demand will increase, quantity supplied will increase, and price will increase.", "Supply will increase, quantity demanded will increase, and price will decrease.",
  "Demand will decrease, quantity supplied will decrease, and price will decrease.", "Demand will increase, quantity supplied will decrease, and price will increase."],
 "a", "Consoles and games are complements. Cheaper consoles increase demand for games (shift right). That raises price and causes a movement up the supply curve (quantity supplied increases).", None),
("In the diagram, which of these factors would cause the demand curve to shift from D<sub>1</sub> to D<sub>2</sub>?",
 ["An increase in the price of a complement", "A decrease in the price of a substitute", "A decrease in income if this is a normal good", "A decrease in the price of a complement"],
 "d", "D<sub>1</sub> to D<sub>2</sub> is a rightward shift (an increase in demand). A cheaper complement increases demand. The other three choices all decrease demand.", ("fig", "q31", 3.4)),
("Using the midpoint formula, what is the price elasticity of supply between point C and point D?",
 ["10", "1.5", "0.67", "0.1"],
 "c", "%change in Q = 200 / 600 = 33.3%. %change in P = 20 / 40 = 50%. Elasticity = 33.3 / 50 = 0.67.", ("fig", "q32", 3.4)),
("Suppose there is a tax of $2 per unit, the elasticity of supply is 1, and the elasticity of demand is 4 (in absolute value). How much of the $2 tax is paid by sellers?",
 ["$0.40", "$0.50", "$1.00", "$1.60"],
 "d", "Sellers' share = E<sub>d</sub> / (E<sub>d</sub> + E<sub>s</sub>) = 4 / 5 = 80%. 0.8 × $2 = $1.60. The less elastic side (here, supply) bears more of the tax.", None),
("Marcus is considering a 2-year full-time MBA program. Tuition is $40,000 per year, books are $2,000 per year, and rent is $18,000 per year (he pays the same rent whether or not he enrolls). If he doesn't enroll, he will keep his job paying $70,000 per year. What is the total opportunity cost of the 2-year MBA?",
 ["$112,000", "$144,000", "$224,000", "$260,000", "$84,000"],
 "c", "Per year: $40,000 tuition + $2,000 books + $70,000 forgone salary = $112,000. Rent is paid either way, so it is not an opportunity cost. Over 2 years: $224,000.", None),
("If demand increases and the slope of demand stays the same (supply unchanged), producer surplus:",
 ["decreases.", "increases.", "stays the same.", "cannot be determined from the information provided."],
 "b", "A rightward shift in demand raises both equilibrium price and quantity, so the area above supply and below price grows.", None),
("Comparative advantage is determined by which producer has:",
 ["the greater output per worker.", "the lower opportunity cost of producing the good.", "the larger population.", "more natural resources."],
 "b", "Comparative advantage means producing at a lower opportunity cost. Higher output per worker describes absolute advantage.", None),
("Lena's maximum willingness to pay for a concert ticket is $150. The venue would accept as little as $90. Normally she pays the market price of $120. If a $40 tax raises the ticket price to $155 and Lena no longer goes, what is the deadweight loss of the tax?",
 ["$20", "$30", "$40", "$60", "$150"],
 "d", "Before the tax, the trade created $150 - $90 = $60 of total surplus ($30 to Lena and $30 to the venue). The tax prevents the trade and collects no revenue from it, so all $60 is lost.", None),
("Use the PPFs for Countries X and Y. The dots show each country's production and consumption without trade. Suppose each country fully specializes according to comparative advantage, and X trades 25 lbs of fish to Y for 20 loaves of bread. Compared with no trade, X consumes _____ more fish and _____ more bread, and Y consumes _____ more fish and _____ more bread.",
 ["25; 20; 25; 20", "0; 5; 15; 0", "30; 5; 10; 20", "5; 0; 15; 5", "5; 5; 15; 0"],
 "e", "Opportunity cost of 1 bread: X = 2 fish, Y = 0.5 fish, so X makes 60 fish and Y makes 40 bread. After trade, X has 35 fish and 20 bread (vs. 30 and 15), gaining 5 and 5. Y has 25 fish and 20 bread (vs. 10 and 20), gaining 15 and 0.", ("fig", "q38", 5.4)),
("A price ceiling is imposed as shown. Assuming the available units go to the buyers who value them most, which area is the deadweight loss?",
 ["B", "A + B", "C + D", "B + C + D"],
 "c", "Quantity falls from Q* to Q<sub>s</sub>. The lost gains from trade on those units are the area between demand and supply from Q<sub>s</sub> to Q*: C + D. Area B is a transfer from producers to consumers, not a loss.", ("fig", "q39", 3.6)),
("A subsidy paid to the sellers of a good can be shown in the figure by a shift in:",
 ["demand from D<sub>1</sub> to D<sub>2</sub>.", "demand from D<sub>2</sub> to D<sub>1</sub>.", "supply from S<sub>1</sub> to S<sub>2</sub>.", "supply from S<sub>2</sub> to S<sub>1</sub>."],
 "d", "A subsidy to sellers lowers their effective cost, shifting supply to the right (down). In the figure, S<sub>1</sub> is to the right of S<sub>2</sub>, so the shift is from S<sub>2</sub> to S<sub>1</sub>.", ("fig", "q40", 3.4)),
("The figure shows rent control. One supply curve is short-run supply, and the other is long-run supply. Which supply curve is the long-run supply, and how large is the shortage in the long run?",
 ["S<sub>1</sub>; Q<sub>d</sub> - Q<sub>a</sub>", "S<sub>2</sub>; Q<sub>d</sub> - Q<sub>b</sub>", "S<sub>1</sub>; Q<sub>c</sub> - Q<sub>a</sub>", "S<sub>2</sub>; Q<sub>d</sub> - Q<sub>a</sub>"],
 "a", "Supply is more elastic (flatter) in the long run because landlords can convert or stop building units over time. So S<sub>1</sub> is long-run. At the controlled rent, long-run Qs = Q<sub>a</sub> and Qd = Q<sub>d</sub>, so the shortage is Q<sub>d</sub> - Q<sub>a</sub>. (The short-run shortage is Q<sub>d</sub> - Q<sub>b</sub>.)", ("fig", "q41", 3.6)),
("The maximum price that consumers are willing to pay for _____ units of good Y is _____ per unit.",
 ["10; $8", "30; $4", "15; $12", "40; $4", "30; $8"],
 "b", "Read the demand curve: at Q = 30, the height of demand is $4. (Q = 10 gives $12, Q = 15 gives $8, Q = 40 gives $3.)", ("fig", "q42", 3.5)),
("The figure shows two housing supply curves. City X has very few restrictions on new construction, and City Y has many restrictions. In response to an increase in demand from D<sub>1</sub> to D<sub>2</sub>, a city like City Y will see equilibrium move from:",
 ["point A to point B.", "point B to point A.", "point C to point A.", "point A to point C."],
 "a", "Restrictions make housing supply inelastic (steep, S<sub>Y</sub>). An increase in demand then mostly raises price: A to B. A city with few restrictions (flat S<sub>X</sub>) moves from A to C, with a large increase in quantity and little change in price.", ("fig", "q43", 3.5)),
("The government can collect a $0.50 per gallon gasoline tax either from buyers or from sellers. Which statement is true?",
 ["Sellers bear more of the tax if it is collected from sellers.", "Buyers bear more of the tax if it is collected from buyers.",
  "The division of the tax burden is the same either way; it depends only on the elasticities of supply and demand.", "The tax does not affect buyers or sellers; it only raises revenue for the government."],
 "c", "Who legally pays the tax does not determine who bears it. The economic incidence depends only on the relative elasticities of supply and demand.", None),
("S<sub>1</sub> is the supply of an illegal drug with no prohibition, and S<sub>2</sub> is supply with prohibition. Total revenue with prohibition is _____, and total revenue without prohibition is _____. (Area A is the rectangle from $20 to $70 on the y-axis and 0 to 40 on the x-axis. C is the rectangle from $0 to $20 and 0 to 40. D is the rectangle from $0 to $20 and 40 to 50.)",
 ["$1,000; $2,800", "$2,000; $800", "$3,500; $1,000", "$2,800; $800", "$2,800; $1,000"],
 "e", "With prohibition: P = $70, Q = 40, so revenue = $2,800 (areas A + C). Without: P = $20, Q = 50, so revenue = $1,000 (C + D). Because demand is inelastic, prohibition raises total revenue for sellers.", ("fig", "q45", 3.6)),
("The table shows the labor hours needed to produce one unit of each good. The opportunity cost of producing 1 pair of shoes in Vietnam is _____, and in Italy it is _____.",
 ["4 shirts; 1.5 shirts", "0.25 shirt; 0.67 shirt", "8 shirts; 6 shirts", "16 shirts; 24 shirts", "2 shirts; 4 shirts"],
 "a", "Vietnam: 8 hours per pair of shoes / 2 hours per shirt = 4 shirts. Italy: 6 / 4 = 1.5 shirts. Italy has the comparative advantage in shoes.",
 ("table", [["Labor hours to produce:", "1 shirt", "1 pair of shoes"], ["Vietnam", "2", "8"], ["Italy", "4", "6"]])),
("Corn is an input into many products, including ethanol fuel, breakfast cereal, livestock feed, and corn syrup. If a new government mandate sharply increases the demand for ethanol, all else equal:",
 ["the price of corn syrup should rise.", "the demand for breakfast cereal should rise.", "the quantity of livestock feed produced should rise.", "the price of beef should fall."],
 "a", "Higher ethanol demand raises demand for corn, which raises the price of corn. That increases costs for all other corn-based products, decreasing their supply and raising their prices (including corn syrup and, through feed, beef).", None),
]

SHARED = [
("Identify the area corresponding to government revenue after the tax is imposed.",
 ["A + B + C", "B + F", "C + G", "F + G + H", "B + C + F + G"],
 "b", "Revenue = tax × quantity with tax = the rectangle between the buyers' price ($70) and the sellers' price ($50) up to Q = 30: B + F = $20 × 30 = $600."),
("What is the dollar value of the deadweight loss created by the tax?",
 ["$600", "$200", "$50", "$100", "$800"],
 "d", "DWL = triangles C + G = ½ × $20 (tax) × 10 (fall in quantity from 40 to 30) = $100."),
("Identify the change in consumer surplus due to the tax.",
 ["-(B + C)", "-(A + B + C)", "-(F + G)", "-(C + G)", "B + F"],
 "a", "Before the tax, CS = A + B + C (above $60). After, buyers pay $70 and CS = A. Consumers lose B (paid as tax) + C (deadweight loss). Buyers' price rose $10 and sellers' price fell $10, so the burden is split evenly."),
]

def img(name, width_in):
    w, h = PILImage.open(FIG + name + ".png").size
    return Image(FIG + name + ".png", width=width_in*inch, height=width_in*inch*h/w)

def q_block(n, stem, opts, extra=None):
    parts = [Paragraph(f"{n}.&nbsp;&nbsp;{stem}", Q)]
    if extra:
        parts.append(Spacer(1, 4))
        if extra[0] == "fig":
            i = img(extra[1], extra[2]); i.hAlign = "LEFT"
            parts.append(Table([[ "", i]], colWidths=[0.45*inch, None], hAlign="LEFT"))
        else:
            parts.append(Table([["", tbl(extra[1])]], colWidths=[0.45*inch, None], hAlign="LEFT"))
        parts.append(Spacer(1, 2))
    for L, o in zip("abcde", opts):
        parts.append(Paragraph(f"{L}.&nbsp;&nbsp;{o}", OPT))
    parts.append(Spacer(1, 12))
    return KeepTogether(parts)

def header_footer(c, doc):
    c.saveState(); c.setFont("Helvetica", 9)
    c.drawRightString(letter[0] - 0.9*inch, letter[1] - 0.55*inch, "Practice Exam: Version P")
    c.drawRightString(letter[0] - 0.9*inch, 0.5*inch, str(doc.page))
    c.restoreState()

story = [
    Paragraph("Name: ______________________&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Score: _______ / 50", N), Spacer(1, 14),
    Paragraph("ECON 2106: Principles of Microeconomics", C), Paragraph("Midterm 1 Practice Exam", H), Spacer(1, 10),
    Paragraph("Instructions:", N),
    Paragraph("This practice exam has 50 multiple-choice questions, each worth the same number of points. It mirrors the topics and format of Midterm 1.", BUL, bulletText="•"),
    Paragraph("Try it under exam conditions: 75 minutes, no notes, calculator allowed.", BUL, bulletText="•"),
    Paragraph("<b>Choose the <i>best</i> answer for each question.</b> The answer key with explanations is at the end.", BUL, bulletText="•"),
    Spacer(1, 18),
]
for i, (stem, opts, ans, expl, extra) in enumerate(QS, 1):
    story.append(q_block(i, stem, opts, extra))

n0 = len(QS) + 1
intro = Paragraph(f"<b>Assume a tax is imposed in a perfectly competitive market with no pre-existing market failures, as shown in the figure. Use this figure for questions {n0}–{n0+2}.</b>", N)
fi = img("q48", 4.0); fi.hAlign = "CENTER"
first = SHARED[0]
story.append(KeepTogether([intro, Spacer(1, 6), fi, Spacer(1, 6), q_block(n0, first[0], first[1])]))
for j, (stem, opts, ans, expl) in enumerate(SHARED[1:], n0 + 1):
    story.append(q_block(j, stem, opts))

# Answer key
story += [PageBreak(), Paragraph("Answer Key", H), Spacer(1, 8)]
allq = [(a, e) for (_, _, a, e, _) in QS] + [(a, e) for (_, _, a, e) in SHARED]
grid = [["Q", "Ans"] * 5]
for r in range(10):
    row = []
    for c in range(5):
        k = c*10 + r
        row += [str(k + 1), allq[k][0].upper()]
    grid.append(row)
g = Table(grid, colWidths=[0.45*inch, 0.5*inch]*5, hAlign="CENTER")
g.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8")),
                       ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                       ("FONTNAME", (1, 1), (1, -1), "Helvetica-Bold"), ("FONTNAME", (3, 1), (3, -1), "Helvetica-Bold"),
                       ("FONTNAME", (5, 1), (5, -1), "Helvetica-Bold"), ("FONTNAME", (7, 1), (7, -1), "Helvetica-Bold"),
                       ("FONTNAME", (9, 1), (9, -1), "Helvetica-Bold")]))
story += [g, Spacer(1, 10), Paragraph("Explanations", HDR)]
for k, (a, e) in enumerate(allq, 1):
    story.append(Paragraph(f"<b>{k}. ({a})</b>&nbsp;&nbsp;{e}", KEY))

doc = SimpleDocTemplate("ECON2106_Midterm1_Practice_Exam.pdf", pagesize=letter, leftMargin=0.9*inch, rightMargin=0.9*inch,
                        topMargin=0.8*inch, bottomMargin=0.8*inch, title="ECON 2106 Midterm 1 Practice Exam")
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
from collections import Counter
print(len(allq), Counter(a for a, _ in allq))

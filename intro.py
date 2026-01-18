
rfr = .12
e = 2.71828182845

# Simple binomial model
S_0 = 20
S_T1 = 22
S_T2 = 18


# If stock ends at $22
# .683 from initial sale went towards the hedge so is included in the 4.448
# profit = 21 - 16.5 - 4.448
# print ( profit)


# If stock ends at $18
option_value = 0
inventory_value = 4.50
borrowing_cost = 4.315*e**(.12*.25)
borrowing_cost

profit = inventory_value - option_value - borrowing_cost
print (profit)
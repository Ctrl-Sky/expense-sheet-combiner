# expense-sheet-combiner

Use this to get the sum of purchases, excluding large purchases greater or less than 300
=SUMIFS(INDIRECT("F2:F" & ROW()-1), INDIRECT("F2:F" & ROW()-1), "<=300", INDIRECT("F2:F" & ROW()-1), ">=-300")
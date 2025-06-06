# personal-expense-sheet-combiner

This is a personal expense tracker automation tool. This is something I created to help keep track of my expenses across multiple different cards. It takes account activity of each card as a csv format, standardizes all of them to fit my specific format, and then combines them all into one master excel file. Filtering each purchase into a new sheet respective to the month the expense was made in.

**Note**
The sheets directory is not created in this repo and must be created to function

If on windows, to run this use:\
`./execute_application.ps1`\
\
If on linux, to this use:\
`bash execute_application.sh`\
\
Use this to get the sum of purchases, excluding large purchases greater than 300 or large gains less than -300\
`=SUMIFS(INDIRECT("H2:H" & ROW()-1), INDIRECT("H2:H" & ROW()-1), "<=300", INDIRECT("H2:H" & ROW()-1), ">=-300")`
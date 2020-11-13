import xlrd
loc1 = ("D:\\Important Data\\weekly_task.xlsx")

wb1 = xlrd.open_workbook(loc)
sheet1 = wb1.sheet_by_index(0)

loc2 = ("D:\\Important Data\\weekly_task.xlsx")

wb2 = xlrd.open_workbook(loc)
sheet2 = wb2.sheet_by_index(0)

noOfRows1=sheet1.nrows
noOfRows2=sheet2.nrows




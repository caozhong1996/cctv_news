import xlwt

#设置表格样式
def set_style(name,height,bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    font.width = 400
    style.font = font
    return style

#写Excel
def write_excel():
    f = xlwt.Workbook()
    sheet1 = f.add_sheet('新闻',cell_overwrite_ok=True)
    row0 = ["姓名","年龄","出生日期","爱好"]
    row1 = ["张三","18","1996","无"]
    #写第一行
    for i in range(0,len(row0)):
        sheet1.write(0,i,row0[i],set_style('Times New Roman',220,True))
    #写第二行
    for i in range(0,len(row1)):
        sheet1.write(1,i,row1[i],set_style('Times New Roman',220,True))

    f.save('test.xls')

if __name__ == '__main__':
    write_excel()
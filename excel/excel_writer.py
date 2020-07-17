import xlsxwriter


def main_dict_to_excel(main_dict, file_name):
    workbook = xlsxwriter.Workbook('excel/' + file_name + '.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, 'Источник')
    worksheet.write(0, 1, 'Ссылка')
    worksheet.write(0, 2, 'Дата')
    worksheet.write(0, 3, 'Заголовок')
    worksheet.write(0, 4, 'Новость')

    row = 1
    for new in main_dict.values():
        worksheet.write(row, 0, new['Источник'])
        worksheet.write(row, 1, new['Ссылка'])
        worksheet.write(row, 2, new['Дата'])
        worksheet.write(row, 3, new['Заголовок'])
        worksheet.write(row, 4, new['Новость'])
        row += 1

    workbook.close()

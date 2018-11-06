import json
import xlwt
def readFromJson(file):
    with open(file, 'r', encoding='utf8') as fr:
        jsonData = json.load(fr)
    return jsonData

def writeToExcel(file):
    jsondata = readFromJson(file)
    print(jsondata)
    excel = xlwt.Workbook()
    sheet1 = excel.add_sheet('sheet1', cell_overwrite_ok=True)
    sheet2 = excel.add_sheet('sheet2', cell_overwrite_ok=True)

    print('length:%s'% length)

    def cmlxxx(jsondata):
        length = len(jsondata)
        for i in range(0, length):
            for k, v in jsondata.items():
                vSize = len(v)
                # if (vSize > 256):
                #     print(i + 1, vSize)

                for j in range(0, vSize):
                    if j < 256:
                        sheet1.write(i, j, str(v))
                    if j == 0:
                        sheet2.write(i, 0, str(v))

                sheet2.write(i, 1, str(v))

    for k,v in jsondata.items():

    excel.save('E:\cmltest\wer.xls')

if __name__ == '__main__':
    writeToExcel('E:\cmltest\dirname02.json')
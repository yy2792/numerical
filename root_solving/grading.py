import xlwings as xw


def locate_Q(qname, sht, row=200, col=10):
    for i in range(1, row+1):
        for j in range(1, col+1):
            if sht.range((i, j)).value == qname:
                return i, j

    return None, None

def call_marco(path):
    wb = xw.Book(path)
    run_macro = wb.macro('run')

    try:
        xw.Range('target1').value = 1
    except:


    s = wb.sheets['grading sheet']

    print(locate_Q('Q1', s))


    run_macro()
    wb.close()


if __name__ == '__main__':
    call_marco('/Users/yingkeyu/YingkeCode/numerical/submissions/zhaoyifei_292070_4616511_HW3_5030_yz3075.xlsm')
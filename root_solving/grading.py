import xlwings as xw
import os
import yaml
from root_solving.BS_formula import BS_Price
from root_solving.main_bull import helper_val

mp = {
    'Secant Method': 'sec',
    'Regula Falsi': 'reg',
    'Newton': 'new'
}


def load_trials():
    dir = os.path.dirname(os.path.abspath(__file__))
    yml_f = dir + '/ans.yaml'

    with open(yml_f, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return None


def locate(sht, row=200, col=10):

    loc_res = dict()

    for i in range(1, row+1):
        for j in range(1, col+1):
            if 'Q1' in loc_res and 'Q2' in loc_res:
                break
            if sht.range((i, j)).value in ['Q1', 'Q2']:
                loc_res[sht.range((i, j)).value] = (i, j)

    if 'Q1' in loc_res:
        q1_row, q1_col = loc_res['Q1']

        for i in range(20):
            temp_row = q1_row + i
            if 'Q1_new' in loc_res and 'Q1_sec' in loc_res and 'Q1_reg' in loc_res:
                break
            temp_name = sht.range((temp_row, q1_col)).value
            if temp_name in ['Newton', 'Secant Method', 'Regula Falsi']:
                loc_res['Q1_' + mp[temp_name]] = (temp_row, q1_col + 1)
            if temp_name == 'target (I will change)':
                loc_res['t1'] = (temp_row, q1_col + 1)

    if 'Q2' in loc_res:
        q2_row, q2_col = loc_res['Q2']

        for i in range(20):
            temp_row = q2_row + i
            if 'Q2_new' in loc_res and 'Q2_sec' in loc_res and 'Q2_reg' in loc_res:
                break
            temp_name = sht.range((temp_row, q2_col)).value
            if temp_name in ['Newton', 'Secant Method', 'Regula Falsi']:
                loc_res['Q2_' + mp[temp_name]] = (temp_row, q2_col + 1)
            if temp_name == 'target (I will change)':
                loc_res['t2'] = (temp_row, q2_col + 1)

    return loc_res


def call_marco(path):

    trials = load_trials()

    wb = xw.Book(path)
    run_macro = wb.macro('run')

    s = wb.sheets['grading sheet']

    loc_res = locate(s)


    # Q1

    # Q2
    para_json = trials['Price']['Q2']
    for key in para_json:
        if key == 't':
            para_json['t'] = float(para_json['t']) / 365
        else:
            para_json[key] = float(para_json[key])

    s.range(loc_res['t2']).value = 1.6
    run_macro()

    new2 = s.range(loc_res['Q2_new']).value
    sec2 = s.range(loc_res['Q2_sec']).value
    reg2 = s.range(loc_res['Q2_reg']).value

    para_json['vol'] = new2
    new2_res = round(helper_val(para_json), 4)

    para_json['vol'] = sec2
    sec2_res = round(helper_val(para_json), 4)

    para_json['vol'] = reg2
    reg2_res = round(helper_val(para_json), 4)

    print(new2_res)
    print(sec2_res)
    print(reg2_res)

    #wb.close()


if __name__ == '__main__':
    call_marco('/Users/yingkeyu/YingkeCode/numerical/submissions/zhaoyifei_292070_4616511_HW3_5030_yz3075.xlsm')
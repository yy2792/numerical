import xlwings as xw
import os
import yaml
from root_solving.BS_formula import BS_Price
from root_solving.main_bull import helper_val

mp = {
    'Secant Method': 'sec',
    'Regula Falsi': 'reg',
    'Newton': 'new',
    'Regular Falsi': 'reg',
}

mp2 = dict()
for key in mp:
    mp2[key.upper()] = mp[key]

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
            temp_name = sht.range((temp_row, q1_col)).value
            if temp_name == 'target (I will change)':
                loc_res['t1'] = (temp_row, q1_col + 1)
                break

        for i in range(20):
            temp_row = q1_row + i
            if 'Q1_new' in loc_res and 'Q1_sec' in loc_res and 'Q1_reg' in loc_res:
                break
            temp_name = sht.range((temp_row, q1_col)).value
            if isinstance(temp_name, str) and temp_name.upper() in mp2 and temp_row > loc_res['t1'][0]:
                loc_res['Q1_' + mp[temp_name]] = (temp_row, q1_col + 1)

    if 'Q2' in loc_res:
        q2_row, q2_col = loc_res['Q2']

        for i in range(20):
            temp_row = q2_row + i
            temp_name = sht.range((temp_row, q2_col)).value
            if temp_name == 'target (I will change)':
                loc_res['t2'] = (temp_row, q2_col + 1)
                break

        for i in range(20):
            temp_row = q2_row + i
            if 'Q2_new' in loc_res and 'Q2_sec' in loc_res and 'Q2_reg' in loc_res:
                break
            temp_name = sht.range((temp_row, q2_col)).value
            if isinstance(temp_name, str) and temp_name.upper() in mp2 and temp_row > loc_res['t2'][0]:
                loc_res['Q2_' + mp[temp_name]] = (temp_row, q2_col + 1)

    return loc_res


def call_marco(path):

    wb = xw.Book(path)
    errors = []
    trials = load_trials()

    run_macro = wb.macro('run')

    s = wb.sheets['grading sheet']

    loc_res = locate(s)


    # Q1
    para_json = trials['Price']['Q1']
    for key in para_json:
        if key == 't':
            para_json['t'] = float(para_json['t']) / 365
        else:
            para_json[key] = float(para_json[key])

    for val in trials['Q1']:
        s.range(loc_res['t1']).value = float(val)

        run_macro()

        new1 = s.range(loc_res['Q1_new']).value
        sec1 = s.range(loc_res['Q1_sec']).value
        reg1 = s.range(loc_res['Q1_reg']).value

        para_json['vol'] = new1
        new1_res = round(BS_Price(para_json), 4)

        para_json['vol'] = sec1
        sec1_res = round(BS_Price(para_json), 4)

        if float(val) != 10:
            para_json['vol'] = reg1
            reg1_res = round(BS_Price(para_json), 4)
            if reg1_res != float(val):
                errors.append('Q1_reg_{}'.format(val))

        if new1_res != float(val):
            errors.append('Q1_new_{}'.format(val))
        if sec1_res != float(val):
            errors.append('Q1_sec_{}'.format(val))

    # Q2
    para_json = trials['Price']['Q2']
    for key in para_json:
        if key == 't':
            para_json['t'] = float(para_json['t']) / 365
        else:
            para_json[key] = float(para_json[key])

    for val in trials['Q2']:
        s.range(loc_res['t2']).value = float(val)

        run_macro()

        new2 = s.range(loc_res['Q2_new']).value
        sec2 = s.range(loc_res['Q2_sec']).value
        reg2 = s.range(loc_res['Q2_reg']).value

        if float(val) == 1.6:
            para_json['vol'] = new2
            new2_res = round(helper_val(para_json), 4)
            if new2_res != float(val):
                errors.append('Q2_new_{}'.format(val))

        para_json['vol'] = sec2
        sec2_res = round(helper_val(para_json), 4)

        para_json['vol'] = reg2
        reg2_res = round(helper_val(para_json), 4)

        if sec2_res != float(val):
            errors.append('Q2_sec_{}'.format(val))
        if reg2_res != float(val):
            errors.append('Q2_reg_{}'.format(val))

    wb.close()

def grading(wbpath):
    target_files = []
    graded_res = {}

    # get all the xlsm files
    for path, subdirs, files in os.walk(wbpath):
        for filename in files:
            if '.xlsm' in filename:
                f = os.path.join(path, filename).replace('\'', '\\')
                target_files.append(f)

    for xlsm_path in target_files:
        bookname = str(xlsm_path.split('\\')[-1])

        try:
            errors = call_marco(xlsm_path)
            if errors is None:
                continue
            graded_res[bookname] = errors
            print(bookname + ' graded, results:')
            print(errors)
        except Exception as e:
            print(e)
            print(bookname)
            pass


if __name__ == '__main__':
    grading('/Users/yingkeyu/YingkeCode/numerical/submissions/')

    #errors = call_marco('/Users/yingkeyu/YingkeCode/numerical/submissions/mishrapinakpani_393325_4620795_Pinakpani Mishra_HW3_1-1.xlsm')
    #print(errors)
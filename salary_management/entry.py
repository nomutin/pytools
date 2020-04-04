"""
nomutin's salary-management GUI application

todo let common,data file_level mutable　
"""

from labor_datas.commons import commons
import sys
import time

__version__ = '0.0.2'
__author__ = 'nomutin'


entry_statement = f"\nWelcome to salary_management.py ver.{__version__} by {__author__} \n\n" \
                  f"Current your position is {commons['position']}, basic salary is ¥{commons['basic_salary']}, \n" \
                  f"overtime work rate and night work rate is *{commons['overtime_pay_rate']}, " \
                  f"*{commons['night_pay_rate']}, and delivery bonus is ¥{commons['delivery_bonus_per_hour']} /hour\n"\
                  f"\nSelect functon: \n\t(S)how labor " \
                  f"data and salaries \n\t(I)nput labor time \n\t(E)dit common_data \n\t(C)lose this application\n>>"


def entry():
    mode = input(entry_statement)

    try:
        modes = {'c': sys.exit, 'i': input_labor_time}
        modes[mode]()

    except KeyError:
        print(f'Oops! We have not prepared the function {mode} you choose!\n')
        time.sleep(0.4)
        entry()


def input_labor_time():
    i_entry_statement = '\n\nLabor time entry mode: If you want to exit, type (E)xit.'
    print(i_entry_statement)


if __name__ == '__main__':
    entry()

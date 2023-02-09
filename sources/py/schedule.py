'''
Модуль для работы с расписанием.

help_get_url()
возвращает словарь с полями subject (имя предмета),
teacher (имя преподователя), url, date, time для ближайшей пары
или None, если такого не нашлось

help_today()
Возвращает строку в которой перечень занятий на сегодня

help_tomorrow()
Возвращает строку в которой перечень занятий на завтра

help_week()
Возвращает строку в которой перечень занятий на неделю
'''

from schedule_func import *

import groups

#Возвращает словарь с описанием ближайшего занятия или None
def help_get_url(id):
    name = groups.getName(id)

    schedule = get_subj_list(id)

    #Есть ли сегодня занятия, по умолчанию - нет
    classes_today = False

    #Берем текущую дату и время в необходимом для сравнения варианте
    date = get_current_date()
    time = get_current_time()
    
    for subject in schedule:
        #Если дата текущая и время меньше, чем начало пары
        if subject['date'] == date and time < get_int_time(subject['time_end']):
            classes_today = True
            break
    if classes_today:
        return f"🔜Найближче заняття для групи {name}\n📢{subject['name']}\n🗓{subject['date']}\n👤{subject['teacher']}\n🕐{subject['time_begin']}-{subject['time_end']}\n⏩{subject['url']}"
    else:
        return f'⛔Сьогодні вже немає наступних занять для групи {name}'

def help_today(id):
    name = groups.getName(id)

    schedule = get_subj_list(id)
    
    #Есть ли сегодня занятия, по умолчанию - нет
    classes_today = False

    #Берем текущую дату и время в необходимом для сравнения варианте
    date = get_current_date()

    result = f'⏱Розклад на сьогодні для групи {name}\n'
    for subject in schedule:
        #Если дата текущая и время меньше, чем начало пары
        if (subject['date'] == date):
            classes_today = True
            result += ' ✅ ' + subject['time_begin'] + '-' + subject['time_end'] + ' - ' + subject['name'] + '\n'

    if classes_today == True:
        return result
    else:
        return f'⛔️Сьогодні немає занять для групи {name}'

def help_tomorrow(id):
    name = groups.getName(id)

    schedule = get_subj_list(id)

    #Есть ли сегодня занятия, по умолчанию - нет
    classes_tomorrow = False

    #Берем текущую дату и время в необходимом для сравнения варианте
    date = get_current_date()
    date = date_tomorrow(date)

    result = f'⏱Розклад на завтра для групи {name}\n'
    for subject in schedule:
        #Если дата текущая и время меньше, чем начало пары
        if (subject['date'] == date):
            classes_tomorrow = True
            result += ' ✅ ' + subject['time_begin'] + '-' + subject['time_end'] + ' - ' + subject['name'] + '\n'
    if result != f'⏱Розклад на завтра для групи {name}\n':
        return result
    else:
        return f'⛔Завтра немає занять для групи {name}'

def help_week(id):
    name = groups.getName(id)

    schedule = get_subj_list(id)

    date = schedule[0]['date']
    flag = False
    result = f'⏱Розклад на тиждень для групи {name}\n'

    for subject in schedule:
        if (subject['date'] == date):
            if flag == False:
                result += '\n' + date + ':\n'
                flag = True
            result += ' ✅ ' + subject['time_begin'] + '-' + subject['time_end'] + ' - ' + subject['name'] + '\n'
        else:
            flag = False
            
            date = subject['date']

            if (subject['date'] == date):
                if flag == False:
                    result += '\n' + date + ':\n'
                    flag = True
                result += ' ✅ ' + subject['time_begin'] + '-' + subject['time_end'] + ' - ' + subject['name'] + '\n'
                
    if result != f'⏱Розклад на тиждень для групи {name}\n':
        return result
    else:
        return f'⛔На цей тиджень немає занять для групи {name}'

def help_date(id, date):
    name = groups.getName(id)

    schedule = get_subj_list(id)
    
    flag = False

    result = f'⏱Розклад на {date} для групи {name}\n'

    for subject in schedule:
        if (subject['date'] == date):
            flag = True
            result += ' ✅ ' + subject['time_begin'] + '-' + subject['time_end'] + ' - ' + subject['name'] + '\n'

    if flag == True:
        return result
    else:
        return f'⛔На {date} немає занять для групи {name}'
import json    #Работаем с json

import codecs  #Читаем с учетом кодировки

from datetime import datetime #Узнаем текущее время

from tree import *

import  files

from config import *

import groups

schedules = {}

all_subjects = {}

def load():
    global schedules
    global all_subjects

    schedules = {}

    for group in groups.groups.keys():
        code = groups.groups[group]
        filename = 'schedule-' + code + '.json'
        path = schedulesFilePath + '/' + filename

        if os.path.exists(path) == True:
            schedule = files.loadFile(path)

            schedules[code] = schedule

    all_subjects = files.loadFile(subjectsFilePath)

''' ---------ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ----------- '''

#Возвращает следующий день. (надо сделать проверку на 30 день)
#Баг с числом

def getLength(num):
    length = 1
    num = int(num)

    while num >= 10:
        length = length + 1
        num = num / 10

    return length

def getStrFormat(format, num):

    length = getLength(int(num))
    bkp = str(int(num))
    cNum = ''

    if length < format:
        for i in range(format - length):
            cNum += '0'

    cNum += bkp

    return cNum

def createDate(format, date):

    cDate = getStrFormat(format, date[0])

    flag = 0

    for num in date:
        if flag == 1:
            cDate += '.' + getStrFormat(format, num)
        flag = 1

    return cDate

def date_tomorrow(date):
    date_arr = date.split('.')
    date_arr[0] = str(int(date_arr[0]) + 1)

    if int(date_arr[0]) > 31:
        date_arr[0] = '1'
        date_arr[1] = str(int(date_arr[1]) + 1)

    return createDate(2, date_arr)

#Возвращает текушию дату в нужном для сравнения формате
def get_current_date():
    date = str(datetime.now().date()).split('-')
    date.reverse()
    date =  str(date[0]) + '.' + str(date[1]) + '.' + str(date[2])

    return date

#Возвращает текущие время в нужном для сравнения формате
def get_current_time():
    time = str(datetime.now().time()).split(':')
    time =  int(time[0])*60 + int(time[1])
    return time

#Принимает навзание предмета и возвращает ссылку на пару
def url_of_subject(id, namea, nameb):
    name = namea + ' (' + nameb + ')'
    if id not in all_subjects.keys():
        return 'Немає посилання на заняття'
    if all_subjects[id].get(name) != None:
        return all_subjects[id][name]
    if all_subjects[id].get(namea + ' (лабораторне заняття)') != None:
        return all_subjects[id][namea + ' (лабораторне заняття)']
    if all_subjects[id].get(namea + ' (лекція)') != None:
        return all_subjects[id][namea + ' (лекція)']
    return 'Немає посилання на заняття'

#Возвращает дату и время переданного ей предмета
def get_int_time(time):
    time_int = time.split(':')
    time_int = int(time_int[0])*60 + int(time_int[1])
    return time_int

def set_schedule(id):
    code = id
    filename = 'schedule-' + code + '.json'
    path = schedulesFilePath + '/' + filename

    if os.path.exists(path) == False:
        groups.getSchedule(code)
        load()

    return schedules[code]

def sort_list(list):
    for i in range(0, len(list) - 1):
        for j in range(i + 1, len(list)):
            if list[i]['date'] == list[j]['date'] and get_int_time(list[i]['time_begin']) > get_int_time(list[j]['time_begin']):
                tmp = list[i]
                list[i] = list[j]
                list[j] = tmp

def get_subj_list(id):
    #Список с описанием всех предметов
    list_of_subjects = []
    #
    schedule = set_schedule(id)
    #Для каждого предмета создаем словарь
    for subject in schedule:
        name = subject['ABBR_DISC'] + ' (' + subject['NAME_STUD'] + ')'
        time = subject['TIME_PAIR']
        #Записываем все значения
        dict_of_subject = {}
        dict_of_subject['date']     = subject['DATE_REG']

        if subject['ABBR_DISC'] == '':
            dict_of_subject['name'] = subject['NAME_STUD']
        else:
            dict_of_subject['name'] = subject['ABBR_DISC'] + ' (' + subject['NAME_STUD'] + ')'

        dict_of_subject['name'] += ' ' + subject['REASON'] + ' ' + subject['NAME_AUD']

        dict_of_subject['time_begin'] = time[0:5]
        dict_of_subject['time_end']   = time[6:]

        dict_of_subject['url']      = url_of_subject(id, subject['ABBR_DISC'], subject['NAME_STUD'])

        dict_of_subject['teacher']  = subject['NAME_FIO']

        #Добавляем в список
        list_of_subjects.append(dict_of_subject)

    sort_list(list_of_subjects)

    return list_of_subjects

def setLink(code, subject, link):
    all_subjects[code][subject] = link

    files.saveFile(all_subjects, subjectsFilePath)

''' ---------ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ----------- '''

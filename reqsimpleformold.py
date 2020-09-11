import PySimpleGUI as sg
import sqlite3 as sql
from os import path

def form (conn):
    req_id = 1  #TODO заглушка потом подсунуть ИД в параметрах вызова
#   получение информации по заявке
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM list_request WHERE id_req = "+ str(req_id))
    results = cursor.fetchone()
#   получение информации по ИД клиента
    cursor.execute("SELECT fio FROM Cat_cust WHERE id_cust = "+ str(results[5]))
    results1 = cursor.fetchone()
#   получение информации по ИД туроператора
    cursor.execute("SELECT name_short_to FROM Cat_tourop WHERE id_to = "+ str(results[20]))
    results2 = cursor.fetchone()
#   получение информации из таблицы размещений по ИД заявки
    cursor.execute("SELECT date_begin, date_end, hotel, quant_room, accom, meal FROM req_accom WHERE id_req = "+ str(req_id))
    results3 = cursor.fetchall()
#   если гостиницы нет то создать пустую запись
#   TODO переделать на пустой список
    if results3==[]:
        ins_sql = "INSERT INTO req_accom (id_req) VALUES ('" + str(req_id) + "');"
        cursor.execute(ins_sql)
        conn.commit()
        cursor.execute("SELECT date_begin, date_end, hotel, quant_room, accom, meal FROM req_accom WHERE id_req = "+ str(req_id))
        results3 = cursor.fetchall()
#   Заголовок для таблицы гостиниц в форме
    header_list_hotel = ['Заезд', 'Выезд', 'Наименование отеля', 'Номеров', 'Тип размещения', 'Питание' ]
#   получение информации из таблицы туристов по ИД заявки
    cursor.execute("SELECT id_cust FROM req_tourist WHERE id_req = "+ str(req_id))
    results4 = cursor.fetchall()
    header_list_turists = ['Имя (LAT)', 'Фамилия (LAT)', 'Дата рождения', 'Номер ЗП', 'Дата выдачи', 'Действует по', 'Подр.' ]
    results4 = [('', '','', '', '', '', '')]

    agencylayout = [
        [sg.T('Заявка №', auto_size_text=True), sg.T(text = str(results[0]), size=(4,1)), sg.T('от', auto_size_text=True),
        sg.In(results[1], size=(10,1), key='-DATR-'), sg.CalendarButton(button_text='', image_filename=path.join('ico', 'Calendar_24x24.png'), target='-DATR-', format='%d.%m.%Y'),
        sg.T('к договору №', auto_size_text=True),  sg.In(results[2], size=(9,1)),
        sg.T('Заказчик', auto_size_text=True), sg.T(text = str(results1[0]), size=(30,1), relief=sg.RELIEF_SUNKEN),
        sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'User_24x24.png'), key='-CUST-')],
        [sg.T('Страна', size=(6,1)), sg.In(results[3], size=(20,1)), sg.T('Регион', auto_size_text=True), sg.In(results[4], size=(20,1)),
        sg.T('с', auto_size_text=True), sg.In(results[6], size=(10,1), key='-DATEB-'),
        sg.CalendarButton(button_text='', image_filename=path.join('ico', 'Calendar_24x24.png'), target='-DATEB-', format='%d.%m.%Y'),
        sg.T('по', auto_size_text=True), sg.In(results[7], size=(10,1), key='DATEE'),
        sg.CalendarButton(button_text='', image_filename=path.join('ico', 'Calendar_24x24.png'), target='-DATEE-', format='%d.%m.%Y'),
        sg.T('ночей', auto_size_text=True), sg.In(results[8], size=(2,1))],
        [sg.T('Билет', size=(6,1)), sg.In(results[9],size=(50,1)), sg.T('Трансфер', auto_size_text=True), sg.In(results[10],size=(30,1))],
        [sg.T('', size=(6,1))],
        [sg.T('Отели:' , size=(6,1)),
        sg.Table( values=results3 , headings=header_list_hotel, num_rows=2, key='-LHOTEL-', enable_events=True, pad=(5, 5), select_mode=sg.TABLE_SELECT_MODE_BROWSE)],
        [sg.T('', size=(6,1)), sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Add_24x24.png'), key='-AHOTEL-'),
        sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Properties_24x24.png'), key='-MHOTEL-'),
        sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Delete_24x24.png'), key='-DHOTEL-')],
        [sg.T('', size=(6,1))],
        [sg.T('Экскурсионная программа', auto_size_text=True), sg.In(results[11],size=(30,1)),
        sg.T('Прочие услуги', auto_size_text=True), sg.In(results[11],size=(40,1))],
        [sg.Checkbox('Гид', default=results[14]), sg.Checkbox('Экскурсовод', default=results[13]),
        sg.Checkbox('Руководитель группы', default=results[15]), sg.Checkbox('Виза', default=results[16])],
        [sg.T('Страхование: ', auto_size_text=True), sg.Checkbox('медицинское', default=results[17]),
        sg.Checkbox('от несчастного случая', default=results[18]),  sg.Checkbox('от невыезда', default=results[19]),
        sg.T('примечание', auto_size_text=True), sg.In(results[32], size=(20,1))],
        [sg.T('', size=(6,1))],
        [sg.T('Туристы:' , size=(6,1)),
        sg.Table( values=results4 , headings=header_list_turists, num_rows=4, key='-LTURISTS-', enable_events=True, pad=(5, 5), select_mode=sg.TABLE_SELECT_MODE_BROWSE)],
        [sg.T('', size=(6,1)), sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Add_24x24.png'), key='-ATURIST-'),
        sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Properties_24x24.png'), key='-MTURIST-'),
        sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Delete_24x24.png'), key='-DTURIST-')],
        [sg.T('', size=(6,1))],
        [sg.T('Оператор', auto_size_text=True), sg.T(text = str(results2[0]), relief=sg.RELIEF_SUNKEN, size=(30,1)),
        sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Globe_24x24.png'), key='-TOUROP-'),
        sg.T('Валюта тура у туроператора', auto_size_text=True),
        sg.Combo(('Евро', 'Доллар', 'Рубль'), default_value=results[21], size=(10,1))],
        [sg.T('Дата аванса', auto_size_text=True), sg.In(results[22],size=(10,1), key='-DATEA-'),
        sg.CalendarButton(button_text='', image_filename=path.join('ico', 'Calendar_24x24.png'), target='-DATEA-', format='%d.%m.%Y'),
        sg.Checkbox('', default=results[23]),
        sg.T('Дата полной оплаты', auto_size_text=True), sg.In(results[24],size=(10,1), key='-DATEO-'),
        sg.CalendarButton(button_text='', image_filename=path.join('ico', 'Calendar_24x24.png'), target='-DATEO-', format='%d.%m.%Y'),
        sg.Checkbox('', default=results[25]),
        sg.T('Документы до', auto_size_text=True), sg.In(results[26], size=(10,1), key='-DATED-'),
        sg.CalendarButton(button_text='', image_filename=path.join('ico', 'Calendar_24x24.png'), target='-DATED-', format='%d.%m.%Y'),
        sg.Checkbox('',  default=results[27])],
        [sg.T('Полная стоимость (руб)', auto_size_text=True), sg.In(results[29],size=(7,1)),
        sg.T('Полная стоимость (вал)', auto_size_text=True), sg.In(results[28],size=(7,1)),
        sg.T('Аванс', auto_size_text=True), sg.In(results[30],size=(7,1)), sg.T('Курс оператора', auto_size_text=True), sg.In(results[31],size=(7,1))],
        [sg.T('_'  * 100, size=(75, 1))],
        [sg.Button('Сохранить'), sg.Button('Выход')]]

    rewnd = sg.Window('Информация о предприятии', agencylayout, no_titlebar=False)

    while True:
        event, values =rewnd.read()
        if event == 'Выход'  or event is None:
            break

        if event in ('Сохранить'):
            upd_sql = "UPDATE Agency_card SET name = '" + str(values[0]) + "', adress = '" + str(values[1]) + "', inn = '" + str(values[2]) + "', kpp = '" + str(values[3]) + "', ogrn = '" + str(values[4]) + "', okved = '" + str(values[5]) + "', phone = '" + str(values[6]) + "', e_mail = '" + str(values[7]) + "', www = '" + str(values[8]) +"', boss = '" + str(values[9]) + "', bank_name  = '" + str(values[10]) + "', account = '" + str(values[11]) + "', cor_account = '" +str(values[12]) + "', bank_bik = '" + str(values[13]) + "' WHERE id = " + str(agency_id) +";"
            cursor.execute(upd_sql)
            conn.commit()

    rewnd.close()

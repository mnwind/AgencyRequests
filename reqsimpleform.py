import PySimpleGUI as sg
import sqlite3 as sql
import custform # подумать как избежать двух импортов
import touropform
from os import path
from datetime import date

def listcust(cursor,req_id):
# получение информации из списка туристов по заявке
    results4 = []
    listidtour_sql = "SELECT id_cust FROM req_tourist WHERE id_req = '" +str(req_id) +"'"
    cursor.execute(listidtour_sql)
    rows = cursor.fetchall()
    for row in rows:
        listtourist_sql = "SELECT id_cust, fio, date_r, num_for_pass, date_iss_for_pass, date_end_for_pass, who_for_pass FROM Cat_cust WHERE id_cust = '" + str(row[0]) +"'"
        cursor.execute(listtourist_sql)
        r4 = cursor.fetchone()
        results4.append(r4)
    if results4==[]:
        results4 = [('','', '','', '', '', '')]
    return results4
def listhotel(cursor, req_id):
#   получение информации из таблицы размещений по ИД заявки
    cursor.execute("SELECT no_in_table, date_begin, date_end, hotel, type_room, quant_room, accom, meal, hotel_addr FROM req_accom WHERE id_req = "+ str(req_id))
    results3 = cursor.fetchall()
#   если гостиницы нет то создать пустой список
    if results3==[]:
        results3 = [('', '', '', '', '', '', '', '','')]
    return results3

def reqhotelform(conn,results3,req_id):
#   форма редактирования отеля
    reqhotellayout = [
    [sg.T('Проживание с:',size=(16,1)), sg.In(results3[1], size=(10,1), key='-DATEHB-'), sg.T('по:', auto_size_text=True),
    sg.In(results3[2], size=(10,1), key='-DATEHE-'), sg.T('Отель ', auto_size_text=True), sg.In(results3[3], size=(30,1), key='-REQHOTEL-')],
    [sg.T('Номер ', auto_size_text=True), sg.In(results3[4], size=(20,1), key='-NROOMHOTEL-'),sg.T('Количество номеров ', auto_size_text=True), 
    sg.In(results3[5], size=(2,1), key='-QROOMHOTEL-'), sg.T('Тип размещения ', auto_size_text=True),
    sg.In(results3[6], size=(20,1), key='-TROOMHOTEL-'), sg.T('Питание ', auto_size_text=True), sg.In(results3[7], 
    size=(15,1), key='-MEALHOTEL-')],
    [sg.T('Адрес отеля ', auto_size_text=True), sg.In(results3[8], size=(50,1), key='-ADRHOTEL-')],
    [sg.Button('Сохранить'), sg.Button('Выход')]
    ]
    rhwnd = sg.Window('Отели по туру', reqhotellayout, no_titlebar=False)
    while True:
        event, values =rhwnd.read()
        if event == 'Выход'  or event is None:
            break
        if event in ('Сохранить'):
            column_values = (values['-DATEHB-'], values['-DATEHE-'], values['-REQHOTEL-'], values['-ADRHOTEL-'], values['-NROOMHOTEL-'], values['-QROOMHOTEL-'], values['-TROOMHOTEL-'], values['-MEALHOTEL-'], req_id, results3[0])
            upd_sql = "UPDATE req_accom SET date_begin = ?, date_end = ?, hotel = ?, hotel_addr = ?, type_room = ?, quant_room = ?, accom = ?, meal = ? WHERE id_req = ? AND no_in_table= ?;"
            cursor = conn.cursor()
            cursor.execute(upd_sql,column_values)
            conn.commit()
            break
    rhwnd.close()

def form (conn, req_id):
    cursor = conn.cursor()
    if req_id == 0: #если заявка новая создается запись, получается id
        cursor.execute("INSERT INTO list_request (date_req) VALUES ('" + str(date.today().strftime("%d.%m.%Y")) + "')")
        conn.commit()
        cursor.execute("SELECT id_req FROM list_request WHERE rowid=last_insert_rowid()")
        r = cursor.fetchone()
        req_id = r[0]
 
#   получение информации по заявке
    cursor.execute("SELECT * FROM list_request WHERE id_req = "+ str(req_id))
    results = cursor.fetchone()

#   получение информации по ИД клиента
    if results[5] == 0:
        results1 = ['']
        cust_id = 0
    else:
        cursor.execute("SELECT fio FROM Cat_cust WHERE id_cust = "+ str(results[5]))
        results1 = cursor.fetchone()
        cust_id = results[5]

#   получение информации по ИД туроператора
    if results[20] == 0:
        results2 = ['']
        id_oper = 0
    else:
        cursor.execute("SELECT name_short_to FROM Cat_tourop WHERE id_to = "+ str(results[20]))
        results2 = cursor.fetchone()
        id_oper = results[20]

#   получение информации из таблицы размещений по ИД заявки
    results3 = listhotel(cursor, req_id)
#   Заголовок для таблицы гостиниц в форме
    header_list_hotel = ['№ ', 'Заезд', 'Выезд', 'Наименование отеля', 'Номер', 'Номеров', 'Тип размещения', 'Питание', 'Адрес отеля' ]

#   получение информации из таблицы туристов по ИД заявки
    results4 = listcust(cursor,req_id)
    header_list_turists = ['ID','Фамилия Имя Отчество', 'Дата рождения', 'Номер З.Паспорта', 'Дата выдачи', 'Действует по', 'Подр.' ]
#Макет окна заявки
    agencylayout = [
        [sg.T('Заявка №', auto_size_text=True), sg.T(text = str(results[0]), size=(4,1)), sg.T('от', auto_size_text=True),
        sg.In(results[1], size=(10,1), key='-DATR-'), sg.CalendarButton(button_text='', image_filename=path.join('ico', 'Calendar_24x24.png'), target='-DATR-', format='%d.%m.%Y'),
        sg.T('к договору №', auto_size_text=True),  sg.In(results[2], size=(9,1)),
        sg.T('Заказчик', auto_size_text=True), sg.T(text = str(results1[0]), size=(30,1), relief=sg.RELIEF_SUNKEN, key='-FIO-'),
        sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'User_24x24.png'), key='-CUST-', border_width=0)],
        [sg.T('Страна', size=(6,1)), sg.In(results[3], size=(20,1)), sg.T('Регион', auto_size_text=True), sg.In(results[4], size=(20,1)),
        sg.T('с', auto_size_text=True), sg.In(results[6], size=(10,1), key='-DATEB-'),
        sg.CalendarButton(button_text='', image_filename=path.join('ico', 'Calendar_24x24.png'), target='-DATEB-', format='%d.%m.%Y'),
        sg.T('по', auto_size_text=True), sg.In(results[7], size=(10,1), key='-DATEE-'),
        sg.CalendarButton(button_text='', image_filename=path.join('ico', 'Calendar_24x24.png'), target='-DATEE-', format='%d.%m.%Y'),
        sg.T('ночей', auto_size_text=True), sg.In(results[8], size=(2,1))],
        [sg.T('Билет', size=(6,1)), sg.In(results[9],size=(50,1)), sg.T('Трансфер', auto_size_text=True), sg.In(results[10],size=(30,1))],
#        [sg.T('', size=(6,1))],
        [sg.T('Отели:' , size=(6,1)),
        sg.Table( values=results3 , headings=header_list_hotel, num_rows=1, key='-LHOTEL-', enable_events=True, pad=(5, 5), select_mode=sg.TABLE_SELECT_MODE_BROWSE)],
        [sg.T('', size=(6,1)), sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Add_24x24.png'), key='-AHOTEL-'),
        sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Properties_24x24.png'), key='-MHOTEL-'),
        sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Delete_24x24.png'), key='-DHOTEL-')],
#        [sg.T('', size=(6,1))],
        [sg.T('Экскурсионная программа', auto_size_text=True), sg.In(results[11],size=(30,1)),
        sg.T('Прочие услуги', auto_size_text=True), sg.In(results[12],size=(40,1))],
        [sg.T('Гид', size=(20,1)), sg.Combo(('Да','Нет'), default_value=results[13], size=(3,1)),
        sg.T('Экскурсовод', auto_size_text=True), sg.Combo(('Да','Нет'), default_value=results[14], size=(3,1)),
        sg.T('Руководитель группы', auto_size_text=True), sg.Combo(('Да','Нет'), default_value=results[15], size=(3,1)),
        sg.T('Виза', auto_size_text=True), sg.Combo(('Да','Нет'), default_value=results[16], size=(3,1))],
        [sg.T('Страхование: медицинское', auto_size_text=True), sg.Combo(('Да','Нет'), default_value=results[17], size=(3,1)),
        sg.T('от несчасного случая', auto_size_text=True), sg.Combo(('Да','Нет'), default_value=results[18], size=(3,1)),
        sg.T('от невыезда', auto_size_text=True), sg.Combo(('Да','Нет'), default_value=results[19], size=(3,1)),
        sg.T('примечание', auto_size_text=True), sg.In(results[32], size=(20,1))],
#        [sg.T(' ', size=(6,1))],
        [sg.T('Туристы:' , size=(6,1)),
        sg.Table( values=results4 , headings=header_list_turists, num_rows=4, key='-LTURISTS-', enable_events=True, pad=(5, 5), select_mode=sg.TABLE_SELECT_MODE_BROWSE)],
        [sg.T('', size=(6,1)), sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Add_24x24.png'), key='-ATURIST-'),
        sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Delete_24x24.png'), key='-DTURIST-')],
#        [sg.T('', size=(6,1))],
        [sg.T('Оператор', auto_size_text=True), sg.T(text = str(results2[0]), relief=sg.RELIEF_SUNKEN, size=(30,1), key = '-TO-'),
        sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Globe_24x24.png'), key='-TOUROP-', border_width=0),
        sg.T(('Номер заявки у туроператора'), auto_size_text=True), sg.In(results[33], size=(20,1)),
        sg.T('Статус', auto_size_text=True), sg.Combo(('Договор','Бронь','Подтверждено','Исполнена'), default_value=results[34], size=(12,1))],
        [sg.T('Валюта тура', auto_size_text=True), sg.Combo(('Евро', 'Доллар', 'Рубль'), default_value=results[21], size=(10,1)), 
        sg.T('Стоимость (руб)', auto_size_text=True), sg.In(results[29],size=(7,1)),
        sg.T('Стоимость (вал)', auto_size_text=True), sg.In(results[28],size=(7,1)),
        sg.T('Аванс', auto_size_text=True), sg.In(results[30],size=(7,1)), 
        sg.T('Курс оператора(Аванс)', auto_size_text=True), sg.In(results[31],size=(7,1))],
        [sg.T('Дата аванса', auto_size_text=True), sg.In(results[22],size=(10,1), key='-DATEA-'),
        sg.CalendarButton(button_text='', image_filename=path.join('ico', 'Calendar_24x24.png'), target='-DATEA-', format='%d.%m.%Y'),
        sg.Combo(('Получено','Оплачено','Нет'), default_value=results[23], size=(8,1)),
        sg.T('Дата оплаты', auto_size_text=True), sg.In(results[24],size=(10,1), key='-DATEO-'),
        sg.CalendarButton(button_text='', image_filename=path.join('ico', 'Calendar_24x24.png'), target='-DATEO-', format='%d.%m.%Y'),
        sg.Combo(('Получено','Оплачено','Нет'), default_value=results[25], size=(8,1)),
        sg.T('Документы до', auto_size_text=True), sg.In(results[26], size=(10,1), key='-DATED-'),
        sg.CalendarButton(button_text='', image_filename=path.join('ico', 'Calendar_24x24.png'), target='-DATED-', format='%d.%m.%Y'),
        sg.Combo(('Получены','Сданы','Выданы','Нет'), default_value=results[27], size=(8,1))],
        [sg.T('_'  * 100, size=(75, 1))],
        [sg.Button('Сохранить'), sg.Button('Выход')]]

    rewnd = sg.Window('Информация по заявке', agencylayout, no_titlebar=False)

    while True:
        event, values =rewnd.read()
        if event == 'Выход'  or event is None:
            break
        if event == '-AHOTEL-': # добавление нового отеля в список по заявке
            answ = sg.popup('Добавить новый отель? ', custom_text=('Да', 'Нет'), button_type=sg.POPUP_BUTTONS_YES_NO)
            if answ == 'Да':
#           Определение номера строки отеля (no_in_table)  
                cursor.execute('SELECT MAX(no_in_table) FROM req_accom WHERE id_req = "'+str(req_id)+'"')
                n_s_h = cursor.fetchone()
                if n_s_h[0] is None:
                    n_str_hotel = 1
                else:
                    n_str_hotel = n_s_h[0] + 1                
                ins_sql = "INSERT INTO req_accom (id_req, no_in_table, date_begin, date_end) VALUES ('" + str(req_id) + "','" + str(n_str_hotel)+ "','" +str(results[6]) + "','" +str(results[7]) + "');"
                cursor.execute(ins_sql)
                conn.commit()
                results3 = listhotel(cursor, req_id)
                reqhotelform(conn,results3[-1],req_id)
                results3 = listhotel(cursor, req_id)
                rewnd['-LHOTEL-'].update(values=results3)
        if event == '-MHOTEL-': # изменение данных по отелю
            if values['-LHOTEL-'] == []:
                nrow = 0
            else:
                nrow = values['-LHOTEL-'][0]
            reqhotelform(conn,results3[nrow],req_id)
            results3 = listhotel(cursor, req_id)
            rewnd['-LHOTEL-'].update(values=results3)

        if event == '-DHOTEL-': # удаление отеля из списка по заявке
            if values['-LHOTEL-'] == []:
                nrow = 0
            else:
                nrow = values['-LHOTEL-'][0]
            answ = sg.popup('Удалить отель ' + str(results3[nrow][3]) + ' из списка?', custom_text=('Да', 'Нет'), button_type=sg.POPUP_BUTTONS_YES_NO)
            if answ == 'Да':
                del_sql = "DELETE FROM req_accom WHERE id_req = ? AND no_in_table = ?"
                column_values = (req_id, results3[nrow][0])
                cursor.execute(del_sql, column_values)
                conn.commit()
                results3 = listhotel(cursor, req_id)
                rewnd['-LHOTEL-'].update(values=results3)
        
        if event == '-DTURIST-':   # удаление туриста из заявки
            if values['-LTURISTS-'] == []:
                nrow = 0
            else:
                nrow = values['-LTURISTS-'][0]     
            answ = sg.popup('Удалить туриста ' + str(results4[nrow][1]) + ' из списка?', custom_text=('Да', 'Нет'), button_type=sg.POPUP_BUTTONS_YES_NO)
            if answ == 'Да':
                del_sql = "DELETE FROM req_tourist WHERE id_req = ? AND id_cust = ?"
                column_values = (req_id, results4[nrow][0])
                cursor.execute(del_sql, column_values)
                conn.commit()
                results4 = listcust(cursor, req_id)
                rewnd['-LTURISTS-'].update(values=results4)

        if event == '-ATURIST-':   # удаление туриста из заявки
            rewnd.Disable()
            cust_id = custform.form(conn)
            if cust_id != 0:
                ins_sql = "INSERT INTO req_tourist (id_req, id_cust) VALUES ('" + str(req_id) + "','" + str(cust_id) + "');"
                cursor.execute(ins_sql)
                conn.commit()                
                results4 = listcust(cursor,req_id)
                rewnd['-LTURISTS-'].update(values=results4)      
            rewnd.Enable()
            rewnd.BringToFront()

        if event == '-CUST-':
            rewnd.Disable()
            cust_id = custform.form(conn)
            if cust_id != 0:
                cursor.execute("SELECT fio FROM Cat_cust WHERE id_cust = "+ str(cust_id))
                results1 = cursor.fetchone()
                rewnd['-FIO-'].update(results1[0])
                answ = sg.popup('Добавить ' + results1[0] +' в список туристов по заявке?', custom_text=('Да', 'Нет'))
                if answ == 'Да':
                    ins_sql = "INSERT INTO req_tourist (id_req, id_cust) VALUES ('" + str(req_id) + "','" + str(cust_id) + "');"
                    cursor.execute(ins_sql)
                    conn.commit()
                    results4 = listcust(cursor,req_id)
                    rewnd['-LTURISTS-'].update(values=results4)
            rewnd.Enable()
            rewnd.BringToFront()

        if event == '-TOUROP-':
            try:
                rewnd.Disable()
                id_oper = touropform.form(conn)
                if id_oper != 0:
                    cursor.execute("SELECT name_short_to FROM Cat_tourop WHERE id_to = "+ str(id_oper))
                    results2 = cursor.fetchone()
                    rewnd['-TO-'].update(results2[0])
                rewnd.Enable()
                rewnd.BringToFront()
            except:
                answ = sg.popup("ERROR", "-TOUROP-")

        if event == ('Сохранить'):
            answ = sg.popup('Сохранить внесенные изменения ', custom_text=('Сохранить', 'Отмена'), button_type=sg.POPUP_BUTTONS_YES_NO)
#            if answ == 'Сохранить':
#                upd_sql = "UPDATE list_request SET date_req = '" + str(values['-DATR-']) + "', numb_contr = '" + str(values[0]) + \
#                "', country = '" + str(values[1]) + "', region = '" + str(values[2]) + "', id_cust = '" + str(cust_id) + \
#                "', date_tour = '" + str(values['-DATEB-']) + "', date_end_tour = '" + str(values['-DATEE-']) + \
#                "', quant_night = '" + str(values[3]) + "', ticket = '" + str(values[4]) +"', transfer = '" + str(values[5]) + \
#                "', excur_prog  = '" + str(values[6]) + "', other_serv = '" + str(values[7]) + \
#                "', tour_guide = '" +str(values[8]) + "', transl_guide = '" + str(values[9]) + "', team_leader = '" + str(values[10]) + \
#                "', visa = '" + str(values[11]) + "', med_ins = '" + str(values[12]) + "', acc_ins = '" + str(values[13]) + \
#                "', fail_ins = '" + str(values[14]) + "', id_to = '" + str(id_oper) + "', prim_ins = '" + str(values[15]) + "', curr_tour = '" + str(values[16])+ \
#                "', date_prepay = '" + str(values['-DATEA-']) + "', paid_prepay = '" + str(values[17]) + \
#                "', date_full_pay = '" + str(values['-DATEO-']) + "', paid_full_pay = '" + str(values[18]) + \
#                "', date_doc = '" + str(values['-DATED-']) + "', rec_doc = '" + str(values[19]) + "', cost_tour_curr = '" + str(values[20]) + \
#                "', cost_tour_rub = '" + str(values[21]) + "', prepay_rub = '" + str(values[22]) + "', rate_to = '" + str(values[23]) + \
#                "' WHERE id_req = '" + str(req_id) + "';"
#                cursor.execute(upd_sql)
#                conn.commit()
#            break

    rewnd.close()
    return req_id
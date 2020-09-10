import PySimpleGUI as sg
import sqlite3 as sql

def form (conn):
    agency_id = 1
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Agency_card WHERE id = "+ str(agency_id))
    results = cursor.fetchone()

    agencylayout = [
        [sg.T('Информация о предприятии', auto_size_text=True)],
        [sg.T('_'  * 100, size=(75, 1))],
        [sg.T('Наименование', size=(15,1)), sg.In(results[1], size=(70,1))],
        [sg.T('Адрес', size=(15,1)), sg.In(results[2],size=(70,1))],
        [sg.T('ИНН', size=(15,1)), sg.In(results[3],size=(10,1)), sg.T('КПП', auto_size_text=True),
        sg.In(results[4],size=(9,1)), sg.T('ОГРН',auto_size_text=True), sg.In(results[5],size=(15,1)), sg.T('ОКВЭД',
        auto_size_text=True), sg.In(results[6],size=(5,1))],
        [sg.T('Телефон', size=(15,1)), sg.In(results[7],size=(12,1)), sg.T('E-mail', auto_size_text=True),
        sg.In(results[8],size=(15,1)), sg.T('WWW',auto_size_text=True), sg.In(results[9],size=(15,1))],
        [sg.T('Директор', size=(15,1)), sg.In(results[10],size=(25,1))],
        [sg.T('_'  * 100, size=(75, 1))],
        [sg.T('Наименование банка', size=(15,1)), sg.In(results[11],size=(70,1))],
        [sg.T('Р/С', size=(15,1)), sg.In(results[12],size=(70,1))],
        [sg.T('К/С', size=(15,1)), sg.In(results[13],size=(70,1))],
        [sg.T('БИК', size=(15,1)), sg.In(results[14],size=(7,1))],
        [sg.T('_'  * 100, size=(75, 1))],
        [sg.Button('Сохранить'), sg.Button('Выход')]]

    agwnd = sg.Window('Информация о предприятии', agencylayout, no_titlebar=False)

    while True:
        event, values =agwnd.read()
        if event == 'Выход'  or event is None:
            break

        if event in ('Сохранить'):
            upd_sql = "UPDATE Agency_card SET name = '" + str(values[0]) + "', adress = '" + str(values[1]) + "', inn = '" + str(values[2]) + "', kpp = '" + str(values[3]) + "', ogrn = '" + str(values[4]) + "', okved = '" + str(values[5]) + "', phone = '" + str(values[6]) + "', e_mail = '" + str(values[7]) + "', www = '" + str(values[8]) +"', boss = '" + str(values[9]) + "', bank_name  = '" + str(values[10]) + "', account = '" + str(values[11]) + "', cor_account = '" +str(values[12]) + "', bank_bik = '" + str(values[13]) + "' WHERE id = " + str(agency_id) +";"
            cursor.execute(upd_sql)
            conn.commit()

    agwnd.close()

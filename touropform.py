import PySimpleGUI as sg
import sqlite3 as sql
from os import path

def updatewnd(townd, results1):     # Обновление правой колонки макета

    townd['-FNAME-'].update(results1[1])
    townd['-SNAME-'].update(results1[2])
    townd['-ADR-'].update(results1[3])
    townd['-INN-'].update(results1[4])
    townd['-KPP-'].update(results1[5])
    townd['-TEL-'].update(results1[6])
    townd['-EMAIL-'].update(results1[7])
    townd['-NREE-'].update(results1[8])
    townd['-SITE-'].update(results1[9])
    townd['-STRA-'].update(results1[10])
    townd['-ADST-'].update(results1[11])
    townd['-STTEL-'].update(results1[12])
    townd['-STDO-'].update(results1[13])
    townd['-DATEB-'].update(results1[14])
    townd['-DATEE-'].update(results1[15])

def updatelst(cursor, townd):       # Обновление списка туроператоров
    cursor.execute("SELECT name_short_to FROM Cat_tourop ORDER BY name_short_to ASC")
    results = cursor.fetchall()
    townd['-LIST-'].update(results)
    return results[0]

def form (conn):
#   работа с таблицей БД по туроператорам
#   возвращает ID оператора или 0 если выход без выбора
#
#   получение списка туроператоров
    cursor = conn.cursor()
    cursor.execute("SELECT name_short_to FROM Cat_tourop ORDER BY name_short_to ASC")
    results = cursor.fetchall()
#   получение информации по первому туроператору
    s_name = results[0]
    cursor.execute("SELECT * FROM Cat_tourop WHERE name_short_to=?",s_name)
    results1 = cursor.fetchone()
#   макет окна
    column_to = [[sg.Text('Информация о туроператоре')],
    [sg.T('Полное наименование', size=(20,1)), sg.In(size=(70,1), key='-FNAME-', default_text=results1[1])],
    [sg.T('Адрес', size=(20,1)), sg.In(size=(70,1), key='-ADR-', default_text=results1[3])],
    [sg.T('Сокращенное наименование', size=(20,1)), sg.In(size=(30,1), key='-SNAME-', default_text=results1[2])],
    [sg.T('ИНН', size=(20,1)), sg.In(size=(10,1), key='-INN-', default_text=results1[4]), sg.T('КПП', auto_size_text=True),
    sg.In(size=(9,1), key='-KPP-', default_text=results1[5]), sg.T('Номер в реестре', auto_size_text=True), sg.In(size=(10,1), key='-NREE-',default_text=results1[8])],
    [sg.T('Телефон', size=(20,1)), sg.In(size=(12,1), key='-TEL-', default_text=results1[6]),
    sg.T('E-mail', auto_size_text=True), sg.In(size=(20,1), key='-EMAIL-', default_text=results1[7]),
    sg.T('Сайт',auto_size_text=True), sg.In(size=(20,1), key='-SITE-', default_text=results1[9])],
    [sg.T('_'  * 100, size=(100, 1))],
    [sg.T('Финансовое обеспечение', size=(40,1))],
    [sg.T('Наименование страховщика', size=(20,1)), sg.In(size=(70,1), key='-STRA-', default_text=results1[10])],
    [sg.T('Адрес', size=(20,1)), sg.In(size=(70,1), key='-ADST-', default_text=results1[11])],
    [sg.T('Наименование договора', size=(20,1)), sg.In(size=(70,1), key='-STDO-', default_text=results1[13])],
    [sg.T('Период действия, с:', size=(20,1)), sg.In(size=(10,1), key='-DATEB-', default_text=results1[14]), sg.CalendarButton(button_text='', image_filename=path.join('ico', 'Calendar_24x24.png'), target='-DATEB-', format='%d.%m.%Y'),
    sg.T('по:', auto_size_text=True), sg.In(size=(10,1), key='-DATEE-', default_text=results1[15]),  sg.CalendarButton(button_text='', image_filename=path.join('ico', 'Calendar_24x24.png'), target='-DATEE-', format='%d.%m.%Y'),
    sg.T('Телефон', auto_size_text=True), sg.In(size=(12,1), key='-STTEL-', default_text=results1[12])],
    [sg.Button('Сохранить', tooltip='Сохранить внесенные изменения'), sg.Button('Выход', tooltip='Выход')]]

    column_to_list = [[sg.Text('Список туроператоров')],
    [sg.Listbox(values=results, size=(30, 15), key='-LIST-', default_values=results[0], enable_events=True, auto_size_text=True, pad=(5, 5), select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)],
    [sg.Button('Новый', tooltip='Новый туроператор'), sg.Button('Удалить', tooltip='Удалить'), sg.Button('Выбрать', tooltip='Выбор туроператора для договора')]]

    tolayout = [[ sg.Column(column_to_list), sg.Column(column_to)]]

    townd = sg.Window('Список туроператоров', tolayout, no_titlebar=False)

    while True:
        event, values =townd.read()
        if event == "-LIST-":   #перемещение по списку
            p1 = values['-LIST-']
            s_name = p1[0]
            cursor.execute("SELECT * FROM Cat_tourop WHERE name_short_to=?",s_name)
            results1 = cursor.fetchone()
            updatewnd(townd, results1)

        if event == 'Выход'  or event is None:
            id_oper = 0
            break

        if event == 'Новый':
            answ = sg.popup_get_text('Введите сокращенное имя нового оператора')
            if answ != None:
#               вставка записи с введенным именем
                ins_sql = "INSERT INTO Cat_tourop (name_short_to) VALUES ('" + answ + "');"
                cursor.execute(ins_sql)
                conn.commit()
                s_name = updatelst(cursor, townd)
#               получение данных по умолчанию
                sel_sql = "SELECT * FROM Cat_tourop WHERE name_short_to='"+ answ + "';"
                cursor.execute(sel_sql)
                results1 = cursor.fetchone()
                updatewnd(townd, results1)

        if event == 'Удалить':
            answ = sg.popup('Удалить данные оператора ' + results1[2], custom_text=('Удалить', 'Отмена'), button_type=sg.POPUP_BUTTONS_YES_NO)
            if answ == 'Удалить':
#               удаление записи по туроператору
                del_sql = "DELETE FROM Cat_tourop WHERE name_short_to = '" + results1[2] + "';"
                cursor.execute(del_sql)
                conn.commit()
#               обновление списка
                s_name = updatelst(cursor, townd)
#               получение информации по первому в списке и обновление правой части
                sel_sql = "SELECT * FROM Cat_tourop WHERE name_short_to='"+ s_name[0] + "';"
                cursor.execute(sel_sql)
                results1 = cursor.fetchone()
                updatewnd(townd, results1)
        if event == 'Выбрать':
            id_oper = results1[0]
            break

        if event == 'Сохранить':
            answ = sg.popup('Сохранить внесенные изменения ' + results1[2], custom_text=('Сохранить', 'Отмена'), button_type=sg.POPUP_BUTTONS_YES_NO)
            if answ == 'Сохранить':
                upd_sql = "UPDATE Cat_tourop SET name_full_to = '" + str(values['-FNAME-']) + "', name_short_to = '" + str(values['-SNAME-']) + "', adress_to = '" + str(values['-ADR-']) + "', inn_to = '" + str(values['-INN-']) + "', kpp_to = '" + str(values['-KPP-']) + "', tel_to = '" + str(values['-TEL-']) + "', email_to = '" + str(values['-EMAIL-']) + "', num_fedr_to = '" + str(values['-NREE-']) + "', site = '" + str(values['-SITE-']) + "', name_strah = '" + str(values['-STRA-']) + "', adress_strah = '" + str(values['-ADST-']) + "', tel_strah = '" + str(values['-STTEL-']) + "', text_strah = '" + str(values['-STDO-']) + "', date_beg_strah = '" + str(values['-DATEB-']) + "', date_end_strah = '" + str(values['-DATEE-']) + "' WHERE id_to = '" + str(results1[0]) + "';"
                cursor.execute(upd_sql)
                conn.commit()
                s_name = updatelst(cursor, townd)

    townd.close()

    return id_oper

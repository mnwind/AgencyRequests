import PySimpleGUI as sg
import agform
import touropform
import custform
import reqsettings
import reqsimpleform

from os import path
import sqlite3 as sql


def listreq(cursor):
#    results = [['' for _ in range(len(header_list_req))]]
    sel_sql = 'SELECT id_req, id_cust, country, date_tour, date_end_tour, id_to, status_req, date_prepay, paid_prepay, date_full_pay, paid_full_pay, date_doc, rec_doc FROM list_request'
    cursor.execute(sel_sql)
    results = cursor.fetchall()
    count_sql = 'SELECT COUNT(*) FROM req_tourist WHERE id_req = ?'
    sel_sql_cust = 'SELECT fio FROM cat_cust WHERE id_cust = ?'
    sel_sql_to = 'SELECT name_short_to FROM cat_tourop WHERE id_to = ?'
    for i in range(len(results)):
        results[i] = list(results[i])
#       Заказчик по id
        if results[i][1] != 0:
            cursor.execute(sel_sql_cust,(results[i][1],))
            fio_cust = cursor.fetchone()
            results[i][1] = fio_cust[0]
        else:
            results[i][1] = ''
#       Оператор по id
        if results[i][5] != 0:
            cursor.execute(sel_sql_to,(results[i][5],))
            nshort_to = cursor.fetchone()
            results[i][5] = nshort_to[0]
        else:
            results[i][5] = ''
#       вставка количество человек по заявке        
        cursor.execute(count_sql,str(results[i][0]))
        n_p = cursor.fetchall()
        results[i].insert(2,n_p[0])
 
    return results

# Получение настроек
SETTINGS_FILE = path.join(path.dirname(__file__), r'settings_file.cfg')
DEFAULT_SETTINGS = {'db_file': None , 'theme': sg.theme()}
settings = reqsettings.load_settings(SETTINGS_FILE, DEFAULT_SETTINGS )
c_theme = settings['theme']
c_dbfile = settings['db_file']
# Открытие БД
try:
    conn = sql.connect(c_dbfile)
    cursor = conn.cursor()
except:
    reqsettings.form()
    conn = sql.connect(c_dbfile)
    cursor = conn.cursor()
# TODO Проверка БД на пустоту
# Установка темы
sg.theme(c_theme)
#форморование таблицы заявок
header_list_req = ['ID','Заказчик','Туристов','Направление','Начало','Окончание','Оператор','Статус заявки','Аванс до','Статус аванса','Оплата до','Статус оплаты','Документы','Статус']
results = listreq(cursor)
# Макет окна
menu_def = [['Заявки', ['Новая', 'E&xit']],
            ['Справочники', ['Клиенты', 'Операторы', 'Агентство']],
            ['О программе', ['Настройки', '&Help']]
            ]
layout = [
    [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
#    [sg.Text('')],
    [sg.Text('Тут будет что-то про заявки', size=(100, 1))]
    ,[sg.Table( values=results, headings=header_list_req, key='-LREQS-', enable_events=False, justification='center', bind_return_key = True,
    num_rows = 20, select_mode=sg.TABLE_SELECT_MODE_BROWSE, tooltip='Список заявок', auto_size_columns=True)]
    ]
window = sg.Window("Заявки агентства", layout)


while True:     # Обработка событий
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'Новая':
        window.Disable()
        req_id = 0
        req_id = reqsimpleform.form(conn, req_id)
        window.Enable()
        window.BringToFront()
    if event == 'Клиенты':
        window.Disable()
        id_cust = custform.form(conn)
        window.Enable()
        window.BringToFront()
    if event == 'Операторы':
        window.Disable()
        id_oper = touropform.form(conn)
        window.Enable()
        window.BringToFront()
    if event == 'Агентство':
        window.Disable()
        agform.form(conn)
        window.Enable()
        window.BringToFront()
    if event == 'Настройки':
        window.Disable()
        reqsettings.form()
        window.Enable()
        window.BringToFront()
    if event == '-LREQS-':
        if values['-LREQS-'] == []:
            nrow = 0
        else:
            nrow = values['-LREQS-'][0]
        req_id = results[nrow][0]
        req_id = reqsimpleform.form(conn, req_id)
        results = listreq(cursor)
        window['-LREQS-'].update(results)
conn.close()    # Закрытие БД
window.close()

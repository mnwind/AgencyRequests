import PySimpleGUI as sg
import agform
import touropform
import custform
import reqsettings
import reqsimpleform
import xlwt
from tempfile import TemporaryFile
from os import path, startfile
import sqlite3 as sql
from datetime import datetime, date, timedelta


def filtrstr(status_txt):
    today = date.today()
    mmonth = today - timedelta(days=30)
    today = today.strftime("%d.%m.%Y")
    mmonth = mmonth.strftime("%d.%m.%Y")
    bt_layout = [[
                sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Check_24x24.png'), key='-CHECK-', tooltip = 'Применить' ),
                sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Log Out_24x24.png'), key='-EXT-', tooltip = 'Выход' ),
                ]]
    fr_layout = [
                [sg.Radio('Заявки с:', "RADIOFL", key = '-DATER-', default = True), sg.In(size=(10,1), key = '-DATEB-', default_text = mmonth),sg.T('по:'), sg.In(size=(10,1), key = '-DATEE-', default_text = today)],
                [sg.Radio('Оплата (аванс и/или полная)', "RADIOFL", key = '-PAY-'), sg.T('в течение следующих '), sg.In(size=(2,1), key = '-DOPL-',default_text='3'), sg.T('дней')],
                [sg.Radio('Прием/выдача документов', "RADIOFL", key = '-DOCS-'), sg.T('в течение следующих '), sg.In(size=(2,1), key = '-DDOC-',default_text='3'), sg.T('дней')],
                [sg.Radio('Начало тура', "RADIOFL", key = '-BEG-'), sg.T('в течение следующих '), sg.In(size=(2,1), key = '-DBEG-',default_text='3'), sg.T('дней')],
                ]
    fl_layout = [
        [sg.Frame('', fr_layout)],
        [sg.Checkbox('Сбросить все фильтры', key = '-UNCHECK-')],
        [sg.Frame('', bt_layout, element_justification = "center")],
    ]
    flwnd = sg.Window('Фильтры', fl_layout, no_titlebar=False)
    while True:
        event, values =flwnd.read()
        if event in (sg.WIN_CLOSED, '-EXT-'):
            flstr = ''
            break
        if event == '-CHECK-':
            if values['-PAY-']:
                datpay = date.today() + timedelta(days=int(values['-DOPL-'])) 
                status_txt = 'Фильтр: Оплата в течение следующих ' + str(values['-DOPL-']) + ' дней'
                print(datpay)
                flstr = ''
            if values['-DOCS-']:
                datdoc = date.today() + timedelta(days=int(values['-DDOC-']))
                status_txt = 'Фильтр: Документы в течение следующих ' + str(values['-DDOC-']) + ' дней'
                flstr = ' WHERE substr(date_doc,7)||"-"||substr(date_doc,4,2)||"-"||substr(date_doc,1,2) <= "' + str(datdoc) + '" AND rec_doc != "Выданы"'
            if values['-BEG-']:
                dattour = date.today() + timedelta(days=int(values['-DBEG-']))
                status_txt = 'Фильтр: Начало тура в течение следующих ' + str(values['-DBEG-']) + ' дней'
                flstr = ' WHERE substr(date_tour,7)||"-"||substr(date_tour,4,2)||"-"||substr(date_tour,1,2) <= "' + str(dattour) + '" AND status_req != "Исполнена"'
            if values['-DATER-']:
                datbeg = datetime.strptime(values['-DATEB-'], "%d.%m.%Y").date()
                datend = datetime.strptime(values['-DATEE-'], "%d.%m.%Y").date()
                status_txt = 'Фильтр: Дата заявки с ' + str(datbeg) + ' по ' + str(datend)
                flstr = ' WHERE substr(date_req,7)||"-"||substr(date_req,4,2)||"-"||substr(date_req,1,2) BETWEEN "' + str(datbeg) +'" AND "' + str(datend) +'";'
            if values['-UNCHECK-']:
                flstr = ''
                status_txt = 'Без фильтра'
            break
    return flstr, status_txt

def xlsexport(results, header):
    xls_filename=path.join('tpl', 'temp.xls')
    book = xlwt.Workbook()
    sheet1 = book.add_sheet('Заявки')
    results.insert(0, header)
    for rownum, sublist in enumerate(results):
        for colnum, value in enumerate(sublist):
            sheet1.write(rownum, colnum, value)
    try:
        book.save(xls_filename)
        book.save(TemporaryFile())
        startfile(xls_filename)
    except:
        sg.popup('Закройте временный файл')

def delreq (conn, req_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM req_tourist WHERE id_req = '" + str(req_id) + "';")
    cursor.execute("DELETE FROM req_accom WHERE id_req = '" + str(req_id) + "';")
    cursor.execute("DELETE FROM req_trans WHERE id_req = '" + str(req_id) + "';")
    cursor.execute("DELETE FROM list_request WHERE id_req = '" + str(req_id) + "';")
    conn.commit()


def listreq(cursor, flstr):
    sel_sql = 'SELECT id_req, id_cust, country, date_tour, date_end_tour, id_to, status_req, date_prepay, paid_prepay, date_full_pay, paid_full_pay, date_doc, rec_doc FROM list_request' + flstr
#    print(sel_sql)
    cursor.execute(sel_sql)
    results = cursor.fetchall()
    if results == [] and flstr == '':
        sg.popup('Список заявок пуст. Будет вставлена пустая запись')
        ins_sql = "INSERT INTO list_request (country) VALUES (' ');"
        cursor.execute(ins_sql)
        conn.commit()
        cursor.execute(sel_sql)
        results = cursor.fetchall()
    count_sql = 'SELECT COUNT(*) FROM req_tourist WHERE id_req = ?'
    sel_sql_cust = 'SELECT fio FROM cat_cust WHERE id_cust = ?'
    sel_sql_to = 'SELECT name_short_to FROM cat_tourop WHERE id_to = ?'
    for i in range(len(results)):
        results[i] = list(results[i])
#       Заказчик по id
        if results[i][1] != 0:
            try:
                cursor.execute(sel_sql_cust,(results[i][1],))
                fio_cust = cursor.fetchone()
                results[i][1] = fio_cust[0]
            except:
                results[i][1] = ''
        else:
            results[i][1] = ''
#       Оператор по id
        if results[i][5] != 0:
            try:
                cursor.execute(sel_sql_to,(results[i][5],))
                nshort_to = cursor.fetchone()
                results[i][5] = nshort_to[0]
            except:
                results[i][5] = ''
        else:
            results[i][5] = ''
#       вставка количество человек по заявке        
        cursor.execute(count_sql,str(results[i][0]))
        n_p = cursor.fetchall()
        results[i].insert(2,n_p[0][0])
 
    return results

# Получение настроек
SETTINGS_FILE = path.join(path.dirname(__file__), r'settings_file.cfg')
DEFAULT_SETTINGS = {'db_file': None , 'theme': sg.theme()}
settings = reqsettings.load_settings(SETTINGS_FILE, DEFAULT_SETTINGS )
c_theme = settings['theme']
c_dbfile = settings['db_file']
# Открытие БД
try:
    conn = sql.connect(c_dbfile
#    , detect_types=sql.PARSE_DECLTYPES|sql.PARSE_COLNAMES
    )
    cursor = conn.cursor()
except:
    reqsettings.form()
    conn = sql.connect(c_dbfile)
    cursor = conn.cursor()

#conn.execute("PRAGMA foreign_keys = ON")
# TODO Проверка БД на пустоту
# Установка темы
sg.theme(c_theme)
#форморование таблицы заявок
flstr = ''
status_txt = 'Без фильтра                                                            '
header_list_req = ['ID','Заказчик','Туристов','Направление','Начало','Окончание','Оператор','Статус заявки','Аванс до','Статус аванса','Оплата до','Статус оплаты','Документы','Статус']
results = listreq(cursor, flstr)
# Макет окна
#menu_def = [['Заявки', ['Новая', 'Удалить', 'E&xit']],
#            ['Справочники', ['Клиенты', 'Операторы', 'Агентство']],
#            ['О программе', ['Настройки', '&Help']]
#            ]
frame_layout = [[sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Copy v2_32x32.png'), key='-CCUST-', tooltip = 'Справочник клиентов'),
                sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Globe_32x32.png'), key='-COPER-', tooltip = 'Справочник операторов' ), 
                sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Information_32x32.png'), key='-AGNCY-', tooltip = 'Информация о агентстве' ),
                sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Settings_32x32.png'), key='-SETNG-', tooltip = 'Настройки' ),
                sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Help_32x32.png'), key='-HELP-', tooltip = 'Помощь' ),
                sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Log Out_32x32.png'), key='-EXIT-', tooltip = 'Выход' ),
                ]]
layout = [
#    [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
#    [sg.Text('')],
    [sg.Table( values=results, headings=header_list_req, key='-LREQS-', enable_events=False, bind_return_key = True,
    num_rows = 25, select_mode=sg.TABLE_SELECT_MODE_EXTENDED, tooltip='Список заявок', auto_size_columns=True)]
    ,[ sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Add_24x24.png'), key='-AREQ-', tooltip = 'Новая заявка'),
    sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Properties_24x24.png'), key='-MREQ-', tooltip = 'Редактировать заявку'),
    sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Delete_24x24.png'), key='-DREQ-', tooltip = 'Удалить заявку'),
    sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Upload_24x24.png'), key='-EXPORT-', tooltip = 'Экспорт в xls'),
    sg.Button('', auto_size_button=True, image_filename=path.join('ico', 'Zoom In_24x24.png'), key='-FILTR-', tooltip = 'Фильтр')],
    [sg.HorizontalSeparator()],
    [sg.Frame('', frame_layout, element_justification = "center")],
#    [sg.Text(key='-EXPAND-', font='ANY 1', pad=(0,0))],
    [sg.StatusBar(status_txt, key = '-STATUSBAR-', auto_size_text = True, relief = "ridge")]
    ]
window = sg.Window("Заявки агентства", layout, element_justification='center', margins = (15, 15), no_titlebar = False, border_depth = 5, finalize = True)

#window['-EXPAND-'].expand(True, True, True)
while True:     # Обработка событий
    event, values = window.read()
    if event in (sg.WIN_CLOSED, '-EXIT-'):
        break
    if event == '-AREQ-':
#        window.disappear()
        window.Disable()
        req_id = 0
        req_id = reqsimpleform.form(conn, req_id)
        results = listreq(cursor, flstr)
        window['-LREQS-'].update(results)
#        window.reappear()
        window.Enable()
        window.BringToFront()

    if event == '-DREQ-':
        if values['-LREQS-'] == []:
            nrow = 0
        else:
            nrow = values['-LREQS-'][0]
        req_id = results[nrow][0]
        answ = sg.popup('Удалить данные по заявке ' + str(req_id), custom_text=('Удалить', 'Отмена'), button_type=sg.POPUP_BUTTONS_YES_NO)
        if answ == 'Удалить':
           delreq(conn, req_id)
        results = listreq(cursor, flstr)
        window['-LREQS-'].update(results)

    if event == '-CCUST-':
        window.Disable()
        id_cust = custform.form(conn)
        window.Enable()
        window.BringToFront()
        window['-LREQS-'].update(results)
    if event == '-COPER-':
        window.Disable()
        id_oper = touropform.form(conn)
        window.Enable()
        window.BringToFront()
        window['-LREQS-'].update(results)
    if event == '-AGNCY-':
        window.Disable()
        agform.form(conn)
        window.Enable()
        window.BringToFront()
    if event == '-SETNG-':
        window.Disable()
        reqsettings.form()
        window.Enable()
        window.BringToFront()
    if event == '-LREQS-' or event == '-MREQ-':
        if values['-LREQS-'] == []:
            nrow = 0
        else:
            nrow = values['-LREQS-'][0]
        req_id = results[nrow][0]
        req_id = reqsimpleform.form(conn, req_id)
        results = listreq(cursor, flstr)
        window['-LREQS-'].update(results)
    if event == '-EXPORT-':
        answ = sg.popup('Экспортировать таблицу заявок в xls файл? ', custom_text=('Да', 'Нет'), button_type=sg.POPUP_BUTTONS_YES_NO)
        if answ == 'Да':
            xlsexport(results, header_list_req)
    if event == '-FILTR-':
        window.Disable()
        flstr, status_txt = filtrstr(status_txt)
        results = listreq(cursor, flstr)
        window['-LREQS-'].update(results)
        window['-STATUSBAR-'].update(status_txt)
        window.Enable()
        window.BringToFront()

conn.close()    # Закрытие БД
window.close()

import PySimpleGUI as sg
import agform
import touropform
import custform
import reqsettings
import reqsimpleform

from os import path
import sqlite3 as sql

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
# TODO Проверка БД на пустоту
# Установка темы
sg.theme(c_theme)
# Макет окна
menu_def = [['Заявки', ['Новая', 'E&xit']],
            ['Справочники', ['Клиенты', 'Операторы', 'Агентство']],
            ['О программе', ['Настройки', '&Help']]
            ]
layout = [
    [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
    [sg.Text('')],
    [sg.Text('Тут будет что-то про заявки', size=(25, 2))],
    ]
window = sg.Window("Заявки агентства", layout, resizable=True, finalize=True)
window.Maximize()

while True:     # Обработка событий
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'Новая':
        window.Disable()
        id_req = reqsimpleform.form(conn)
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
conn.close()    # Закрытие БД
window.close()

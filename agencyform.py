import wx
import sqlite3 as sql
def form (agencywnd):
        agency_id = 1
        conn = sql.connect('AgencyReq.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Agency_card WHERE id = "+ str(agency_id))
        results = cursor.fetchone()

        bSizer3 = wx.BoxSizer( wx.VERTICAL )
        fgSizer4 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer4.AddGrowableCol( 1 )
        fgSizer4.SetFlexibleDirection( wx.BOTH )
        fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        agencywnd.m_staticText8 = wx.StaticText( agencywnd, wx.ID_ANY, u"Наименование организации" )
        agencywnd.m_staticText8.Wrap( -1 )

        agencywnd.m_staticText8.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        fgSizer4.Add( agencywnd.m_staticText8, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        agencywnd.m_textCtrl4 = wx.TextCtrl( agencywnd, wx.ID_ANY, results[1], wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        fgSizer4.Add( agencywnd.m_textCtrl4, 0, wx.ALL|wx.EXPAND, 5 )

        agencywnd.m_staticText14 = wx.StaticText( agencywnd, wx.ID_ANY, u"Адрес", wx.DefaultPosition, wx.DefaultSize, 0 )
        agencywnd.m_staticText14.Wrap( -1 )

        agencywnd.m_staticText14.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        fgSizer4.Add( agencywnd.m_staticText14, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        agencywnd.m_textCtrl9 = wx.TextCtrl( agencywnd, wx.ID_ANY, results[2], wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer4.Add( agencywnd.m_textCtrl9, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer3.Add( fgSizer4, 0, wx.ALL|wx.EXPAND, 5 )

        fgSizer2 = wx.FlexGridSizer( 0, 8, 0, 0 )
        fgSizer2.SetFlexibleDirection( wx.BOTH )
        fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        agencywnd.m_staticText9 = wx.StaticText( agencywnd, wx.ID_ANY, u"ИНН", wx.DefaultPosition, wx.DefaultSize, 0 )
        agencywnd.m_staticText9.Wrap( -1 )

        fgSizer2.Add( agencywnd.m_staticText9, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        agencywnd.m_textCtrl5 = wx.TextCtrl( agencywnd, wx.ID_ANY, results[3], wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer2.Add( agencywnd.m_textCtrl5, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        agencywnd.m_staticText10 = wx.StaticText( agencywnd, wx.ID_ANY, u"КПП", wx.DefaultPosition, wx.DefaultSize, 0 )
        agencywnd.m_staticText10.Wrap( -1 )

        fgSizer2.Add( agencywnd.m_staticText10, 0, wx.ALL, 5 )

        agencywnd.m_textCtrl6 = wx.TextCtrl( agencywnd, wx.ID_ANY, results[4], wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer2.Add( agencywnd.m_textCtrl6, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        agencywnd.m_staticText11 = wx.StaticText( agencywnd, wx.ID_ANY, u"ОГРН", wx.DefaultPosition, wx.DefaultSize, 0 )
        agencywnd.m_staticText11.Wrap( -1 )

        fgSizer2.Add( agencywnd.m_staticText11, 0, wx.ALL, 5 )

        agencywnd.m_textCtrl7 = wx.TextCtrl( agencywnd, wx.ID_ANY, results[5], wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer2.Add( agencywnd.m_textCtrl7, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        agencywnd.m_staticText12 = wx.StaticText( agencywnd, wx.ID_ANY, u"ОКВЭД", wx.DefaultPosition, wx.DefaultSize, 0 )
        agencywnd.m_staticText12.Wrap( -1 )

        fgSizer2.Add( agencywnd.m_staticText12, 0, wx.ALL, 5 )

        agencywnd.m_textCtrl8 = wx.TextCtrl( agencywnd, wx.ID_ANY, results[6], wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer2.Add( agencywnd.m_textCtrl8, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        agencywnd.m_staticText15 = wx.StaticText( agencywnd, wx.ID_ANY, u"Телефон", wx.DefaultPosition, wx.DefaultSize, 0 )
        agencywnd.m_staticText15.Wrap( -1 )

        fgSizer2.Add( agencywnd.m_staticText15, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        agencywnd.m_textCtrl10 = wx.TextCtrl( agencywnd, wx.ID_ANY, results[7], wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer2.Add( agencywnd.m_textCtrl10, 0, wx.ALL, 5 )

        agencywnd.m_staticText16 = wx.StaticText( agencywnd, wx.ID_ANY, u"E-mail", wx.DefaultPosition, wx.DefaultSize, 0 )
        agencywnd.m_staticText16.Wrap( -1 )

        fgSizer2.Add( agencywnd.m_staticText16, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        agencywnd.m_textCtrl11 = wx.TextCtrl( agencywnd, wx.ID_ANY, results[8], wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer2.Add( agencywnd.m_textCtrl11, 0, wx.ALL, 5 )

        agencywnd.m_staticText17 = wx.StaticText( agencywnd, wx.ID_ANY, u"WWW", wx.DefaultPosition, wx.DefaultSize, 0 )
        agencywnd.m_staticText17.Wrap( -1 )

        fgSizer2.Add( agencywnd.m_staticText17, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        agencywnd.m_textCtrl12 = wx.TextCtrl( agencywnd, wx.ID_ANY, results[9], wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer2.Add( agencywnd.m_textCtrl12, 0, wx.ALL, 5 )

        agencywnd.m_staticText151 = wx.StaticText( agencywnd, wx.ID_ANY, u"Директор", wx.DefaultPosition, wx.DefaultSize, 0 )
        agencywnd.m_staticText151.Wrap( -1 )

        fgSizer2.Add( agencywnd.m_staticText151, 0, wx.ALL, 5 )

        agencywnd.m_textCtrl141 = wx.TextCtrl( agencywnd, wx.ID_ANY, results[10], wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer2.Add( agencywnd.m_textCtrl141, 1, wx.ALL, 5 )


        bSizer3.Add( fgSizer2, 0, wx.EXPAND, 5 )

        bSizer4 = wx.BoxSizer( wx.VERTICAL )

        agencywnd.m_staticText13 = wx.StaticText( agencywnd, wx.ID_ANY, u"Банковские реквизиты", wx.DefaultPosition, wx.DefaultSize, 0 )
        agencywnd.m_staticText13.Wrap( -1 )

        agencywnd.m_staticText13.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        bSizer4.Add( agencywnd.m_staticText13, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        bSizer3.Add( bSizer4, 0, wx.EXPAND, 5 )

        fgSizer5 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer5.AddGrowableCol( 1 )
        fgSizer5.SetFlexibleDirection( wx.BOTH )
        fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        agencywnd.m_staticText19 = wx.StaticText( agencywnd, wx.ID_ANY, u"Наименование банка", wx.DefaultPosition, wx.DefaultSize, 0 )
        agencywnd.m_staticText19.Wrap( -1 )

        fgSizer5.Add( agencywnd.m_staticText19, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        agencywnd.m_textCtrl16 = wx.TextCtrl( agencywnd, wx.ID_ANY, results[11], wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer5.Add( agencywnd.m_textCtrl16, 0, wx.ALL|wx.EXPAND, 5 )

        agencywnd.m_staticText21 = wx.StaticText( agencywnd, wx.ID_ANY, u"Р/С", wx.DefaultPosition, wx.DefaultSize, 0 )
        agencywnd.m_staticText21.Wrap( -1 )

        fgSizer5.Add( agencywnd.m_staticText21, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        agencywnd.m_textCtrl14 = wx.TextCtrl( agencywnd, wx.ID_ANY, results[12], wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer5.Add( agencywnd.m_textCtrl14, 0, wx.ALL|wx.EXPAND, 5 )

        agencywnd.m_staticText22 = wx.StaticText( agencywnd, wx.ID_ANY, u"К/С", wx.DefaultPosition, wx.DefaultSize, 0 )
        agencywnd.m_staticText22.Wrap( -1 )

        fgSizer5.Add( agencywnd.m_staticText22, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        agencywnd.m_textCtrl18 = wx.TextCtrl( agencywnd, wx.ID_ANY, results[13], wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer5.Add( agencywnd.m_textCtrl18, 0, wx.ALL|wx.EXPAND, 5 )

        agencywnd.m_staticText23 = wx.StaticText( agencywnd, wx.ID_ANY, u"БИК", wx.DefaultPosition, wx.DefaultSize, 0 )
        agencywnd.m_staticText23.Wrap( -1 )

        fgSizer5.Add( agencywnd.m_staticText23, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        agencywnd.m_textCtrl19 = wx.TextCtrl( agencywnd, wx.ID_ANY, results[14], wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer5.Add( agencywnd.m_textCtrl19, 0, wx.ALL, 5 )


        bSizer3.Add( fgSizer5, 0, wx.EXPAND, 5 )


        agencywnd.SetSizer( bSizer3 )
        agencywnd.Layout()

        agencywnd.Centre( wx.BOTH )
# Измение в полях ввода
        agencywnd.m_textCtrl4.Bind( wx.EVT_TEXT, nameval() )

# закрыть соединение с базой данных
        conn.close()
# проверка ввода организации
    def nameval ( self, event ):
        result[1] = agencywnd.m_textCtrl4.GetValue()

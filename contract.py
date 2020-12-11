def dogform(cursor, results, cust_id, id_oper, req_id):
# формирование договора из шаблона  
    doc_filename=path.join('tpl', 'contracttpl.docx')
    doc = DocxTemplate(doc_filename)
#   формирование строки передаваемой в редактор   
#   блок полей заказчика    
    if cust_id == 0:
        results1 = ['', '', '', '', '', '', '']
    else:
        cursor.execute("SELECT fio, num_local_pass, date_local_pass, who_local_pass, cust_adress, cust_tel, cust_email \
        FROM Cat_cust WHERE id_cust = "+ str(cust_id))
        results1 = cursor.fetchone()
#   блок полей оператора
    if id_oper == 0:
        results2 = ['', '', '', '', '', '', '', '', '', '', '', '', '']
    else:
        cursor.execute("SELECT name_full_to, name_short_to, adress_to, tel_to, site, email_to, num_fedr_to, text_strah,\
        date_beg_strah, date_end_strah, name_strah, adress_strah, tel_strah FROM cat_tourop WHERE id_to = "+ str(id_oper))
        results2 = cursor.fetchone()
#   блок полей отелей
    hotel_contents = []
    cursor.execute("SELECT hotel, hotel_addr, quant_room, type_room, accom, date_begin, date_end, meal FROM req_accom WHERE id_req = "+ str(req_id))
    while True:
        results3 = cursor.fetchone()
        if results3 == None:
            break
        hotel_contents.append({'name_hotel' : results3[0], 'adr_hotel' : results3[1], 'q_room' : results3[2], \
        't_room' : results3[3], 'accom' : results3[4], 'dateb' : results3[5], 'datee' : results3[6], 'meal' : results3[7]},)
#   блок полей туристов
    tourist_contents = []
    cursor.execute("SELECT id_cust FROM req_tourist WHERE id_req = '" +str(req_id) +"'")
    rows = cursor.fetchall()
    for row in rows:
        cursor.execute("SELECT fio, date_r, num_for_pass, date_iss_for_pass, date_end_for_pass FROM cat_cust WHERE id_cust = "+ str(row[0]))
        results3 = cursor.fetchone()
        tourist_contents.append({'fio' : results3[0], 'dater' : results3[1], 'numpass' : results3[2], 'dateiss' : results3[3], \
        'dateendpass' : results3[4]},)
#   блок полей перевозки
    trans_contents = []
    cursor.execute("SELECT type_trans, route, date_there, date_back FROM req_trans WHERE id_req = "+ str(req_id))
    while True:
        results5 = cursor.fetchone()
        if results5 == None:
            break
        trans_contents.append({'typetrans' : results5[0], 'routetrans' : results5[1], 'dthere' : results5[2], \
        'dback' : results5[3],},)
#   данные агентства
    cursor.execute("SELECT * FROM Agency_card")
    results6 = cursor.fetchone()

    context =   {'trans_contents' : trans_contents, 'trst_contents' : tourist_contents, 'htl_contents' : hotel_contents, 'customer' : results1[0], 'custpass' : results1[1], 'custpassdate' : results1[2],\
    'custpasswho' : results1[3], 'custadr' : results1[4], 'custtel' : results1[5], 'custemail' : results1[6], \
    'namefullto' : results2[0], 'nameshortto' : results2[1], 'adressto' : results2[2], 'tellto' : results2[3], 'siteto' : results2[4], \
    'emailto' : results2[5], 'numreestr' : results2[6], 'textstrah' : results2[7], 'datebegstrah' : results2[8], \
    'dateendstrah' : results2[9], 'namestrah' : results2[10], 'adressstrah' : results2[11], 'telstrah' : results2[12], \
    'datereq' : results[1], 'numbcontr' : results[2], 'country' : results[3], 'region' : results[4], 'datetour' : results[6], \
    'dateendtour' : results[7], 'quantn' : results[8], 'ticket' : results[9], 'transfer' : results[10], 'excurprog' : results[11], \
    'otherserv' : results[12], 'tourgid' : results[13], 'transl' : results[14], 'lead' : results[15], 'viza' : results[16], \
    'med' : results[17], 'acc' : results[18], 'fail' : results[19], 'datefullpay' : results[24], 'costrub' : results[29], \
    'costcur' : results[28], 'curtour' : results[21], 'prepayrub' : results[30],'datedoc' : results[26], 'rateto' : results[31], \
    'nameag' : results6[1], 'adressag' : results6[2], 'innag' : results6[3], 'kppag' : results6[4], 'ogrnag' : results6[5], \
    'okvedag' : results6[6], 'phoneag' : results6[7], 'emailag' : results6[8], 'siteag' : results6[9], 'bossag' : results6[10], \
    'bankag' : results6[11], 'accountag' : results6[12], 'coraccount' : results6[13], 'bikag' : results6[14]}
    doc.render(context)
    gen_doc_filename = path.join('tpl', 'contractgen.docx')
    doc.save(gen_doc_filename)
    startfile(gen_doc_filename)
    return
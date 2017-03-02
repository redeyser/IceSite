#!/usr/bin/python
# -*- coding: utf-8
# DataBase for IceSite
import my
import re
from datetime import datetime

""" Условия запроса """
def qw_where(postdata,prefix="",repq={},repf={}):
    query=[]
    if prefix!="":
        prefix=prefix+"."
    for key,val in postdata.items():
        _key=key
        _prefix=prefix
        _ap="`"
        if repq.has_key(key):
            query.append( repq[key][val["value"]])
            continue
        if repf.has_key(key):
            _key=repf[key][0]
            _prefix=""
            _ap=""
            if repf[key][1]!=None:
                val['mod']=repf[key][1]
        if val["mod"]==None:
            val["mod"]="="
        if val["mod"] in ["IN","NOT IN"]:
            value="(%s)" % val["value"]
        elif val["mod"] in ["LIKE"]:
            value="('%"+val["value"]+"%')"
        elif re.match("^-*[0-9\.]+$",val['value']):
            value="%s" % val["value"]
        else:
            value="'%s'" % val["value"]
        query.append("%s%s%s%s %s %s" % (_prefix,_ap,_key,_ap,val["mod"],value))
    return query

""" Список полей с префиксом и исключением """
def qw_get_fieldlist(prefix,fieldsorder,without,add=[]):
    if prefix!="":
        prefix+="."
    res=[]
    for f in fieldsorder:
        if not f in without:
            res.append(prefix+f)
    return res+add

def qw_where_trsc(data_hd,data_ct):
        #print data_hd
        repq_hd={  "isegais": {"0":"egais_sign=''","1":"egais_sign<>''"},\
                   "isdiscountcard":{"0":"discount_card=''","1":"discount_card<>''"},\
                   "isbonuscard":{"0":"bonus_card=''","1":"bonus_card<>''"},\
                   "iserror":{"0":"errors=''","1":"errors<>''"},\
                   "type_pay":{"0":"pay_bnal=0","1":"pay_bnal<>0","2":"pay_bnal<>0 and pay_nal<>0"},\
        }
        repf_hd= {  "date1":["hd.date",">="],\
                    "date2":["hd.date","<="],\
                    "time1":["hd.time",">="],\
                    "time2":["hd.time","<="],\
                    "summa_wod":["hd.summa-hd.discount_sum-hd.bonus_discount",None],\
        }
        repq_ct={  "limitprice": {"0":"p_maxprice=0 and p_minprice=0","1":"(p_maxprice<>0 or p_minprice<>0)"},\
                   "ch_cena":{"0":"p_cena=paramf1","1":"p_cena<>paramf1"},\
        }
        repf_ct= {  "ct_bonus":["(ct.bonus/ct.paramf3)*100",None],\
                    "ct_bonus_discount":["(ct.bonus_discount/ct.paramf3)*100",None],
                    "discount":["(ct.discount/ct.paramf3)*100",None],
        }

        hd_query=qw_where(data_hd,"hd",repq_hd,repf_hd)
        ct_query=qw_where(data_ct,"ct",repq_ct,repf_ct)

        thd_query=" and ".join(hd_query)
        tct_query=" and ".join(ct_query)
        if tct_query!="":
            tct_query=" and "+tct_query
        q_where = "where hd.idreg=ct.idreg and hd.idplace=ct.idplace and hd.nkassa=ct.nkassa and hd.id=ct.idhd "
        q_order = " order by hd.idreg, hd.idplace, hd.nkassa, hd.date, hd.time, ct.id"
        q   = q_where+" and "+thd_query+tct_query+q_order
        return q

def qw_query_trsc_short(hd,ct,fields,fields_calc):
    add=[]
    for k,v in fields_calc.items():
        add.append("(%s) as %s" % (v,k))
    f=",".join(fields+add)
    w=qw_where_trsc(hd,ct)
    return "select %s from tb_trsc_hd as hd,tb_trsc_ct as ct %s" % (f,w)

def qw_query_trsc_full(hd,ct,fields,fields_calc):
    add=[]
    for k,v in fields_calc.items():
        add.append("(%s) as %s" % (v,k))
    f=",".join(fields+add)
    w=qw_where_trsc(hd,ct)
    sub = "select distinct hd.idreg,hd.idplace,hd.nkassa,hd.id from tb_trsc_hd as hd,tb_trsc_ct as ct %s" % (w)
    q   = "select %s from (%s) as hdd,tb_trsc_hd as hd,tb_trsc_ct as ct \
    where hdd.idreg=hd.idreg and hdd.idplace=hd.idplace and hdd.nkassa=hd.nkassa and hdd.id=hd.id and\
    hd.idreg=ct.idreg and hd.idplace=ct.idplace and hd.nkassa=ct.nkassa and hd.id=ct.idhd" % (f,sub)
    return q


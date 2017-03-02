#!/usr/bin/python
# -*- coding: utf-8
# DataBase for IceSite
import my
import os
import re
import tbIceSite as tbs
from datetime import datetime
from md5 import md5
from qIceSite import *

DATABASE        = "IceServ"
MYSQL_USER      = "iceserv"
MYSQL_PASSWORD  = "iceserv1024"

TB_USER         = "tb_user"
TB_USER_VARS    = "tb_user_vars"
#TB_USER_FILES   = "tb_user_files"  #filerule
#TB_USER_MESSAGE = "tb_user_vars"   #chatmessage
#TB_USER_DOC_HD  = "tb_user_doc_hd" #html mysql multidoc
TB_RULE         = "tb_rule"
TB_MENU         = "tb_menu"
TB_QUERY        = "tb_query"
#TB_QUERY_TEXT   = "tb_query_text" #created html by manager in mysql

TB_GROUP        = "tb_group"
TB_PROPERTY     = "tb_property"

TB_REGS      = "tb_regs"
TB_SETS      = "tb_sets"
TB_KASSES    = "tb_kasses"
TB_PRICE     = "tb_price"
TB_PRICE_SHK = "tb_price_shk"

TB_TRSC_HD   = "tb_trsc_hd"
TB_TRSC_CT   = "tb_trsc_ct"

TYPE_OFF    = 0
TYPE_ON     = 1

PROPERTYHD_USER = 0
PROPERTYHD_GROUP= 1

PROPERTY_USER   = 0
PROPERTY_RULE   = 1
PROPERTY_MENU   = 2
PROPERTY_QUERY  = 3

def cur_dttm():
    return datetime.now().strftime(format="%Y_%m_%d_%H_%M_%S")

def hash_password(password):
    return md5(password).hexdigest()

def _round(V,n):
    z=str(V.__format__(".4f")).split(".")
    if len(z)<2:
        return str(V)
    else:
        d=int(z[0])
        f=z[1].ljust(n,"0")
    l=len(f)
    a=[]
    for i in range(l):
        a.append(int(f[i]))
    r=range(l)[n:]
    r.reverse()
    x=range(l)[:n]
    x.reverse()
    ost=0
    for i in r:
        a[i]+=ost
        if a[i]>=5:
            ost=1
        else:
            ost=0
    for i in x:
        a[i]+=ost
        if a[i]>9:
            a[i]=0
            ost=1
        else:
            ost=0
            break
    d+=ost
    s=""
    for i in range(n):
        s+=str(a[i])
    if n>0:
        s="."+s
    result=str(d)+s
    return result


class dbIceSite(my.db):

    def _tbinit(self,name):
        tb=getattr(tbs, name)
        self.tbs[name] = tb(name)

    def _tbcreate(self,tn):
        self.run(self.tbs[tn]._create())

    def _recreate(self):
        for name in self.tbs.keys():
            if not name in self.tables:
               self._tbcreate(name)
               print "created table %s" % name

    def _tables(self):
        res=self.get("show tables")
        db=[]
        for r in res:
            db.append(r[0])
        self.tables=db

    """ Переопределенный расширенный метод. Подключение, проверка таблиц, создание не существующих """
    def open(self,recreated=True):
        r=my.db.open(self)
        if r:
            self._tables()
            if recreated:
                self._recreate()
        return r

    def __init__(self,dbname,host,user,password):
        my.db.__init__(self,dbname,host,user,password)
        self.tbs={}
        self._tbinit(TB_REGS)
        self._tbinit(TB_KASSES)
        self._tbinit(TB_SETS)
        self._tbinit(TB_PRICE)
        self._tbinit(TB_PRICE_SHK)
        self._tbinit(TB_USER)
        self._tbinit(TB_USER_VARS)
        self._tbinit(TB_RULE)
        self._tbinit(TB_MENU)
        self._tbinit(TB_QUERY)
        self._tbinit(TB_GROUP)
        self._tbinit(TB_PROPERTY)
        self._tbinit(TB_TRSC_HD)
        self._tbinit(TB_TRSC_CT)

    def _create(self):
        self._truncate(TB_USER)
        self._truncate(TB_RULE)
        self._truncate(TB_MENU)
        self._truncate(TB_QUERY)
        self._truncate(TB_GROUP)
        self._truncate(TB_PROPERTY)
        self._insert(TB_USER,{'login':'admin','name':'Administrator of site','password':hash_password('admin678543'),'type':TYPE_ON,'idreg':1})
        self._insert(TB_USER,{'login':'manager','name':'Manager of site','password':hash_password('manager678543'),'type':TYPE_OFF,'idreg':1})
        self._insert(TB_USER,{'login':'user','name':'User','password':hash_password('766766'),'type':TYPE_OFF,'idreg':1})

        self._insert(TB_RULE,{'tag':'admin','title':'Администрирование'})
        self._insert(TB_RULE,{'tag':'user','title':'Пользователь сайта'})
        
        self._insert(TB_GROUP,{'tag':'admins','title':'Администраторы сайта'})
        self._insert(TB_GROUP,{'tag':'users','title':'Пользователи сайта'})

        self._insert(TB_MENU,{'tag':'self','title':'Персональные данные','template':'my'})

        self._insert(TB_MENU,{'tag':'admin','title':'Администрирование','template':'','idhd':0})
        self._insert(TB_MENU,{'tag':'admin','title':'Пользователи','template':'admin/users','idhd':2})
        self._insert(TB_MENU,{'tag':'admin','title':'Права','template':'admin/rules','idhd':2})
        self._insert(TB_MENU,{'tag':'admin','title':'Меню','template':'admin/menues','idhd':2})
        self._insert(TB_MENU,{'tag':'admin','title':'Группы','template':'admin/groups','idhd':2})
        self._insert(TB_MENU,{'tag':'admin','title':'Операции','template':'admin/queries','idhd':2})
        self._insert(TB_MENU,{'tag':'admin','title':'Свойства','template':'admin/properties','idhd':2})

        self._insert(TB_QUERY,{'url':'/admin','title':'Админские запросы'})
        self._insert(TB_QUERY,{'url':'/self','title':'Сохранение персональных данных'})
        self._insert(TB_QUERY,{'url':'/sprav','title':'Работа со справочниками'})

        self._insert(TB_PROPERTY,{'hd_type':PROPERTYHD_GROUP,'idhd':1,'ct_type':PROPERTY_USER,'idct':1})
        self._insert(TB_PROPERTY,{'hd_type':PROPERTYHD_GROUP,'idhd':1,'ct_type':PROPERTY_RULE,'idct':1})
        self._insert(TB_PROPERTY,{'hd_type':PROPERTYHD_GROUP,'idhd':1,'ct_type':PROPERTY_QUERY,'idct':1})
        self._insert(TB_PROPERTY,{'hd_type':PROPERTYHD_GROUP,'idhd':1,'ct_type':PROPERTY_QUERY,'idct':2})
        self._insert(TB_PROPERTY,{'hd_type':PROPERTYHD_GROUP,'idhd':1,'ct_type':PROPERTY_QUERY,'idct':3})
        self._insert(TB_PROPERTY,{'hd_type':PROPERTYHD_GROUP,'idhd':1,'ct_type':PROPERTY_MENU,'idct':1})
        self._insert(TB_PROPERTY,{'hd_type':PROPERTYHD_GROUP,'idhd':1,'ct_type':PROPERTY_MENU,'idct':2})
        self._insert(TB_PROPERTY,{'hd_type':PROPERTYHD_GROUP,'idhd':1,'ct_type':PROPERTY_MENU,'idct':3})
        self._insert(TB_PROPERTY,{'hd_type':PROPERTYHD_GROUP,'idhd':1,'ct_type':PROPERTY_MENU,'idct':4})
        self._insert(TB_PROPERTY,{'hd_type':PROPERTYHD_GROUP,'idhd':1,'ct_type':PROPERTY_MENU,'idct':5})
        self._insert(TB_PROPERTY,{'hd_type':PROPERTYHD_GROUP,'idhd':1,'ct_type':PROPERTY_MENU,'idct':6})
        self._insert(TB_PROPERTY,{'hd_type':PROPERTYHD_GROUP,'idhd':1,'ct_type':PROPERTY_MENU,'idct':7})
        self._insert(TB_PROPERTY,{'hd_type':PROPERTYHD_GROUP,'idhd':1,'ct_type':PROPERTY_MENU,'idct':8})



    """ Optimize functions ----------------------- """

    def _gets(self,tn,tostr=False,dttm2str=True):
        result = self.get(self.tbs[tn]._gets())
        if len(result)==0:
            return None
        else:
            res=[]
            for r in result:
                res.append(self.tbs[tn].result2values(r,tostr=tostr,dttm2str=dttm2str))
            return res

    """ Получить запись по id """
    def _getid(self,tn,id,tostr=False,dttm2str=True):
        res = self.get(self.tbs[tn]._getid(id))
        if len(res)==0:
            return None
        else:
            return self.tbs[tn].result2values(res[0],tostr=tostr,dttm2str=dttm2str)

    """ Получить записи по idhd """
    def _gethd(self,tn,id,tostr=False,dttm2str=True):
        res = self.get(self.tbs[tn]._gethd(id))
        if len(res)==0:
            return []
        else:
            result=[]
            for r in res:
                result.append( self.tbs[tn].result2values(r,tostr=tostr,dttm2str=dttm2str) )
        return result

    """ Получить Заголовочную запись и подчиненные """
    def _get_data_hd_ct(self,tb_hd,tb_ct,id,tostr=False,dttm2str=True):
        hd = self._getid(tb_hd,id,tostr=tostr,dttm2str=dttm2str)
        if hd != None:
            ct = self._gethd( tb_ct,id,tostr=tostr,dttm2str=dttm2str ) 
        else:
            ct=None
        return (hd,ct)

    """ Очистить таблицу """    
    def _truncate(self,tn):
        self.run("truncate %s" % tn)
        return True

    """ Переделать в хэш """
    def _db2hash(self,r,id,val):
        h={}
        for rec in r:
            h[rec[id]]=rec[val]
        return h

    """ Переделать в массив """
    def _db2arr(self,r,id):
        t=[]
        for rec in r:
            t.append(rec[id])
        return t

    """ Простая выборка """
    def _select(self,tn,where="",fields=None,order=None,group=None,tostr=False,dttm2str=True,toarr=False,tohash=False):
        self.result_order=[]
        if where!="" and fields==None:
            where= " where %s" % where
        if group:
            _group=" group by "+group
        else:
            _group=""
        if order:
            _order=" order by "+order
        else:
            _order=""
        if fields==None:
            result = self.get(self.tbs[tn].query_all_select()+where+_group+_order)
        else:
            result = self.get(self.tbs[tn].query_select(fields,where)+_group+_order)
        if len(result)==0:
            return []
        else:
            if toarr:
                res=[]
                for r in result:
                    if tostr:
                        s=str(r[0])
                    else:
                        s=r[0]
                    res.append(s)
                return res
            if tohash:
                res={}
                self.result_order=[]
                for r in result:
                    if tostr:
                        s=str(r[1])
                    else:
                        s=r[1]
                    res[r[0]]=s
                    self.result_order.append(r[0])
                return res
            res=[]
            for r in result:
                res.append(self.tbs[tn].result2values(r,tostr=tostr,dttm2str=dttm2str))
            return res

    """ Добавить запись """
    def _insert(self,tn,struct):
        r=self.run(self.tbs[tn].query_insert(struct))
        if not r:
            self.lastid=0
            return False
        self.lastid=self.get(my.Q_LASTID)[0][0]
        return True

    """ Изменить запись """
    def _update(self,tn,struct,where):
        return self.run(self.tbs[tn].query_update(struct)+" where %s" % where)

    """ Удалить запись """
    def _delete(self,tn,where):
        return self.run(self.tbs[tn].query_delete(where))

    """ Пустая запись """
    def _empty(self,tn):
        return self.tbs[tn].empty_all_values()

    """ ------------------------------------------ """

    def sets_read(self):
        self.sets = self._select(TB_SETS,"",['name','value'],tohash=True)

    def sets_insert(self,g,n,v):
        r=self._getid(TB_SETS,n)
        if r:
            return False
        else:
            self._insert(TB_SETS,{'group':g,'name':n,'value':v})
            return True

    def user_auth(self,login,password):
        user=self._select(TB_USER,"login='%s'" % login)
        if len(user)==0:
            return False
        else:
            self.user=user[0]
            if hash_password(password)==self.user['password']:
                return True
            else:
                return False

    def menu_gets(self,idhd,toarr=False,tostr=False):
        if toarr:
            fields=['id']
        else:
            fields=[]
        return self._select( TB_MENU, "idhd=%s" % idhd,fields,toarr=toarr,tostr=tostr )

    def ot_trsc(self,type_query,data_hd,data_ct):
        fields_hd=qw_get_fieldlist("hd",self.tbs[TB_TRSC_HD].fieldsorder,['egais_sign'])
        fields_ct=qw_get_fieldlist("ct",self.tbs[TB_TRSC_CT].fieldsorder,['idreg','idplace','nkassa'])
        fields_calc={'summa_wod':'hd.summa-hd.discount_sum-hd.bonus_discount',\
            'title':'select p.name from tb_price as p, tb_kasses as k where \
            p.idreg=hd.idreg and k.idreg=hd.idreg and k.idplace=hd.idplace and k.nkassa=1 and\
            k.idprice=p.idprice and p.id=ct.code limit 1',\
        }
        fields=fields_hd+fields_ct
        
        if type_query=='short':
            qtext=qw_query_trsc_short(data_hd,data_ct,fields,fields_calc)
        if type_query=='full':
            qtext=qw_query_trsc_full(data_hd,data_ct,fields,fields_calc)
        #print fields
        #print qtext
        result=self.get(qtext)
        #print len(result)
        return (fields+fields_calc.keys(),result)
        




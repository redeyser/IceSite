#!/usr/bin/python
# -*- coding: utf-8

"""
    IceSite 1.0
    License GPL
    writed by Romanenko Ruslan
    redeyser@gmail.com
"""

from   BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from   SocketServer import ThreadingMixIn
from   fhtml import *
import threading
import urlparse
import Cookie
import cgi
import time
import sys,os
import re
import json
import subprocess
PIPE = subprocess.PIPE
import my
from dbIceSite import *
from datetime import datetime

MYSQL_HOST  = 'localhost'
VERSION     = '1.0.000'

POST_TRUE       = "1"
POST_FALSE      = "0"
_RESULT         = 'result'
_ID             = 'id'
Q_SELF_GET            = "/self/get"
Q_SELF_PUT            = "/self/put"
Q_ADMIN_USERS         = "/admin/users"
Q_ADMIN_USER_GET      = "/admin/user/get"
Q_ADMIN_USER_PUT      = "/admin/user/put"
Q_ADMIN_USER_DEL      = "/admin/user/del"

Q_ADMIN_RULES         = "/admin/rules"
Q_ADMIN_RULE_GET      = "/admin/rule/get"
Q_ADMIN_RULE_PUT      = "/admin/rule/put"
Q_ADMIN_RULE_DEL      = "/admin/rule/del"

Q_ADMIN_MENUES        = "/admin/menues"
Q_ADMIN_MENU_GET      = "/admin/menu/get"
Q_ADMIN_MENU_PUT      = "/admin/menu/put"
Q_ADMIN_MENU_DEL      = "/admin/menu/del"

Q_ADMIN_GROUPS        = "/admin/groups"
Q_ADMIN_GROUP_GET     = "/admin/group/get"
Q_ADMIN_GROUP_PUT     = "/admin/group/put"
Q_ADMIN_GROUP_DEL     = "/admin/group/del"

Q_ADMIN_QUERIES       = "/admin/queries"
Q_ADMIN_QUERY_GET     = "/admin/query/get"
Q_ADMIN_QUERY_PUT     = "/admin/query/put"
Q_ADMIN_QUERY_DEL     = "/admin/query/del"

Q_ADMIN_PROPERTIES    = "/admin/properties"
Q_ADMIN_PROPERTY_GET  = "/admin/property/get"
Q_ADMIN_PROPERTY_PUT  = "/admin/property/put"
Q_ADMIN_PROPERTY_DEL  = "/admin/property/del"

Q_SPRAV_REGS_GET      = "/sprav/regs/get"
Q_SPRAV_PLACE_GET     = "/sprav/place/get"
Q_SPRAV_RULE_GET      = "/sprav/rule/get"
Q_SPRAV_QUERY_GET     = "/sprav/query/get"
Q_SPRAV_MENU_GET      = "/sprav/menu/get"
Q_SPRAV_USER_GET      = "/sprav/user/get"
Q_SPRAV_GROUP_GET     = "/sprav/group/get"

Q_OT_TRSC             = "/ot/trsc"

icelock=threading.Lock()

def ice_lock():
    icelock.acquire()

def ice_unlock():
    icelock.release()

def json_serial_str(obj):
    """JSON serializer for objects not serializable by default json code"""
    return str(obj)

class Handler(BaseHTTPRequestHandler):

    def mysql_open(self):
        self.db = dbIceSite(DATABASE, MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD) 
        return self.db.open()
        
    def _getval(self,key,default):
        if self.get_vals.has_key(key):
            return self.get_vals[key]
        else:
            return default

    def _send_HEAD(self,tp,code=200):
        self.send_response(code)
        self.send_header("Content-type", tp)
        self.end_headers()

    def _send_redirect(self,url):
        self.send_response(302)
        self.send_header('Location', url)

    def _redirect(self,url):
        self._send_redirect(url)
        self.end_headers()

    def do_HEAD(self):
        self._send_HEAD('text/html')
        self.send_response(200)

    def GetAuth(self,gets):
        if gets.has_key("_user") and gets.has_key("_password"):
            self.curlogin    = gets['_user']
            self.curpassword = gets['_password']
            return True
        else:
            return False
            
    def PostAuth(self,form):
        if form.has_key("_user") and form.has_key("_password"):
            self.curlogin    = form['_user'].value
            self.curpassword = form['_password'].value
            return True
        else:
            return False

    def ReadCookie(self):
        if "Cookie" in self.headers:
            c = Cookie.SimpleCookie(self.headers["Cookie"])
            if c.has_key('Icelogin') and c.has_key('Icepassword'):
                self.curlogin    = c['Icelogin'].value
                self.curpassword = c['Icepassword'].value
                return True
            else:
                self.curlogin    = None
                self.curpassword = None
                return False

    def WriteCookie(self,form):
        if form.has_key("login"):
            c = Cookie.SimpleCookie()
            c['Icelogin'] = form["login"].value
            c['Icepassword'] = form["password"].value
            self.send_header('Set-Cookie', c.output(header=''))

    def ClearCookie(self):
        c = Cookie.SimpleCookie()
        c['Icelogin'] = ""
        c['Icepassword'] = ""
        self.send_header('Set-Cookie', c.output(header=''))

    def get_file(self,path="",decode=True):
        if path[0]!='/':
            path='/'+path
        path='site'+path
        try:
            f=open(path,"r")
            message=f.read()
            f.close()
        except:
            message=''
        if decode:
            message=message.decode("utf8")
        return message

    def put_file(self,filedata,path):
        path='site'+path
        try:
            f=open(path,"w")
            f.write(filedata)
            f.close()
            return True
        except:
            return False
            pass
        return 
    
    def pattern_params_get(self,html):
        params={}
        a=re.findall("%%#.*?#.*?%%",html)
        for n in a:
            m=re.search("%%#(.*?)#(.*?)%%",n)
            if m!=None and len(m.groups())==2:
                tag=m.group(1)
                params[tag]=m.group(2)
        return params

    def pattern_rep_arr(self,html,amark,aval):
        return ht_reptags_arr(html,amark,aval)

    def pattern_rep_hash(self,html,h):
        return ht_reptags_hash(html,h)

    def pattern_params_clear(self,html):
        a=re.findall("%%#.*?#.*?%%",html)
        for n in a:
            html=html.replace(n,"")
        a=re.findall("%.*?%",html)
        for n in a:
            html=html.replace(n,"")
        return html

    def _write(self,html):
        self.wfile.write(html.encode("utf8"))

    def write_file(self,f):
        self._send_HEAD("application/x")
        html=self.get_file(f,False)
        self.wfile.write(html)

    def wbody(self,p):
        b=self.get_file(p)
        self._send_HEAD("text/html")
        html=self.get_file('/head.html')
        info_ip=self.client_address[0]
        html = ht_reptags_arr(html,["%css%","%body%"],[self.cur_css,b])
        html = ht_reptags_arr(html,["%user%","%info_ip%"],[self.curlogin,info_ip])
        self._write(html)

    def wbodyh(self,b):
        self._send_HEAD("text/html")
        html=self.get_file('/head.html')
        info_ip=self.client_address[0]
        html = ht_reptags_arr(html,["%css%","%body%"],[self.cur_css,b])
        html = ht_reptags_arr(html,["%user%","%info_ip%"],[self.curlogin,info_ip])
        self._write(html)

    def wjson(self,j):
        self._send_HEAD("application/json")
        self._write(j)

    def get_userproperty(self):
        user_rules    = self.db._select( TB_PROPERTY,"hd_type=%d and idhd=%d and ct_type=%d" % (PROPERTYHD_USER,self.iduser,PROPERTY_RULE)  , ['idct'],toarr=True,tostr=True )
        user_queries  = self.db._select( TB_PROPERTY,"hd_type=%d and idhd=%d and ct_type=%d" % (PROPERTYHD_USER,self.iduser,PROPERTY_QUERY) , ['idct'],toarr=True,tostr=True )
        user_menues   = self.db._select( TB_PROPERTY,"hd_type=%d and idhd=%d and ct_type=%d" % (PROPERTYHD_USER,self.iduser,PROPERTY_MENU)  , ['idct'],toarr=True,tostr=True )

        user_groups = self.db._select( TB_PROPERTY,"hd_type=%d and ct_type=%d and idct=%d" % (PROPERTYHD_GROUP,PROPERTY_USER,self.iduser),['idhd'],toarr=True,tostr=True )
        grouplist=",".join(user_groups)

        group_rules    = self.db._select( TB_PROPERTY,"hd_type=%d and idhd in (%s) and ct_type=%d" % (PROPERTYHD_GROUP,grouplist,PROPERTY_RULE)  , ['idct'],toarr=True,tostr=True  )
        group_queries  = self.db._select( TB_PROPERTY,"hd_type=%d and idhd in (%s) and ct_type=%d" % (PROPERTYHD_GROUP,grouplist,PROPERTY_QUERY) , ['idct'],toarr=True,tostr=True  )
        group_menues   = self.db._select( TB_PROPERTY,"hd_type=%d and idhd in (%s) and ct_type=%d" % (PROPERTYHD_GROUP,grouplist,PROPERTY_MENU)  , ['idct'],toarr=True,tostr=True  )
        
        user_rules = user_rules + group_rules
        user_queries = user_queries + group_queries

        self.user_menues = user_menues + group_menues
        self.user_rules     = self.db._select( TB_RULE, "id in (%s)" % ",".join(user_rules),["tag"], toarr=True )
        self.user_queries   = self.db._select( TB_QUERY,"id in (%s)" % ",".join(user_queries),["url"], toarr=True )

    def get_usermenu(self,idhd):
        if int(idhd)!=0:
            t=self.db._select( TB_MENU, "id=%s" % idhd )
            self.curmenu=t[0]
            pid=t[0]['idhd']
        else:
            pid=0
            self.curmenu={'title':u'Главное меню'}
        menues=self.db.menu_gets(idhd,toarr=True,tostr=True)
        gmenu=[]
        for m in menues:
            if m in self.user_menues:
                gmenu.append(m)
        if len(gmenu):
            r=self.db._select( TB_MENU, "id in (%s)" % ",".join(gmenu) )
            if int(idhd)!=0:
                r.append({'tag':'exit','template':'','title':u'Выход ','id':pid})
            return r
        else:
            return []

    def verify(self):   
        if self.db.user_auth(self.curlogin,self.curpassword):
            if self.db.user['type']==TYPE_OFF:
                return False
            if self.db.user['css']!='':
                self.cur_css=self.db.user['css']
            self.currule=self.db.user['type']
            self.iduser=self.db.user['id']
            self.get_userproperty()
            return True
        else:
            return False

    def user_access(self,p):
        for q in self.user_queries:
            if re.match(q,p):
                print "accept",q,p
                return True
        print "deny",p,self.user_queries
        return False

    def return_false(self):
        j=json.dumps({_RESULT:False})
        self.wjson(j)

    def qstd_gets(self,table,where="",fields=None,order=None,group=None,tohash=False,toarr=False,usegets=False):
        if usegets:
            data=self.db._gets( table )
        else:
            data=self.db._select(table,where=where,fields=fields,group=group,order=order,tohash=tohash,toarr=toarr)
        #print data
        #print self.db.result_order
        j=json.dumps({_RESULT:True,'data':data,'order':self.db.result_order},ensure_ascii=False)
        self.wjson(j)
        return True

    def qstd_getid(self,table,fid="id"):
        id=self._getval('id',None)
        if id==None:
            self.return_false()
            return False
        if int(id)==0:
            data=self.db._empty( table )
        else:
            data=self.db._select( table, "%s=%s" % (fid,id) )
            data=data[0]
        j=json.dumps({_RESULT:True,'data':data},ensure_ascii=False)
        self.wjson(j)
        return True

    def qstd_putid(self,table,fid="id"):
        if not self.form.has_key("data"):
            self.return_false()
            return False
        data=json.loads(self.form["data"].value)
        if data['id']==0:
            del data['id']
            r=self.db._insert( table, data )
            id=self.db.lastid
        else:
            r=self.db._update( table, data, "%s=%s" % (fid,data['id']) )
            id=data['id']
        j=json.dumps({_RESULT:r,_ID:id})
        self.wjson(j)
        return True

    def qstd_delid(self,table,fid="id"):
        if not self.form.has_key("data"):
            self.return_false()
            return False
        data=json.loads(self.form["data"].value)
        r=self.db._delete( table, "id=%s" % data['id'] )
        j=json.dumps({_RESULT:r})
        self.wjson(j)
        return True

    def do_GET(self):

        self.cur_css='black.css'
        parsed_path = urlparse.urlparse(self.path)
        getvals=parsed_path.query.split('&')
        self.get_vals={}

        try:
            for s in getvals:
                if s.find('=')!=-1:
                    (key,val) = s.split('=')
                    self.get_vals[key] = val
        except:
            print "error get!"
            self.get_vals={}
                

        if self.path.find(".woff")!=-1:
            self._send_HEAD("application/x-font-woff",200)
            message=self.get_file(self.path)
            self._write(message)
            return
        if self.path.find(".js")!=-1:
            self._send_HEAD("text/javascript",200)
            message=self.get_file(self.path)
            self._write(message)
            return
        if self.path.find(".css")!=-1:
            self._send_HEAD("text/css",200)
            message=self.get_file(self.path)
            self._write(message)
            return
        if (self.path.find(".png")!=-1)or(self.path.find(".gif")!=-1):
            self._send_HEAD("image/png",200)
            message=self.get_file(self.path,decode=False)
            self.wfile.write(message)
            return

        if not self.mysql_open():
            self._send_HEAD("text/html",404)
            return
        else:
            self.db.sets_read()

        if self.path=='/login':
            self.iduser=0
            self.curlogin=""
            self.wbody("/login.html")
            return

        if not self.ReadCookie():
            if not self.GetAuth(self.get_vals):
                self._redirect("/login")
                return

        self.GetAuth(self.get_vals)

        if not self.verify():
            self._redirect("/login")
            return

        if (self.path.find("/unlogin")==0):
            self._send_redirect("/login")
            self.ClearCookie()
            self.end_headers()
            return

        """ GET SIMPLE REQUEST
            ------------------
        """    
        if self.path=='/':
            self.wbody("/index.html")
            return

        if self.path.find("/template/")!=-1:
            h=self.get_file(self.path)
            self._send_HEAD("text/html")
            self._write(h)
            return

        if parsed_path.path=='/get/menu':
            id=self._getval('id',None)
            if id:
                menu=self.get_usermenu(id)
            else:
                menu=[]
            j=json.dumps({'curmenu':self.curmenu,'menu':menu},ensure_ascii=False)
            self.wjson(j)
            return

        """ GET USER REQUEST
            ------------------
        """    
        if not self.user_access(parsed_path.path):
            self.return_false()
            return

        if parsed_path.path==Q_SELF_GET:
            data=self.db._select( TB_USER, "id=%s" % self.iduser )
            j=json.dumps({_RESULT:True,'data':data},ensure_ascii=False)
            self.wjson(j)
            return

        if parsed_path.path==Q_ADMIN_USERS:
            return self.qstd_gets(TB_USER,"",None,"",usegets=True)
        
        if parsed_path.path==Q_ADMIN_MENUES:
            return self.qstd_gets(TB_MENU,"",None,"",usegets=True)

        if parsed_path.path==Q_ADMIN_PROPERTIES:
            hd=self._getval('hd',1)
            ct=self._getval('ct',0)
            idhd=self._getval('idhd','0')
            self.db.tbs[TB_PROPERTY]._set4gets(hd,idhd,ct)
            return self.qstd_gets(TB_PROPERTY,"",None,"",usegets=True)

        if parsed_path.path==Q_SPRAV_REGS_GET:
            return self.qstd_gets(TB_REGS,"",["id","name"],None,tohash=True)

        if parsed_path.path==Q_SPRAV_PLACE_GET:
            where=" off=0 and not name like(\"%test%\")"
            if self.db.user['idreg']>1:
                where+=" and idreg=%d" % self.db.user['idreg']
            return self.qstd_gets(TB_KASSES,where,["idplace","name"],group="idreg,idplace",order="idreg,name",tohash=True)

        if parsed_path.path==Q_SPRAV_MENU_GET:
            return self.qstd_gets(TB_MENU,"",["id","title"],None,tohash=True)

        if parsed_path.path==Q_SPRAV_USER_GET:
            return self.qstd_gets(TB_USER,"",["id","login"],None,tohash=True)

        if parsed_path.path==Q_SPRAV_GROUP_GET:
            return self.qstd_gets(TB_GROUP,"",["id","title"],None,tohash=True)

        if parsed_path.path==Q_SPRAV_QUERY_GET:
            return self.qstd_gets(TB_QUERY,"",["id","url"],None,tohash=True)

        if parsed_path.path==Q_SPRAV_RULE_GET:
            return self.qstd_gets(TB_RULE,"",["id","tag"],None,tohash=True)

        if parsed_path.path==Q_ADMIN_RULES:
            return self.qstd_gets(TB_RULE,"",None,"tag")

        if parsed_path.path==Q_ADMIN_GROUPS:
            return self.qstd_gets(TB_GROUP,"",None,"tag")

        if parsed_path.path==Q_ADMIN_QUERIES:
            return self.qstd_gets(TB_QUERY,"",None,"url")

        if parsed_path.path==Q_ADMIN_USER_GET:
            return self.qstd_getid(TB_USER)

        if parsed_path.path==Q_ADMIN_RULE_GET:
            return self.qstd_getid(TB_RULE)

        if parsed_path.path==Q_ADMIN_GROUP_GET:
            return self.qstd_getid(TB_GROUP)

        if parsed_path.path==Q_ADMIN_MENU_GET:
            return self.qstd_getid(TB_MENU)

        if parsed_path.path==Q_ADMIN_QUERY_GET:
            return self.qstd_getid(TB_QUERY)

        if parsed_path.path==Q_ADMIN_PROPERTY_GET:
            return self.qstd_getid(TB_PROPERTY)

        self._send_HEAD("text/html",404)

    def do_POST(self):
        self.cur_css='black.css'
        self.form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        
        if not self.mysql_open():
            self._send_HEAD("text/html",404)
            print "error. not open mysql"
            return
        else:
            self.db.sets_read()
        
        if (self.path.find("/login")==0):
            self._send_redirect("/")
            self.WriteCookie(self.form)
            self.end_headers()
            return

        if not self.ReadCookie():
            if not self.PostAuth(self.form):
                self._redirect("/login")
                return

        self.PostAuth(self.form)

        if not self.verify():
            print "not verify"
            self._redirect("/login")
            return

        if self.path==Q_SELF_PUT:
            if not self.form.has_key("data"):
                self.return_false()
                return
            data=json.loads(self.form["data"].value)
            if data.has_key('password') and data['password']!='':
                data['password']=hash_password(data['password'])
            r=self.db._update( TB_USER, data, "id=%s" % self.iduser )
            j=json.dumps({_RESULT:r})
            self.wjson(j)
            return

        if self.path==Q_ADMIN_USER_PUT:
            if not self.form.has_key("data"):
                self.return_false()
                return
            data=json.loads(self.form["data"].value)
            if data.has_key('password') and data['password']!='':
                data['password']=hash_password(data['password'])
            if data['id']==0:
                del data['id']
                r=self.db._insert( TB_USER, data )
                id=self.db.lastid
            else:
                r=self.db._update( TB_USER, data, "id=%s" % data['id'] )
                id=data['id']
            j=json.dumps({_RESULT:r,_ID:id})
            self.wjson(j)
            return

        if self.path==Q_ADMIN_USER_DEL:
            return self.qstd_delid(TB_USER)

        if self.path==Q_ADMIN_RULE_PUT:
            return self.qstd_putid(TB_RULE)

        if self.path==Q_ADMIN_RULE_DEL:
            return self.qstd_delid(TB_RULE)

        if self.path==Q_ADMIN_MENU_PUT:
            return self.qstd_putid(TB_MENU)

        if self.path==Q_ADMIN_MENU_DEL:
            return self.qstd_delid(TB_MENU)

        if self.path==Q_ADMIN_GROUP_PUT:
            return self.qstd_putid(TB_GROUP)

        if self.path==Q_ADMIN_GROUP_DEL:
            return self.qstd_delid(TB_GROUP)

        if self.path==Q_ADMIN_QUERY_PUT:
            return self.qstd_putid(TB_QUERY)

        if self.path==Q_ADMIN_QUERY_DEL:
            return self.qstd_delid(TB_QUERY)

        if self.path==Q_ADMIN_PROPERTY_PUT:
            return self.qstd_putid(TB_PROPERTY)

        if self.path==Q_ADMIN_PROPERTY_DEL:
            return self.qstd_delid(TB_PROPERTY)

        """ В дальнейшем, все сохранение сложных таблиц только с предварительной блокировкой """

        """ Отчеты """
        if self.path==Q_OT_TRSC:
            if not self.form.has_key("data_hd") or not self.form.has_key("data_ct") or not self.form.has_key("type_query"):
                self.return_false()
                return
            data_hd=json.loads(self.form["data_hd"].value)
            data_ct=json.loads(self.form["data_ct"].value)
            if int(self.db.user['idreg'])>1:
                data_hd["idreg"]={"value":str(self.db.user['idreg']),"mod":None}
            #print data_hd
            fields,data=self.db.ot_trsc(self.form["type_query"].value,data_hd,data_ct)
            j=json.dumps({_RESULT:True,'fields':fields,'data':data},default=json_serial_str,ensure_ascii=False)
            self.wjson(j)
            return True;    

        self._send_HEAD("text/html",404)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ Создаем веб сервер многопоточный """

if __name__ == '__main__':
    db = dbIceSite(DATABASE, MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD) 
    if db.open():
        pass
    else:
        print "Database not exist"
        sys.exit(1)

    db.sets_read()
    #db._create()
    print "opened database"

    server = ThreadedHTTPServer(('', int(db.sets['server_port'])+1), Handler)
    print 'Start dIceSite Server v %s [%s]' % (VERSION,int(db.sets['server_port'])+1)
    db.close()
    server.serve_forever()



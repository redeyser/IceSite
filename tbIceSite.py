#!/usr/bin/python
# -*- coding: utf-8
"""
    Tables of IceCashSite
"""
import my


class tb_user(my.table):
    def __init__ (self,dbname):
        my.table.__init__(self,dbname)
        self.addfield('id','d')
        self.addfield('idreg','d')
        self.addfield('name','s')
        self.addfield('login','s')
        self.addfield('chatname','s')
        self.addfield('password','s')
        self.addfield('type','d')
        self.addfield('code','s')
        self.addfield('idtab','d')
        self.addfield('css','s')

    def _create(self):
        q="""create table `%s` (
        `id`    int(4) unsigned NOT NULL AUTO_INCREMENT,
        `idreg` int(4) default 0,
        `name`      char(128) default '',
        `login`     char(32) default '',
        `chatname`  char(32) default '',
        `password`  char(32) default '',
        `type` tinyint(1) default 0,
        `code`  char(24) default '',
        `idtab`  int(4) default 0,
        `css`  char(100) default '',
        primary key (`id`),
        key `login` (`idreg`,`login`)
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8""" % self.tablename
        return q

    def _gets(self):
        self.query_all_select()
        self.query_fields.append("v_reg")
        return "select *,(select name from tb_regs as r where r.id=idreg) as v_reg from %s  order by login" % self.tablename

class tb_user_vars(my.table):
    def __init__ (self,dbname):
        my.table.__init__(self,dbname)
        self.addfield('id','d')
        self.addfield('idhd','d')
        self.addfield('name','s')
        self.addfield('value','s')

    def _create(self):
        q="""create table `%s` (
        `id`    int(4) unsigned NOT NULL AUTO_INCREMENT,
        `idhd`  int(4) default 0,
        `name`  varchar(64)  default '',
        `value` varchar(255) default '',
        primary key (`id`),
        key `rule` (`idhd`,`name`)
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8""" % self.tablename
        return q

class tb_rule(my.table):
    def __init__ (self,dbname):
        my.table.__init__(self,dbname)
        self.addfield('id','d')
        self.addfield('tag','s')
        self.addfield('title','s')

    def _create(self):
        q="""create table `%s` (
        `id`    int(4) unsigned NOT NULL AUTO_INCREMENT,
        `tag`       char(32) default '',
        `title`     char(128) default '',
        primary key (`id`),
        key `tag` (`tag`)
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8""" % self.tablename
        return q

class tb_menu(my.table):
    def __init__ (self,dbname):
        my.table.__init__(self,dbname)
        self.addfield('id','d')
        self.addfield('idhd','d')
        self.addfield('tag','s')
        self.addfield('title','s')
        self.addfield('template','s')

    def _create(self):
        q="""create table `%s` (
        `id`    int(4) unsigned NOT NULL AUTO_INCREMENT,
        `idhd`  int(4) default 0,
        `tag`       char(32) default '',
        `title`     char(128) default '',
        `template`       char(255) default '',
        primary key (`id`),
        key `hd`  (`idhd`,`id`),
        key `url` (`template`)
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8""" % self.tablename
        return q

    def _gets(self):
        self.query_all_select()
        self.query_fields.append("v_parent")
        return "select *,(select title from tb_menu as m where m.id=a.idhd) as v_parent from %s as a order by idhd,id" % self.tablename

class tb_query(my.table):
    def __init__ (self,dbname):
        my.table.__init__(self,dbname)
        self.addfield('id','d')
        self.addfield('url','s')
        self.addfield('title','s')

    def _create(self):
        q="""create table `%s` (
        `id`    int(4) unsigned NOT NULL AUTO_INCREMENT,
        `url`       char(255) default '',
        `title`     char(128) default '',
        primary key (`id`),
        key `url` (`url`)
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8""" % self.tablename
        return q

class tb_group(my.table):
    def __init__ (self,dbname):
        my.table.__init__(self,dbname)
        self.addfield('id','d')
        self.addfield('tag','s')
        self.addfield('title','s')

    def _create(self):
        q="""create table `%s` (
        `id`    int(4) unsigned NOT NULL AUTO_INCREMENT,
        `tag`       char(32) default '',
        `title`     char(128) default '',
        primary key (`id`),
        key `tag` (`tag`)
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8""" % self.tablename
        return q

class tb_property(my.table):
    def __init__ (self,dbname):
        my.table.__init__(self,dbname)
        self.addfield('id','d')
        self.addfield('hd_type','d')
        self.addfield('ct_type','d')
        self.addfield('idhd','d')
        self.addfield('idct','d')
        self.tab_ct=[\
                      {'table':'tb_user', 'fields':'login,name'},\
                      {'table':'tb_rule', 'fields':'tag,title'},\
                      {'table':'tb_menu', 'fields':'title,template'},\
                      {'table':'tb_query','fields':'title,url'},\
                    ]

    def _create(self):
        q="""create table `%s` (
        `id`    int(4) unsigned NOT NULL AUTO_INCREMENT,
        `hd_type`  int(4) default 0,
        `idhd`     int(4) default 0,
        `ct_type`  int(4) default 0,
        `idct`     int(4) default 0,
        primary key (`id`),
        key `rule` (`hd_type`,`idhd`,`ct_type`,`idct`)
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8""" % self.tablename
        return q

    def _set4gets(self,hd,idhd,ct):
        self.hd=int(hd)
        self.idhd=int(idhd)
        self.ct=int(ct)

    def _gets(self):
        self.query_all_select()
        self.query_fields.append("s_tag")
        self.query_fields.append("s_title")
        self.query_fields.append("d_idd")
        idd=",id as idd"
        tabct=self.tab_ct[self.ct]['table']
        fdct =self.tab_ct[self.ct]['fields']+idd
        return "\
        select a.*,b.*\
                from %s as a, (select %s from %s) as b\
                where a.idhd=%d and a.idct = b.idd and hd_type=%d and ct_type=%d\
                order by a.idhd,a.idct"\
        % (self.tablename,fdct,tabct,self.idhd,self.hd,self.ct)

class tb_sets(my.table):
    def __init__ (self,dbname):
        my.table.__init__(self,dbname)
        self.addfield('id','d')
        self.addfield('group','s')
        self.addfield('name','s')
        self.addfield('value','s')

    def _getid(self,name):
        return self.query_select(['value']," where name='%s'" % name)

    def _gethd(self,name):
        return self.query_select(['value']," where group='%s'" % name)

class tb_regs(my.table):
    def __init__ (self,dbname):
        my.table.__init__(self,dbname)
        self.addfield('id','d')
        self.addfield('regid','s')
        self.addfield('adm_pass','s')
        self.addfield('client_pass','s')
        self.addfield('name','s')
        self.addfield('css','s')
        self.addfield('action','d')
        self.addfield('sets','d')

class tb_kasses(my.table):
    def __init__ (self,dbname):
        my.table.__init__(self,dbname)
        self.addfield('id','d')
        self.addfield('idplace','d')
        self.addfield('idreg','d')
        self.addfield('nkassa','d')
        self.addfield('idprice','d')
        self.addfield('name','s')
        self.addfield('nickname','s')
        self.addfield('password','s')
        self.addfield('ip','s')
        self.addfield('css','s')
        self.addfield('date','D')
        self.addfield('time','t')
        self.addfield('up_date','D')
        self.addfield('up_time','t')
        self.addfield('off','d')
        self.addfield('version','s')
        self.addfield('upgrade','s')
        self.addfield('prn_name','s')
        self.addfield('prn_type','s')

class tb_trsc_hd(my.table):
    def __init__ (self,dbname):
        my.table.__init__(self,dbname)
        self.addfield('id','d')
        self.addfield('idreg','d')
        self.addfield('idplace','d')
        self.addfield('nkassa','d')
        self.addfield('_id','d')

        self.addfield('date','D')
        self.addfield('time','t')

        self.addfield('type','d')
        self.addfield('iduser','d')
        self.addfield('seller','d')

        self.addfield('ncheck','d')
        self.addfield('ispayed','d')
        self.addfield('pay_nal','f')
        self.addfield('pay_bnal','f')

        self.addfield('summa','f')
        self.addfield('discount_card','s')
        self.addfield('bonus_card','s')
        self.addfield('discount_proc','f')
        self.addfield('bonus_proc','f')
        self.addfield('bonus_max','f')
        self.addfield('bonus_sum','f')

        self.addfield('bonus','f')
        self.addfield('discount_sum','f')
        self.addfield('bonus_discount','f')
        self.addfield('bonus_type','d')
        self.addfield('errors','s')
        self.addfield('up','d')
        self.addfield('isfiscal','d')
        self.addfield('egais_url','s')
        self.addfield('egais_sign','s')
        
class tb_trsc_ct(my.table):
    def __init__ (self,dbname):
        my.table.__init__(self,dbname)
        self.addfield('id','d')
        self.addfield('idreg','d')
        self.addfield('idplace','d')
        self.addfield('nkassa','d')
        self.addfield('idhd','d')

        self.addfield('date','D')
        self.addfield('time','t')

        self.addfield('code','d')
        self.addfield('storno','d')

        self.addfield('p_idgroup','d')
        self.addfield('p_section','d')
        self.addfield('p_cena','d')
        self.addfield('p_sheme','d')
        self.addfield('p_max_skid','f')
        self.addfield('p_real','d')
        self.addfield('p_type','d')
        self.addfield('p_alco','d')
        self.addfield('p_minprice','f')
        self.addfield('p_maxprice','f')

        self.addfield('multiprice','d')

        self.addfield('paramf1','f')
        self.addfield('paramf2','f')
        self.addfield('paramf3','f')

        self.addfield('mark','s')
        self.addfield('dcount','f')
        self.addfield('discount','f')
        self.addfield('bonus','f')
        self.addfield('bonus_discount','f')
        self.addfield('p_litrag','f')
        self.addfield('p_shk','s')
        self.addfield('barcode','s')
        self.record_add = self.fieldsorder[0:] 

class tb_prices(my.table):
    def __init__ (self,dbname):
        my.table.__init__(self,dbname)
        self.addfield('id','d')
        self.addfield('idreg','d')
        self.addfield('name','s')
        self.addfield('date','D')
        self.addfield('time','t')
        self.record_add = self.fieldsorder[1:] 

class tb_price(my.table):
    def __init__ (self,dbname):
        my.table.__init__(self,dbname)
        self.addfield('idreg','d')
        self.addfield('idprice','d')
        self.addfield('id','s')
        self.addfield('shk','s')
        self.addfield('name','s')
        self.addfield('litrag','f')

        self.addfield('cena','f')
        self.addfield('ostatok','f')
        self.addfield('sheme','d')
        self.addfield('real','d')

        self.addfield('section','d')
        self.addfield('max_skid','f')
        self.addfield('type','d')
        self.addfield('alco','d')

        self.addfield('minprice','f')
        self.addfield('maxprice','f')
        self.addfield('reserved2','s')
        self.addfield('idgroup','s')
        self.addfield('istov','d')

class tb_price_shk(my.table):
    def __init__ (self,dbname):
        my.table.__init__(self,dbname)
        self.addfield('idreg','d')
        self.addfield('idprice','d')
        self.addfield('id','d')
        self.addfield('shk','s')
        self.addfield('name','s')
        self.addfield('cena','f')
        self.addfield('koef','f')

class tb_Zet(my.table):
    def __init__ (self,dbname):
        my.table.__init__(self,dbname)
        self.addfield('id','d')
        self.addfield('idreg','d')
        self.addfield('idplace','d')
        self.addfield('nkassa','d')
        self.addfield('_id','d')

        self.addfield('begin_date','D')
        self.addfield('begin_time','t')
        self.addfield('end_date','D')
        self.addfield('end_time','t')
        self.addfield('date','D')

        self.addfield('begin_ncheck','f')
        self.addfield('end_ncheck','f')

        self.addfield('summa_ret','f')
        self.addfield('c_sale','d')
        self.addfield('c_return','d')
        self.addfield('c_error','d')
        self.addfield('c_cancel','d')

        self.addfield('summa','f')
        self.addfield('summa_ret','f')
        self.addfield('summa_nal','f')
        self.addfield('summa_bnal','f')

        self.addfield('discount','f')
        self.addfield('bonus','f')
        self.addfield('bonus_discount','f')

        self.addfield('number','d')
        self.addfield('vir','f')
        self.addfield('up','d')

class tb_Zet_cont(my.table):
    def __init__ (self,dbname):
        my.table.__init__(self,dbname)
        self.addfield('id','d')
        self.addfield('idreg','d')
        self.addfield('idplace','d')
        self.addfield('nkassa','d')
        self.addfield('idhd','d')

        self.addfield('section','d')
        self.addfield('idgroup','d')
        self.addfield('code','s')
        self.addfield('alco','d')

        self.addfield('paramf1','f')
        self.addfield('paramf2','f')
        self.addfield('paramf3','f')

        self.addfield('discount','f')
        self.addfield('bonus','f')
        self.addfield('bonus_discount','f')

class tb_gplace_hd(my.table):
    def __init__ (self,dbname):
        my.table.__init__(self,dbname)
        self.addfield('id','d')
        self.addfield('idreg','d')
        self.addfield('name','s')
        self.record_add = self.fieldsorder[1:] 

class tb_gplace_ct(my.table):
    def __init__ (self,dbname):
        my.table.__init__(self,dbname)
        self.addfield('ida','d')
        self.addfield('idreg','d')
        self.addfield('idplace','d')
        self.addfield('act_date','D')
        self.addfield('act_time','t')
        self.record_add = self.fieldsorder[1:] 

class tb_tlist_hd(my.table):
    def __init__ (self,dbname):
        my.table.__init__(self,dbname)
        self.addfield('id','d')
        self.addfield('idreg','d')
        self.addfield('idprice','d')
        self.addfield('name','s')
        self.record_add = self.fieldsorder[1:] 

class tb_tlist_ct(my.table):
    def __init__ (self,dbname):
        my.table.__init__(self,dbname)
        self.addfield('ida','d')
        self.addfield('idreg','d')
        self.addfield('idt','d')
        self.addfield('dopcode','d')
        self.addfield('count','f')
        self.record_add = self.fieldsorder[1:] 


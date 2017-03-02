init_data();
fill_form(TDATA_SETS_HD);
fill_form(TDATA_SETS_CT);
function init_data(){

    TDATA_SPRAV={};
    CLASS_ED="itext strong";
    CLASS_MOD="but small";
    CLASS_BUT="but small";
    PREFIX_TD="td_";
    PREFIX_MOD="mod_";
    PREFIX_DATA="data_";
    PREFIX_QUERY="/sprav/";
    POSTFIX_QUERY="/get";
    QUERY_URL="/ot/trsc";
    TDATA_SETS_HD = { 
        "idreg"   :  {"type":TYPE_SP,   "all": true,    "query"     :"regs"  ,"class":"autor" }, 
        "idplace" :  {"type":TYPE_SP,   "all": true,    "query"     :"place" ,"class":"autor" }, 
        "nkassa"  :  {"type":TYPE_LIST, "all": true,    "values"    :{1:1,2:2,3:3} , "class":"autor" },
        "date1"   :  {"type":TYPE_TEXT, "pattern"   :"20[1,2][0-9]-[0-1][0-9]-[0-3][0-9]","placeholder":"20YY-MM-DD","default":"curdate","size":8,"mod":['date']},   
        "date2"   :  {"type":TYPE_TEXT, "pattern"   :"20[1,2][0-9]-[0-1][0-9]-[0-3][0-9]","placeholder":"20YY-MM-DD","default":"curdate","size":8,"mod":['date']},   
        "time1"   :  {"type":TYPE_TEXT, "pattern"   :"[0-2][0-9]:[0-5][0-9]","placeholder":"HH:MM","default":"","size":8,"mod":['empty']},   
        "time2"   :  {"type":TYPE_TEXT, "pattern"   :"[0-2][0-9]:[0-5][0-9]","placeholder":"HH:MM","default":"","size":8,"mod":['empty']},   
        "ispayed" :  {"type":TYPE_LIST, "all": true, "values"    :{0:"Отмененные",1:"Оплаченные"} },
        "type"    :  {"type":TYPE_LIST, "all": true, "values"    :{0:"Продажа",1:"Возврат"} },
        "isfiscal":  {"type":TYPE_LIST, "all": true, "values"    :{0:"Без чека",1:"Фискальльный"} },
        "iserror" :  {"type":TYPE_LIST, "all": true, "values"    :{0:"Без ошибок",1:"С ошибками"} },
        "isegais" :  {"type":TYPE_LIST, "all": true, "values"    :{0:"Обычный чек",1:"ЕГАИС чек"} },
        "ncheck"  :  {"type":TYPE_TEXT, "placeholder":"Любой","default":"","size":8,"mod":['empty']},   
        "isdiscountcard"   :  {"type":TYPE_LIST, "all": true, "values"    :{1:"Есть",0:"Нет"} },
        "isbonuscard"      :  {"type":TYPE_LIST, "all": true, "values"    :{1:"Есть",0:"Нет"} },
        "discount_card"    :  {"type":TYPE_TEXT, "placeholder":"Любая","default":"","size":5,"mod":['empty']},   
        "discount_proc"    :  {"type":TYPE_TEXT, "placeholder":"Любой","default":"","size":5,"mod":['empty','ifnum']},   
        "discount_sum"     :  {"type":TYPE_TEXT, "placeholder":"Любая","default":"","size":5,"mod":['empty','ifnum']},   
        "bonus_card"       :  {"type":TYPE_TEXT, "placeholder":"Любая","default":"","size":5,"mod":['empty']},   
        "bonus_proc"       :  {"type":TYPE_TEXT, "placeholder":"Любой","default":"","size":5,"mod":['empty','ifnum']},   
        "bonus_sum"        :  {"type":TYPE_TEXT, "placeholder":"Любая","default":"","size":5,"mod":['empty','ifnum']},   
        "bonus"            :  {"type":TYPE_TEXT, "placeholder":"Любое","default":"","size":5,"mod":['empty','ifnum']},   
        "bonus_discount"   :  {"type":TYPE_TEXT, "placeholder":"Любое","default":"","size":5,"mod":['empty','ifnum']},   
        "bonus_type"       :  {"type":TYPE_LIST, "all": true, "values"    :{0:"Начисление",1:"Списание"} },
        "summa"            :  {"type":TYPE_TEXT, "placeholder":"Любая","default":"","size":5,"mod":['empty','ifnum']},   
        "summa_wod"        :  {"type":TYPE_TEXT, "placeholder":"Любая","default":"","size":5,"mod":['empty','ifnum']},   
        "type_pay"         :  {"type":TYPE_LIST, "all": true, "values"    :{0:"Наличный",1:"Безналичный",2:"Смешаный"} },
    }
    TDATA_SETS_CT = { 
        "code"             :  {"type":TYPE_TEXT, "placeholder":"Любой","default":"","size":8,"mod":['empty','ifnumc']},   
        "p_idgroup"        :  {"type":TYPE_TEXT, "placeholder":"Любая","default":"","size":5,"mod":['empty','ifnumc']},   
        "p_section"        :  {"type":TYPE_TEXT, "placeholder":"Любая","default":"","size":5,"mod":['empty','ifnum']},   
        "storno"           :  {"type":TYPE_LIST, "all": true, "values"    :{0:"Нет",1:"Да"} },
        "p_real"           :  {"type":TYPE_LIST, "all": true, "values"    :{0:"Нет",1:"Да"} },
        "p_alco"           :  {"type":TYPE_LIST, "all": true, "values"    :{0:"Нет",1:"Да"} },
        "ch_cena"          :  {"type":TYPE_LIST, "all": true, "values"    :{0:"Нет",1:"Да"} },
        "limitprice"       :  {"type":TYPE_LIST, "all": true, "values"    :{0:"Нет",1:"Да"} },
        "p_cena"           :  {"type":TYPE_TEXT, "placeholder":"Любая","default":"","size":5,"mod":['empty','ifnum']},   
        "p_max_skid"       :  {"type":TYPE_TEXT, "placeholder":"Любая","default":"","size":5,"mod":['empty','ifnum']},   
        "discount"         :  {"type":TYPE_TEXT, "placeholder":"Любая","default":"","size":5,"mod":['empty','ifnum']},   
        "ct_bonus"            :  {"type":TYPE_TEXT, "placeholder":"Любой","default":"","size":5,"mod":['empty','ifnum']},   
        "ct_bonus_discount"   :  {"type":TYPE_TEXT, "placeholder":"Любое","default":"","size":5,"mod":['empty','ifnum']},   
        "paramf1"          :  {"type":TYPE_TEXT, "placeholder":"Любая","default":"","size":5,"mod":['empty','ifnum']},   
        "paramf2"          :  {"type":TYPE_TEXT, "placeholder":"Любая","default":"","size":5,"mod":['empty','ifnum']},   
        "paramf3"          :  {"type":TYPE_TEXT, "placeholder":"Любая","default":"","size":5,"mod":['empty','ifnum']},   
        "mark"             :  {"type":TYPE_TEXT, "placeholder":"Любая","default":"","size":4,"mod":['empty','ifnumc']},   
        "p_litrag"         :  {"type":TYPE_TEXT, "placeholder":"Любой","default":"","size":4,"mod":['empty','ifnum']},   
        "dcount"           :  {"type":TYPE_TEXT, "placeholder":"Любое","default":"","size":4,"mod":['empty','ifnum']},   
        "p_shk"            :  {"type":TYPE_TEXT, "placeholder":"Любой","default":"","size":8,"mod":['empty','ifnum']},   
    };
    TDATA_LIST_TRSC_HD = {
    'hd.ncheck'         :{"name":"Чек","class":"strong"},
    'hd.id'             :{"name":"#"},
    'hd.idplace'        :{"name":"Точка","sp":"place","class":"autor"},
    'hd.nkassa'         :{"name":"Касса","class":"autor"},
    'hd.discount_card'  :{"name":"ДКарта","class":"rusty"},
    'hd.discount_proc'  :{"name":"%"},
    'hd.bonus_max'      :{"name":"Макс"},

    'hd.date'           :{"name":"Дата","line":1},
    'hd.pay_nal'        :{"name":"Нал","fixed":2},
    'hd.pay_bnal'       :{"name":"Б/Нал","fixed":2},
    'hd.bonus'          :{"name":"Бонус","class":"code","fixed":2},
    'hd.bonus_card'     :{"name":"БКарта","class":"energy"},
    'hd.bonus_proc'     :{"name":"%"},
    'hd.bonus_sum'      :{"name":"Остаток","fixed":2},
 

    'hd.time'           :{"name":"Время","line":2},  
    'hd.summa'          :{"name":"Всего","class":"bold big","fixed":2},
    'hd.discount_sum'   :{"name":"Скидка","class":"flame","fixed":2},
    'hd.bonus_discount' :{"name":"Списание","class":"flame","fixed":2},
    'summa_wod'         :{"name":"Итого","class":"bg1 bold big","fixed":2,"span":5},

    }
    TDATA_LIST_TRSC_CT = { 
    'ct.id'             :{'name':'#','class':'strong bold'},
    'ct.time'           :{'name':'Время'},
    'ct.code'           :{'name':'Код'},
    'title'             :{'name':'Наименование'},
    'ct.mark'           :{'name':'*'},
    'ct.p_cena'         :{'name':'Цена',"fixed":2},
    'ct.p_max_skid'     :{'name':'М%'},
    'ct.paramf1'        :{'name':'$Цена',"fixed":2,"class":"strong"},
    'ct.paramf2'        :{'name':'Кол',"fixed":3,"class":"strong"},
    'ct.paramf3'        :{'name':'Сумма',"fixed":2,"class":"strong"},
    'ct.dcount'         :{'name':'КБ','nonull':1},
    'ct.discount'       :{'name':'Скид',"fixed":2,"class":"flame"},
    'ct.bonus'          :{'name':'Б+',"fixed":2,"class":"code"},
    'ct.bonus_discount' :{'name':'Б-',"fixed":2,"class":"flame"},
    'ct.p_litrag'       :{'name':'Литр',"fixed":3},
    'ct.p_shk'          :{'name':'Штрихкод'},
    }

    TDATA_ITOG_HD   = {
        'count'            :{'name':'Чеков',"class":"big bold"},
        'hd.type'          :{'name':'Возвратов',"class":"big bold flame"},
        'hd.summa'         :{'name':'Сумма без скидок',"fixed":2,"class":"big bold strong"},
        'hd.discount_sum'  :{'name':'Скидки',"fixed":2,"class":"big bold flame"},
        'hd.bonus_discount':{'name':'Списание бонусов',"fixed":2,"class":"big bold flame"},
        'summa_wod'        :{'name':'ИТОГО',"fixed":2,"class":"big bold strong"},
        'hd.bonus'         :{'name':'Начисление бонусов',"fixed":2,"class":"big bold code"},
        'hd.pay_nal'       :{'name':'Сумма наличными',"fixed":2,"class":"big bold strong"},
        'hd.pay_bnal'      :{'name':'Сумма безналичными',"fixed":2,"class":"big bold strong"},
    }
    TDATA_ITOG_CT   = {
        'count'            :{'name':'Позиций',"class":"big bold"},
        'ct.paramf2'       :{'name':'Количество',"fixed":3,"class":"big bold"},
        'ct.paramf3'       :{'name':'Стоимость',"fixed":2,"class":"big bold strong"},
        'ct.discount'      :{'name':'Скидки',"fixed":2,"class":"big bold flame"},
        'ct.bonus_discount':{'name':'Списание бонусов',"fixed":2,"class":"big bold flame"},
        'summa'            :{'name':'ИТОГО',"fixed":2,"class":"big bold strong"},
        'ct.bonus'         :{'name':'Начисление бонусов',"fixed":2,"class":"big bold code"},
    }
}
function run_query(t){
    qhd=create_query(TDATA_SETS_HD,false);
    qct=create_query(TDATA_SETS_CT,false);
    jshd=JSON.stringify(qhd);
    jsct=JSON.stringify(qct);
    async_post(QUERY_URL,{"data_hd":jshd,"data_ct":jsct,"type_query":t},show_result);
}
function show_result(j,p){
    TR_CLASS="";
    js=JSON.parse(j);
    if (!js['result']){
        alert("Ошибка запроса");
        return;
    }
    fd=js["fields"];
    data=js["data"];
    eltb=document.getElementById('tbdata');
    _ct="";
    last=0;
    n=0;
    clear_tdata_itog(TDATA_ITOG_CT);
    clear_tdata_itog(TDATA_ITOG_HD);
    for (i in data) {
        r=data[i];
        id=r[fd.indexOf('hd.idreg')]+"_"+r[fd.indexOf('hd.idplace')]+"_"+r[fd.indexOf("hd.id")];
        if (id!=last){
            inc_tdata_itog(TDATA_ITOG_HD,fd,r);
            n+=1;
            trid="data_"+i;
            if (r[fd.indexOf('hd.type')]==1){TR_CLASS='bg4';TDATA_LIST_TRSC_HD['summa_wod']['class']='bold big bg4';} 
            else {TR_CLASS='';TDATA_LIST_TRSC_HD['summa_wod']['class']='bold big bg1';}
            if (r[fd.indexOf('hd.errors')]!=""){TDATA_LIST_TRSC_HD['hd.ncheck']['class']='flame';}
            else{TDATA_LIST_TRSC_HD['hd.ncheck']['class']='strong';}
            if (r[fd.indexOf('hd.ispayed')]==0){TR_CLASS='bg2';} 
            if (r[fd.indexOf('hd.isfiscal')]==0){TDATA_LIST_TRSC_HD['summa_wod']['class']='big bg2';}
            if (r[fd.indexOf('hd.egais_url')]!=''){TDATA_LIST_TRSC_HD['summa_wod']['class']='big bg3';}
            trhd="<tr><td class='big center'>"+n+"</td>"+
            "<td><table class='tbp wall'>"+create_line_head_content(TDATA_LIST_TRSC_HD,fd,trid,r)+"</table>";
            trct="<table class='tbp wall'>"+create_line_head(TDATA_LIST_TRSC_CT);
            last=id;
            if (i>0){ _ct+="</table></td></tr>"; }
            _ct+=trhd+trct;
        }
            trid="data_"+i;
            if (r[fd.indexOf('ct.storno')]==1){
                TR_CLASS='bg2';
                TDATA_LIST_TRSC_CT['title']['class']='flame';} 
            else {
                TR_CLASS='';
                TDATA_LIST_TRSC_CT['title']['class']='';}
            if (r[fd.indexOf('ct.p_alco')]==1){
                TR_CLASS='bg3';
                TDATA_LIST_TRSC_CT['title']['class']='energy';} 
            if (r[fd.indexOf('ct.paramf1')]==0){
                TR_CLASS='bg1';
                TDATA_LIST_TRSC_CT['title']['class']='code';} 
            if (r[fd.indexOf('ct.paramf1')]==r[fd.indexOf('ct.p_cena')]){
                TDATA_LIST_TRSC_CT['ct.paramf1']['class']='strong'; 
                TDATA_LIST_TRSC_CT['ct.p_cena']['class']='';}
            else{
                TDATA_LIST_TRSC_CT['ct.paramf1']['class']='rusty';
                TDATA_LIST_TRSC_CT['ct.p_cena']['class']='rusty'; } 
            if (r[fd.indexOf('hd.type')]==1){TDATA_LIST_TRSC_CT['ct.paramf3']['class']='energy';}
            else{TDATA_LIST_TRSC_CT['ct.paramf3']['class']='strong';}
            if ((r[fd.indexOf('ct.p_minprice')]!=0)||(r[fd.indexOf('ct.p_maxprice'!=0)])){
                TDATA_LIST_TRSC_CT['ct.paramf1']['class']='energy';
                TDATA_LIST_TRSC_CT['ct.mark']['class']='energy';
                } else{TDATA_LIST_TRSC_CT['ct.mark']['class']='';}
            
            inc_tdata_itog(TDATA_ITOG_CT,fd,r);
            trct=create_line_content(TDATA_LIST_TRSC_CT,fd,trid,r);
            _ct+=trct;
    }
    TDATA_ITOG_HD['hd.pay_nal']['value']=TDATA_ITOG_HD['summa_wod']['value']-TDATA_ITOG_HD['hd.pay_bnal']['value'];
    TDATA_ITOG_CT['summa']['value']=TDATA_ITOG_CT['ct.paramf3']['value']-TDATA_ITOG_CT['ct.discount']['value']-TDATA_ITOG_CT['ct.bonus_discount']['value'];
    TR_CLASS='bg1';
    if (i>0){ _ct+="</table></td></tr>"; }
    trit_hd="<tr><td></td><td><table class='tbp wall'>"+create_line_head(TDATA_ITOG_HD)+create_line_content_hash(TDATA_ITOG_HD)+"</table></td>";
    trit_ct="<tr><td></td><td><table class='tbp wall'>"+create_line_head(TDATA_ITOG_CT)+create_line_content_hash(TDATA_ITOG_CT)+"</table></td>";
    eltb.innerHTML=_ct+trit_hd+trit_ct;
    tbdata.scrollIntoView(true);
}

q_hd=['user','group'];
q_ct=['user','rule','menu','query'];
IDHD=0;IDCT=0;
TYPE_HD=1;TYPE_CT=0;
load_sphd();
load_spct();
//get_data();
function get_data(){
    init_data();
    async_get("/admin/properties?hd="+TYPE_HD+"&ct="+TYPE_CT+"&idhd="+IDHD,show_data);
}
function load_spct(){
    async_get("/sprav/"+q_ct[TYPE_CT]+"/get",fill_ct);
}
function fill_ct(j,p){
    json_hd=JSON.parse(j);
    if (!json_hd['result']){
        return;
    }
    sp_ct=json_hd['data'];
    _fillsprav(sp_ct,'d_idct');
    get_data();
}
function load_sphd(){
    async_get("/sprav/"+q_hd[TYPE_HD]+"/get",fill_hd);
}
function fill_hd(j,p){
    json_hd=JSON.parse(j);
    if (!json_hd['result']){
        return;
    }
    sp_hd=json_hd['data'];
    _fillsprav(sp_hd,'d_idhd');
}
function show_data(j,p){
    tbdata.hidden=true;
    json=JSON.parse(j);
    if (!json['result']){
        alert('Извините, но у вас нет доступа к этой функции');
        return;
    }
    data=json['data'];
    ct=_data2table(data,['s_tag','s_title'],{});

    fd=['Тэг','Содержимое'];
    th="";
    for (i in fd){ th+="<th>"+fd[i]+"</th>";  }
    tbdata.innerHTML="<tr><th>#</th>"+th+"</tr>"+ct;
    recreate_table();
    tbdata.hidden=false;
}
function recreate_table(){
    for (i in data){
        rc=data[i];
        tr='tbdata_'+i;
        eltr=document.getElementById(tr);
        eltr.addEventListener('click', tronclick, false); 
    }
}
function tronclick(){
    id=this.id.substr(7);
    QID=data[parseInt(id)]['id'];
    delete_data();
}
function init_data(){
    TYPE_HD = document.getElementById('d_hd_type').value;
    TYPE_CT = document.getElementById('d_ct_type').value;
    IDHD = d_idhd.value;
    IDCT = d_idct.value;
    if (IDHD==''){ IDHD=1; }
    if (IDCT==''){ IDCT=0; }
    ld_data={'id':0,'hd_type':TYPE_HD,'idhd':IDHD,'ct_type':TYPE_CT,'idct':IDCT};
}
function add_data(){
    init_data();
    json=JSON.stringify(ld_data);
    async_post("/admin/property/put",{'data':json},post_change);
}
function delete_data(){
    if (confirm("Вы действительно хотите удалить эту запись?")){
        init_data();
        ld_data['id']=QID;
        json=JSON.stringify(ld_data);
        async_post("/admin/property/del",{'data':json},post_change);
    }
}
function post_change(j,p){
    json=JSON.parse(j);
    stat=document.getElementById("stat");
    if (!json['result']){
        stat.innerHTML="<span class='flame'>Ошибка сохранения данных.</span>";
        return;
    }else{
        QID=json['id'];
    }
    get_data();
}

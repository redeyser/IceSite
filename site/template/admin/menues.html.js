get_data();
function get_data(){
    async_get("/admin/menues",show_data);
}
function show_data(j,p){
    tbdata.hidden=true;
    json=JSON.parse(j);
    if (!json['result']){
        alert('Извините, но у вас нет доступа к этой функции');
        return;
    }
    data=json['data'];
    ct=_data2table(data,['v_parent','tag','title','template'],{});

    fd=['Родитель','Тэг','Наименование','Шаблон'];
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
    async_get('/template/admin/menu.html',show_content);LAST_PAGE=THIS_PAGE;
}
function add_data(){
    QID=0;
    async_get('/template/admin/menu.html',show_content);LAST_PAGE=THIS_PAGE;
}


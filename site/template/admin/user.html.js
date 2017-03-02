get_data();
function get_data(){
    async_get("/sprav/regs/get",fill_regs);
    async_get("/admin/user/get?id="+QID,show_data); 
}
function show_data(j,p){
    json=JSON.parse(j);
    if (!json['result']){
        alert('Извините, но у вас нет доступа к этой функции');
        return;
    }
    data=json['data'];
    ld_data=_filldata(data,['password']);
}
function fill_regs(j,p){
    json_regs=JSON.parse(j);
    if (!json_regs['result']){
        return;
    }
    sp_regs=json_regs['data'];
    _fillsprav(sp_regs,'d_idreg');
}
function save_data(){
    if (confirm("Вы действительно хотите сохранить данные?")){
        data=_loaddata(ld_data);
        if (d_password.value!=''){
            data['password']=d_password.value;
        }
        if (Object.keys( data ).length==0){
            stat.innerHTML="<span class='flame'>Изменений не зафиксировано. Сохранение отменено.</span>";
            return;
        }
        data['id']=QID;
        json=JSON.stringify(data);
        async_post("/admin/user/put",{'data':json},put_data);
    }
}
function delete_data(){
    if (confirm("Вы действительно хотите удалить эту запись?")){
        data['id']=QID;
        json=JSON.stringify(data);
        async_post("/admin/user/del",{'data':json},put_data);
    }
}
function put_data(j,p){
    json=JSON.parse(j);
    stat=document.getElementById("stat");
    if (!json['result']){
        stat.innerHTML="<span class='flame'>Ошибка сохранения данных. Возможно доступ к сохранению ограничен.</span>";
        return;
    }else{
        QID=json['id'];
        //get_data();
        stat.innerHTML="<span class='code'>Данные успешно сохранены.</span>";
        async_get(LAST_PAGE,show_content);
    }
}

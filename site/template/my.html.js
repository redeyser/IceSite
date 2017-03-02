get_data();
function get_data(){
    async_get("/self/get",show_data);
}
function show_data(j,p){
    json=JSON.parse(j);
    if (!json['result']){
        alert('Извините, но у вас нет доступа к этой функции');
        return;
    }
    data=json['data'][0];
    ld_data=_filldata(data,['password']);
    //d_password.value='';
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
        json=JSON.stringify(data);
        async_post("/self/put",{'data':json},put_data);
    }
}
function put_data(j,p){
    json=JSON.parse(j);
    stat=document.getElementById("stat");
    if (!json['result']){
        stat.innerHTML="<span class='flame'>Ошибка сохранения данных. Возможно доступ к сохранению ограничен.</span>";
        return;
    }else{
        get_data();
        stat.innerHTML="<span class='code'>Данные успешно сохранены.</span>";
    }
}

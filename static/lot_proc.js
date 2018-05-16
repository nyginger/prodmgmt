
$(document).ready(function() {

    $('#proc-up').bind('click', function() {
        $('#auto_procs option:selected').each( function() {
            var nexPos = $('#auto_procs option').index(this) - 1;
            if (nexPos > -1) {
                $('#auto_procs option').eq(nexPos).before("<option value='"+$(this).val()+"' selected='selected'>"+$(this).text()+"</option>");
                $(this).remove();
            }
        });
    });
    $('#proc-down').bind('click', function() {
        var cntOpts = $('#auto_procs option').size();
        $('#auto_procs option:selected').each( function() {
            var nexPos = $('#auto_procs option').index(this) + 1;
            if (nexPos < cntOpts) {
                $('#auto_procs option').eq(nexPos).after("<option value='"+$(this).val()+"' selected='selected'>"+$(this).text()+"</option>");
                $(this).remove();
            }
        });
    });
    $('#proc-add').click(function(){
        $('#newprc option:selected').each( function() {
                $('#auto_procs').append("<option value='"+$(this).text()+"'>"+$(this).text()+"</option>");
        });
   
    });
    $('#proc-remove').click(function(){
        $('#auto_procs option:selected').each( function() {

            $(this).remove();
        });
    });

    $('#btn-add').click(function(){
        $('#select-from option:selected').each( function() {
                $('#select-to').append("<option value='"+$(this).val()+"'>"+$(this).text()+"</option>");
            $(this).remove();
        });
    });
    $('#btn-remove').click(function(){
        $('#select-to option:selected').each( function() {
            $('#select-from').append("<option value='"+$(this).val()+"'>"+$(this).text()+"</option>");
            $(this).remove();
        });
    });
    $('#btn-up').bind('click', function() {
        $('#select-to option:selected').each( function() {
            var newPos = $('#select-to option').index(this) - 1;
            if (newPos > -1) {
                $('#select-to option').eq(newPos).before("<option value='"+$(this).val()+"' selected='selected'>"+$(this).text()+"</option>");
                $(this).remove();
            }
        });
    });
    $('#btn-down').bind('click', function() {
        var countOptions = $('#select-to option').size();
        $('#select-to option:selected').each( function() {
            var newPos = $('#select-to option').index(this) + 1;
            if (newPos < countOptions) {
                $('#select-to option').eq(newPos).after("<option value='"+$(this).val()+"' selected='selected'>"+$(this).text()+"</option>");
                $(this).remove();
            }
        });
    });
    $('#btn-reset').bind('click', function(){
        document.getElementById('select-from').options.length=0;
        $.getJSON(app_url+'/api/stage?q={"order_by":[{"field":"id","direction":"asc"}]}', function(data) {
            for (x in data.objects){
                $('#select-from').append('<option value="'+data.objects[x].work+'">'+data.objects[x].work+'</option>')
            }
        });
        
    });

    $('#btn-del_proclist').bind('click', function(){
        var proc_id = $('#sel_product2 option:selected').val();
        var r = confirm("공정목록을 삭제하시겠습니까?");
        if (r == true) {

            $.ajax({
            type: "DELETE",
            url: app_url+'/api/stage_procs/'+proc_id,
           
            });
            location.replace(app_url + '/proclist_info');
        }

    });


});


function procAll() { 
    var procBox = document.getElementById("auto_procs");
    for (var i = 0; i < procBox.options.length; i++) 
    { 
        procBox.options[i].selected = true; 
    } 
}

function addAll() { 
    var procBox = document.getElementById("auto_procs");
    $('#auto_procs option').each(function(){
        $('#new_stage_list').append("<option value='"+$(this).text()+"'>"+$(this).text()+"</option>");
    }) 
    var newprcBox=document.getElementById("new_stage_list");
    for (var j=0; j < newprcBox.options.length; j++){
        newprcBox.options[j].selected=true;
    }
}


function selectfromAll(e) { 
    e.preventDefault();
    var selectBox = document.getElementById("select-from");
    for (var k = 0; k < selectBox.options.length; k++) 
    { 
        selectBox.options[k].selected = true; 
    } 
}

function selectAll() { 
        
        var selectBox = document.getElementById("select-to");
        for (var k = 0; k < selectBox.options.length; k++) 
        { 
            selectBox.options[k].selected = true; 
        } 
    }


function procLoad1(){
    
    var n=$('#sel_product option:selected').val();
    var select=document.getElementById('select-to');
    select.options.length = 0;
    $.getJSON(app_url+'/api/stage_procs?q={"filters":[{"name":"id","op":"equals","val":"' + n + '"}]}', function(data) {
        var items=data.objects[0];
        var q=items.length;
        for (index in items){
            if( index!='id' && index!='company' && index!='product' && items[index]!=null && items[index]!=''){
                select.options[select.options.length]=new Option(items[index]);
            }
        }
    });
}



function procLoad2(){
    
    var n=$('#sel_product2 option:selected').val();
    var select=document.getElementById('auto_procs');
    select.options.length = 0;
    $.getJSON(app_url+'/api/stage_procs?q={"filters":[{"name":"id","op":"equals","val":"' + n + '"}]}', function(data) {
        var items=data.objects[0];
        var q=items.length;
        for (index in items){
            if( index!='id' && index!='company' && index!='product' && items[index]!=null && items[index]!=''){
                select.options[select.options.length]=new Option(items[index]);
            }
        }
    });
}

function procUpdate(e){
    e.preventDefault();
    var r=confirm('공정 목록을 수정하시겠습니까?')
    if (r==true){
        $('#proc_id').val($('#sel_product2').val());
        var procBox = document.getElementById("auto_procs");
        for (var i = 0; i < procBox.options.length; i++) 
        { 
            procBox.options[i].selected = true; 
        } 
        var form_data = new FormData($('#procform')[0]);
           $.ajax({
               type: 'POST',
               url: '/update_proclist',
               data: form_data,
               contentType: false,
               cache: false,
               processData: false,
               async: false,
               success: function(data) {
                    alert("공정목록이 수정되었습니다.");
               },
           });
        }
} 


function procAdd(e){
    e.preventDefault();
    var select=document.getElementById('auto_procs');
    var n=select.options.length;
    var com= $('#com option:selected').text();
    var product=$('#prod_cat').val();
    var proc=[];
    if (n<25){
        for (var i = 0; i < n; i++) { 
            proc[i]=select.options[i].value;
        }
        for (var j=n; j <25;j++){
            proc[j]=undefined;
        }        
    } else{
        for (var i = 0; i < 25; i++) { 
            proc[i]=select.options[i].value;
        }
    }
    $.ajax({
        type: "POST",
        url: app_url + "/api/stage_procs" ,
        data: JSON.stringify({
            company: com,
            product: product,
            proc01 : proc[0],
            proc02 : proc[1],
            proc03 : proc[2],
            proc04 : proc[3],
            proc05 : proc[4],
            proc06 : proc[5],
            proc07 : proc[6],
            proc08 : proc[7],
            proc09 : proc[8],
            proc10 : proc[9],
            proc11 : proc[10],
            proc12 : proc[11],
            proc13 : proc[12],
            proc14 : proc[13],
            proc15 : proc[14],
            proc16 : proc[15],
            proc17 : proc[16],
            proc18 : proc[17],
            proc19 : proc[18],
            proc20 : proc[19],
            proc21 : proc[20],
            proc22 : proc[21],
            proc23 : proc[22],
            proc24 : proc[23],
            proc25 : proc[24]
        } ),
        dataType: "json",
        contentType : "application/json"
      });
      reloadProcList();
      alert('추가되었습니다!');
}

function reloadProcList(){
    try{
        var select=document.getElementById('sel_product');
        var select2=document.getElementById('sel_product2');
        select.options.length=0
        select2.options.length=0;
        select.options[0]=new Option('공정선택');
        $.getJSON(app_url+'/api/stage_procs?q={"order_by":[{"field":"company","direction":"asc"}]}', function(data) {
            for (x in data.objects){
                
                $('#sel_product').append('<option value="'+data.objects[x].id+'">'+data.objects[x].company+' | '+data.objects[x].product+'</option>')
                $('#sel_product2').append('<option value="'+data.objects[x].id+'">'+data.objects[x].company+' | '+data.objects[x].product+'</option>')
            }
        });
    }  catch(e){
        var select2=document.getElementById('sel_product2');
        select2.options.length=0;
        $.getJSON(app_url+'/api/stage_procs?q={"order_by":[{"field":"company","direction":"asc"}]}', function(data) {
            for (x in data.objects){
                
                $('#sel_product2').append('<option value="'+data.objects[x].id+'">'+data.objects[x].company+' | '+data.objects[x].product+'</option>')
            }
        });
    }
    
    
}
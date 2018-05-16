var socket = io.connect();

$(document).ready( function() {
    
    // broadcast a message
    socket.on( 'connect', function() {
        //var form = $( 'msgform' ).on( 'submit', function( e ) {
        var form = $( '#msgform' ).on( 'submit', function( e ) {
        //var form =  $(document.getElementById('msgform')).on( 'submit', function( e ) {
            e.preventDefault()
            var dt_lot_id = $("#lot").val();
            if (dt_lot_id=='') {
                alert('LOT이 존재하지 않거나 입력값이 없습니다.')
            } else if ($("#person").val()==''){
                alert('작업자를 입력하여 주십시오.')
            } else {
                var r = confirm("작업을 입력하시겠습니까?");
                if (r == true) {
                    
                    var dt_work_name = $("#wn option:selected").text();
                    var dt_in_out = $("#io").val();
                    var dt_company = $("#com").val();
                    var dt_prod_name = $("#prod").val();
                    var dt_message = $("#msg").val();
                    var dt_person = $("#person").val();
                    var arr_person = dt_person.split(",");
                    var cnt_person = arr_person.length;
                    socket.emit( 'event', {
                        lot_id: dt_lot_id,
                        work_name : dt_work_name,
                        in_out: dt_in_out,
                        person: dt_person,
                        person_count: cnt_person,
                        message: dt_message,
                        filename:''
                    } );
                    alert('작업이 입력되었습니다.\n'+dt_lot_id+'\n'+dt_work_name+'\n'+dt_company);
                }
            }
        });

        var form = $( '#photoform' ).on( 'submit', function( e ) {
            //var form =  $(document.getElementById('msgform')).on( 'submit', function( e ) {
            e.preventDefault();
            r=confirm('사진을 업로드하시겠습니까?')
            if (r==true){
                var com=$("#com").val();
                if (com==''){
                    alert('Lot정보없음\nLot정보를 조회해주십시오.')
                    return false;
                } else if ($("#person").val()==''){
                    alert('작업자를 입력하여 주십시오.')
                } else {
                    var dt_lot_id = $("#lot").val();
                    var dt_work_name = $("#wn option:selected").text();
                    var dt_in_out = $("#io").val();
                    var dt_company = $("#com").val();
                    var dt_prod_name = $("#prod").val();
                    var dt_message = $("#msg").val();
                    var dt_person = $("#person").val();
                    var arr_person = dt_person.split(",");
                    var cnt_person = arr_person.length;
                    //Extract filename
                    var fullPath = document.getElementById('file').value;
                    var startIndex = (fullPath.indexOf('\\') >= 0 ? fullPath.lastIndexOf('\\') : fullPath.lastIndexOf('/'));
                    var filename = fullPath.substring(startIndex);
                    if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0) {
                        filename = filename.substring(1);
                    }

                    socket.emit( 'event', {
                        lot_id: dt_lot_id,
                        work_name : dt_work_name,
                        in_out: dt_in_out,
                        person: dt_person,
                        person_count: cnt_person,
                        message: dt_message,
                        filename:filename
                    } );
                    photoSubmit();
                }
            }
        });




    });

    socket.on( 'response', function( msg ) {
        console.log( msg )
        if( typeof msg.work_name !== 'undefined' ) {
            $( 'h1' ).remove()
            var htmlperson='';
            var htmlfilename='';
            var pub_time=msg.pub_time.substr(0,4)+'-'+msg.pub_time.substr(4,2)+'-'+msg.pub_time.substr(6,2)+' @ '+msg.pub_time.substr(8,2)+':'+msg.pub_time.substr(10,2);
            if (typeof msg.person !== 'undefined'){
                var persons= msg.person.split(",");
                for (ix in persons){
                    htmlperson+='<a href="/search?query='+persons[ix]+'" target="_blank">'+persons[ix]+'&nbsp;</a>';
                }
            }
            if (typeof msg.filename!=='undefined' && msg.filename!=''){
                htmlfilename='<li><a class="ajax" href="/gallery",lot_id='+msg.lot_id+'"><i class="material-icons" style="font-size:25px;color:red">photo_library</i></a></li>';
            }
            $( '#zone'+msg.zone ).prepend( '<div id="'+msg.id+'" class="grid-item"><ul class="list-unstyled"><li><b style="color: #000">'+msg.work_name+'&nbsp;</b></li>'+
                '<li><a href="/lot_info?lot_id='+msg.lot_id+'" target="_blank"><b style="color:brown;">'+msg.lot_id+'&nbsp;</b> </a></li>'+
                '<li><a href="/search?query='+msg.company+'" target="_blank"><b style="color:darkblue;">'+msg.company+'&nbsp;</b></a></li>'+
                '<li><a href="/search?query='+msg.prod_name+'" target="_blank">'+msg.prod_name+'&nbsp;</a>'+msg.in_out+'</li>'+
                '<li>'+htmlperson+'</li>'+
                htmlfilename+
                '<input type=hidden id="work_no" value="'+msg.id+'">'+
                '<small>'+pub_time+'</small>'+
                '<a id="w'+msg.id+'" style="text-align:right;" href="#" onclick="delWork(this);"><small><span class="badge badge-pill badge-light">x</span></small></a></div>')
        }
    });  

    socket.on('del_msg',function(msg){
        console.log(msg);
        var dt_work_id=msg.work_id;
        $('#'+dt_work_id).remove();
    });

    $('#upload-file-btn').click(function() {
     r=confirm('사진을 업로드하시겠습니까?')
     if (r==true){
         var com=$("#com").val();
         if (com==''){
             alert('Lot정보없음\nLot정보를 조회해주십시오.')
             return false;
         } else{
           $('#wn2').val($('#wn').val());
           $('#lot2').val($('#lot').val());
           $('#com2').val($('#com').val());
           $('#prod2').val($('#prod').val());
           $('#io2').val($('#io').val());
           $('#msg2').val($('#msg').val());
           $('#per2').val($('#person').val());
           var form_data = new FormData($('#photoform')[0]);
           $.ajax({
               type: 'POST',
               url: '/up_result',
               data: form_data,
               contentType: false,
               cache: false,
               processData: false,
               async: false,
               success: function(data) {
                   console.log('Success!');
               },
           });
         }
       } 
    });
}); 

function delWork(elem){
    var dt_work_id = elem.id.substring(1);
    var r = confirm("작업기록을 삭제하시겠습니까?");
    if (r == true) {
        var dt_table='works';
        $.ajax({
        type: "POST",
        url: app_url + "/delete",
        data: JSON.stringify({
            datatable: dt_table,
            data_id : dt_work_id
        } ),
        dataType: "json",
        contentType : "application/json"
        });
        $('#'+dt_work_id).remove();
        location.reload();
        socket.emit('del_msg', {
                    work_id:dt_work_id
        });
    }
}

function scan_lot(e){
    e.preventDefault();
    var person=$('#person').val();
    if (person!=''){
        localStorage.setItem("person",person);
    }
    localStorage.setItem("barcodeitem",'lot_barcode');
    window.open(app_url +'/barcode' , "_self");
}

function scan_person(e){
    e.preventDefault();
    var lot=$('#lot').val();
    if (lot!=''){
        localStorage.setItem("lot",lot);
    }
    localStorage.setItem("barcodeitem",'person_barcode');
    window.open(app_url +'/barcode' ,  "_self");
}

function onSearchLot(e){
    if (e.keyCode == 13) {
        search_lot(e);
        return false;
    } else{
        return true;
    }

}

function search_lot(e){
    e.preventDefault();
    $('#com').remove();
    $('#prod').remove();
    var lot_id= $('#lot').val();
    window.open(app_url + "/lot_info?lot_id=" + lot_id);
    $.getJSON(app_url + '/api/lot?q={"filters":[{"name":"lot_id","op":"equals","val":"' + lot_id + '"}]}', function(data) {
            var items=data.objects[0];
            $('div.info').append('<input type="text" id="com" name="company" class=" form-control" value='+items.company+' readonly><div style="padding-top: 5px;"></div>');
            $('div.info').append('<input type="text" id="prod" name="prod_name" class=" form-control" value='+items.prod_name+' readonly>');
            });
}






function onInsPer(e){
    if (e.keyCode == 13) {
        insPerson(e);
        return false;
    } else {
        return true;
    }  
    
}

function insPerson(e){
    
        e.preventDefault();
        var add_person=$('#per').val();
        var str_person= document.getElementById('person').value;
        var work_person= str_person.split(",");
        work_person=$.grep(work_person, function(a){
            return a!='';
        });
        var idx = work_person.indexOf(add_person);
        if (idx < 0) {
            work_person.push(add_person);
            $('div.person_box' ).append( '<input type="button" value="' + add_person + '" class="btn btn-success" onclick="RemoveItself(this);" />&nbsp;' );
            document.getElementById("person").setAttribute("value", work_person.toString());    
        }
        $('#per').val('');

}




//function procChange(){
//    var wn1=$("#wn option:selected").text();
//    document.getElementById('wn2').value =wn1;
//}



   
function photoSubmit(){
    //document.photoform.work_name.value =document.msgform.work_name.value;
    //document.photoform.lot_id.value =document.msgform.lot_id.value;

    $('#wn2').val($('#wn').val());
    $('#lot2').val($('#lot').val());
    $('#com2').val($('#com').val());
    $('#prod2').val($('#prod').val());
    $('#io2').val($('#io').val());
    $('#msg2').val($('#msg').val());
    $('#per2').val($('#person').val());
    var form_data = new FormData($('#photoform')[0]);
    $.ajax({
        type: 'POST',
        url: '/up_result',
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        async: false,
        success: function(data) {
            console.log('Success!');
        },
    });
}
      





function sendForm(e){
    e.preventDefault();
    var dt_lot_id = $("#lot").val();
    if (dt_lot_id=='') {
        alert('LOT이 존재하지 않거나 입력값이 없습니다.')
    } else {
        var r = confirm("작업을 입력하시겠습니까?");
        if (r == true) {
            var dt_lot_id = $("#lot").val();
            var dt_work_name = $("#wn option:selected").text();
            var dt_in_out = $("#io").val();
            var dt_company = $("#com").val();
            var dt_prod_name = $("#prod").val();
            var dt_message = $("#msg").val();
            var dt_person = $("#person").val();
            var arr_person = dt_person.split(",");
            var cnt_person = arr_person.length;
            $.ajax({
            type: "POST",
            url: app_url + "/create",
            data: JSON.stringify({
                lot_id: dt_lot_id,
                work_name : dt_work_name,
                in_out: dt_in_out,
                person: dt_person,
                person_count: cnt_person,
                message: dt_message
            } ),
            dataType: "json",
            contentType : "application/json"
            });
            alert('입력되었습니다!');
        } else{
            alert('입력이 취소되었습니다.')
        }
    }
}





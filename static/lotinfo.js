$(document).ready(function(){
	$('#chart_work_url').attr("href",chart_url + '/chart_work' );
	$('#chart_lot_url').attr("href",chart_url + '/chart_lot' );
})

var id;
var lot_id;
var company;
var com_id;
var product;
var prod_id;
var prod_name;
var cnt;
var person;
var gen;
var anod_type;
var prod_serial;
var pol;
var mask;
var shil;
var shil_type;
var surf;
var ra;
var indate;
var tdate;

$(document).ready(function(){
	$('#company').on('change', function(){
		//$.getJSON(app_url + '/api/company?q={"filters":[{"name":"com_name","op":"eq","val":"'+$(this).val() + '"}]}', 
		//	function(data) {
		//		$('#com_id').val(data.objects[0].id);
		//	}
		//);
		
		//var filters=[{"name":"com_name","op":"eq","val":$(this).val()}];
		//$.ajax({
		//	type:"GET",
		//	url: app_url + "/api/company",
		//	data: {"q": JSON.stringify({
		//		"filters":filters
		//	})},
		//	dataType: "json",
		//	contentType : "application/json",
		//	success: function(data){
		//		$('#com_id').val(data.objects[0].id);
		//		console.log($('#com_id').val());
		//	}
		
		var filters=[{"name":"com_name","op":"eq","val":$(this).val()}];
		$.get(app_url+'/api/company',{"q":JSON.stringify({
					filters:filters
				})}
			,function(data){
				$('#com_id').val(data.objects[0].id);
			} 
		)
	});

	$('#product').on('change', function(){
		var filters=[{"name":"prod_name","op":"eq","val":$(this).val()}];
		$.get(app_url+'/api/product',{"q":JSON.stringify({
					filters:filters
				})}
			,function(data){
				$('#prod_id').val(data.objects[0].prod_no);
			} 
		)	
	});


	$('#btn_reiss').on('click', function(e){
		e.preventDefault();
		lot_id= $('#lot_id').val();
		
		console.log(lot_re_code);
		var filters=[{"name":"lot_id","op":"eq","val":lot_id+'-RW1'}];
		$.get(app_url+'/api/lot',{"q":JSON.stringify({
					filters:filters
				})}
			,function(data){
				var items=data.num_results;
				if (items>0) {
					alert(data.objects[0].lot_id+'은 이미 재발행되어 있습니다.');
				} else {
					func_lot_rw(e);
				}
			}
		);
	});

	$('#btn_split_show').on('click', function(e){
		e.preventDefault();
		$('#modal1').modal('show');
	})
    $('#btn-right').click(function(){
        $('#lot_select1 option:selected').each( function() {
                $('#lot_select2').append("<option value='"+$(this).val()+"'>"+$(this).text()+"</option>");
            $(this).remove();
        });
    });
    $('#btn-left').click(function(){
        $('#lot_select2 option:selected').each( function() {
            $('#lot_select1').append("<option value='"+$(this).val()+"'>"+$(this).text()+"</option>");
            $(this).remove();
        });
	});
	$('#lot_sp_code1').on('change',function(){
		var lot_sp_code1=$('#lot_sp_code1 option:selected').val();
		if (lot_sp_code1=='nm'){
			$('#lot_sp_code2').val('ma');
		} else if (lot_sp_code1=='ma') {
			$('#lot_sp_code2').val('nm');
		} else if (lot_sp_code1=='sp1') {
			$('#lot_sp_code2').val('sp2');
		} else {
			$('#lot_sp_code2').val('sp1');
		}
	
	});

	$('#btn_split').click(function(){
		lot_id= $('#lot_id').val();
		var lot_sp_code1=$('#lot_sp_code1 option:selected').val();
		var lot_sp_code2=$('#lot_sp_code2 option:selected').val();
		if (lot_sp_code1==''){
			alert('Lot1의 분할코드를 선택해주세요');
		} else if (lot_sp_code2==''){
			alert('Lot2의 분할코드를 선택해주세요');
		} else {
			var filters=[{"name":"lot_id","op":"eq","val":lot_id+'-'+lot_sp_code1.toUpperCase()}];
			$.get(app_url+'/api/lot',{"q":JSON.stringify({
						filters:filters
					})}
				,function(data){
					var items=data.num_results;
					if (items>0) {
						conf=confirm(data.objects[0].lot_id+'은 이미 분할되어 있습니다.\n또, 분할하시겠습니까?');
						if (conf==True){
							func_lot_split();
						} else{
							alert('취소되었습니다.');
						}
					} else {
						func_lot_split();
					}
				}
			);
		}
	});
})



function load_info(e){
    if (e.keyCode == 13) {
        //search_info(e);
		
		 load_lotpage(e);
		return false;
    } else{
        return true;
    }
}

function load_lotpage(e){
	e.preventDefault();
	lot_id= $('#lot_id').val();
	var filters=[{"name":"lot_id","op":"eq","val":lot_id}];
	$.get(app_url+'/api/lot',{"q":JSON.stringify({
			filters:filters
		})},
		function(data){
			var items=data.num_results;
			if (items==0) {
				alert('Lot등록 정보가 없습니다!');
			} else {
				location.replace(app_url+'/load_lotinfo?lot_id='+lot_id,"_self");
			}
		}
	)
}

function search_info(e){
    e.preventDefault();
	lot_id= $('#lot_id').val();
	$('#btns_2add').html('');
	var filters=[{"name":"lot_id","op":"eq","val":lot_id}];
	$.get(app_url+'/api/lot',{"q":JSON.stringify({
			filters:filters
		})},
		function(data){
			var items=data.objects[0];
			$('#id').val(items.id);
			console.log(items.id);
			$('#company').val(items.company);
			$('#com_id').val(items.com_id);
			$('#product').val(items.prod_category);
			$('#prod_id').val(items.prod_type);
			$('#prod_name').val(items.prod_name);
			$('#cnt').val(items.counts);
			$('#person').val(items.person);
			$('#gen').val(items.gen);
			$('#anod_type').val(items.anod_type);
			$('#prod_serial').val(items.prod_serial);
			$('#pol option:selected').val(items.pol_YN);
			$('#mask option:selected').val(items.mask_YN);
			$('#shil option:selected').val(items.shil_YN);
			$('#shil_type option:selected').val(items.shil_type);
			$('#surf').val(items.surf_layer);
			$('#ra').val(items.RA);
			tdate=moment(items.target_date).format('YYYY-MM-DD')
			$('#tdate').val(tdate);
			$('#btn').attr('onclick','update_lotinfo(event);').html('수정');
			$('#btns_2add').append('<div class="form-group col-md-3"><button id="btn_reiss" class="btn btn-lg btn-primary btn-block">Lot재작업/작업분할</button>'+
			 '</div><div class="form-group col-md-3"><button id="btn_split_show" class="btn btn-lg btn-primary btn-block" >Lot분할</button></div>');
			console.log(items.prod_category);
			document.getElementById('lot_id').readOnly = true;
			document.getElementById('lot_reissue').readOnly = false;
		}
	)
}




function confLotDel(){
	return confirm(" 정말로 삭제하시겠습니까?" );
}


function update_lotinfo(e){
	e.preventDefault();
	id=$('#id').val();
	lot_id=$('#lot_id').val();
	company=$('#company').val().toUpperCase();
	com_id=parseInt($('#com_id').val());
	product=$('#product').val();
	prod_id=parseInt($('#prod_id').val());
	prod_name=$('#prod_name').val().replace(' ','_').toUpperCase();
	cnt=parseInt($('#cnt').val());
	person=$('#person').val();
	gen=$('#gen').val();
	anod_type=$('#anod_type').val();
	prod_serial=$('#prod_serial').val().toUpperCase();
	pol=$('#pol option:selected').text();
	mask=$('#mask option:selected').text();
	shil=$('#shil option:selected').text();
	shil_type=$('#shil_type option:selected').text();
	surf=$('#surf').val();
	ra=$('#ra').val();
	tdate=$('#tdate').val();
	console.log(id);

    $.ajax({
        type: "PUT",
        url: app_url + "/api/lot/" + id,
        data: JSON.stringify({
            
            company : company,
			prod_name : prod_name,
	        counts : cnt,
            person : person,
            gen : gen,
            anod_type :anod_type,
            prod_serial : prod_serial,
            pol_YN : pol,
            mask_YN : mask,
			shil_YN : shil,
			shil_type: shil_type,
			surf_layer: surf,
			RA: ra,
			target_date: tdate,
			com_id: com_id,
			prod_type: prod_id

      
        } ),
        dataType: "json",
		contentType : "application/json",
		success: alert('LOT정보가 수정되었습니다!')
		
	  })
	  location.replace(app_url+'/load_lotinfo?lot_id='+lot_id);
}



function up_lotinfo(e){
    e.preventDefault();
    lot_id=$('#lot_id').val();
	var form_data = new FormData($('#lotform')[0]);
    $.ajax({
        type: 'POST',
        url: app_url + '/update_lot',
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        async: false,
        success: function(data) {
			location.replace(app_url+'/load_lotinfo?lot_id='+lot_id);
			alert('Lot이 수정되었습니다.');
      }
	});
}




function create_lot(e){
    e.preventDefault();
    lot_id= $('#lot_id').val();
	var filters=[{"name":"lot_id","op":"eq","val":lot_id}];
	$.get(app_url+'/api/lot',{"q":JSON.stringify({
			filters:filters
		})},
		function(data){
			var items=data.num_results;
			if (items==0) {
				func_createlot(e);		
			} else {
				alert('Lot이 이미 등록되어 있습니다.');
				location.replace(app_url+'/load_lotinfo?lot_id='+lot_id);
			}
		})
}

function func_createlot(e){
	e.preventDefault();
    lot_id= $('#lot_id').val();
	var form_data = new FormData($('#lotform')[0]);
    $.ajax({
        type: 'POST',
        url: app_url + '/create_lot',
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        async: false,
        success: function(data) {
			location.replace(app_url+'/load_lotinfo?lot_id='+lot_id);
			alert('Lot이 등록되었습니다.');
      }
	});
}


function func_lot_rw(e){
	lot_id= $('#lot_id').val();
	var lot_re_code='RW';
	var r = confirm("재작업Lot을 발행하시겠습니까?");
	if (r == true) {
		$.ajax({
		type: "POST",
		url: app_url + "/lot_rework",
		data: JSON.stringify({
			lot_id: lot_id,
			lot_re_code : lot_re_code
		} ),
		dataType: "json",
		contentType : "application/json"
		});
		alert('lot이　추가발행되었습니다．')
	} else{
		alert('lot 추가발행이　취소되었습니다．')
	}
}

function func_lot_split(e){
	lot_id= $('#lot_id').val();
	var lot_sp_code1=$('#lot_sp_code1 option:selected').val();
	var lot_sp_code2=$('#lot_sp_code2 option:selected').val();
	var lot_select1=document.getElementById('lot_select1');
	var lot_select2=document.getElementById('lot_select2');
	var lot_sn1='';
	var lot_sn2='';
	for (var i=0;i<lot_select1.options.length;i++){
		lot_sn1+=lot_select1.options[i].value+',';
	}
	for (var j=0;j<lot_select2.options.length;j++){
		lot_sn2+=lot_select2.options[j].value+',';
	}
	var r = confirm("Lot을 분할하시겠습니까?");
	if (r == true) {
		$.ajax({
		type: "POST",
		url: app_url + "/lot_split",
		data: JSON.stringify({
			lot_id: lot_id,
			lot_sp_code1 : lot_sp_code1,
			lot_sp_code2 : lot_sp_code2,
			lot_sn1:lot_sn1,
			lot_sn2:lot_sn2
		} ),
		dataType: "json",
		contentType : "application/json"
		});
		
		alert('lot이　분할되었습니다．');
		$('#modal1').modal('hide');
		window.open(app_url+'/load_lotinfo?lot_id='+lot_id+'-'+lot_sp_code1.toUpperCase());
		window.open(app_url+'/load_lotinfo?lot_id='+lot_id+'-'+lot_sp_code2.toUpperCase());
		
		

	} else{
		alert('lot분할이　취소되었습니다．');
	}
}
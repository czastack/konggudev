$(function(){
	$.fn.cza_modal = function(action){
		fn = ''
		if (action == 'show') 
			fn = 'add';
		else if (action == 'hide') 
			fn = 'remove';
		else
			return;
		fn += 'Class'
		$(document.body)[fn]('modal-open-body');
		$(this)[fn]('modal-open');
	};

	$('.modal').click(function(){
		$(this).cza_modal('hide');
	})
	.find('.modal-dialog').click(function(event){
		event.stopPropagation();
	})
	.find('.modal-cancel,.modal-ok').click(function(){
		console.log($(this).parents('.modal:eq(0)'));
		$(this).parents('.modal:eq(0)').cza_modal('hide');
	});
});
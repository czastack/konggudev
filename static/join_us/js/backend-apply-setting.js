$(function(){
	$(".btn-edit").click(function(){
		var $this = $(this);
		$("#depart_info").find('input, textarea').removeAttr('readonly');
		$this.hide().nextAll('button').show();
	}).nextAll('button').hide();
	$(".btn-cancel,.btn-submit").click(function(){
		$(this).siblings('.btn-edit').show().nextAll('button').hide();
		$("#depart_info").find('input, textarea').attr('readonly', true);
	});
});
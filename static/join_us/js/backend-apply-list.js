/*document.onreadystatechange = function() {
	if (document.readyState=="complete" || document.readyState=='interactive') {
		document.onreadystatechange = null;
		
		checkall.onchange = function(){
			var checked = this.checked;
			var items = document.querySelectorAll('.detail td input[type=checkbox]');
			for (var i = 0; i < items.length; i++) {
				items[i].checked = checked;
			}
		};
	}
}*/
$(function(){
	$("#checkall").change(function(){
		$('.detail td input[type=checkbox]').attr('checked', this.checked)
	});
	$(".btn-info").click(function(){
		var $parent = $(this).parent();
		$.get($parent.attr('href') + 'detail', {'id': $parent.attr('uid')}, function(data){
			$detail = $('#modal-detail');
			$detail.find('.modal-content').html(data);
			$detail.cza_modal('show');
		});
	});
	$(".btn-delete").click_confirm('#modal-delete');
});
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
		this[fn]('modal-open');
		return this;
	};
	$.fn.click_confirm = function(target, onconfirm){
		var self = this;
		$(target).on('modal-cancel', function(){
			self.confirmed = false;
		}).find('.modal-ok').click(function(){
			$(self).click();
		});
		this.click(function(){
			if (!self.confirmed){
				onconfirm && onconfirm();
				$(target).cza_modal('show');
			}
			return !(self.confirmed = !self.confirmed);
		});
		return this;
	};

	$('.modal').click(function(){
		$(this).cza_modal('hide').trigger('modal-cancel');
	})
	.find('.modal-dialog').click(function(event){
		event.stopPropagation();
	})
	.find('.modal-cancel').click(function(){
		$(this).parents('.modal:eq(0)').click();
	})
	.end().find('.modal-ok').click(function(){
		$(this).parents('.modal:eq(0)').cza_modal('hide');
	});
});
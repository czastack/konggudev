$(function(){
	$.fn.cza_modal = function(action){
		if (action == 'show') {
			if (!$('.modal-open').length) 
				$(document.body).addClass('modal-open-body');
			this.addClass('modal-open');
		} else if (action == 'hide') {
			this.removeClass('modal-open');
			if (!$('.modal-open').length) 
				$(document.body).removeClass('modal-open-body');
		}
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
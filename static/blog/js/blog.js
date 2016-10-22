$(function(){
	$code = $("#qrcode");
	$code.qrcode({ 
		render: "canvas",
		size: $code.width(),
		text: location.href
	});

	// 回到顶部
	var $scoll = $(window);
	var $toTop  = $(".to_top");
	$toTop.hide().click(function(){
		$("html, body").animate({'scrollTop': 0}, 800);
	});
	$scoll.scroll(function(){
		if ($scoll.scrollTop() > 500) 
			$toTop.fadeIn();
		else
			$toTop.fadeOut();
	});
});
window.onload = function(){
	var elems = document.querySelectorAll('select');
	for (var i = 0; i < elems.length; i++) {
		elems[i].value = '';
	}
}
window.onload = function(){
	function confirmDelete(){
		if (!confirm('确认删除？')) {
			return false;
		}
	}
	document.querySelectorAll('.delete').forEach(function(e){
		e.onclick = confirmDelete;
	});
}
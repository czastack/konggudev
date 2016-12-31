window.onload = function(){
    var snippets = {
        bold:   ["**@**", "Bold"],
        italic: ["*@*", "Italic"],
        anchor: ["[Link](http://@/)", "example.com"],
        line:   ["\n> @", ""],
        code:   ["`@`", "code"],
        img:    ["![Img](http://@/)", "example.com"],
        li:     ["\n- @", ""],
        title:  ["\n# @", ""],
        hr:     ["\n\n---\n\n", ""],
        table:  ["\n\n| title | title | title |\n| --- | --- | --- |\n| item | item | item |", ""],
    };

    var inputer = document.getElementById('inputer');
    inputer.oninput = function(){
        html.innerHTML = marked(this.value);
    };
    inputer.oninput();
    
    function insertSnippet(){
        inputer.focus();
        var snippet = snippets[this.key];
        var start = inputer.selectionStart
        var end = inputer.selectionEnd;
        var selected = start != end;
        var sText = selected ? inputer.value.substring(start, end) : snippet[1];
        var content = snippet[0];
        var offset = content.indexOf('@');
        if (offset != -1) {
            content = content.replace('@', sText);
        }
        else {
            offset = 0;
        }
        document.execCommand("insertText", true, content);
        if (sText) {
            inputer.setSelectionRange(start + offset, start + offset + sText.length);
        }
        return false;
    }
    document.querySelectorAll('.btns button').forEach(function(e){
        e.key = e.getAttribute('key');
        e.tabIndex = -1;
        e.onclick = insertSnippet;
    });
};
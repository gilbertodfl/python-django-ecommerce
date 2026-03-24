var url = new URL(document.URL);
var itens= document.getElementsByClassName("produtos__select");
for( i = 0; i < itens.length; i++){
    url.hash = ""; // remove o # do final
    url.searchParams.set("ordem",itens[i].value);
    itens[i].value=url.href;
}

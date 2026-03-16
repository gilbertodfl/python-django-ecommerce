var url = new URL(document.URL);
var itens= document.getElementsByClassName("item-ordernar");
for( i = 0; i < itens.length; i++){
    url.hash = ""; // remove o # do final
    url.searchParams.set("ordem",itens[i].name);
    itens[i].href=url.href;
}

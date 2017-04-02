// ==UserScript==
// @name       cn-proxy
// @namespace  https://github.com/WingGao/ProxyChecker
// @version    1.2
// @description  get proxy
// @match      http://cn-proxy.com/
// @copyright  2017+, WingGao
// ==/UserScript==
function getProxy() {
    var list = [];
    jQuery('tbody tr').each(function (i, ele) {
        var $ele = $(ele);
        //console.log($ele);
        //console.log($ele.children()[0]);
        list.push('http://' + $ele.children()[0].innerHTML + ':' + $ele.children()[1].innerHTML);
        //console.log('"http://'+ $ele.children()[0].innerHTML+':'+$ele.children()[1].innerHTML+'",');
    });
    var thtml = '';
    list.forEach(function (l) {
        thtml += l + "<br>"
    });
    $('body').html(thtml);
}
window.addEventListener('load', function () {
    window.$ = jQuery;
    $('.current_page_item').append('<button id="wing-action">GETPROXY</button>');
    $('#wing-action').click(getProxy);

}, false);

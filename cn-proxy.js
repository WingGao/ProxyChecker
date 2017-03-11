//http://cn-proxy.com/
window.$ = jQuery;
var list = [];
jQuery('tr').each(function (i, ele) {
    var $ele = $(ele);
    //console.log($ele);
    if ($ele.hasClass('roweven') || $ele.hasClass('rowodd')) {
        //console.log($ele.children()[0]);
        list.push('http://' + $ele.children()[0].innerHTML + ':' + $ele.children()[1].innerHTML);
        //console.log('"http://'+ $ele.children()[0].innerHTML+':'+$ele.children()[1].innerHTML+'",');
    }
});
var html = ''
list.forEach(function (l) {
    html += '"' + l + '",'
})
$('body').html(html);

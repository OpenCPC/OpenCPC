//For non-website-specific functions

//https://stackoverflow.com/questions/24816/escaping-html-strings-with-jquery

var entityMap = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
    '/': '&#x2F;',
    '`': '&#x60;',
    '=': '&#x3D;'
};
  
function htmlspecialchars (string) {
    //Notice: This function should NOT encrypt [ or ] - VERY IMPORTANT
    return String(string).replace(/[&<>"'`=\/]/g, function (s) {
        return entityMap[s];
    });
}
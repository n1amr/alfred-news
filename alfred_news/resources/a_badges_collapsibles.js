//Background
var idle_header_color = "#393D49";
var active_header_color = "#393D49";
var body_color = "#212830";
var border_color = "1px " + "solid " + "#1C2027";
//Text
var title_color = "#C4CBD8";
var content_color = "#EFEFEF";

$(".collapsible-header").css("background-color", idle_header_color);
$(".collapsible-header").css("border-bottom", border_color);
$(".collapsible-header > .collapsible-header-value").css('color', title_color);
$(".collapsible-body > p").css('color', content_color);
$(".collapsible-body").css("background-color", body_color);


$(".collapsible-header").click(function () {
    if ($(this).attr("class") == "collapsible-header") {
        $(".collapsible-header").css("background-color", idle_header_color)
        $(this).css("background-color", active_header_color)
    }
    else if ($(this).attr("class") == "collapsible-header active") {
        $(this).css("background-color", idle_header_color)
    }
});

//Background
var idle_header_color = "#b3e5fc"
var active_header_color = "#03a9f4"
var body_color = "#e64a19"
var border_color = "1px " + "solid " + "#000000"
//Text
var title_color = "#ff9100"
var content_color = "#ffff00"


$(".collapsible-header").css("background-color", idle_header_color)
$(".collapsible-header").css("border-bottom", border_color)
$(".collapsible-header > .collapsible-header-value").css('color', title_color)
$(".collapsible-body > p").css('color', content_color)
$(".collapsible-body").css("background-color", body_color)



$(".collapsible-header").click(function(){
  if($(this).attr("class") == "collapsible-header"){
    $(".collapsible-header").css("background-color",idle_header_color)
    $(this).css("background-color", active_header_color)
  }
  else if($(this).attr("class") == "collapsible-header active"){
    $(this).css("background-color",idle_header_color)
  }
})

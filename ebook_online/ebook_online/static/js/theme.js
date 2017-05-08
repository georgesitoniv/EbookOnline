$(document).ready(function(){
    $('.parallax').parallax();
    $(".button-collapse").sideNav();
    $('.dropdown-button#menu-item-books').dropdown({
      inDuration: 300,
      outDuration: 225,
      belowOrigin:true,
      hover:true,
      constrainWidth:false,
    });
    $('.dropdown-button#menu-item-profile').dropdown({
      inDuration: 300,
      outDuration: 225,
      belowOrigin:true,
      hover:true,
      constrainWidth:false,
    });
    $('ul.tabs').tabs();
    $('.modal').modal();
    $('.col .card').matchHeight();
    $('.materialboxed').materialbox();
});

if($(window).width() < 768){
  $(".card.horizontal.book-detail").removeClass("horizontal");
} else{
  $(".card.book-detail").addClass("horizontal");  
}
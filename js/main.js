document.addEventListener("DOMContentLoaded",function(){
var cards=document.querySelectorAll(".feature-card");
if(cards.length){
var observer=new IntersectionObserver(function(e){e.forEach(function(e){if(e.isIntersecting){e.target.style.opacity="1";e.target.style.transform="translateY(0)"}});},{threshold:0.1});
cards.forEach(function(c){c.style.opacity="0";c.style.transform="translateY(20px)";c.style.transition="all .4s ease-out";observer.observe(c)})
}
});

const button1=document.getElementById("animation_button1");
const button2=document.getElementById("animation_button2");
const my_div=document.getElementById("colored_image")

button1.addEventListener('click', function() {
    my_div.classList.add("mask_animation");
});
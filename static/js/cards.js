const humans= document.querySelector('.humans');
const fantasy =document.querySelector('.fantasy');

humans.addEventListener('click', function () {
    const human_cards=document.querySelectorAll(".humans_cards");
    human_cards.forEach(element => {
        element.style.display= 'block'
    });
})
fantasy.addEventListener('click', function () {
    const fantasy_cards=document.querySelectorAll(".fantasy_cards");
    fantasy_cards.forEach(element => {
        element.style.display='block'
    });
})

fantasy.load
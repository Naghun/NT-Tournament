document.getElementById('draw_numbers').addEventListener('click', function () {
    generate_new_numbers();
});

function generate_new_numbers() {
    fetch('/novi_brojevi')
    .then(response => response.json())
    .then(data => {
        const number_list = getElementById('random-numbers-list');
        number_list.innerHTML = '';
        data.forEach(number => {
            const li=document.createElement('li');
            li.textContent=number
            number_list.appendChild(li)
        });
    });
}

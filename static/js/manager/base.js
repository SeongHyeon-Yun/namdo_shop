const all_menu = document.getElementById('all-menu');
const mobile = document.getElementById('mobile');
const btn_close = document.getElementById('btn-close');

all_menu.addEventListener("click", () => {
    console.log('test')
    mobile.classList.toggle('hidden')
})

btn_close.addEventListener('click', () => {
    mobile.classList.toggle('hidden')
})
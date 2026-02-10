// 유저 상태창 토글 버튼
const name_box = document.getElementById('name');
const user_menu_box = document.getElementById('user-menu-box');

name_box.addEventListener('click', () => {
    user_menu_box.classList.toggle('active');
})


// 메뉴 토글 버튼
const menu = document.getElementById('menu');
const nav = document.getElementById('nav');

menu.addEventListener('click', () => {
    nav.classList.toggle('active');
})
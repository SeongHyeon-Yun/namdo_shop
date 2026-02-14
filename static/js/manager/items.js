// 리스트 타입 버튼
const item_list = document.getElementById("item-list");
const item_grid = document.getElementById("item-grid");

// 리스트 구역
const items_table_area = document.getElementById('items-table-area');
const items_img_area = document.getElementById('items-img-area');


item_list.addEventListener('click', () => {
    if (!item_list.classList.contains('icon-active')) {
        item_grid.classList.remove('icon-active');
        item_list.classList.add('icon-active');
        items_img_area.classList.add("item-hidden");
        items_table_area.classList.remove("item-hidden");
    }
})

item_grid.addEventListener('click', () => {
    if (!item_grid.classList.contains('icon-active')) {
        item_list.classList.remove('icon-active');
        item_grid.classList.add('icon-active');
        items_img_area.classList.remove("item-hidden");
        items_table_area.classList.add("item-hidden");
    }
})
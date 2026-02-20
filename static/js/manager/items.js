// 상품 추가하기 오프캔버스 열기
const item_add_btn = document.getElementById('item-add');
const add_area = document.getElementById('add_area');
const close_btn = document.getElementById('close-btn');

item_add_btn.addEventListener("click", () => {
    console.log('test');
    console.log(add_area.classList.remove("hidden"));
})

// 상품 추가하기 오프캔버스 닫기
close_btn.addEventListener('click', () => {
    console.log('close_test');
    add_area.classList.add("hidden");
})


ClassicEditor
    .create(document.querySelector('#editor'), {
        toolbar: [
            'bold',
            'italic',
            'link',
            '|',
            'bulletedList',
            'numberedList',
            '|',
            'imageUpload',
            '|',
            'undo',
            'redo'
        ]
    })
    .catch(error => {
        console.error(error);
    });


// 모달 닫기
const modal_close_btn = document.getElementById("modal_close_btn");
const modal_area = document.getElementById('modal_area')
modal_close_btn.addEventListener("click", () => {
    modal_area.remove()
})


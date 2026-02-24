// 상품 추가하기 오프캔버스 열기
const item_add_btn = document.getElementById('item-add');
const add_area = document.getElementById('add_area');
const close_btn = document.getElementById('close-btn');

item_add_btn.addEventListener("click", () => {
    console.log(add_area.classList.remove("hidden"));
})

// 상품 추가하기 오프캔버스 닫기
close_btn.addEventListener('click', () => {
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

const del_btn = document.getElementById('del_btn');
del_btn.addEventListener('click', () => {
    console.log('del-btn test')
})

// 전체 체크 기능
const all_check = document.getElementById("all-check");
all_check.addEventListener('click', () => {
    const checkboxes = document.querySelectorAll('.item-check');

    checkboxes.forEach((checkbox) => {
        checkbox.checked = all_check.checked;
    });
});

// 숫자만 입력 가능
function onlyNumber(el) {
    el.value = el.value.replace(/[^0-9]/g, '');
}

// 숫자만 입력 가능하고 , 표시
function onlyPrice(el) {

    // 1️⃣ 숫자만 남기기
    let value = el.value.replace(/\D/g, '');

    // 3️⃣ 콤마 추가
    if (value) {
        value = Number(value).toLocaleString('ko-KR');
    }

    // 4️⃣ 다시 input에 넣기
    el.value = value;
}


// 모달
const item_detail_modal = document.getElementById("item_detail");
const item_detail_off = document.getElementById("item_detail_off");

// 모든 행 클릭 이벤트 등록
document.querySelectorAll(".item-row").forEach(row => {
    row.addEventListener("click", function (e) {

        // 체크박스 클릭했을 때는 모달 열지 않음
        if (e.target.type === "checkbox") return;

        const itemId = this.dataset.id;
        openItemDetail(itemId);
    });
});

// 모달 열기 + 데이터 가져오기
function openItemDetail(id) {
    fetch(`/manager/item_detail/${id}/`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("modal_title").innerText = data.title;
            document.getElementById("modal_price").innerText = Number(data.price).toLocaleString();
            document.getElementById("origin").innerText = data.origin;
            document.getElementById("item_delivery_1").innerText = Number(data.delivery_1).toLocaleString();
            document.getElementById("item_delivery_2").innerText = data.delivery_2;
            document.getElementById("text").innerText = data.text;
            document.getElementById("status").innerText = data.status;
            document.getElementById("description").innerHTML = data.description;

            item_detail_modal.classList.remove("hidden");

            const d2 = document.getElementById("delivery_2");

            console.log("엘리먼트:", d2);
            d2.innerText = Number(data.delivery_2).toLocaleString();
            console.log("넣은 후:", d2.innerText);

        })
        .catch(err => console.error(err));
}

// 모달 닫기
item_detail_off.addEventListener("click", () => {
    item_detail_modal.classList.add("hidden");
});

console.log(document.querySelector('[role="tab"]'))
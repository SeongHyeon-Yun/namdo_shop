// 상품 추가하기 오프캔버스 열기
const item_add_btn = document.getElementById('item-add');
const add_area = document.getElementById('add_area');
const close_btn = document.getElementById('close-btn');

item_add_btn.addEventListener("click", () => {
    add_area.classList.remove("hidden");
})

// 상품 추가하기 오프캔버스 닫기
close_btn.addEventListener('click', () => {
    add_area.classList.add("hidden");
})

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
    item_detail_modal.classList.remove("hidden");

    fetch(`/manager/item_detail/${id}/`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("status").innerText = data.status;
            document.getElementById("tex").innerText = data.tex;
            document.getElementById("modal_title").innerText = data.title;
            document.getElementById("origin").innerText = data.origin;
            document.getElementById("modal_price").innerText = Number(data.price).toLocaleString();
            document.getElementById("item_delivery_1").innerText = Number(data.delivery_1).toLocaleString();
            document.getElementById("item_delivery_2").innerText = Number(data.delivery_2).toLocaleString();
            document.getElementById("description").innerHTML = data.desc;

            renderCarousel(data.img_list);
        })
        .catch(err => console.error(err));
}

function renderCarousel(imgList) {
    const wrapper = document.getElementById("carousel_wrapper");

    wrapper.innerHTML = ""; // 기존 이미지 제거

    imgList.forEach((url, index) => {
        const img = document.createElement("img");
        img.src = url;
        img.classList.add("img");

        if (index === 0) {
            img.classList.add("active");
        }

        wrapper.appendChild(img);
        total.innerText = imgList.length;
    });
}

// 모달 닫기
item_detail_off.addEventListener("click", () => {
    item_detail_modal.classList.add("hidden");
});


const input = document.getElementById("file-upload");
const previewList = document.getElementById("preview-list");
const countText = document.querySelector(".current");
const deleteAllBtn = document.getElementById("delete-all");

let filesArr = [];

input.addEventListener("change", (e) => {
    const files = Array.from(e.target.files);

    if (filesArr.length + files.length > 5) {
        alert("최대 5개까지만 업로드 가능합니다.");
        return;
    }

    files.forEach(file => {
        if (!file.type.startsWith("image/")) {
            alert("이미지 파일만 업로드 가능합니다.");
            return;
        }

        filesArr.push(file);
        createThumbnail(file);
    });

    updateCount();
});

// 썸네일 기능
function createThumbnail(file) {
    const li = document.createElement("li");
    li.className = "thumb-item";

    const wrapper = document.createElement("div");
    wrapper.className = "thumb-wrapper";

    const img = document.createElement("img");
    img.src = URL.createObjectURL(file);
    img.className = "thumb-img";

    const delBtn = document.createElement("button");
    delBtn.innerHTML = "✕";
    delBtn.className = "thumb-delete";

    delBtn.addEventListener("click", () => {
        filesArr = filesArr.filter(f => f !== file);
        li.remove();
        updateCount();
    });

    wrapper.appendChild(img);
    wrapper.appendChild(delBtn);
    li.appendChild(wrapper);

    previewList.appendChild(li);
}

function updateCount() {
    countText.innerText = filesArr.length + "개";
}

deleteAllBtn.addEventListener("click", () => {
    filesArr = [];
    previewList.innerHTML = "";
    updateCount();
});


const dropArea = document.getElementById("drop-area");

// 드래그 중 스타일 방지
["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
    dropArea.addEventListener(eventName, e => {
        e.preventDefault();
        e.stopPropagation();
    });
});

// 드래그 들어왔을 때 스타일
dropArea.addEventListener("dragover", () => {
    dropArea.classList.add("drag-over");
});

dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("drag-over");
});

// 드롭했을 때
dropArea.addEventListener("drop", (e) => {
    dropArea.classList.remove("drag-over");

    const files = Array.from(e.dataTransfer.files);

    if (files.length === 0) return;

    if (filesArr.length + files.length > 5) {
        alert("최대 5개까지만 업로드 가능합니다.");
        return;
    }

    files.forEach(file => {
        if (!file.type.startsWith("image/")) {
            alert("이미지 파일만 가능합니다.");
            return;
        }

        filesArr.push(file);
        createThumbnail(file);
    });

    updateCount();
});


// carousel 기능
const total = document.getElementById("total");
const current = document.getElementById("current");
const next_btn = document.getElementById("next-btn");
const previous_btn = document.getElementById("previous_btn");

let img_count = 1;

// 🔥 캐러셀 이미지 전환 함수
function show_img(index) {
    const imgs = document.querySelectorAll(".img");

    imgs.forEach(img => img.classList.remove("active"));

    if (imgs[index - 1]) {
        imgs[index - 1].classList.add("active");
    }
}


// 🔥 다음 버튼
next_btn.addEventListener("click", () => {

    const imgs = document.querySelectorAll(".img");

    if (imgs.length === 0) return;

    img_count++;

    if (img_count > imgs.length) {
        img_count = 1;
    }

    current.innerText = img_count;
    show_img(img_count);
});


// 🔥 이전 버튼
previous_btn.addEventListener("click", () => {

    const imgs = document.querySelectorAll(".img");

    if (imgs.length === 0) return;

    img_count--;

    if (img_count < 1) {
        img_count = imgs.length;
    }

    current.innerText = img_count;
    show_img(img_count);
});
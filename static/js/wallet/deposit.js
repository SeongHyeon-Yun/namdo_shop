const user_input = document.getElementById('user_input');

function only_number(input) {
    // 숫자 아닌 거 제거
    let value = input.value.replace(/\D/g, "");

    // 빈 값 처리
    if (value === "") {
        input.value = "";
        return;
    }

    // 숫자로 변환 후 콤마
    input.value = Number(value).toLocaleString("ko-KR");
}

user_input.addEventListener('keyup', only_korea);

function only_korea() {
    var pattern = /[a-z0-9]|[ \[\]{}()<>?|`~!@#$%^&*-_+=,.;:\"'\\]/g;
    this.value = this.value.replace(pattern, '');
}
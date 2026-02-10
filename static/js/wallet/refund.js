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


const refundForm = document.getElementById("refundForm");
const refundBtn = document.getElementById("refundBtn");

refundBtn.addEventListener("click", () => {

    // 현재 보유 잔고
    let user_balance = document.getElementById('user_balance').innerText;
    user_balance = user_balance.replace(/[^0-9]/g, "");
    user_balance = Number(user_balance);
    // 환급 신청 금액
    let refund_value = document.getElementById('refund_value').value;
    refund_value = refund_value.replace(/[^0-9]/g, "")
    refund_value = Number(refund_value)


    if (user_balance >= refund_value) {
        if (confirm('환급을 신청하시겠습니까?')) {
            console.log(refundBtn);
            refundForm.submit();
        }
    } else {
        alert("보유 금액을 초과했습니다.");
    }
})
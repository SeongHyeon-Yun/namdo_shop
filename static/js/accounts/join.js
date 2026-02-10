const all_check = document.getElementById('all-check');
const check_1 = document.getElementById('check-1');
const check_2 = document.getElementById('check-2');
const joinBtn = document.getElementById('join-btn');

/* 전체 체크 → 개별 체크 */
all_check.addEventListener('change', () => {
    check_1.checked = all_check.checked;
    check_2.checked = all_check.checked;
});

/* 개별 체크 → 전체 체크 */
[check_1, check_2].forEach(check => {
    check.addEventListener('change', () => {
        all_check.checked = check_1.checked && check_2.checked;
    });
});


joinBtn.addEventListener("click", () => {
    if (!all_check.checked) {
        alert('약관 동의 체크해주세요.');
        return;
    }

    window.location.href = "/accounts/userJoin"

})
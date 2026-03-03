const msg_btn = document.getElementById("msg_btn")
const msg_modal = document.querySelectorAll(".msg_modal")
msg_btn.addEventListener("click", () => {
    msg_modal.forEach(e => {
        e.classList.add("hidden")
    });
})
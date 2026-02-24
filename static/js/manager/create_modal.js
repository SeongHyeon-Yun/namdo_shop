const modal_close_btn = document.getElementById("modal_close_btn");
const modal_area = document.getElementById("modal_area");

if (modal_close_btn && modal_area) {
    modal_close_btn.addEventListener("click", () => {
        modal_area.remove();
    });
}
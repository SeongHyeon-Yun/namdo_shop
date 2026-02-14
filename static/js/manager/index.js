const slider = document.querySelector('.top-menus');

let isDown = false;
let startX;
let scrollLeft;

slider.addEventListener('mousedown', (e) => {
  isDown = true;
  slider.classList.add('active');
  startX = e.pageX - slider.offsetLeft;
  scrollLeft = slider.scrollLeft;
});

slider.addEventListener('mouseleave', () => {
  isDown = false;
});

slider.addEventListener('mouseup', () => {
  isDown = false;
});

slider.addEventListener('mousemove', (e) => {
  if (!isDown) return;
  e.preventDefault();
  const x = e.pageX - slider.offsetLeft;
  const walk = (x - startX) * 1.2; // 드래그 감도
  slider.scrollLeft = scrollLeft - walk;
});

// ---------------- 차트 ----------------
const order_count_chart = document.getElementById('order_count');

new Chart(order_count_chart, {
  type: 'bar',
  data: {
    labels: ['1', '2', '3', '4', '5', '6', "7"],
    datasets: [{
      label: '#주문 건',
      data: [12, 19, 3, 5, 2, 3, 10],
      borderWidth: 1
    },
    {
      label: '#취소 건',
      data: [2, 1, 0, 1, 0, 1, 2],
      borderWidth: 1
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});

const order_value = document.getElementById('order_value');
new Chart(order_value, {
  type: 'line',
  data: {
    labels: ['1', '2', '3', '4', '5', '6', "7"],
    datasets: [{
      label: '#매출',
      data: [12, 19, 3, 5, 2, 3, 10],
      borderWidth: 1
    },
    {
      label: '#환불',
      data: [2, 3, 1, 1, 0, 2, 4],
      borderWidth: 1
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});
// ---------------- 차트 ----------------

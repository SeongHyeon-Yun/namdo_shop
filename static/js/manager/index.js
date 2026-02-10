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

flatpickr("#dateRange", {
  mode: "range",
  dateFormat: "d M",     // 내부 포맷
  locale: {
    rangeSeparator: " – "
  },
  onChange: function (selectedDates) {
    if (selectedDates.length === 2) {
      const options = { day: "2-digit", month: "short" };

      const start = selectedDates[0].toLocaleDateString("en-GB", options);
      const end = selectedDates[1].toLocaleDateString("en-GB", options);

      document.getElementById("dateRange").value = `${start} – ${end}`;
    }
  }
});


const ctx = document.getElementById('myChart');

new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    datasets: [{
      label: '# of Votes',
      data: [12, 19, 3, 5, 2, 3],
      borderWidth: 1
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});
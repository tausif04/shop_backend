// js/main.js
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize Lucide Icons
    lucide.createIcons();

    // --- Sidebar Toggle ---
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const wrapper = document.getElementById('wrapper');

    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            wrapper.classList.toggle('sidebar-toggled');
        });
    }

    // --- Chart.js Sales Chart ---
    let salesChart; // To hold the chart instance
    const salesChartCanvas = document.getElementById('salesChart');
    
    function createSalesChart(theme) {
        if (!salesChartCanvas) return;

        const ctx = salesChartCanvas.getContext('2d');
        
        // Destroy previous chart instance if it exists
        if (salesChart) {
            salesChart.destroy();
        }

        // Define colors based on the theme
        const isDark = theme === 'dark';
        const gridColor = isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';
        const textColor = isDark ? '#c9d1d9' : '#1f2937';
        const accentColor = isDark ? '#00f5d4' : '#2563eb';
        
        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, `${accentColor}4D`); // 30% opacity
        gradient.addColorStop(1, `${accentColor}00`); // 0% opacity

        salesChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
                datasets: [{
                    label: 'Sales',
                    data: [65, 59, 80, 81, 56, 55, 90],
                    fill: true,
                    backgroundColor: gradient,
                    borderColor: accentColor,
                    tension: 0.4,
                    pointBackgroundColor: accentColor,
                    pointBorderColor: '#fff',
                    pointHoverRadius: 7,
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: accentColor,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false,
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false,
                        },
                        ticks: {
                            color: textColor
                        }
                    },
                    y: {
                        grid: {
                            color: gridColor,
                            borderDash: [5, 5]
                        },
                        ticks: {
                            color: textColor,
                            callback: function(value) {
                                return '$' + value;
                            }
                        }
                    }
                }
            }
        });
    }

    // --- Theme Toggle ---
    const themeToggle = document.getElementById('theme-toggle');
    const htmlEl = document.documentElement;

    function updateThemeIcon(theme) {
        if (themeToggle) {
            const icon = theme === 'dark' ? 'sun' : 'moon';
            themeToggle.innerHTML = `<i data-lucide="${icon}"></i>`;
            lucide.createIcons();
        }
    }

    const savedTheme = localStorage.getItem('theme') || 'dark';
    htmlEl.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
    createSalesChart(savedTheme); // Create initial chart

    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = htmlEl.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            htmlEl.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
            createSalesChart(newTheme); // Re-create chart with new theme colors
        });
    }
});

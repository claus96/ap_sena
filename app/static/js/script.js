// Función para agregar ítems dinámicamente en el formulario de pedidos (/pedido)
function agregarItem() {
    let items = document.getElementById('items');
    if (!items) return; // Evitar errores si el elemento no existe
    let nuevoItem = items.firstElementChild.cloneNode(true);
    nuevoItem.querySelector('input').value = '';
    nuevoItem.querySelector('select').value = '';
    items.appendChild(nuevoItem);
}

// Función para inicializar el gráfico de stock en el dashboard
function inicializarGraficoStock(gelatinas, stocks) {
    const ctx = document.getElementById('stockChart');
    if (!ctx) return; // Evitar errores si el canvas no existe

    // Mapear nombres de gelatinas y cantidades de stock
    const nombres = gelatinas.map(gelatina => gelatina.nombre);
    const cantidades = gelatinas.map(gelatina => {
        const stock = stocks.find(s => s.id_gelatina === gelatina.id_gelatina);
        return stock ? stock.cantidad : 0;
    });

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: nombres,
            datasets: [{
                label: 'Stock Actual',
                data: cantidades,
                backgroundColor: 'rgba(40, 167, 69, 0.6)', // Verde con opacidad
                borderColor: 'rgba(40, 167, 69, 1)',
                borderWidth: 1,
                barThickness: 40, // Aumentar el grosor de las barras
                maxBarThickness: 50
            }]
        },
        options: {
            maintainAspectRatio: false, // Permitir que el gráfico se ajuste al contenedor
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Cantidad en Stock',
                        font: {
                            size: 14
                        }
                    },
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Gelatinas',
                        font: {
                            size: 14
                        }
                    },
                    ticks: {
                        font: {
                            size: 12
                        },
                        maxRotation: 45, // Rotar etiquetas para evitar solapamiento
                        minRotation: 45,
                        autoSkip: false
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        font: {
                            size: 14
                        }
                    }
                }
            }
        }
    });
}

// Ejecutar inicialización cuando la página esté lista
document.addEventListener('DOMContentLoaded', function() {
    console.log('Página inicializada');
    // Animación para tarjetas en la página de inicio
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transition = 'opacity 0.5s ease';
        setTimeout(() => {
            card.style.opacity = '1';
        }, index * 200);
    });
});
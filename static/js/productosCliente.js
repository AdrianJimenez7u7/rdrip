document.addEventListener('DOMContentLoaded', function () {
    const categorias = document.querySelectorAll('.list-group-item');
    const productos = document.querySelectorAll('.col-md-4');

    categorias.forEach(function (categoria) {
        categoria.addEventListener('click', function () {
            const categoriaSeleccionada = this.textContent.trim();

            productos.forEach(function (producto) {
                const categoriaProducto = producto.getAttribute('data-categoria');

                if (categoriaSeleccionada === 'Todas' || categoriaSeleccionada === categoriaProducto) {
                    producto.style.display = 'block';
                } else {
                    producto.style.display = 'none';
                }
            });
        });
    });
});

//esta madre es para cuando le des al boton de agregar carrito se envien los datos del producto
document.addEventListener('DOMContentLoaded', function () {
    var botonesAgregarCarrito = document.querySelectorAll('.btn-agregar-carrito');

    botonesAgregarCarrito.forEach(function (boton) {
        boton.addEventListener('click', function () {
            // Obtener datos del producto desde el botón
            var idProducto = this.getAttribute('data-id');
            var nombreProducto = this.getAttribute('data-nombre');
            var precioProducto = this.getAttribute('data-precio');

            // Enviar datos del producto al servidor (usando fetch o AJAX)
            fetch('/agregar_al_carrito', {
                method: 'POST',
                body: new URLSearchParams({
                    'idProducto': idProducto,
                    'nombreProducto': nombreProducto,
                    'precioProducto': precioProducto
                }),
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            })
                .then(response => response.json())
                .then(data => {
                    // Manejar la respuesta del servidor (puedes mostrar un mensaje, actualizar el carrito, etc.)
                    console.log(data);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var enlace = document.getElementById('enlace');
    var imagen = document.getElementById('iconoCarrito');

    imagen.addEventListener('click', function () {
        window.location.href = 'carrito';
    });
});
$(document).ready(function () {
    var mensajes = [
        "ENVIOS GRATIS EN TODA LA TIENDA",
        "UNETE A NUESTRA COMUNIDAD"
    ];

    var mensajeSuperior = $('#mensajeSuperior');

    function cambiarMensaje() {
        var indice = mensajes.indexOf(mensajeSuperior.text());
        indice = (indice + 1) % mensajes.length;
        mensajeSuperior.fadeOut(function () {
            $(this).text(mensajes[indice]).fadeIn();
        });
    }

    setInterval(cambiarMensaje, 7000);
});

$(document).ready(function () {
    $('#imagenPromocion').carousel();

    $('.carousel-control-prev').click(function () {
        $('#imagenPromocion').carousel('prev');
    });

    $('.carousel-control-next').click(function () {
        $('#imagenPromocion').carousel('next');
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const marcas = document.querySelectorAll('.marca');

    marcas.forEach(function (marca) {
        marca.addEventListener('mouseover', function () {
            this.style.backgroundColor = '#f0f0f0';
        });

        marca.addEventListener('mouseout', function () {
            this.style.backgroundColor = '#fff';
        });
    });
});






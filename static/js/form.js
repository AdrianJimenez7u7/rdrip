function validarTarjetaLength(input) {
    var maxLength = 16; // Cambia esto al valor máximo permitido
    if (input.value.length > maxLength) {
        input.value = input.value.slice(0, maxLength);
    }
}


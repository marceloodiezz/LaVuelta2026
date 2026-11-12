"use strict";

class Formulario {

    constructor() {
        this.puntuacion = 0;
        this.dureza = null;
        this.descripcion = "";
        this.usuario = "";

        const boton = document.querySelector('form button[type="submit"]');

        boton.addEventListener("click", (event) => {
            this.analizar(event);
        });
    }

    analizar(event) {
        event.preventDefault();

        const form = event.target.closest("form");

        this.puntuacion = 0;

        // Pregunta 1: Número de etapa
        const numero = form.querySelector('input[name="numero-etapa"]');
        if (numero.value === "10")
            this.puntuacion++;

        // Pregunta 2: Fecha
        const fecha = form.querySelector('input[name="fecha-etapa"]');
        if (fecha.value === "2026-09-01")
            this.puntuacion++;

        // Pregunta 3: Lugar de salida
        const salida = form.querySelector('select[name="salida-etapa"]');
        if (salida.value === "alcaraz")
            this.puntuacion++;

        // Pregunta 4: Lugar de llegada
        const llegada = form.querySelector('select[name="llegada-etapa"]');
        if (llegada.value === "elche-de-la-sierra")
            this.puntuacion++;

        // Pregunta 5: Tipo de etapa
        const tipo = form.querySelector('input[name="tipo-etapa"]:checked');
        if (tipo && tipo.value === "ondulada")
            this.puntuacion++;

        // Pregunta 6: Hitos de la etapa
        const puerto = form.querySelector('input[name="hito-puerto-montana"]').checked;
        const especial = form.querySelector('input[name="hito-puerto-especial"]').checked;
        const sprint = form.querySelector('input[name="hito-sprint-intermedio"]').checked;
        const bonificado = form.querySelector('input[name="hito-sprint-bonificado"]').checked;
        const sinHitos = form.querySelector('input[name="hito-sin-hitos"]').checked;
        if (puerto && !especial && sprint && bonificado && !sinHitos)
            this.puntuacion++;

        // Pregunta 7: Dureza (no puntúa)
        this.dureza = form.querySelector('input[name="dificultad-etapa"]').value;

        // Pregunta 8: Longitud
        const longitud = form.querySelector('input[name="longitud-etapa"]');
        if (longitud.value !== "" && Number(longitud.value) === 184.7)
            this.puntuacion++;

        // Pregunta 9: Desnivel acumulado
        const desnivel = form.querySelector('input[name="desnivel-etapa"]');
        if (desnivel.value !== "" && Number(desnivel.value) === 2991)
            this.puntuacion++;

        // Pregunta 10: Descripción (no puntúa)
        this.descripcion = form.querySelector('textarea[name="descripcion-etapa"]').value;

        // Nombre del participante (no puntúa)
        this.usuario = form.querySelector('input[name="nombre-participante"]').value;

        this.calificar();
    }

    calificar() {
        let parrafo = document.querySelector("#resultado-formulario");

        if (!parrafo) {
            parrafo = document.createElement("p");
            parrafo.id = "resultado-formulario";

            const form = document.querySelector("main form");
            form.insertAdjacentElement("afterend", parrafo);
        }

        parrafo.textContent = this.usuario + ", has obtenido " +
            this.puntuacion + " puntos, la dureza que has asignado a la etapa es " +
            this.dureza + " y tu descripción es: " + this.descripcion;
    }

}

const formulario = new Formulario();
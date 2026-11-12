"use strict";

class Menu {

    constructor() {
        this.boton = document.querySelector("header > button");
        this.menu = document.querySelector("header > nav");

        this.boton.addEventListener("click", () => {
            this.desplegar();
        });
    }

    desplegar() {
        const abierto = this.menu.classList.toggle("abierto");

        if (abierto) {
            this.boton.textContent = "x";
            this.boton.setAttribute("aria-expanded", "true");
        }
        else {
            this.boton.textContent = "☰";
            this.boton.setAttribute("aria-expanded", "false");
        }
    }

}

const menu = new Menu();

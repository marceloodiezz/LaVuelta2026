"use strict";

class Ciudad {

    constructor(nombre, pais, gentilicio) {
        this.nombre = nombre;
        this.pais = pais;
        this.gentilicio = gentilicio;

        this.poblacion = null;
        this.longitud = null;
        this.latitud = null;
    }

    rellenarAtributos() {
        this.poblacion = 1283;
        this.longitud = -2.4926058;
        this.latitud = 38.6701929;
    }

    getCiudad() {
        return this.nombre;
    }

    getPais() {
        return this.pais;
    }

    getInformacionSecundaria() {
        return "<ul>" + 
                    "<li>Gentilicio: " + this.gentilicio + "</li>" +
                    "<li>Población: " + this.poblacion + " habitantes</li>" +
                "</ul>";
    }

    escribeCoordenadas() {
        const seccion = document.querySelector("main > section");

        const parrafo = document.createElement("p");
        parrafo.textContent = "Coordenadas: " + this.latitud + "°, " + Math.abs(this.longitud) + "°";

        seccion.appendChild(parrafo);
    }

}

const alcaraz = new Ciudad("Alcaraz", "España", "alcaraceño");
alcaraz.rellenarAtributos();

const seccion = document.createElement("section");

const titulo = document.createElement("h3");
titulo.textContent = alcaraz.getCiudad() + " (" + alcaraz.getPais() + ")";
seccion.appendChild(titulo);

seccion.insertAdjacentHTML("beforeend", alcaraz.getInformacionSecundaria());

const encabezado = document.querySelector("main > h2");
encabezado.insertAdjacentElement("afterend", seccion);

alcaraz.escribeCoordenadas();
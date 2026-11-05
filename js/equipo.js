"use strict";

class Equipo {

    constructor(nombre, codigoUCI, pais) {
        this.nombre = nombre;
        this.codigoUCI = codigoUCI;
        this.pais = pais;

        this.director = null;
        this.categoria = null;
        this.paginaWeb = null;
    }

    rellenarAtributos() {
        this.director = "Damien García";
        this.categoria = "UCI ProTeam";
        this.paginaWeb = "https://www.lavuelta.es/es/equipo/BBH/burgos-burpellet-bh";
    }

    datosBasicos() {
        return this.nombre + " (" + this.codigoUCI + ")";
    }

    getPais() {
        return this.pais;
    }

    getInformacionSecundaria() {
        return "<ul>" + 
                    "<li>Director: " + this.director + "</li>" +
                    "<li>Categoría: " + this.categoria + "</li>" +
                "</ul>";
    }

    getPaginaWeb() {
        const seccion = document.querySelector("main > section");

        const parrafo = document.createElement("p");
        const enlace = document.createElement("a");

        enlace.href = this.paginaWeb;
        enlace.textContent = "Ficha del equipo en La Vuelta";

        parrafo.appendChild(enlace);
        seccion.appendChild(parrafo);
    }

}

const burgos = new Equipo("Burgos Burpellet BH", "BBH", "España");
burgos.rellenarAtributos();

const seccion = document.createElement("section");

const titulo = document.createElement("h3");
titulo.textContent = burgos.datosBasicos() + " - " + burgos.getPais();
seccion.appendChild(titulo);

seccion.insertAdjacentHTML("beforeend", burgos.getInformacionSecundaria());

const encabezado = document.querySelector("main > h2");
encabezado.insertAdjacentElement("afterend", seccion);

burgos.getPaginaWeb();
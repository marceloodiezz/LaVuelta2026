"use strict";

class Ciclista {

    constructor(dorsal, nacionalidad, nacionalidadCodigo, nombre, apellidos, fechaNacimiento) {
        this.dorsal = dorsal;
        this.nacionalidad = nacionalidad;
        this.nacionalidadCodigo = nacionalidadCodigo;
        this.nombre = nombre;
        this.apellidos = apellidos;
        this.fechaNacimiento = fechaNacimiento;
    }

    getNombreCompleto() {
        return this.nombre + " – " + this.apellidos;
    }

    getDorsal() {
        return this.dorsal;
    }

    getInformacionAdicional() {
        return this.fechaNacimiento + " - " + this.nacionalidad;
    }

}

class Equipo {

    constructor(nombre, codigoUCI, pais) {
        this.nombre = nombre;
        this.codigoUCI = codigoUCI;
        this.pais = pais;

        this.director = null;
        this.categoria = null;
        this.paginaWeb = null;

        this.alineacion = [];
    }

    rellenarAtributos() {
        this.director = "Damien García";
        this.categoria = "UCI ProTeam";
        this.paginaWeb = "https://www.lavuelta.es/es/equipo/BBH/burgos-burpellet-bh";
    }

    async leerEquipo() {
        try {
            const respuesta = await fetch("js/lavuelta.json");

            if (!respuesta.ok)
                throw new Error("Error al leer el fichero JSON");

            const datos = await respuesta.json();
            const equipo = datos.equipos.find(equipo => equipo.codigo_uci === this.codigoUCI);

            if (equipo)
                this.alinearCiclistas(equipo.corredores);
        }
        catch (error) {
            console.error("Error al obtener la información del equipo:", error);
        }
    }

    alinearCiclistas(corredores) {
        corredores.forEach(corredor => {
            const ciclista = new Ciclista(
                corredor.dorsal,
                corredor.nacionalidad,
                corredor.nacionalidad_codigo,
                corredor.nombre,
                corredor.apellidos,
                corredor.fecha_nacimiento
            );

            this.alineacion.push(ciclista);
        });
    }


    mostrarAlineacion() {
        const seccion = document.querySelector("main > section:last-of-type");

        this.alineacion.sort((a, b) => a.getDorsal() - b.getDorsal());

        this.alineacion.forEach(ciclista => {
            const articulo = document.createElement("article");

            const titulo = document.createElement("h4");
            titulo.textContent = ciclista.getNombreCompleto();
            articulo.appendChild(titulo);

            const imagen = document.createElement("img");
            imagen.src = "multimedia/ciclista.png";
            imagen.alt = "Icono genérico de un ciclista";
            imagen.width = 128;
            imagen.height = 128;
            articulo.appendChild(imagen);

            const dorsal = document.createElement("p");
            dorsal.textContent = ciclista.getDorsal();
            articulo.appendChild(dorsal);

            const informacion = document.createElement("p");
            informacion.textContent = ciclista.getInformacionAdicional();
            articulo.appendChild(informacion);

            seccion.appendChild(articulo);
        });
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

burgos.leerEquipo().then(() => burgos.mostrarAlineacion());
"use strict";

class Buscador {

    constructor() {
        const imagen = document.querySelector("search label img");
        const input = document.querySelector('search input[type="search"]');

        imagen.addEventListener("click", this.buscar.bind(this));

        input.addEventListener("keypress", (event) => {
            if (event.key === "Enter")
                this.buscar();
        });
    }

    buscar() {
        this.limpiar_busqueda();

        const resultados = [];
        const texto = document.querySelector('search input[type="search"]').value.trim();

        if (texto === "")
            return;

        // Expresión regular
        const busqueda = texto.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
        const regexp = new RegExp(busqueda, "gi");

        // Obtener nodos de texto
        const walker = document.createTreeWalker(
            document.querySelector("body"),
            NodeFilter.SHOW_TEXT
        );

        let nodo = walker.nextNode();

        // Buscar coincidencias
        while (nodo) {
            const padre = nodo.parentElement;

            if (padre && !padre.closest("script, style, search, mark")) {
                regexp.lastIndex = 0;

                if (regexp.test(nodo.textContent))
                    resultados.push(nodo);
            }

            nodo = walker.nextNode();
        }

        // Resaltar coincidencias
        resultados.forEach(nodo => {
            const fragmento = document.createDocumentFragment();
            const textoOriginal = nodo.textContent;

            regexp.lastIndex = 0;
            let inicio = 0;

            for (const coincidencia of textoOriginal.matchAll(regexp)) {
                fragmento.appendChild(
                    document.createTextNode(textoOriginal.slice(inicio, coincidencia.index))
                );

                const marca = document.createElement("mark");
                marca.textContent = coincidencia[0];
                fragmento.appendChild(marca);

                inicio = coincidencia.index + coincidencia[0].length;
            }

            fragmento.appendChild(
                document.createTextNode(textoOriginal.slice(inicio))
            );

            nodo.replaceWith(fragmento);
        });
    }

    limpiar_busqueda() {
        const marcas = document.querySelectorAll("mark");

        marcas.forEach(marca => {
            const texto = document.createTextNode(marca.textContent);
            marca.replaceWith(texto);
        });

        document.body.normalize();
    }

}

const buscador = new Buscador();
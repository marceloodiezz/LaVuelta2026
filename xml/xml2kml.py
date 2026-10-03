# -*- coding: utf-8 -*-

"""
Genera el archivo etapa.kml a partir de etapaEsquema.xml.

Se utilizan expresiones XPath para obtener los datos del XML.
El programa está implementado mediante programación orientada a objetos.
"""

import xml.etree.ElementTree as ET


class Xml2Kml:

    def __init__(self, archivo_xml, archivo_kml):
        """
        Carga el archivo XML y crea la estructura inicial del KML.
        """

        self.archivo_xml = archivo_xml
        self.archivo_kml = archivo_kml

        # Espacio de nombres utilizado por etapaEsquema.xml
        self.ns = {
            "u": "http://www.uniovi.es"
        }

        # Leer etapaEsquema.xml y construir el árbol DOM
        try:
            self.arbol = ET.parse(self.archivo_xml)
            self.raiz_xml = self.arbol.getroot()

        except IOError:
            print("No se encuentra el archivo", self.archivo_xml)
            raise

        except ET.ParseError:
            print("Error procesando el archivo XML", self.archivo_xml)
            raise

        # Crear el árbol KML
        self.raiz_kml = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")

        self.documento = ET.SubElement(self.raiz_kml, "Document")

        ET.SubElement(self.documento, "name").text = "Etapa 10 - Alcaraz a Elche de la Sierra"

        self.crearEstilos()


    def crearEstiloPunto(self, identificador, color):
        """
        Crea un estilo para los puntos del mapa.
        """

        estilo = ET.SubElement(self.documento, "Style", id=identificador)

        icon_style = ET.SubElement(estilo, "IconStyle")

        ET.SubElement(icon_style, "color").text = color

        ET.SubElement(icon_style, "scale").text = "1.1"

        icono = ET.SubElement(icon_style, "Icon")

        ET.SubElement(icono, "href").text = ("http://maps.google.com/mapfiles/kml/" "shapes/placemark_circle.png")


    def crearEstilos(self):
        """
        Crea los estilos requeridos para la práctica.
        """

        # Rojo
        self.crearEstiloPunto("salidaMeta", "ff0e27ed")

        # Verde
        self.crearEstiloPunto("puerto", "ff2bc430")

        # Azul
        self.crearEstiloPunto("sprint", "ffedc52f")

        # Amarillo
        self.crearEstiloPunto("anonimo", "ff00e6ff")

        # Estilo de la línea de recorrido
        estilo = ET.SubElement(self.documento, "Style", id="ruta")

        linea = ET.SubElement(estilo, "LineStyle")

        ET.SubElement(linea, "color").text = "ff0000ff"

        ET.SubElement(linea, "width").text = "4"


    def obtenerCoordenadas(self, nodo):
        """
        Obtiene longitud, latitud y altitud de un nodo utilizando expresiones XPath.
        """

        longitud = nodo.find("u:coordenadas/u:longitudGeografica", self.ns).text

        latitud = nodo.find("u:coordenadas/u:latitudGeografica", self.ns).text

        altitud = nodo.find("u:coordenadas/u:altitud", self.ns).text

        return longitud, latitud, altitud


    def addPlacemark(self, nombre, descripcion, longitud, latitud, altitud, estilo):
        """
        Añade un punto al documento KML.
        """

        placemark = ET.SubElement(self.documento, "Placemark")

        ET.SubElement(placemark, "name").text = nombre

        ET.SubElement(placemark, "description").text = descripcion

        ET.SubElement(placemark, "styleUrl").text = "#" + estilo

        punto = ET.SubElement(placemark, "Point")

        ET.SubElement(punto, "coordinates").text = "{},{},{}".format(longitud, latitud, altitud)

        ET.SubElement(punto, "altitudeMode").text = "absolute"


    def addLineString(self, nombre, coordenadas):
        """
        Añade la línea que representa el recorrido de la etapa.
        """

        placemark = ET.SubElement(self.documento, "Placemark")

        ET.SubElement(placemark, "name").text = nombre

        ET.SubElement(placemark, "styleUrl").text = "#ruta"

        linea = ET.SubElement(placemark, "LineString")

        ET.SubElement(linea, "extrude").text = "0"

        ET.SubElement(linea, "tessellate").text = "1"

        ET.SubElement(linea, "coordinates").text = coordenadas

        ET.SubElement(linea, "altitudeMode").text = "absolute"


    def generarSalidaMeta(self):
        """
        Añade salida y meta en color rojo.
        """

        # XPath: salida
        salida = self.raiz_xml.find("u:salida", self.ns)

        nombre_salida = salida.find("u:lugar", self.ns).text

        longitud, latitud, altitud = self.obtenerCoordenadas(salida)

        self.addPlacemark("Salida - " + nombre_salida, "Salida de la etapa", longitud, latitud, altitud, "salidaMeta")

        # XPath: meta
        meta = self.raiz_xml.find("u:meta", self.ns)

        nombre_meta = meta.find("u:lugar", self.ns).text

        longitud, latitud, altitud = self.obtenerCoordenadas(meta)

        self.addPlacemark("Meta - " + nombre_meta, "Meta de la etapa", longitud, latitud, altitud, "salidaMeta")


    def generarPuertos(self):
        """
        Añade los puertos de montaña en color verde.
        """

        # Expresión XPath
        puertos = self.raiz_xml.findall("u:hitos/u:puerto", self.ns)

        for puerto in puertos:

            nombre = puerto.find("u:nombreHito", self.ns).text

            categoria = puerto.get("categoria")

            distancia = puerto.find("u:distancia", self.ns).text

            longitud, latitud, altitud = self.obtenerCoordenadas(puerto)

            descripcion = ("Puerto de categoría " + categoria + " - km " + distancia)

            self.addPlacemark(nombre, descripcion, longitud, latitud, altitud, "puerto")


    def generarSprints(self):
        """
        Añade los sprint intermedios en color azul.
        """

        # Expresión XPath con filtro por atributo
        sprints = self.raiz_xml.findall("u:hitos/u:sprint[@tipo='intermedio']", self.ns)

        for sprint in sprints:

            nombre = sprint.find("u:nombreHito", self.ns).text

            distancia = sprint.find("u:distancia", self.ns).text

            longitud, latitud, altitud = self.obtenerCoordenadas(sprint)

            self.addPlacemark("Sprint - " + nombre, "Sprint intermedio - km " + distancia, longitud, latitud, altitud, "sprint")


    def generarPuntosAnonimos(self):
        """
        Añade en amarillo los puntos normales del trazado.

        Los puntos especiales (salida, meta, puertos y sprint) también pertenecen al trazado,
        pero no se pintan de amarillo porque ya tienen su marcador específico.
        """

        # XPath: todos los puntos del trazado
        puntos = self.raiz_xml.findall("u:trazado/u:punto", self.ns)

        # Coordenadas de los puntos que tienen un marcador especial
        especiales = set()

        # Salida
        salida = self.raiz_xml.find("u:salida", self.ns)
        especiales.add(self.obtenerCoordenadas(salida))

        # Meta
        meta = self.raiz_xml.find("u:meta", self.ns)
        especiales.add(self.obtenerCoordenadas(meta))

        # Puertos
        puertos = self.raiz_xml.findall("u:hitos/u:puerto", self.ns)

        for puerto in puertos:
            especiales.add(self.obtenerCoordenadas(puerto))

        # Sprint intermedio
        sprints = self.raiz_xml.findall("u:hitos/u:sprint[@tipo='intermedio']", self.ns)

        for sprint in sprints:
            especiales.add(self.obtenerCoordenadas(sprint))

        numero = 1

        for punto in puntos:

            longitud, latitud, altitud = self.obtenerCoordenadas(punto)

            coordenadas = (longitud, latitud, altitud)

            # Si ya es un punto especial, tendrá su propio color
            if coordenadas in especiales:
                continue

            distancia = punto.find("u:distancia", self.ns).text

            nombre = punto.find("u:nombrePunto", self.ns)

            # Un punto amarillo puede tener nombre o no
            if nombre is not None:
                nombre_punto = nombre.text
            else:
                nombre_punto = "Punto " + str(numero)

            self.addPlacemark(nombre_punto, "Punto del recorrido - km " + distancia, longitud, latitud, altitud, "anonimo")

            numero += 1


    def generarTrazado(self):
        """
        Genera la línea completa de la etapa.
        """

        # XPath: todos los puntos del recorrido
        puntos = self.raiz_xml.findall("u:trazado/u:punto", self.ns)

        coordenadas = []

        for punto in puntos:

            longitud, latitud, altitud = self.obtenerCoordenadas(punto)

            coordenadas.append("{},{},{}".format(longitud, latitud, altitud))

        lista_coordenadas = "\n".join(coordenadas)

        self.addLineString("Recorrido de la etapa", lista_coordenadas)


    def escribir(self):
        """
        Escribe el árbol KML en etapa.kml.
        """

        arbol_kml = ET.ElementTree(self.raiz_kml)

        ET.indent(arbol_kml, space="    ")

        arbol_kml.write(self.archivo_kml, encoding="UTF-8", xml_declaration=True)


    def generar(self):
        """
        Genera todos los elementos del KML.
        """

        self.generarTrazado()
        self.generarSalidaMeta()
        self.generarPuertos()
        self.generarSprints()
        self.generarPuntosAnonimos()

        self.escribir()


    @staticmethod
    def main():
        """
        Ejecuta el programa.
        """

        generador = Xml2Kml("etapaEsquema.xml", "etapa.kml")

        generador.generar()

        print("Creado el archivo etapa.kml")


if __name__ == "__main__":
    Xml2Kml.main()
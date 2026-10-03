# -*- coding: utf-8 -*-

"""
Genera el archivo altimetria.svg a partir de etapaEsquema.xml.

Se utilizan expresiones XPath para obtener los datos del XML.
El programa está implementado mediante programación orientada a objetos.
"""

import math
import xml.etree.ElementTree as ET


class Xml2Altimetria:

    def __init__(self, archivo_xml, archivo_svg):
        """
        Carga el XML y crea la estructura inicial del SVG.
        """

        self.archivo_xml = archivo_xml
        self.archivo_svg = archivo_svg

        # Namespace de etapaEsquema.xml
        self.ns = {
            "u": "http://www.uniovi.es"
        }

        # Dimensiones del SVG
        self.ancho = 1200
        self.alto = 750

        # Zona destinada al perfil
        self.x_izquierda = 100
        self.x_derecha = 1100
        self.y_superior = 300
        self.y_inferior = 580

        # Leer el XML
        try:
            self.arbol = ET.parse(self.archivo_xml)
            self.raiz_xml = self.arbol.getroot()

        except IOError:
            print("No se encuentra el archivo", self.archivo_xml)
            raise

        except ET.ParseError:
            print("Error procesando el archivo XML", self.archivo_xml)
            raise

        # Crear el SVG
        self.raiz_svg = ET.Element("svg",
            {
                "xmlns": "http://www.w3.org/2000/svg",
                "version": "2.0",
                "width": str(self.ancho),
                "height": str(self.alto),
                "viewBox": "0 0 {} {}".format(self.ancho, self.alto)
            }
        )

        # Obtener datos del XML
        self.puntos = self.obtenerPuntos()

        self.distancia_total = float(self.raiz_xml.find("u:longitud", self.ns).text)

        self.desnivel = self.raiz_xml.find("u:desnivel",self.ns).text

        # Calcular límites verticales automáticamente
        altitudes = [
            punto["altitud"]
            for punto in self.puntos
        ]

        self.altitud_minima = 0

        self.altitud_maxima = (math.ceil(max(altitudes) / 200) * 200)


    def addLine(self, x1, y1, x2, y2, color="#000000", ancho="1"):
        """
        Añade una línea al SVG.
        """

        ET.SubElement(self.raiz_svg, "line",
            {
                "x1": str(x1),
                "y1": str(y1),
                "x2": str(x2),
                "y2": str(y2),
                "stroke": color,
                "stroke-width": str(ancho)
            }
        )


    def addText(self, texto, x, y, tamano="14", color="#000000", peso="normal", ancla="middle", transformacion=None):
        """
        Añade texto al SVG.
        """

        atributos = {
            "x": str(x),
            "y": str(y),
            "font-family": "Arial, sans-serif",
            "font-size": str(tamano),
            "fill": color,
            "font-weight": peso,
            "text-anchor": ancla
        }

        if transformacion is not None:
            atributos["transform"] = transformacion

        ET.SubElement(self.raiz_svg, "text", atributos).text = texto


    def addCircle(self, cx, cy, radio, color):
        """
        Añade un círculo al SVG.
        """

        ET.SubElement(self.raiz_svg, "circle",
            {
                "cx": str(cx),
                "cy": str(cy),
                "r": str(radio),
                "fill": color
            }
        )


    def addPolyline(self, puntos, color_borde, ancho_borde, color_relleno, opacidad_relleno="0.75"):
        """
        Añade una polilínea al SVG.
        """

        ET.SubElement(self.raiz_svg, "polyline",
            {
                "points": puntos,
                "stroke": color_borde,
                "stroke-width": str(ancho_borde),
                "fill": color_relleno,
                "fill-opacity": str(opacidad_relleno),
                "stroke-linejoin": "round"
            }
        )


    def obtenerPuntos(self):
        """
        Obtiene mediante XPath todos los puntos del trazado, junto con su distancia y altitud.
        """

        puntos_xml = self.raiz_xml.findall("u:trazado/u:punto", self.ns)

        puntos = []

        for punto in puntos_xml:

            distancia = float(punto.find("u:distancia", self.ns).text)

            altitud = float(punto.find("u:coordenadas/u:altitud", self.ns).text)

            nombre_xml = punto.find("u:nombrePunto", self.ns)

            if nombre_xml is not None:
                nombre = nombre_xml.text
            else:
                nombre = None

            puntos.append(
                {
                    "distancia": distancia,
                    "altitud": altitud,
                    "nombre": nombre
                }
            )

        return puntos


    def obtenerHitos(self):
        """
        Obtiene salida, meta, puertos y sprint intermedio mediante expresiones XPath.
        """

        hitos = []

        # Salida
        salida = self.raiz_xml.find("u:salida", self.ns)

        hitos.append(
            {
                "nombre": salida.find("u:lugar", self.ns).text,
                "distancia": 0.0,
                "altitud": float(salida.find("u:coordenadas/u:altitud", self.ns).text),
                "tipo": "salida"
            }
        )

        # Puertos
        puertos = self.raiz_xml.findall("u:hitos/u:puerto", self.ns)

        for puerto in puertos:

            hitos.append(
                {
                    "nombre": puerto.find("u:nombreHito", self.ns).text,
                    "distancia": float(puerto.find("u:distancia", self.ns).text),
                    "altitud": float(puerto.find("u:coordenadas/u:altitud", self.ns).text),
                    "tipo": "puerto"
                }
            )

        # Sprint intermedio
        sprints = self.raiz_xml.findall("u:hitos/u:sprint[@tipo='intermedio']", self.ns)

        for sprint in sprints:

            hitos.append(
                {
                    "nombre": sprint.find("u:nombreHito", self.ns).text,
                    "distancia": float(sprint.find( "u:distancia", self.ns).text),
                    "altitud": float(sprint.find("u:coordenadas/u:altitud", self.ns).text),
                    "tipo": "sprint"
                }
            )

        # Meta
        meta = self.raiz_xml.find("u:meta", self.ns)

        hitos.append(
            {
                "nombre": meta.find("u:lugar",self.ns).text,
                "distancia": self.distancia_total,
                "altitud": float(meta.find("u:coordenadas/u:altitud", self.ns).text),
                "tipo": "meta"
            }
        )

        return hitos


    def convertirX(self, distancia):
        """
        Convierte una distancia en kilómetros a una coordenada X del SVG.
        """

        ancho_grafica = (self.x_derecha - self.x_izquierda)

        return (self.x_izquierda + distancia / self.distancia_total * ancho_grafica)


    def convertirY(self, altitud):
        """
        Convierte una altitud en metros a una coordenada Y del SVG.
        """

        alto_grafica = (self.y_inferior - self.y_superior)

        proporcion = ((altitud - self.altitud_minima) / (self.altitud_maxima - self.altitud_minima))

        # El eje Y del SVG crece hacia abajo
        return (self.y_inferior - proporcion * alto_grafica
        )


    def dibujarTitulo(self):
        """
        Añade el título del gráfico.
        """

        nombre = self.raiz_xml.find("u:nombre", self.ns).text

        numero = self.raiz_xml.find("u:numero", self.ns).text

        self.addText("Etapa {} - {}".format(numero, nombre), self.ancho / 2, 35, "24", "#000000", "bold")


    def dibujarEscalaVertical(self):
        """
        Dibuja las líneas horizontales y los valores de altitud.
        """

        altitud = int(self.altitud_minima)

        while altitud <= self.altitud_maxima:

            y = self.convertirY(altitud)

            # Línea horizontal
            self.addLine(self.x_izquierda, y, self.x_derecha, y, "#D0D0D0", "1")

            # Número de altitud
            self.addText(str(altitud), self.x_izquierda - 12, y + 5, "12", "#444444", "normal", "end")

            altitud += 200

        # Unidad
        self.addText("Altitud (m)", 30, (self.y_superior + self.y_inferior) / 2, "14", "#000000", "bold", "middle",
            "rotate(-90 30 {})".format(
                (self.y_superior + self.y_inferior) / 2
            )
        )


    def dibujarEscalaHorizontal(self):
        """
        Dibuja solamente la línea del eje X y su título.
        No se dibujan marcas intermedias, ya que se dejan solo las de los hitos.
        """

        self.addLine(self.x_izquierda, self.y_inferior, self.x_derecha, self.y_inferior, "#000000", "1")

        self.addText("Distancia (km)", self.ancho / 2, self.y_inferior + 55, "14", "#000000", "bold")


    def dibujarPerfil(self):
        """
        Dibuja el perfil altimétrico usando todos los puntos del trazado.
        """

        puntos_perfil = []

        for punto in self.puntos:

            x = self.convertirX(punto["distancia"])

            y = self.convertirY(punto["altitud"])

            puntos_perfil.append("{:.2f},{:.2f}".format(x, y))

        # Cerrar la polilínea contra el suelo
        x_inicio = self.convertirX(self.puntos[0]["distancia"])

        x_final = self.convertirX(self.puntos[-1]["distancia"])

        puntos_cerrados = ["{:.2f},{:.2f}".format(x_inicio, self.y_inferior)]

        puntos_cerrados.extend(puntos_perfil)

        puntos_cerrados.append("{:.2f},{:.2f}".format(x_final, self.y_inferior))

        puntos_cerrados.append("{:.2f},{:.2f}".format(x_inicio, self.y_inferior))

        self.addPolyline(" ".join(puntos_cerrados), "#C41E0B", "2", "#ED270E", "0.65")


    def colorHito(self, tipo):
        """
        Devuelve el color correspondiente al tipo de hito.
        """

        if tipo == "puerto":
            return "#30C42B"

        if tipo == "sprint":
            return "#2FC5ED"

        return "#ED270E"


    def letraHito(self, tipo):
        """
        Devuelve la letra que aparecerá dentro del marcador.
        """

        if tipo == "puerto":
            return "P"

        if tipo == "sprint":
            return "S"

        if tipo == "salida":
            return "S"

        return "M"


    def dibujarHitos(self):
        """
        Representa salida, meta, puertos y sprint.
        """

        hitos = self.obtenerHitos()

        for hito in hitos:

            x = self.convertirX(hito["distancia"])
            color = self.colorHito(hito["tipo"])

            y_marcador = 250

            # Línea vertical desde el marcador hasta el eje X
            self.addLine(x, y_marcador + 17, x, self.y_inferior, "#666666", "1")

            # Marcador circular
            self.addCircle(x, y_marcador, 17, color)

            # Letra dentro del marcador
            self.addText(self.letraHito(hito["tipo"]), x, y_marcador + 6, "16", "#FFFFFF", "bold")

            # Texto vertical con nombre y altitud
            texto = "{} / {} m".format(hito["nombre"], int(hito["altitud"]))

            self.addText(texto, x + 6, y_marcador - 28, "14", "#222222", "bold", "start",
                "rotate(-90 {} {})".format(
                    x + 6,
                    y_marcador - 28
                )
            )

            # Distancia del hito debajo del eje X
            self.addText("{:g}".format(hito["distancia"]), x, self.y_inferior + 28, "12", "#000000", "bold")


    def dibujarDesnivel(self):
        """
        Añade el desnivel positivo total.
        """

        self.addText("Desnivel positivo: {} m".format(self.desnivel), self.ancho / 2, self.y_inferior + 110, "20", "#000000", "bold")


    def escribir(self):
        """
        Escribe el documento SVG.
        """

        arbol_svg = ET.ElementTree(self.raiz_svg)

        ET.indent(arbol_svg, space="    ")

        arbol_svg.write(self.archivo_svg, encoding="UTF-8", xml_declaration=True)


    def generar(self):
        """
        Genera la altimetría completa.
        """

        self.dibujarTitulo()

        # Primero las escalas, para que queden detrás
        self.dibujarEscalaVertical()
        self.dibujarEscalaHorizontal()

        # Después el perfil
        self.dibujarPerfil()

        # Por último los hitos
        self.dibujarHitos()

        self.dibujarDesnivel()

        self.escribir()


    @staticmethod
    def main():
        """
        Ejecuta el programa.
        """

        generador = Xml2Altimetria("etapaEsquema.xml", "altimetria.svg")

        generador.generar()

        print("Creado el archivo altimetria.svg")


if __name__ == "__main__":
    Xml2Altimetria.main()
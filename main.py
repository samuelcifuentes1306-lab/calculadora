import flet as ft

LIMITE = 100


def sumar(a, b):
    return a + b


def restar(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    if b == 0:
        return "Error"
    return a / b


def sumatoria(n):
    if n == 0:
        return 0
    return n + sumatoria(n - 1)


def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)


def potencia(base, exponente):
    if exponente == 0:
        return 1
    return base * potencia(base, exponente - 1)


def es_entero_valido(n):
    return n == int(n) and n >= 0 and n <= LIMITE


def formatear(numero):
    if numero == "Error":
        return "Error"
    if numero > 1e100 or numero < -1e100:
        return "Error"
    numero = round(numero, 8)
    if numero == int(numero):
        return str(int(numero))
    return str(numero)


def operar(operador, a, b):
    if operador == "+":
        return sumar(a, b)
    if operador == "-":
        return restar(a, b)
    if operador == "*":
        return multiplicar(a, b)
    if operador == "/":
        return dividir(a, b)
    if operador == "^":
        if es_entero_valido(b):
            return potencia(a, int(b))
        return "Error"
    return "Error"


def tamano_texto(texto):
    if len(texto) <= 6:
        return 70
    if len(texto) <= 9:
        return 50
    return 34


def estado_inicial():
    return ["0", 0.0, "", True]


def estado_error():
    return ["Error", 0.0, "", True]


def escribir_digito(estado, tecla):
    if estado[3] or estado[0] == "0":
        pantalla = tecla
    else:
        pantalla = estado[0] + tecla
    return [pantalla, estado[1], estado[2], False]


def escribir_punto(estado):
    if estado[3]:
        return ["0.", estado[1], estado[2], False]
    if "." in estado[0]:
        return estado
    return [estado[0] + ".", estado[1], estado[2], False]


def cambiar_signo(estado):
    if estado[0] == "0":
        return estado
    if estado[0][0] == "-":
        pantalla = estado[0][1:]
    else:
        pantalla = "-" + estado[0]
    return [pantalla, estado[1], estado[2], estado[3]]


def aplicar_porcentaje(estado):
    valor = float(estado[0])
    return [formatear(valor / 100), estado[1], estado[2], True]


def aplicar_recursiva(estado, tecla):
    valor = float(estado[0])
    if not es_entero_valido(valor):
        return estado_error()
    if tecla == "n!":
        resultado = factorial(int(valor))
    else:
        resultado = sumatoria(int(valor))
    return [formatear(resultado), estado[1], estado[2], True]


def elegir_operador(estado, tecla):
    valor = float(estado[0])
    if estado[2] != "" and not estado[3]:
        resultado = operar(estado[2], estado[1], valor)
        texto = formatear(resultado)
        if texto == "Error":
            return estado_error()
        return [texto, resultado, tecla, True]
    return [estado[0], valor, tecla, True]


def calcular_igual(estado):
    if estado[2] == "":
        return estado
    resultado = operar(estado[2], estado[1], float(estado[0]))
    texto = formatear(resultado)
    if texto == "Error":
        return estado_error()
    return [texto, 0.0, "", True]


def procesar_tecla(estado, tecla):
    if estado[0] == "Error" and tecla != "AC" and tecla not in "0123456789.":
        return estado
    if tecla in "0123456789":
        return escribir_digito(estado, tecla)
    if tecla == ".":
        return escribir_punto(estado)
    if tecla == "AC":
        return estado_inicial()
    if tecla == "+/-":
        return cambiar_signo(estado)
    if tecla == "%":
        return aplicar_porcentaje(estado)
    if tecla == "n!" or tecla == "sum":
        return aplicar_recursiva(estado, tecla)
    if tecla == "=":
        return calcular_igual(estado)
    return elegir_operador(estado, tecla)


def crear_boton(texto, fondo, color_texto, ancho, alto, funcion_click):
    return ft.Container(
        content=ft.Text(texto, size=30, color=color_texto),
        width=ancho,
        height=alto,
        bgcolor=fondo,
        border_radius=alto // 2,
        alignment=ft.Alignment(0, 0),
        data=texto,
        on_click=funcion_click,
    )


def main(page: ft.Page):
    page.title = "Calculadora"
    page.bgcolor = "#000000"
    page.padding = 20

    estado = estado_inicial()

    pantalla = ft.Text("0", size=70, color="#FFFFFF")

    def manejar_click(e):
        nuevo = procesar_tecla(estado, e.control.data)
        for i in range(4):
            estado[i] = nuevo[i]
        pantalla.value = estado[0]
        pantalla.size = tamano_texto(estado[0])
        page.update()

    gris_oscuro = "#333333"
    gris_claro = "#A5A5A5"
    naranja = "#FF9F0A"

    pantalla_contenedor = ft.Container(
        content=pantalla,
        height=130,
        alignment=ft.Alignment(1, 1),
    )

    fila_recursivas = ft.Row(
        spacing=13,
        controls=[
            crear_boton("n!", gris_oscuro, naranja, 111, 60, manejar_click),
            crear_boton("sum", gris_oscuro, naranja, 111, 60, manejar_click),
            crear_boton("^", gris_oscuro, naranja, 111, 60, manejar_click),
        ],
    )

    fila1 = ft.Row(
        spacing=13,
        controls=[
            crear_boton("AC", gris_claro, "#000000", 80, 80, manejar_click),
            crear_boton("+/-", gris_claro, "#000000", 80, 80, manejar_click),
            crear_boton("%", gris_claro, "#000000", 80, 80, manejar_click),
            crear_boton("/", naranja, "#FFFFFF", 80, 80, manejar_click),
        ],
    )

    fila2 = ft.Row(
        spacing=13,
        controls=[
            crear_boton("7", gris_oscuro, "#FFFFFF", 80, 80, manejar_click),
            crear_boton("8", gris_oscuro, "#FFFFFF", 80, 80, manejar_click),
            crear_boton("9", gris_oscuro, "#FFFFFF", 80, 80, manejar_click),
            crear_boton("*", naranja, "#FFFFFF", 80, 80, manejar_click),
        ],
    )

    fila3 = ft.Row(
        spacing=13,
        controls=[
            crear_boton("4", gris_oscuro, "#FFFFFF", 80, 80, manejar_click),
            crear_boton("5", gris_oscuro, "#FFFFFF", 80, 80, manejar_click),
            crear_boton("6", gris_oscuro, "#FFFFFF", 80, 80, manejar_click),
            crear_boton("-", naranja, "#FFFFFF", 80, 80, manejar_click),
        ],
    )

    fila4 = ft.Row(
        spacing=13,
        controls=[
            crear_boton("1", gris_oscuro, "#FFFFFF", 80, 80, manejar_click),
            crear_boton("2", gris_oscuro, "#FFFFFF", 80, 80, manejar_click),
            crear_boton("3", gris_oscuro, "#FFFFFF", 80, 80, manejar_click),
            crear_boton("+", naranja, "#FFFFFF", 80, 80, manejar_click),
        ],
    )

    fila5 = ft.Row(
        spacing=13,
        controls=[
            crear_boton("0", gris_oscuro, "#FFFFFF", 173, 80, manejar_click),
            crear_boton(".", gris_oscuro, "#FFFFFF", 80, 80, manejar_click),
            crear_boton("=", naranja, "#FFFFFF", 80, 80, manejar_click),
        ],
    )

    page.add(
        ft.Column(
            spacing=13,
            controls=[
                pantalla_contenedor,
                fila_recursivas,
                fila1,
                fila2,
                fila3,
                fila4,
                fila5,
            ],
        )
    )


ft.app(target=main)
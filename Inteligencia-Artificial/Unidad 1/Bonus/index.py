class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.izquierda = None
        self.derecha = None

class Arbol:
    def __init__(self, dato=None):
        if dato is None:
            self.raiz = None
        else:
            self.raiz = Nodo(dato)
    
    def vacio(self):
        return self.raiz is None

    def __agregar_recursivo(self, nodo, dato):
        if dato < nodo.dato:
            if nodo.izquierda is None:
                nodo.izquierda = Nodo(dato)
            else:
                self.__agregar_recursivo(nodo.izquierda, dato)
        else:
            if nodo.derecha is None:
                nodo.derecha = Nodo(dato)
            else:
                self.__agregar_recursivo(nodo.derecha, dato)

    def __inorden(self, nodo):
        if nodo is not None:
            self.__inorden(nodo.izquierda)
            print(nodo.dato, end=", ")
            self.__inorden(nodo.derecha)

    def __preorden(self, nodo):
        if nodo is not None:
            print(nodo.dato, end=", ")
            self.__preorden(nodo.izquierda)
            self.__preorden(nodo.derecha)

    def agregar(self, dato):
        if self.raiz is None:
            self.raiz = Nodo(dato)
        else:
            self.__agregar_recursivo(self.raiz, dato)

    def buscarNodo(self, dato):
        return self.__buscarNodoRec(self.raiz, dato)

    def __buscarNodoRec(self, nodo, dato):
        if nodo is None:
            return None
        if nodo.dato == dato:
            return nodo
        elif dato < nodo.dato:
            return self.__buscarNodoRec(nodo.izquierda, dato)
        else:
            return self.__buscarNodoRec(nodo.derecha, dato)

    # Métodos públicos para impresión
    def inorden(self):
        print("Inorden: ", end="")
        self.__inorden(self.raiz)
        print("")
    def preorden(self):
        print("Preorden: ", end="")
        self.__preorden(self.raiz)
        print("")
    def postorden(self):
        print("Postorden: ", end="")
        self.__postorden(self.raiz)
        print("")


# Ejemplo de uso:
arbol = Arbol()
arbol.agregar(10)
arbol.agregar(4)
arbol.agregar(2)
arbol.agregar(5)
arbol.agregar(11)

print("¿Árbol vacío?:", arbol.vacio())
arbol.inorden()
arbol.preorden()

nodo = arbol.buscarNodo(5)
print("Nodo encontrado:", nodo.dato if nodo else "No existe")

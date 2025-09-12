import tkinter as tk
from tkinter import messagebox
import heapq
import time


puzzleInicial = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 0, 8] ]

puzzleFinal = [  
    [1, 2, 3], 
    [4, 5, 6], 
    [7, 8, 0] ]

def findZero(puzzle):
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] == 0:
                return i, j

def movePice(puzzle, movement):
    new_puzzle = [row.copy() for row in puzzle]
    i, j = findZero(new_puzzle)
    if movement == "Arriba" and i > 0:
        new_puzzle[i][j], new_puzzle[i-1][j] = new_puzzle[i-1][j], new_puzzle[i][j]
    elif movement == "Abajo" and i < 2:
        new_puzzle[i][j], new_puzzle[i+1][j] = new_puzzle[i+1][j], new_puzzle[i][j]
    elif movement == "Izquierda" and j > 0:
        new_puzzle[i][j], new_puzzle[i][j-1] = new_puzzle[i][j-1], new_puzzle[i][j]
    elif movement == "Derecha" and j < 2:
        new_puzzle[i][j], new_puzzle[i][j+1] = new_puzzle[i][j+1], new_puzzle[i][j]
    else:
        return None
    return new_puzzle

class Node:
    def __init__(self, puzzle, movimiento, costo , heuristica, parent):
        self.puzzle = puzzle
        self.movimiento = movimiento
        self.costo = costo
        self.heuristica = heuristica
        self.parent = parent
        
    def __lt__(self, other):
        return (self.costo + self.heuristica) < (other.costo + other.heuristica)

def CalcularHeuristica(puzzle):
    heuristica = 0
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] != 0:
                i2, j2 = getPosicion(puzzle[i][j])
                heuristica += abs(i - i2) + abs(j - j2)
    return heuristica

def getPosicion(valor):
    for i in range(3):
        for j in range(3):
            if puzzleFinal[i][j] == valor:
                return i,j

def algoritmo_a_star(puzzle):
    nodosVisitados = set()
    cola = []
    heapq.heappush(cola, Node(puzzle, "", 0, CalcularHeuristica(puzzle), None))

    while cola:
        actual = heapq.heappop(cola)
        if actual.puzzle == puzzleFinal:
            break
        nodosVisitados.add(str(actual.puzzle))
        for movimiento in ["Arriba","Abajo","Izquierda","Derecha"]:
            siguiente = movePice(actual.puzzle, movimiento)
            if siguiente and str(siguiente) not in nodosVisitados:
                heapq.heappush(cola, Node(siguiente, movimiento, actual.costo+1, CalcularHeuristica(siguiente), actual))
    
    recorrido = []
    while actual:
        recorrido.append(actual)
        actual = actual.parent
    return recorrido[::-1]

def es_resolvible(puzzle):
    plano = [num for fila in puzzle for num in fila if num != 0]
    inversiones = sum(1 for i in range(len(plano)) for j in range(i+1,len(plano)) if plano[i] > plano[j])
    return inversiones % 2 == 0

# --- Interfaz Tkinter ---
class PuzzleUI:
    def __init__(self, root, puzzleInicial):
        self.root = root
        self.root.title("8 Puzzle Solver")
        self.puzzle = puzzleInicial

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.labels = [[tk.Label(self.frame, text="", font=("Arial", 24), width=4, height=2, relief="ridge") for j in range(3)] for i in range(3)]
        for i in range(3):
            for j in range(3):
                self.labels[i][j].grid(row=i, column=j)

        self.btn_solve = tk.Button(root, text="Resolver con A*", command=self.resolver)
        self.btn_solve.pack(pady=10)

        self.mostrarPuzzle()

    def mostrarPuzzle(self):
        for i in range(3):
            for j in range(3):
                val = self.puzzle[i][j]
                self.labels[i][j].config(text="" if val==0 else str(val))

    def resolver(self):
        if not es_resolvible(self.puzzle):
            messagebox.showerror("Error","🚨 Este puzzle NO tiene solución. Intenta con otro orden. 🚨")
            return
        inicio = time.time()
        pasos = algoritmo_a_star(self.puzzle)
        duracion = time.time()-inicio
        self.animar(pasos,0)
        messagebox.showinfo("Listo!", f"Resuelto en {len(pasos)-1} movimientos.\nTiempo: {duracion:.3f} s")

    def animar(self, pasos, idx):
        if idx >= len(pasos): return
        self.puzzle = pasos[idx].puzzle
        self.mostrarPuzzle()
        self.root.after(500, lambda: self.animar(pasos, idx+1))

# --- Ejecutar ---
root = tk.Tk()
app = PuzzleUI(root, puzzleInicial)
root.mainloop()

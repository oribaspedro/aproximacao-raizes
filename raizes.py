from math import *
import re
from tabulate import tabulate

def formatarFuncao(txt):
    #adicionando multiplicacoes implicitas (xx, xlog(x), 2x, etc)
    txt = re.sub(r'([0-9xe])([lxe])', r'\1*\2', txt)
    txt = re.sub(r'([xe])([0-9xe])', r'\1*\2', txt)
    txt = re.sub(r'([0-9xe)])([(])', r'\1*\2', txt)
    txt = re.sub(r'([)])([0-9xe(])', r'\1*\2', txt)
    #substituindo pelos termos funcionais do python
    txt = txt.replace("log", "log10")
    txt = txt.replace("ln", "log")
    txt = txt.replace("^", "**")
    txt = txt.replace("sen", "sin")
    txt = txt.replace("e", "exp(1)")
    return txt

def calcularFuncao(x, funcao):
    return eval(funcao)

#funcao para criar nova linha na tabela de resultados caso ainda nao exista
def createNewLine(saida, k):
    if(len(saida) <= k):
        saida.append([k, '#', '#', '#', '#', '#'])

def bissec(a, b, delta, it, funcao, saida):
    k = 0
    if(abs(b-a) < delta):
        return a
    else:
        while(abs(b-a) > delta and abs(calcularFuncao(a, funcao)) > delta and k < it):
            k = k + 1
            meio = (a+b)/2
            finicio = calcularFuncao(a, funcao)
            fmeio = calcularFuncao(meio, funcao)
            createNewLine(saida, k)
            saida[k][1] = meio
            if(finicio * fmeio < 0):
                b = meio
            else:
                a = meio
        print(k)
        return a

def mil(funcao, phi, x, delta, it, saida):
    k = 0
    prev = 0
    while(abs(calcularFuncao(x, funcao)) > delta and abs(x - prev) > delta and k < it):
        k = k + 1
        prev = x
        x = calcularFuncao(x, phi)
        createNewLine(saida, k)
        saida[k][2] = x
    print(k)
    return x

def newton(funcao, derivada, x, delta, it, saida):
    k = 0
    prev = 0
    while(abs(calcularFuncao(x, funcao)) > delta and abs(x - prev) > delta and k < it):
        k = k + 1
        prev = x
        x = x-(calcularFuncao(x, funcao)/calcularFuncao(x, derivada))
        createNewLine(saida, k)
        saida[k][3] = x
    print(k)
    return x

def secante(funcao, x0, x1, delta, it, saida):
    k = 0
    while(abs(calcularFuncao(x1, funcao)) > delta and abs(x0 - x1) > delta and k < it):
        k = k + 1
        aux = x1
        x1 = x1 - ((calcularFuncao(x1, funcao) * (x1 - x0))/(calcularFuncao(x1, funcao) - calcularFuncao(x0, funcao)))
        x0 = aux
        createNewLine(saida, k)
        saida[k][4] = x1
    print(k)
    return x1

def regulaFalsi(funcao, x0, x1, delta, it, saida):
    k = 0
    x = x0
    while(abs(calcularFuncao(x, funcao)) > delta and abs(x0 - x1) > delta and k < it):
        k = k + 1
        x = (x0*calcularFuncao(x1, funcao) - x1*calcularFuncao(x0, funcao))/(calcularFuncao(x1, funcao)-calcularFuncao(x0, funcao))
        if((calcularFuncao(x, funcao) < 0 and calcularFuncao(x0, funcao) < 0) or (calcularFuncao(x, funcao) > 0 and calcularFuncao(x0, funcao) > 0)):
            x0 = x
        else:
            x1 = x
        createNewLine(saida, k)
        saida[k][5] = x
    print(k)
    return x

#abrindo o arquivo txt e separando cada item do arquivo em uma linha do array
file_obj = open("entrada.txt", "r")
dados = file_obj.readlines()

#formatando todos os dados do txt de modo que possam ser utilizados
funcao = formatarFuncao(dados[0].split('=')[1])

derivada = formatarFuncao(dados[1].split('=')[1])

phi = formatarFuncao(dados[2].split('=')[1])

precisao = dados[3].split('=')[1]
precisao = formatarFuncao(precisao)

intervalo = dados[4].split('=')[1]
intervalo = re.sub(r'[\[\]\s]', r'', intervalo)
intervalo = intervalo.split(',')

x0 = float(dados[5].split('=')[1])

newLine = ['#', '#', '#', '#', '#']

saida = [["k", "bisseccao", "mil", "newton", "secante", "regulaFalsi"]]
bissec(int(intervalo[0]), int(intervalo[1]), eval(precisao), 100, funcao, saida)
mil(funcao, phi, x0, calcularFuncao(0, precisao), 100, saida)
newton(funcao, derivada, x0, calcularFuncao(0, precisao), 100, saida)
secante(funcao, float(intervalo[0]), float(intervalo[1]), calcularFuncao(0, precisao), 100, saida)
regulaFalsi(funcao, float(intervalo[0]), float(intervalo[1]), calcularFuncao(0, precisao), 100, saida)
for row in saida:
    print(row)

with open("saida.txt", "w") as file:
    file.write(tabulate(saida[1:], headers=saida[0], tablefmt="grid"))
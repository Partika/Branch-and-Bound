from copy import deepcopy
from math import floor
from xmlrpc.client import MAXINT
import numpy as np
import simplex as sp

# Passo 1   Termine as computacoes se a Lista-Mestra estiver vazia, senao tire um problema de
#           P.L. da Lista-Mestra.

# Passo 2   Resolva o problema escolhido. Se este nao tiver nenhuma solucao viavel ou se o valor
#           otimo Z for menor ou igual Z^t, entao faca Z^(t+1) = Z^t e retorne ao Passo 1.

# Passo 3   Se a solucao otima obtida para o problema de P.L. satisfizer as restricoes de inteiros,
#           entao registre-a, faca Z^(t+1) ser o valor otimo correspondente da funcao objetivo X e
#           retorne ao Passo 1, senao, prossiga ao Passo 4.

# Passo 4   Escolha qualquer variavel xj, com j = 1, 2, ..., p que nao tenha um valor inteiro na
#           solucao otima obtida para o problema escolhido de P.L. Faca bj denotar este valor e
#           ⌊bj⌋ significa o maior inteiro menor ou igual a bj (arredondar para baixo). Acrescente
#           dois problemas de P.L. a Lista-Mestra, identicos ao problema escolhido no Passo 1,
#           sendo em um o limite inferior Lj para xj e ⌊bj⌋ + 1 e no outro o limite superior Uj
#           para xj e ⌊bj⌋. Faca Z^(t+1) = Z^t e retorne ao Passo 1.


class No:
    def __init__(self, funcoes: list, nivel: int) -> None:
        self.funcoes = funcoes
        self.nivel = nivel
        self.xOtimos = None
        self.solucaoOtima = None
        self.variaveis = None

    def resolve(self, funcaoZ: list, funcaoInicial: list) -> bool:
        print(self.funcoes)
        resultados = sp.Simplex(funcaoZ, self.funcoes)
        if(not(isinstance(resultados, bool))):
            self.xOtimos = resultados[0]
            self.variaveis = resultados[1]
            self.solucaoOtima = sp.Valor_funcao(
                funcaoInicial, self.xOtimos, self.variaveis)
            if(ta_certo_mesmo(self.xOtimos, self.funcoes, self.variaveis, len(funcaoInicial))):
                return True
            else: return False
        else:
            return False


def todos_inteiros(xFactiveis: list, variaveis: list, tamanho: int) -> list:
    tam = len(xFactiveis)
    for i in range(tam):
        if(not(xFactiveis[i] == floor(xFactiveis[i])) and (variaveis[i] < (tamanho))):
            return [False, i]
    return [True]


def ta_certo_mesmo(xAchados: list, funcoes: list, xBasicos: list, tam: int) -> bool:
    taCerto = True
    tam2 = len(funcoes)
    tam3 = len(xBasicos)
    for i in range(tam2):
        igual = True
        for j in range(tam3):
            if(xAchados[j]<0):
                taCerto=False
                break
            if(xBasicos[j] >= tam):
                continue
            if(funcoes[i][xBasicos[j]] == 1):
                igual = True
                for k in range(tam):
                    if(j == k):
                        continue
                    if(funcoes[i][k] != 0):
                        igual = False
                        break
                if(not(igual)):
                    break
                if(funcoes[i][-2] == "<="):
                    if(xAchados[j] > funcoes[-1]):
                        taCerto = False
                elif(funcoes[i][-2] == ">="):
                    if(xAchados[j] < funcoes[-1]):
                        taCerto = False
                else:
                    if(xAchados[j] != funcoes[-1]):
                        taCerto = False
                break
        if(not(taCerto)):
            continue
    if(taCerto):
        return True
    else:
        return False


def nova_restricao(restricoes: list, novaRestricao: list, nivel: int, arvore: list) -> None:
    tam1 = len(restricoes)
    tam2 = len(novaRestricao)-2
    mesma = True
    for i in range(tam1):
        for j in range(tam2):
            if(restricoes[i][j] != novaRestricao[j]):
                mesma = False
                break
    if(mesma):
        if(novaRestricao[-2] == restricoes[i][-2]):
            novas = deepcopy(restricoes)
            novas[i][-1] = novaRestricao[-1]
            arvore.append(No(novas, nivel))
            return
        else:
            return
    novas = deepcopy(restricoes)
    novas.append(novaRestricao)
    arvore.append(No(novas, nivel))


def main():
    funcaoZ, funcoes, minMax = sp.Leitura()
    inicial = No(funcoes, 0)
    funcaoInicial = deepcopy(funcaoZ)
    melhorZ = MAXINT
    tam = len(funcaoZ)
    if(minMax == 'max'):
        melhorZ *= -1
        for i in range(tam):
            funcaoZ[i] *= -1
    solucaoOtima = []
    basicas = []
    lista = [inicial]
    no = 0
    nivelMax = 20
    while(lista != [] and no < nivelMax):
        u = lista.pop(0)
        no += 1
        print('no: ', no, 'z = ', melhorZ)
        print(u.funcoes)

        # verifica se o no atual eh factivel
        factivel = u.resolve(deepcopy(funcaoZ), funcaoInicial)
        if(not(factivel)):
            print('nao factivel')
            continue

        # encontrando a variavel nao inteira
        inteiro = todos_inteiros(u.xOtimos, u.variaveis, tam)
        bound = 0
        print(inteiro, u.xOtimos)

        # criando os galhos
        if(inteiro[0]):
            print('resposta inteira encontrada')
            if(minMax == "max"):
                if(u.solucaoOtima > melhorZ):
                    solucaoOtima = u.xOtimos
                    basicas = u.variaveis
                    melhorZ = u.solucaoOtima
            else:
                if(u.solucaoOtima < melhorZ):
                    solucaoOtima = u.xOtimos
                    basicas = u.variaveis
                    melhorZ = u.solucaoOtima
            continue
        else:
            print('resposta nao interia encontrada')
            bound = inteiro[1]

        # pegando o arredondamento
        bound1 = floor(u.xOtimos[bound])
        bound2 = bound1+1
        variavel = u.variaveis[bound]
        restricaoBase = []
        for i in range(tam):
            if(i == variavel):
                restricaoBase.append(1.0)
            else:
                restricaoBase.append(0.0)

        # as novas restricoes
        restricao1 = deepcopy(restricaoBase)
        restricao1.append('<=')
        restricao1.append(bound1)
        restricao2 = restricaoBase
        restricao2.append('>=')
        restricao2.append(bound2)

        # valida a nova restricao
        nova_restricao(u.funcoes, restricao1, u.nivel+1, lista)
        nova_restricao(u.funcoes, restricao2, u.nivel+1, lista)

    tam = len(basicas)
    for i in range(tam):
        print(f'x{basicas[i]} = {solucaoOtima[i]}')
    print('z = ', sp.Valor_funcao(funcaoInicial, solucaoOtima, basicas))


main()

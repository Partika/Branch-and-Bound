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
        resultados = sp.Simplex(funcaoZ, self.funcoes)
        if(not(isinstance(resultados, bool))):
            self.xOtimos = resultados[0]
            self.variaveis = resultados[1]
            self.solucaoOtima = sp.Valor_funcao(
                funcaoInicial, self.xOtimos, self.variaveis)
            return True
        else:
            return False


def todosInteiros(xFactiveis: list, variaveis: list, tamanho: int):
    tam = len(xFactiveis)
    for i in range(tam):
        if(not(isinstance(xFactiveis[i], int)) and (variaveis[i] < (tamanho-1))):
            return [False, i]
    return [True]


def main():
    funcaoZ, funcoes, minMax = sp.Leitura()
    inicial = No(funcoes, 0)
    funcaoInicial = deepcopy(funcaoZ)
    tam = len(funcaoZ)
    if(minMax == 'max'):
        for i in range(tam):
            funcaoZ[i] *= -1
    solucaoOtima = []
    basicas = []
    lista = [inicial]
    melhorZ = -MAXINT
    no = 0
    nivelMax = 20
    while(lista != [] and no < nivelMax):
        u = lista.pop(0)
        no += 1
        print('no: ', no, 'z = ', melhorZ)
        factivel = u.resolve(deepcopy(funcaoZ), funcaoInicial)
        if(not(factivel)):
            print('nao factivel')
            continue
        inteiro = todosInteiros(u.xOtimos, u.variaveis, tam)
        bound = 0
        print(inteiro, u.xOtimos)
        if(inteiro[0]):
            print('resposta inteira encontrada')
            if(u.solucaoOtima > melhorZ):
                solucaoOtima = u.xOtimos
                basicas = u.variaveis
                melhorZ = u.solucaoOtima
        else:
            print('resposta nao interia encontrada')
            bound = inteiro[1]
        bound1 = floor(u.xOtimos[bound])
        bound2 = bound1+1
        variavel = u.variaveis[bound]
        restricaoBase = []
        for i in range(tam):
            if(i == variavel):
                restricaoBase.append(1.0)
            else:
                restricaoBase.append(0.0)
        restricao1 = deepcopy(restricaoBase)
        restricao1.append('<=')
        restricao1.append(bound1)
        restricao2 = restricaoBase
        restricao2.append('<=')
        restricao2.append(bound2)
        novaRestricao = deepcopy(u.funcoes)
        novaRestricao.append(restricao1)
        lista.append(No(novaRestricao, u.nivel+1))
        novaRestricao = deepcopy(u.funcoes)
        novaRestricao.append(restricao2)
        lista.append(No(novaRestricao, u.nivel+1))

    for i in range(tam):
        print(f'x{basicas[i]} = {solucaoOtima[i]}')
    print('z = ', sp.Valor_funcao(funcaoInicial, solucaoOtima, basicas))


main()

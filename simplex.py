from copy import deepcopy
from xmlrpc.client import MAXINT
import numpy as np

# funcoes extras necessarias


def Multiplicacao_matrizes(matrizA: list, matrizB: list) -> float:
    matrizC = np.matmul(matrizA, matrizB)
    return matrizC


def Multiplicacao_vetores(vetorA: list, vetorB: list) -> float:
    resultado = np.dot(vetorA, vetorB)
    return resultado


def Transposta(matriz: list) -> list:
    return np.transpose(matriz)


def Determinante(m: list) -> float:
    return np.linalg.det(m)


def Inversa(matrizA: list, independentes: list) -> float:
    # determinante !=0?
    if(Determinante(matrizA) == 0):
        return False

    n = len(matrizA)

    inv = []
    for i in range(n):
        linha = [0]*n
        inv.append(linha)

    for i in range(n):
        inv[i][i] = 1

    # Performing elementary operations
    for i in range(n):
        if (matrizA[i][i] == 0):

            c = 1
            while ((i + c) < n and matrizA[i + c][i] == 0):
                c += 1
            if ((i + c) == n):
                break

            j = i

            # se trocar o pivo e os independentes da errado
            # temp = independentes[j]
            # independentes[j] = independentes[j+c]
            # independentes[j+c] = temp
            for k in range(n):

                temp = matrizA[j][k]
                temp2 = inv[j][k]

                matrizA[j][k] = matrizA[j+c][k]
                inv[j][k] = inv[j+c][k]

                matrizA[j+c][k] = temp
                inv[j+c][k] = temp2

        for j in range(n):

            # Excluding all i == j
            if (i != j):
                # Converting Matrix to reduced row
                # echelon form(diagonal matrix)
                p = matrizA[j][i] / matrizA[i][i]

                for k in range(n):
                    matrizA[j][k] = matrizA[j][k] - (matrizA[i][k]) * p
                    inv[j][k] = inv[j][k] - (inv[i][k]) * p

    for i in range(n):
        if(matrizA[i][i] != 1):
            p = 1/matrizA[i][i]
            for j in range(n):
                matrizA[i][j] *= p
                inv[i][j] *= p

    return inv, independentes


def Inversa_(matriz: list, independentes: list) -> float:
    return np.linalg.inv(matriz)


def Cria_submatriz(matrizA: list, vetorX: list) -> float:
    submatriz = []
    for j in range(len(matrizA)):
        linha = []
        for i in range(len(vetorX)):
            linha.append(matrizA[j][vetorX[i]])
        submatriz.append(linha)
    return submatriz


# SIMPLEX, SIMPLAO, COMPLEX

# Fase I:

#   1. Determine inicialmente uma parti¸c˜ao b´asica fact´ıvel A=[B,N]. A rigor, precisa-se de
#   dois vetores de ´ındices b´asicos e n˜ao-b´asicos:
#   (B1, B2, ..., Bm) e (N1, N2, ..., Nn−m)
#   Os vetores das vari´aveis b´asicas e n˜ao-b´asicas, respectivamente:
#   x transpost basico = (xB1, xB2, ..., xBm ) e
#   x transposto nao basico = (xN1, xN2, ..., xNn−m ).


def Separacao_da_matriz(funcaoZ: list, funcoes: list) -> list:
    # definicao da existencia de variaveis de folga
    inequacoes = []
    for i in range(len(funcoes)):
        condicao = funcoes[i][-2]
        if condicao != '=':
            funcaoZ.append(0.0)
            if(condicao == '<='):
                inequacoes.append(1.0)
            else:
                inequacoes.append(-1.0)
        else:
            inequacoes.append(0.0)
    # fim da definicao das variaveis de folga

    # inicio do aumento da matriz A
    matrizA = []
    for i in range(len(funcoes)):
        linha = funcoes[i][:-2]
        for j in range(len(inequacoes)):
            if(i == j):
                linha.append(inequacoes[j])
            else:
                linha.append(0.0)
        matrizA.append(linha)
    # fim do aumento da matriz A

    # inicio da definicao basicas e nao basicas
    basicas = []
    naoBasicas = []
    maxBasicas = len(funcoes)
    tam = len(funcaoZ)
    for i in range(tam-1, -1, -1):
        if(i < maxBasicas-1):
            naoBasicas.append(i)
        else:
            basicas.append(i)
    basicas.sort()
    naoBasicas.sort()
    # fim da definicao basicas e nao basicas

    # inicio da criacao da matriz de termos independentes
    independentes = []
    for i in range(len(funcoes)):
        independentes.append(funcoes[i][-1])
    # fim da criacao da matriz de termos independentes

    return matrizA, basicas, naoBasicas, independentes


#   2. Fa¸ca itera¸c˜ao ← 1.


# Fase II: {in´ıcio da itera¸c˜ao simplex}

#   Passo 1: {c´alculo da solu¸c˜ao b´asica}
#       x relativo basico ← B^−1*b (equivalentemente, resolva o sistema B * x relativo basico = b)
#       x relativo nao basico ← 0
# !!!(devido a analises, o x relativo nao basico nao foi feito, afinal ele nao aparece mais)!!!

def Calculo_x_relativo(BInversa: list, b: list) -> float:
    xRelativoBasico = Multiplicacao_matrizes(
        BInversa, Transposta(np.matrix(b)))
    return xRelativoBasico


#   Passo 2: {c´alculo dos custos relativos}

#       2.1) {vetor multiplicador simplex}
#           λ transposto ← c transposto basico B^−1
#           (equivalentemente, resolva o sistema B transposto * λ = cB)


def Custo(funcaoZ: list, variaveis: list) -> float:
    custoBasico = [0]*len(variaveis)
    for i in range(len(custoBasico)):
        custoBasico[i] = funcaoZ[variaveis[i]]
    return custoBasico


def Calcula_lambda(custoBasico: list, basicaInversa: list) -> float:
    lambdaSimplex = Multiplicacao_matrizes(custoBasico, basicaInversa)
    return lambdaSimplex


#       2.2) {custos relativos}
#           c relativo nao basico j ← c nao basico j − (λ transposto * a nao bascio j)
#           j = 1, 2, ..., n − m

def Custos_Relativos(lambdaSimplex: list, custoNaoBasico: list, matrizNaoBasica: list) -> float:
    naoBasicaTransposta = Transposta(matrizNaoBasica)
    for i in range(len(custoNaoBasico)):
        custoNaoBasico[i] -= (Multiplicacao_vetores(lambdaSimplex,
                              naoBasicaTransposta[i]))
    return custoNaoBasico


#       2.3) {determina¸c˜ao da vari´avel a entrar na base}
#           c relativo nao basico k ← min{c relativo nao basico j, j = 1, 2, ..., n − m}
#           (a variavel x nao basico k entra na base)

def Calcula_k(custoRelativoNaoBasico: list) -> int:
    menor = min(custoRelativoNaoBasico)
    return custoRelativoNaoBasico.index(menor)


# print(Calcula_k(Custos_Relativos([1, 0], [-2, -1], [[1, 0], [1, 1]])))

#   Passo 3: {teste de otimalidade}
#       Se c relativo nao basico k ≥ 0, ent˜ao: pare {solu¸c˜ao na itera¸c˜ao atual ´e ´otima}


def Otimalidade(custoRelativoNaoBasico: list, k: int) -> bool:
    if(custoRelativoNaoBasico[k] >= 0):
        return True
    else:
        return False


#   Passo 4: {c´alculo da dire¸c˜ao simplex}
#       y ← B^−1 * a nao basico k
#       (equivalentemente, resolva o sistema: B*y = a nao basico k)


def Direcao_simplex(BasicaInversa: list, matrizA: list, k: int, naoBasicas: list) -> float:
    colunaK = [0]*len(matrizA)
    for i in range(len(matrizA)):
        colunaK[i] = matrizA[i][naoBasicas[k]]
    colunaK = Transposta(colunaK)
    y = Multiplicacao_matrizes(BasicaInversa, colunaK)
    return y

# print(Direcao_simplex([[1,0],[0,1]],[1,1]))

#   Passo 5: {determina¸c˜ao do passo e vari´avel a sair da base}
#       Se y ≤ 0, ent˜ao: pare {problema n˜ao tem solu¸c˜ao ´otima finita f(x) → −∞ }
#       Caso contr´ario, determine a vari´avel a sair da base pela raz˜ao m´ınima:
#       ε ← x relativo basico l/yl= min{x relativo basico i/yi, tal que yi> 0, i = 1, 2, ..., m}
#       (a variavel xBl sai da base)


def Calcula_l(y: list, xRelativoBasico: list) -> int:

    # se y <= 0
    seguro = False
    for i in range(len(y)):
        if y[i] > 0:
            seguro = True
            break
    if(not(seguro)):
        return False

    razoes = []
    for i in range(len(xRelativoBasico)):
        if(y[i] <= 0):
            razoes.append(MAXINT)
        else:
            razoes.append(xRelativoBasico[i]/y[i])

    passo = min(razoes)
    l = razoes.index(passo)

    return l


#   Passo 6: {atualiza¸c˜ao: nova parti¸c˜ao b´asica, troque a l-´esima coluna de B pela k-´esima
#   coluna de N}
#       matriz b´asica nova: B ← [a basico 1...a basico (l−1) a nao basico k a basico (l+1) ...a basico m ]
#       matriz n˜ao-b´asica nova: N ← [a nao basico 1...a nao basico (k−1) a basico l a naos basico (k+1) ...a nao basico (n−m) ]
#       itera¸c˜ao ← itera¸c˜ao + 1
#       Retorne ao Passo 1
#       {fim da itera¸c˜ao simplex}

def Troca_k_l(basicas: list, naoBasicas: list, k: int, l: int) -> list:
    aux = basicas[l]
    basicas[l] = naoBasicas[k]
    naoBasicas[k] = aux
    return basicas, naoBasicas


# 3. Calcule o valor da fun¸c˜ao objetivo f(x) =⇒ FIM.


def Valor_funcao(funcaoZ: list, xRelativoBasico: list, basicas: list) -> float:
    resultado = 0
    for i in range(len(xRelativoBasico)):
        resultado += funcaoZ[basicas[i]]*xRelativoBasico[i]
    return resultado


# main

def Leitura():
    funcaoZ = input("digite a funcao z separada por espacos (2 -4 3): ")
    funcaoZ = funcaoZ.split(' ')
    for i in range(len(funcaoZ)):
        funcaoZ[i] = float(funcaoZ[i])
    minMax = input('digite min para minimizar e max para maximizar')
    numeroFuncoes = int(input("qual o numero de funcoes? "))
    print("insira as funcoes separadas por enter")
    funcoes = []
    # gera mat (matriz das funcoes) e B (matriz dos termos independentes)
    for i in range(numeroFuncoes):
        novaFuncao = input(
            f"digite a funcao {i+1} separada por espacos (2 -4 3 <= 5): ").split()
        for j in range(len(novaFuncao)):
            if (novaFuncao[j] != novaFuncao[-2]):
                novaFuncao[j] = float(novaFuncao[j])
        funcoes.append(novaFuncao)
    return funcaoZ, funcoes, minMax


def Simplex(funcaoZ, funcoes, minMax):
    matrizA, basicas, naoBasicas, independentes = Separacao_da_matriz(
        funcaoZ, funcoes)
    indFixo = deepcopy(independentes)
    funcaoFin = deepcopy(funcaoZ)
    tam = len(funcaoZ)
    if(minMax == 'max'):
        for i in range(tam):
            funcaoZ[i] *= -1
    it = 1
    maxit = 10
    solucaoOtima = []
    deu = True
    while(it < maxit):
        print()
        independentes = indFixo
        print('it: ', it)
        matrizBasica = Cria_submatriz(matrizA, basicas)
        matrizNaoBasica = Cria_submatriz(matrizA, naoBasicas)
        matrizBasicaInversa, independentes = Inversa(
            matrizBasica, independentes)
        if(not(matrizBasicaInversa)):
            deu = False
            break

        xRelativo = Calculo_x_relativo(matrizBasicaInversa, independentes)

        custoBasico = Custo(funcaoZ, basicas)
        lambdaTransposto = Calcula_lambda(
            custoBasico, matrizBasicaInversa)

        custoNaoBasico = Custo(funcaoZ, naoBasicas)
        custoRelativoNaoBasico = Custos_Relativos(
            lambdaTransposto, custoNaoBasico, matrizNaoBasica)

        k = Calcula_k(custoRelativoNaoBasico)

        if(Otimalidade(custoRelativoNaoBasico, k)):
            print("Otimo!")
            solucaoOtima = xRelativo
            break
        print("Nao otimo!")

        y = Direcao_simplex(matrizBasicaInversa, matrizA, k, naoBasicas)

        l = Calcula_l(y, xRelativo)

        basicas, naoBasicas = Troca_k_l(basicas, naoBasicas, k, l)

        it += 1
    # fim do laco de repeticao simplex

    if(deu):
        print("A solucao factivel otima eh:")
        for i in range(len(solucaoOtima)):
            print(f'x{basicas[i]} = {solucaoOtima[i]}, ', end=' ')
        print(f'z = {Valor_funcao(funcaoFin, solucaoOtima, basicas)}')
    else:
        print('Em algum momento nao deu para fazer a inversa porque o determinante deu 0')

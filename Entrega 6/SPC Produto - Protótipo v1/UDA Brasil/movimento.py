print("##########  TABELA MOVIMENTO  ##########")
import pandas as pd 
from data import fatec_movimento, fatec_operacao, fatec_fonte, indice_fontes
print(" * Dados importados")

# DECLARANDO VARIAVEIS GLOBAIS




#Este arquivo irá análisar cada fonte e retornará os indicadores ja calculados


'''
CONFIABILIDADE
'''
def datasInvalidas_movimento(fonte):
    datas_invalidas = list()
    dataframe = fatec_movimento[(fatec_movimento['id_fnt'] == fonte)]
    for index in zip(list(dataframe['id_mvt_cad_pos']), list(dataframe['dat_vct'])):
        if len(index[1]) < 8:
            datas_invalidas.append(index)
    porcentagem = (len(datas_invalidas) / dataframe.shape[0]) * 100
    return porcentagem, datas_invalidas





'''
CONSISTÊNCIA
'''

def consistencia(df_base, series_base, series_referencia):
    matriz = list([fonte] for fonte in indice_fontes)
    for fonte in indice_fontes:
        campos_inconsistentes = list()
        for campo in range(len(series_base)):
            if df_base['id_fnt'][campo] == fonte and campo not in series_referencia:
                campos_inconsistentes.append(campo)
        
        porcentagem = 100 - (len(campos_inconsistentes) / len(series_base)) * 100
        matriz[indice_fontes.index(fonte)].append(porcentagem)
    
    return matriz



'''
UNIÃO DOS TRÊS INDICADORES
Abaixo estamos concatenando todas as funções no seu respectivo indicador
'''

def indicadores_fatec_movimento():
    # Criando a matriz, em que cada array recebe as fontes de forma ordena
    matriz_fatec_movimento = list([fonte] for fonte in indice_fontes)
    print(" * Matriz MOVIMENTO criada")

    # CONSISTENCIA
    # A função abaixo retorna uma matriz com a fonte e a consistência entre as duas series abaixo inseridas como argumento
    consistenciaMatriz = consistencia(fatec_movimento, fatec_movimento['id_opr_cad_pos'], fatec_operacao['id_opr_cad_pos'])
    print(" * Matriz consistência criada")


    # O loop abaixo adicionará à todas as listas da matriz "matriz_fatec_operacao" a consistência recebida acima
    for linha in range(len(consistenciaMatriz)):
        matriz_fatec_movimento[linha].append(consistenciaMatriz[linha][1])
    print(" * Consistência adicionada a matriz")






    # CONFIABILIDADE
    # O código abaixo fará a mesma adição na matriz, porém para o indicador de confiabilidade
    for fonte in range(len(matriz_fatec_movimento)):
        porcentagem_invalida = datasInvalidas_movimento(indice_fontes[fonte])[0]
        confiabilidade = 100 - porcentagem_invalida
        matriz_fatec_movimento[fonte].append(confiabilidade)


    return matriz_fatec_movimento
print(" * Funções definidas . . . Chamando função dos indicadores")
indicadores = indicadores_fatec_movimento()

for fonte in indicadores:
    print(fonte)
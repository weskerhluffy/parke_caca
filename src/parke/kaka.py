'''
Created on 06/02/2018

@author: 

XXX: https://code.google.com/codejam/contest/433101/dashboard#s=p2
'''

import logging
from sys import stdin
from itertools import cycle, starmap
from collections import namedtuple

nivel_log = logging.ERROR
#nivel_log = logging.DEBUG
logger_cagada = None

class ciclo_mierda:
    def __init__(self, arreglo):
        self.arreglo = arreglo
        self.arreglo_tam = len(arreglo)
        self.idx = 0
        
    def __iter__(self):
        return self
    
    def next(self):
        caca = self.peekar()
        self.idx += 1
        return caca
    
    def peekar(self):
        caca = self.arreglo[self.idx % self.arreglo_tam]
        return caca
    __next__ = next

grupito_pendejo = namedtuple("grupito_pendejo", "idx cacas")

def parke_kaka_obten_siguiente_grupo_pendejo(cacapacidad, grupos_pendejos):
    acum = 0
    grupos_putos = []
    gpo_act = next(grupos_pendejos)
    grupos_putos.append(gpo_act)
    acum = gpo_act.cacas
#    logger_cagada.debug("caca {}".format(gpo_act))
    while acum + grupos_pendejos.peekar().cacas <= cacapacidad and grupos_pendejos.peekar().idx != grupos_putos[0].idx:
        gpo_act = next(grupos_pendejos)
        acum += gpo_act.cacas
        grupos_putos.append(gpo_act)
#        logger_cagada.debug("caca  aora {}".format(gpo_act))
    return tuple(grupos_putos)

def parke_kaka_obten_siguiente_siguiente_grupo_pendejo(cacapacidad, grupos_pendejos):
    parke_kaka_obten_siguiente_grupo_pendejo(cacapacidad, grupos_pendejos)
    return parke_kaka_obten_siguiente_grupo_pendejo(cacapacidad, grupos_pendejos)

def parke_kaka_obten_valor_grupo(grupo):
    return sum(map(lambda gpo:gpo.cacas, grupo))

def parke_kaka_determina_valor_sequencia(cacapacidad, grupos):
    contador_fuera_de_ciclo = 0
    contador_dentro_de_ciclo = 0
    valores_dentro_de_ciclo = []
    valores_fuera_de_ciclo = []
    valor = 0
    grupos_pendejos_tortuga = ciclo_mierda(grupos)
    grupos_pendejos_liebre = ciclo_mierda(grupos)
    parke_kaka_obten_siguiente_grupo_pendejo(cacapacidad, grupos_pendejos_tortuga)
    parke_kaka_obten_siguiente_grupo_pendejo(cacapacidad, grupos_pendejos_liebre)
    gpo_tortuga = parke_kaka_obten_siguiente_grupo_pendejo(cacapacidad, grupos_pendejos_tortuga)
    gpo_liebre = parke_kaka_obten_siguiente_siguiente_grupo_pendejo(cacapacidad, grupos_pendejos_liebre)
    logger_cagada.debug("tort {} liebre {}".format(gpo_tortuga, gpo_liebre))
    while(gpo_liebre != gpo_tortuga):
        logger_cagada.debug(" aora tort {} liebre {}".format(gpo_tortuga, gpo_liebre))
        gpo_tortuga = parke_kaka_obten_siguiente_grupo_pendejo(cacapacidad, grupos_pendejos_tortuga)
        gpo_liebre = parke_kaka_obten_siguiente_siguiente_grupo_pendejo(cacapacidad, grupos_pendejos_liebre)
    
    logger_cagada.debug("se encontro ciclo en {}".format(gpo_liebre))
    
    grupos_pendejos_tortuga = ciclo_mierda(grupos)
    gpo_tortuga = parke_kaka_obten_siguiente_grupo_pendejo(cacapacidad, grupos_pendejos_tortuga)
    
    valores_fuera_de_ciclo.append(valor)
    while(gpo_liebre != gpo_tortuga):
        valor += parke_kaka_obten_valor_grupo(gpo_tortuga)
        valores_fuera_de_ciclo.append(valor)
        logger_cagada.debug("fuera ciclo aora tort {} liebre {}".format(gpo_tortuga, gpo_liebre))
        gpo_tortuga = parke_kaka_obten_siguiente_grupo_pendejo(cacapacidad, grupos_pendejos_tortuga)
        gpo_liebre = parke_kaka_obten_siguiente_grupo_pendejo(cacapacidad, grupos_pendejos_liebre)
        contador_fuera_de_ciclo += 1
    
    valor = 0
    valores_dentro_de_ciclo.append(valor)
    valor += parke_kaka_obten_valor_grupo(gpo_tortuga)
    valores_dentro_de_ciclo.append(valor)
    gpo_tortuga = parke_kaka_obten_siguiente_grupo_pendejo(cacapacidad, grupos_pendejos_tortuga)
    while(gpo_liebre != gpo_tortuga):
        valor += parke_kaka_obten_valor_grupo(gpo_tortuga)
        valores_dentro_de_ciclo.append(valor)
        gpo_tortuga = parke_kaka_obten_siguiente_grupo_pendejo(cacapacidad, grupos_pendejos_tortuga)
        contador_dentro_de_ciclo += 1

    logger_cagada.debug("los valores fuera {} dentro {}".format(valores_fuera_de_ciclo, valores_dentro_de_ciclo))
    return valores_fuera_de_ciclo, valores_dentro_de_ciclo

def parke_kaka_fuerza_bruta(grupos, vueltas, cacapacidad):
    grupos_pendejos = ciclo_mierda(grupos)
    vueltas_cnt = 0
    mierda = 0
    gpo = parke_kaka_obten_siguiente_grupo_pendejo(cacapacidad, grupos_pendejos)
    while vueltas_cnt < vueltas:
        mierda += parke_kaka_obten_valor_grupo(gpo)
        gpo = parke_kaka_obten_siguiente_grupo_pendejo(cacapacidad, grupos_pendejos)
        vueltas_cnt += 1
        logger_cagada.debug("la mierda act en {} {}".format(vueltas_cnt, mierda))
    return mierda
    

def parke_kaka_core(grupos, vueltas, cacapacidad):
    logger_cagada.debug("vueltas {} cacapacidad {}".format(vueltas, cacapacidad))
    caca = 0
    valores_lineales, valores_ciclicos = parke_kaka_determina_valor_sequencia(cacapacidad, grupos)
    valores_lineales_tam = len(valores_lineales)-1
    valores_ciclicos_tam = len(valores_ciclicos)-1
    logger_cagada.debug("q caraxo {}".format(min(valores_lineales_tam, vueltas)))
    caca = valores_lineales[min(valores_lineales_tam, vueltas)]
    vueltas -= min(valores_lineales_tam, vueltas)
    vueltas_completas = vueltas // valores_ciclicos_tam
    vueltas_sobrantes = vueltas % valores_ciclicos_tam
    logger_cagada.debug("las vueltas comp {} las sobrantes {}".format(vueltas_completas, vueltas_sobrantes))
    caca += vueltas_completas * valores_ciclicos[-1] + valores_ciclicos[vueltas_sobrantes]
    return caca

def caca_comun_lee_linea_como_num():
    return int(stdin.readline().strip())

def caca_comun_lee_linea_como_monton_de_numeros():
    return list(map(int, stdin.readline().strip().split(" ")))

def parke_kaka_main():
    cacasos = caca_comun_lee_linea_como_num()
    for cacaso in range(cacasos):
        vueltas, cacapacidad, grupos_tam = caca_comun_lee_linea_como_monton_de_numeros()
        grupos_tams = caca_comun_lee_linea_como_monton_de_numeros()
        grupos = list(starmap(grupito_pendejo, enumerate(grupos_tams)))
#        logger_cagada.debug("los gpos {}".format(list(grupos)))
        
        chosto = parke_kaka_core(grupos, vueltas, cacapacidad)
#        ass = parke_kaka_fuerza_bruta(grupos, vueltas, cacapacidad)
#        assert chosto == ass, "lo calculado {} lo q debe ser {}".format(chosto, ass)
        print("Case #{}: {}".format(cacaso + 1, chosto))

if __name__ == '__main__':
        FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(level=nivel_log, format=FORMAT)
        logger_cagada = logging.getLogger("asa")
        logger_cagada.setLevel(nivel_log)
        parke_kaka_main()

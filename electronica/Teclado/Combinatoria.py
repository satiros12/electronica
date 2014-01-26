def indexes(nelements, nc):  # nc>=2
    s = range(nelements)
    res = [[i, j] for i in s for j in s]
    for n in range(nc - 2):
        res = [[i] + t for i in s for t in res]
    return [t for t in res if len(set(t)) == nc]

def combianciones(l, num):
    return [[l[i] for i in t] for t in indexes(len(l), num) ]

def combinatoriaBooleana(cuantos):
    resultado = [] 
    rango = range(2 ** cuantos)
    for i in rango:
        # print i
        combinacion = []
        desp = 0
        for j in range(0, cuantos):
            cual = (cuantos - 1) - j
            binario = str(bin(i))[2:]
            if(len(binario) <= cual):
                desp = desp + 1
                combinacion.append(False)
            elif(binario[j - desp] == '1'):
                combinacion.append(True)
            else:
                combinacion.append(False)
        resultado.append(combinacion)
    return resultado
 
print str(combinatoriaBooleana(5))

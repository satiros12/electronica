import logging
from datetime import datetime

#Creacion de logger:
logging.basicConfig(level=logging.DEBUG, filename = ("Resistencias" + str(datetime.now())+ ".log"), filemode ='a')


#configuracion inicial
vin = 5
precision = 0.005
r2 = 1000 
LIMITE_ARRAY = 1000000
ERROR_DE_PRECISION = 1 #Error de precision seria : +/- precision * ERROR_DE_PRECISION

#inicializar Matriz
MatrizVolt = []
cuantos = int(vin/precision)
if(cuantos > LIMITE_ARRAY):
 logging.error("Array demasiado grande "+ str(cuantos) + ">" + str(LIMITE_ARRAY))
 raise NameError("Array demasiado grande "+ str(cuantos) + ">" + str(LIMITE_ARRAY))
else:
 for i in range(cuantos):
  MatrizVolt.append(0)

def registrarVoltageEnVector(vector, vout, precision, error_precision): #vector(int or float list): donde estan los voltages de cada combinacion de resistencias, vout(float): tension de salida, precision(float): precision minima de mdida, error_precision(int): espacio a error ~ error: +/- error_precision * precision.
 position = int(vout/precision)
 if(position >= len(vector)):
  logging.debug("Se ha pasado")
  return False 
 elif(vector[position] > 0):
  logging.debug("posicion:"+ str(position) + ">" + '0')
  return False  
 else:
  if(position == 0):
   if(vector[position + error_precision] > 0):
    logging.debug("posicion + " + str(error_precision) + ":"+ str(position + error_precision) + ">" + '0')
    return False
   else:
    vector[position] = vector[position] + 1
    return True
  elif(position == (len(vector) - 1)):
   if(vector[position - error_precision] > 0):
    logging.debug("posicion - " + str(error_precision) + ":"+ str(position - error_precision) + ">" + '1')
    return False
   else:
    vector[position] = vector[position] + 1 
    return True
  else:
   if(vector[position + error_precision] > 0):
    logging.debug("posicion + " + str(error_precision) + ":"+ str(position + error_precision) + ">" + '1')
    return False
   elif(vector[position - error_precision] > 0):
    logging.debug("posicion - " + str(error_precision) + ":"+ str(position - error_precision) + ">" + '1')
    return False
   else:
    vector[position] = vector[position] + 1 
    return True

#TEST:
#print registrarVoltageEnVector(MatrizVolt, 0,precision,ERROR_DE_PRECISION)
#print registrarVoltageEnVector(MatrizVolt, 5,precision,ERROR_DE_PRECISION)
#print registrarVoltageEnVector(MatrizVolt, 1.25,precision,ERROR_DE_PRECISION)
#print registrarVoltageEnVector(MatrizVolt, 1.251,precision,ERROR_DE_PRECISION)
#print registrarVoltageEnVector(MatrizVolt, 1.244,precision,ERROR_DE_PRECISION)

def resistenciaGenerica(resitencias):
 resistenciaTotal = 0.0
 for i in resitencias:
  if(type(i) != type([])):
   resistenciaTotal = resistenciaTotal + (i * 1.0)
  else:
   resistenciaTotalParllel = 0.0
   for j in i:
    resistenciaTotalParllel = resistenciaTotalParllel + (1 * 1.0)/j
   resistenciaTotal = resistenciaTotal + (1*1.0)/ (resistenciaTotalParllel)
 return resistenciaTotal

#print resistenciaGenerica([1,2,3,400,5.5])
#print resistenciaGenerica([0,2,3,0,5.5])
#print resistenciaGenerica([1,[1,5,8,9],3,[1,400],5.5])

def voltageDivider(r1,r2,vin):
 return vin * ((r2 * 1.0) / (r1 + r2))

#print voltageDivider(1,1,5)
#print voltageDivider(2,1,5)
#print voltageDivider(1,2,5)
#print voltageDivider(50,1000,5)

def voltageDividerVector(resistencias1, resistencias2, vin):
 resistenciaTotal1 = resistenciaGenerica(resistencias1)
 resistenciaTotal2 = resistenciaGenerica(resistencias2)
 return voltageDivider(resistenciaTotal1, resistenciaTotal2, vin)

def test_resistenciasIguales(cuantas, vin, precision):
    r = [10,13,15,18,22,27,33,39,47,56,68,82]
    multiplos = 4
    #Voy provando una por una y saco las que pasan el test.
    r1 = []
    r2 = []
    #r1.append(r)
    #r2.append(r)
    res = r
    for i in range(multiplos):
        for t in range(len(res)):
             r1.append(r[t] * 10**i)
             r2.append(r[t] * 10**i)
    todos = []#Para sacalos a todos
    mejor = [0,0,0]
    for r11 in r1:
        for r22 in r2:
            #if(__test_resistencias(r11,r22,vin,precision, cuantas) != None):
                salida = __test_resistencias_minPrecision(r11,r22,vin, cuantas)
                if (mejor[0] < salida):
                    mejor = [salida , r11 ,r22] 
                print "Con las resistencias r1, r2 y vin: ",r11,r22,vin," la precision minima es:\n",  salida
    print "El mejor es:",mejor
    
    
def __test_resistencias(r11,r22,vin,precision, cuantas):
    tensiones = []
    for i in range(cuantas):
        tensiones.append(voltageDivider(r11 + r11 * i, r22, vin))
    anterior = tensiones[0]
    for j in tensiones[1:]:
        if(anterior - j < precision):
            return None
        else:
            anterior = j
    return tensiones

def __test_resistencias_minPrecision(r11,r22,vin, cuantas):
    tensiones = []
    for i in range(cuantas):
        tensiones.append(voltageDivider(r11 + r11 * i, r22, vin))
    anterior = tensiones[0]
    for j in range(len(tensiones[1:])):
        #print anterior - tensiones[1:][j]
        if(j == 0):
            precision = anterior - tensiones[1:][j]
        elif(anterior - tensiones[1:][j] < precision):
            precision = anterior - tensiones[1:][j]
        anterior = tensiones[1:][j]
    return precision
            
            
    
#print voltageDividerVector([10,10,10,10,10], [r2], vin)

#test_resistenciasIguales(5, 5, 0.1)
#El mejor es: [0.2786276223776225, 15, 68]


print __test_resistencias_minPrecision(15, 68, 5, 5)
#for i in range(5):
#    print "voltios para ",10 + 10 * i,voltageDivider(10 + 10 * i, 100, 5)


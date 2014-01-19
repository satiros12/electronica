#Python
import math
import random
import logging
from datetime import datetime
from Combinatoria import combinatoriaBooleana

class CaluclosElectronicos:
 def __init__(self):
  #logging.debuf(str(datetime.now())
  logging.basicConfig(filename=str(datetime.now()),level=logging.DEBUG)
  self.BaseResistencias = self.cargarBaseResistencias()
    
 def cargarBaseResistencias(self):
  BaseResistencias = [10,12,15,18,22,27,33,39,47,56,68,82]
  Resistencias = []
  Nivelresistencia = range(0,5)
  for i in BaseResistencias:
   for j in Nivelresistencia:
    Resistencias.append((1.0 * i) +  (10**j))
  return Resistencias
  
 def divisorTension(self, r1, r2, vin):
  return (vin * r2)/(r1 + r2)

 def provarCombinaciones(self,listaResistencias, precision, r2, vin):
  VECES_PRECISION = 2
  logging.basicConfig(filename='salida',level=logging.DEBUG)
  combiancion = self.combinatoria(listaResistencias)
  for caso in combiancion:
   
   resultado = []
   for resistencia in caso: #Rellenar resultado
    resultado.append(self.divisorTension(resistencia * 1.0,r2,vin))
   logging.debug("Resultado: " + str(resultado))
   falloEncontrado = False
   for result in range(len(resultado) - 1):
    for rango in resultado[(result+1):]:
     logging.debug("Prueva con: " + str(resultado[result]) + " y " + str(rango))
     if((resultado[result] < precision) or (rango < precision)):
      logging.debug("Fallo: " + str(resultado[result]) + " o " + str(rango) + "<"+ str(precision))
      falloEncontrado = True
      break;
     if(abs(resultado[result]-rango) < (VECES_PRECISION * precision)):      
      logging.debug("Fallo: abs" + str(resultado[result]) + "-" + str(rango) + " = "+ str(abs(resultado[result]-rango)) +" >= " + str((VECES_PRECISION * precision)))
      falloEncontrado = True
      break;
    if(falloEncontrado):
     break;
   if(not falloEncontrado):
    print "Caso: " + str(caso) + "  Resultado: " + str(resultado)
  
 def combinatoria(self, lista):
  combiancion = combinatoriaBooleana(len(lista))
  for i in combiancion: #Cada combinacion [r1,r2,r3,r4,...]
   for j in range(len(i)):
    if i[j]:
     i[j] = lista[j]
    else:
     i[j] = 0
  return combiancion

 def lessVariationVoltSameResistences(self, r1, r2, n, vin):
  lessVariation = 0
  last = self.divisorTension(r1,r2,vin)
  index = 2
  lessVariation = last - self.divisorTension(r1 * index,r2,vin)
  while (index <= n):
   index = index + 1
   newV = self.divisorTension(r1 * index,r2,vin)
   logging.debug("Variacion nueva: " + str(last)+" - "+ str(newV)+" = "+ str(last - newV) + "  Variacion actual: "+str(lessVariation))
   if(lessVariation > (last - newV)):
    lessVariation = (last - newV)
   last = newV
  return lessVariation

 def seleccionarAleatorioLista(self, lista, cuantos, repetidos):
  if(not repetidos):
   if(len(lista) < cuantos):
    raise NameError("La lista es pequenia")
    return None
   else:
    listaSlaida = []
    escogidos = []
    for i in range(0, cuantos):
     termino = False
     while (not termino):
      reslutadoRandom = random.randint(0,len(lista))
      termino = True
      for j in escogidos:
       if(j == reslutadoRandom):
        termino = False
      if(termino):
        escogidos.append(termino)
       #terminar

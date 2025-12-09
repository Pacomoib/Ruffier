'''Un módulo para calcular el resultado del test de Ruffier.


Idealmente, la suma de la frecuencia cardíaca debe ser medida en tres intentos (antes del ejercicio físico, inmediatamente después y después de un pequeño descanso)
no debe exceder más de 200 latidos por minuto.
Proponemos que los niños midan su pulso por 15 segundos
y encuentren el resultado de latidos por minuto multiplicándolo por 4:
   S = 4 * (P1 + P2 + P3)
Mientras más lejano sea el resultado de los 200 latidos, peor es.
Tradicionalmente, las tablas son dadas por valores divididos entre 10.


Índice de Ruffier  
   IR = (S - 200) / 10
es evaluado correspondiente a la edad según la tabla:
       7-8             9-10                11-12               13-14               15+ (¡solo para adolescentes!)
perf.    6.4 y menos    4.9  y menos       3.4  y menos         1.9  y menos               0.4  y menos
bueno    6.5 - 11.9     5 - 10.4          3.5 - 8.9           2 - 7.4                   0.5 - 5.9
sat.  12 - 16.9      10.5 - 15.4       9 - 13.9            7.5 - 12.4                6 - 10.9
débil  17 - 20.9      15.5 - 19.4       14 - 17.9           12.5 - 16.4               11 - 14.9
insat.   21 y más     19.5 y más      18 y más          16.5 y más              15 y más


para todas las edades, la diferencia entre los resultados débil e insatisfactorio es 4,
la diferencia entre los resultados débil y satisfactorio es 5 y la diferencia entre los resultados bueno y satisfactorio es 5.5


por lo tanto, vamos a programar la función ruffier_result(r_index, level) que recibiría
el índice de Ruffier calculado y el nivel "insatisfactorio" para la edad probada de la persona y retornará el resultado


'''
# aquí puedes especificar las cadenas que representan el resultado:
txt_index = "Tu Índice de Ruffier: "
txt_workheart = "Rendimiento cardíaco: "
txt_nodata = '''
no hay datos para esta edad'''
txt_res = []
txt_res.append('''bajo.
¡Ve a ver a tu doctor de inmediato!''')
txt_res.append('''satisfactorio.
¡Consulta tu doctor!''')
txt_res.append('''promedio.
Tal vez valga la pena hacerse unas pruebas adicionales con el doctor.''')
txt_res.append('''
más alto que el promedio''')
txt_res.append('''
alto''')


def ruffier_index(P1, P2, P3):
   '''retorna el valor del índice según los tres cálculos de pulso para su comparación con la tabla'''
   return (4 * (P1+P2+P3) - 200) / 10


def neud_level(age):
   '''las opciones con una edad menor que 7 y con adultos deben ser procesadas por separado;
   aquí seleccionamos el nivel “insatisfactorio” solo dentro de la tabla:
   para la edad de 7, “insatisfactorio” es un índice de 21, luego en adelante cada 2 años disminuye en 1.5 hasta el nivel de 15 a los 15-16 años'''
   norm_age = (min(age, 15) - 7) // 2  # hasta los 15, cada 2 años la diferencia entre la edad y 7 años debe ser tomada como 1
   result = 21 - norm_age * 1.5 # cada 2 años de la diferencia debe ser multiplicado por 1.5; de esta forma los niveles en la tabla están distribuidos
   return result
  
def ruffier_result(r_index, level):
   '''la función obtiene el índice de Ruffier y lo interpreta,
   retornamos el nivel de preparación: un número del 0 al 4
   (mientras más alto el nivel de preparación, mejor).'''
   if r_index >= level:
       return 0
   level = level - 4 # esto no se ejecutará si ya se retornó la respuesta “insatisfactorio”
   if r_index >= level:
       return 1
   level = level - 5 # de manera análoga, terminamos aquí si el nivel es, como mínimo, “satisfactorio”
   if r_index >= level:
       return 2
   level = level - 5.5 # siguiente nivel
   if r_index >= level:
       return 3
   return 4 # terminamos aquí si el índice es menor que todos los niveles intermedios, es decir, la persona evaluada tiene grandes resultados.


def test(P1, P2, P3, age):
   '''esta función puede ser usada fuera del módulo para calcular el índice de Ruffier.
   Retorna los textos terminados que serán colocados en el lugar correcto
   Para los textos, usa las constantes especificadas al inicio del módulo.'''
   if age < 7:
       return (txt_index + "0", txt_nodata) # Esto es un misterio más allá de esta prueba
   else:
       ruff_index = ruffier_index(P1, P2, P3) # cálculo
       result = txt_res[ruffier_result(ruff_index, neud_level(age))] # la interpretación; conversión del valor numérico del nivel fitness a texto
       res = txt_index + str(ruff_index) + '\n' + txt_workheart + result
       return res

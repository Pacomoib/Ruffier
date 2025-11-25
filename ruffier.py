''' Módulo para calcular los resultados de los tests de Ruffier.


La suma de las tres entradas en lecturas de pulso (antes del esfuerzo, después del esfuerzo y justo después de un pequeño descanso)

idealmente, no debe haber más de 200 latidos por minuto.

Proponemos que los niños midan su pulso por 15 segundos y encuentren el resultado de latidos por minuto multiplicándolo por 4:

   S = 4 * (P1 + P2 + P3)

Mientras más lejano sea el resultado de los 200 latidos, peor es.

Tradicionalmente, las tablas son dadas por valores divididos entre 10.


Índice de Ruffier  

   IR = (S - 200) / 10

es evaluado correspondiente a la edad según la tabla:

       7–8             9–10                11–12               13–14               15+ (¡solo para adolescentes)

perfecto    6.4 y menos   4.9 y menos       3.4 y menos         1.9 y menos               0.4 y menos

bueno    6.5–11.9     5–10.4          3.5–8.9           2–7.4                   0.5–5.9

satisfactorio  12–16.9      10.5–15.4       9–13.9            7.5–12.4                6–10.9

débil  17–20.9      15.5–19.4       14–17.9           12.5–16.4               11–14.9

insatisfactorio   21 y más     19.5 y más      18 y más          16.5 y más             15 y más


el resultado “insatisfactorio” es 4 del resultado “débil” para todas las edades, “débil” se separa de “satisfactorio” por 5 y “bueno” de “satisfactorio” por 5.5


así que escribiremos una función ruffier_result(r_index, level) que producirá el índice Ruffier calculado y el nivel “insatisfactorio” para la edad probada y producirá un resultado


'''

# estas son las líneas que producen el resultado

txt_index = "Tu índice de Ruffier: "

txt_workheart = "Eficiencia del corazón: "

txt_nodata = '''

no hay datos para edad'''

txt_res = []

txt_res.append('''bajo.

¡Visita a tu doctor de inmediato!''')

txt_res.append('''satisfactory.

¡Visita a tu doctor de inmediato!''')

txt_res.append('''promedio.

Tal vez valga la pena hacerse unas pruebas adicionales con el doctor.''')

txt_res.append('''

más alto que el promedio''')

txt_res.append('''

alto''')


def ruffier_index(P1, P2, P3):

   ''' Retorna el valor del índice según los tres cálculos de pulso para su comparación con la tabla'''

   return (4 * (P1+P2+P3) - 200) / 10


def neud_level(age):

   ''' las opciones con una edad menor que 7 y con adultos deben ser procesadas por separado,

   aquí seleccionamos el nivel “insatisfactorio” solo dentro de la tabla:

   para la edad de 7, “insatisfactorio” es un índice de 21, luego en adelante cada 2 años disminuye en 1.5 hasta el nivel de 15 a los 15-16 años '''

   norm_age = (min(age, 15) - 7) // 2  # cada dos años desde los siete años se convierte en una unidad, hasta los 15 años

   result = 21 - norm_age * 1.5 # cada dos años se multiplica la diferencia por 1.5, así son organizados los niveles en la tabla

   return result

 

def ruffier_result(r_index, level):

   ''' la función obtiene el índice de Ruffier y lo interpreta, retornamos el nivel de preparación: un número del 0 al 4 (mientras más alto el nivel de preparación, mejor).  '''

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

   return 4 # terminamos aquí si el índice es menor que todos los niveles intermedios, es decir, el círculo probado.


def test(P1, P2, P3, age):
    #'esta función puede ser usada desde afuera del módulo para calcular el índice de Ruffier.'

   #'Retornamos los textos listos que solo necesitan ser escritos en el lugar necesario'

   #'Usamos las constantes usadas al inicio del módulo para textos.'

    if age < 7:
        return (txt_index + "0", txt_nodata) # Esto es un misterio más allá de esta prueba

    else:
        ruff_index = ruffier_index(P1, P2, P3) # cálculo

    result = txt_res[ruffier_result(ruff_index, neud_level(age))] # la interpretación y conversión del nivel de preparación numérica a dato de texto

    res = txt_index + str(ruff_index) + '\n' + txt_workheart + result

    return res
# Importa la clase base para aplicaciones Kivy
from kivy.app import App

# Importa el gestor de pantallas y la clase base Screen
from kivy.uix.screenmanager import ScreenManager, Screen

# Importa layouts y widgets que se usarán en la interfaz
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView

# Importa textos predefinidos desde otros archivos
from instructions import txt_instruction, txt_test1, txt_test2, txt_test3, txt_sits

# Importa la función que evalúa el índice Ruffier
from ruffier import test

# Importa el widget personalizado Seconds, usado como temporizador
from seconds import Seconds

# Variables globales para almacenar datos del usuario y mediciones del pulso
age = 7
name = ""
p1, p2, p3 = 0, 0, 0


def check_int(str_num):
   # Intenta convertir una cadena en un entero; si falla, devuelve False
   try:
       return int(str_num)
   except:
       return False


# ------------------------------------------------------------------------------------
# PANTALLA 1: Pantalla de instrucciones y entrada de nombre/edad
# ------------------------------------------------------------------------------------
class InstrScr(Screen):
  def __init__(self, **kwargs):
      # Llama al constructor de la clase padre (Screen)
      super().__init__(**kwargs)

      # Texto inicial con instrucciones
      instr = Label(text=txt_instruction)

      # Etiqueta para pedir el nombre
      lbl1 = Label(text='Ingresa tu nombre:', halign='right')

      # Entrada de texto para el nombre
      self.in_name = TextInput(multiline=False)

      # Etiqueta para la edad
      lbl2 = Label(text='Ingresa tu edad:', halign='right')

      # Entrada para la edad, con valor inicial 7
      self.in_age = TextInput(text='7', multiline=False)

      # Botón para continuar al siguiente paso
      self.btn = Button(text='Iniciar', size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5})

      # Asigna la función "next" a la acción on_press del botón
      self.btn.on_press = self.next

      # Primera línea horizontal: etiqueta + caja de texto del nombre
      line1 = BoxLayout(size_hint=(0.8, None), height='30sp')

      # Segunda línea horizontal: etiqueta + caja de texto de edad
      line2 = BoxLayout(size_hint=(0.8, None), height='30sp')

      # Rellena los layouts con los widgets
      line1.add_widget(lbl1)
      line1.add_widget(self.in_name)
      line2.add_widget(lbl2)
      line2.add_widget(self.in_age)

      # Layout principal vertical
      outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
      outer.add_widget(instr)
      outer.add_widget(line1)
      outer.add_widget(line2)
      outer.add_widget(self.btn)

      # Agrega el layout principal a la pantalla
      self.add_widget(outer)

  def next(self):
      # Obtiene valores de nombre y edad
      name = self.in_name.text
      age = check_int(self.in_age.text)

      # Valida edad (debe ser un número mayor o igual a 7)
      if age == False or age < 7:
         age = 7
         self.in_age.text = str(age)
      else:
         # Avanza a la siguiente pantalla
         self.manager.current = 'pulse1'


# ------------------------------------------------------------------------------------
# PANTALLA 2: Primer medición del pulso (15 segundos)
# ------------------------------------------------------------------------------------
class PulseScr(Screen):
  def __init__(self, **kwargs):
      super().__init__(**kwargs)

      # Indica si ya se terminó el tiempo y se puede avanzar
      self.next_screen = False
    
      # Texto con instrucciones
      instr = Label(text=txt_test1)

      # Widget Seconds de 15 segundos
      self.lbl_sec = Seconds(15)

      # Se conecta la propiedad 'done' del temporizador a la función sec_finished
      self.lbl_sec.bind(done=self.sec_finished)

      # Línea con entrada para escribir el resultado del conteo
      line = BoxLayout(size_hint=(0.8, None), height='30sp')
      lbl_result = Label(text='Ingresa el resultado:', halign='right')
      self.in_result = TextInput(text='0', multiline=False)

      # Deshabilitada al inicio para obligar al usuario a esperar los 15 segundos
      self.in_result.set_disabled(True)
    
      line.add_widget(lbl_result)
      line.add_widget(self.in_result)

      # Botón para iniciar temporizador o continuar
      self.btn = Button(text='Iniciar', size_hint=(0.3, 0.4), pos_hint={'center_x': 0.5})
      self.btn.on_press = self.next

      # Layout general
      outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
      outer.add_widget(instr)
      outer.add_widget(self.lbl_sec)
      outer.add_widget(line)
      outer.add_widget(self.btn)

      self.add_widget(outer)

  def sec_finished(self, *args):
      # Llamado cuando el temporizador 'Seconds' termina
      self.next_screen = True
      self.in_result.set_disabled(False)  # Permite capturar el pulso
      self.btn.set_disabled(False)        # Reactiva el botón
      self.btn.text = 'Continuar'         # Cambia el texto del botón

  def next(self):
      # Si el temporizador NO ha terminado, iniciarlo
      if not self.next_screen:
          self.btn.set_disabled(True)
          self.lbl_sec.start()
      else:
          # Procesar entrada del pulso
          global p1
          p1 = check_int(self.in_result.text)

          # Si no es número válido, corregir a 0
          if p1 == False or p1 <= 0:
              p1 = 0
              self.in_result.text = str(p1)
          else:
              # Avanzar
              self.manager.current = 'sits'


# ------------------------------------------------------------------------------------
# PANTALLA 3: Instrucción para hacer sentadillas
# ------------------------------------------------------------------------------------
class CheckSits(Screen):
  def __init__(self, **kwargs):
      super().__init__(**kwargs)

      # Texto con indicaciones para las sentadillas
      instr = Label(text=txt_sits)

      # Botón para continuar
      self.btn = Button(text='Continuar', size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5})
      self.btn.on_press = self.next

      outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
      outer.add_widget(instr)
      outer.add_widget(self.btn)
      self.add_widget(outer)

  def next(self):
      # Pasa a la siguiente fase del pulso
      self.manager.current = 'pulse2'


# ------------------------------------------------------------------------------------
# PANTALLA 4: Segundo y tercer registro del pulso (15s + descanso + 15s)
# ------------------------------------------------------------------------------------
class PulseScr2(Screen):
  def __init__(self, **kwargs):

      # Inicialmente no se puede avanzar
      self.next_screen = False

      # Controla en qué fase estamos: 0 = primer pulso, 1 = descanso, 2 = segundo pulso
      self.stage = 0

      super().__init__(**kwargs)

      instr = Label(text=txt_test3)

      # Temporizador de 15 segundos (primer pulso)
      self.lbl_sec = Seconds(15)
      self.lbl_sec.bind(done=self.sec_finished)

      # Texto superior que cambia según la fase
      self.lbl1 = Label(text='Cuenta tu pulso')

      # Layout para la primera medición
      line1 = BoxLayout(size_hint=(0.8, None), height='30sp')
      lbl_result1 = Label(text='Resultado:', halign='right')
      self.in_result1 = TextInput(text='0', multiline=False)

      line1.add_widget(lbl_result1)
      line1.add_widget(self.in_result1)

      # Layout para la medición después del descanso
      line2 = BoxLayout(size_hint=(0.8, None), height='30sp')
      lbl_result2 = Label(text='Resultado después de descanso:', halign='right')
      self.in_result2 = TextInput(text='0', multiline=False)

      line2.add_widget(lbl_result2)
      line2.add_widget(self.in_result2)

      # Ambas entradas inicialmente deshabilitadas
      self.in_result1.set_disabled(True)
      self.in_result2.set_disabled(True)

      # Botón para iniciar o completar
      self.btn = Button(text='Iniciar', size_hint=(0.3, 0.5), pos_hint={'center_x': 0.5})
      self.btn.on_press = self.next

      # Layout principal
      outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
      outer.add_widget(instr)
      outer.add_widget(self.lbl1)
      outer.add_widget(self.lbl_sec)
      outer.add_widget(line1)
      outer.add_widget(line2)
      outer.add_widget(self.btn)
      self.add_widget(outer)

  def sec_finished(self, *args):
     # Fase 0: terminó primer conteo
     if self.lbl_sec.done:
         if self.stage == 0:
             self.stage = 1
             self.lbl1.text = 'Descansa'
             # Arranca 30 segundos para descanso
             self.lbl_sec.restart(30)
             self.in_result1.set_disabled(False)  # Activar resultado 1

         # Fase 1: terminó el descanso
         elif self.stage == 1:
             self.stage = 2
             self.lbl1.text='Cuenta tu pulso'
             # Nueva ronda de 15 segundos
             self.lbl_sec.restart(15)

         # Fase 2: terminó segundo conteo
         elif self.stage == 2:
             self.in_result2.set_disabled(False)
             self.btn.set_disabled(False)
             self.btn.text = 'Completar'
             self.next_screen = True

  def next(self):
      # Si aún estamos corriendo un temporizador, iniciarlo
      if not self.next_screen:
           self.btn.set_disabled(True)
           self.lbl_sec.start()
      else:
           # Guardar resultados
           global p2, p3
           p2 = check_int(self.in_result1.text)
           p3 = check_int(self.in_result2.text)

           # Validaciones
           if p2 == False:
               p2 = 0
               self.in_result1.text = str(p2)
           elif p3 == False:
               p3 = 0
               self.in_result2.text = str(p3)
           else:
               # Ir al resultado final
               self.manager.current = 'result'


# ------------------------------------------------------------------------------------
# PANTALLA 5: Resultado del índice Ruffier
# ------------------------------------------------------------------------------------
class Result(Screen):
  def __init__(self, **kwargs):
      super().__init__(**kwargs)

      # Layout principal
      self.outer = BoxLayout(orientation='vertical', padding=8, spacing=8)

      # Etiqueta donde se mostrará el puntaje Ruffier
      self.instr = Label(text = '')

      self.outer.add_widget(self.instr)
      self.add_widget(self.outer)

      # Ejecuta la función "before" al entrar a la pantalla
      self.on_enter = self.before

  def before(self):
      # Calcula y muestra el resultado con nombre y valores p1,p2,p3
      global name
      self.instr.text = name + '\n' + test(p1, p2, p3, age)


# ------------------------------------------------------------------------------------
# APLICACIÓN PRINCIPAL
# ------------------------------------------------------------------------------------
class HeartCheck(App):
  def build(self):
      # Crea un gestor de pantallas
      sm = ScreenManager()

      # Se agregan las pantallas con nombres para navegación
      sm.add_widget(InstrScr(name='instr'))
      sm.add_widget(PulseScr(name='pulse1'))
      sm.add_widget(CheckSits(name='sits'))
      sm.add_widget(PulseScr2(name='pulse2'))
      sm.add_widget(Result(name='result'))

      return sm


# Instancia y ejecuta la aplicación
app = HeartCheck()
app.run()

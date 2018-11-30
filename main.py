from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json

import os

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

class ImageButton1(ButtonBehavior, Image):
    source = 'locais.jpeg'

class ImageButton2(ButtonBehavior, Image):
    source = 'objetos.jpeg'

class ImageButton3(ButtonBehavior, Image):
    source = 'sair.jpeg'
class ImageAdd(ButtonBehavior, Image):
    source='plus.jpeg'
class ImageLoad(ButtonBehavior,Image):
    source='load.jpeg'
class ImageSave(ButtonBehavior, Image):
    source='save.jpeg'

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

caminho = ''
textodoobjeto = ''
textodolocal = ''
foto_local = ''

class MyImageWidget(Screen):
    def __init__(self,**kwargs):
        global caminho
        caminho = App.get_running_app().user_data_dir+'/'
        super(MyImageWidget,self).__init__(**kwargs)
        self.image = Image(source=caminho+'Resposta.png')
        self.add_widget(self.image)
        Clock.schedule_interval(self.update_pic,1)

    def update_pic(self,dt):
        self.image.reload()

class NaoEncontrado(Screen):
    def __init__(self,**kwargs):
        super(NaoEncontrado, self).__init__(**kwargs)
        self.image = Image(source='notfound.jpeg')
        self.add_widget(self.image)

class DefinaImagem(Screen):
    def __init__(self,**kwargs):
        super(DefinaImagem, self).__init__(**kwargs)
        self.image = Image(source='selecionefoto.jpeg')
        self.add_widget(self.image)


class Gerenciador(ScreenManager):
    
    pass

class Menu(Screen):
    pass

class Test(App):
    def build(self):
        return Gerenciador()

class Local(BoxLayout):
    def __init__(self,text='',**kwargs):
        super(Local, self).__init__(**kwargs)
        self.ids.label2.text = text

class Locais(Screen):
    locais = []
    def on_pre_enter(self):
        global caminho
        caminho = App.get_running_app().user_data_dir+'/'
        self.ids.box2.clear_widgets()
        self.loadData()
        Window.bind(on_keyboard=self.voltar)
        for local in self.locais:
            self.ids.box2.add_widget(Local(text=local))

    def voltar(self,window,key,*args):
        if key == 27:
            App.get_running_app().root.current = 'menu'
            return True

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)

    def loadData(self,*args):
        global caminho
        try:        
            with open(caminho+'data2.json', 'r') as data:
                try:
                    self.locais = json.load(data)
                except ValueError:
                    pass
        except FileNotFoundError:
            pass

    def saveData(self, *args):
        global caminho
        with open(caminho+'data2.json', 'w') as data:
            json.dump(self.locais,data)

    def removeWidget2(self, local):
        texto = local.ids.label2.text
        self.ids.box2.remove_widget(local)
        self.locais.remove(texto)
        self.saveData()

    def addWidget2(self):
        texto = self.ids.texto2.text
        self.ids.box2.add_widget(Local(text=texto))
        self.ids.texto2.text = ''
        self.locais.append(texto)
        self.saveData()

class Objeto(BoxLayout):
    def __init__(self,text='',**kwargs):
        super(Objeto, self).__init__(**kwargs)
        self.ids.label.text = text

class Objetos(Screen):
    objetos = []

    def on_pre_enter(self):
        global caminho
        self.ids.box.clear_widgets()
        caminho = App.get_running_app().user_data_dir+'/'
        self.loadData()
        Window.bind(on_keyboard=self.voltar)
        for objeto in self.objetos:
            self.ids.box.add_widget(Objeto(text=objeto))

    def voltar(self,window,key,*args):
        if key == 27:
            App.get_running_app().root.current = 'menu'
            return True

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)

    def loadData(self,*args):
        try:        
            with open(caminho+'data.json', 'r') as data:
                try:
                    self.objetos = json.load(data)
                except ValueError:
                    pass
        except FileNotFoundError:
            pass

    def saveData(self, *args):
        with open(caminho+'data.json', 'w') as data:
            json.dump(self.objetos,data)

    def removeWidget(self, objeto):
        texto = objeto.ids.label.text
        self.ids.box.remove_widget(objeto)
        self.objetos.remove(texto)
        self.saveData()

    def addWidget(self):
        texto = self.ids.texto.text
        self.ids.box.add_widget(Objeto(text=texto))
        self.ids.texto.text = ''
        self.objetos.append(texto)
        self.saveData()
    
    def encontrarObjeto(self, x):
        global imagem_resposta
        global foto_local
        foto = caminho+x
        foto_L = caminho+foto_local
        try:
            #Imagem padrao
            img = cv.imread(foto_L,0)
            img2 = img.copy()
            try:
	        #Imagem a ser encontrada na imagem padrao
                template = cv.imread(foto,0)
                w, h = template.shape[::-1]
    
                # All the 6 methods for comparison in a list
                #methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
                        #'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
        
                img = img2.copy()
                method = eval('cv.TM_CCOEFF_NORMED')
    
	        # Apply template Matching
                res = cv.matchTemplate(img,template,method)
                min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        
                top_left = max_loc
            
                bottom_right = (top_left[0] + w, top_left[1] + h)
                cv.rectangle(img,top_left, bottom_right, 255, 2)
        
            #plt.subplot(121),plt.imshow(template,cmap = 'gray')
            #plt.title('Objeto da busca'), plt.xticks([]), plt.yticks([])
        
                plt.plot(122),plt.imshow(img,cmap = 'gray')
                plt.title('Ponto detectado'), plt.xticks([]), plt.yticks([])
                plt.suptitle(x)
    
            #para criar uma nova figura!
                fig = plt.gcf() #getcurrentfigure
                fig.savefig(caminho+'Resposta.png')

                App.get_running_app().root.current = 'resposta'
            #plt.show() #faz em formato de executavel
            except cv.error as e:
                App.get_running_app().root.current = 'naoencontrado'
        except AttributeError:
            App.get_running_app().root.current = 'definaimagem'

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Root2(Screen):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)

    def fotoDoLocal(self, text):
        global foto_local
        foto_local = text

    def textoDoLocal(self, local):
        global textodolocal
        textodolocal = local.ids.label2.text

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()


    def load(self, filename):
        self.ids.image2.source = filename[0]

        self.dismiss_popup()

    def save(self):
	with open((self.ids.image2.source), 'rb') as f:
            data = f.read()
        with open(caminho+textodolocal, 'rw') as stream: #mudado pra rw
            stream.write(data)

        self.dismiss_popup()

class Root(Screen):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)

    def textoDoObjeto(self, objeto):
        global textodoobjeto
        textodoobjeto = objeto.ids.label.text

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()


    def load(self, filename):
        self.ids.image.source = filename[0]

        self.dismiss_popup()

    def save(self):
	with open((self.ids.image.source), 'rb') as f:
            data = f.read()
        with open(caminho+textodoobjeto, 'rw') as stream: #mudado pra rw
            stream.write(data)

        self.dismiss_popup()


Test().run()

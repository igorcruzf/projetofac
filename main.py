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
import json

import os
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

caminho = ''
textodatarefa = ''

class MyImageWidget(Screen):
    def __init__(self,**kwargs):
        super(MyImageWidget,self).__init__(**kwargs)
        self.image = Image(source='Resposta.png')
        self.add_widget(self.image)
        Clock.schedule_interval(self.update_pic,1)

    def update_pic(self,dt):
        self.image.reload()


class Gerenciador(ScreenManager):
    pass

class Menu(Screen):
    pass

class Test(App):
    def build(self):
        return Gerenciador()

class Tarefa(BoxLayout):
    def __init__(self,text='',**kwargs):
        super(Tarefa, self).__init__(**kwargs)
        self.ids.label.text = text

class Tarefas(Screen):
    tarefas = []
    def on_pre_enter(self):
        global caminho
        self.ids.box.clear_widgets()
        caminho = App.get_running_app().user_data_dir+'/'
        self.loadData()
        Window.bind(on_keyboard=self.voltar)
        for tarefa in self.tarefas:
            self.ids.box.add_widget(Tarefa(text=tarefa))

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
                    self.tarefas = json.load(data)
                except ValueError:
                    pass
        except FileNotFoundError:
            pass

    def saveData(self, *args):
        with open(caminho+'data.json', 'w') as data:
            json.dump(self.tarefas,data)

    def removeWidget(self, tarefa):
        texto = tarefa.ids.label.text
        self.ids.box.remove_widget(tarefa)
        self.tarefas.remove(texto)
        self.saveData()

    def addWidget(self):
        texto = self.ids.texto.text
        self.ids.box.add_widget(Tarefa(text=texto))
        self.ids.texto.text = ''
        self.tarefas.append(texto)
        self.saveData()
    
    def encontrarObjeto(self, x):
        global imagem_resposta
        foto = caminho+x
    
        #Imagem padrao
        img = cv.imread('Foto.jpg',0)
        img2 = img.copy()
    
        #Imagem a ser encontrada na imagem padrao
        template = cv.imread(foto,0)
        w, h = template.shape[::-1]
    
        # All the 6 methods for comparison in a list
        #methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
                    #'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
        
        img = img2.copy()
        method = eval('cv.TM_CCOEFF_NORMED')
    
        try:
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
            fig.savefig('Resposta.png')

        #plt.show() #faz em formato de arquivo
        except:
            pass

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(Screen):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)

    def textoDaTarefa(self, tarefa):
        global textodatarefa
        textodatarefa = tarefa.ids.label.text

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
        with open(caminho+textodatarefa, 'w') as stream:
            stream.write(data)

        self.dismiss_popup()


Test().run()

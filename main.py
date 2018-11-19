from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

import os
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

class Imagem(Screen):
    pass

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
    def __init__(self,tarefas=[],**kwargs):
        super(Tarefas, self).__init__(**kwargs)
        for tarefa in tarefas:
            self.ids.box.add_widget(Tarefa(text=tarefa))

    def on_pre_enter(self):
        Window.bind(on_keyboard=self.voltar)

    def voltar(self,window,key,*args):
        if key == 27:
            App.get_running_app().root.current = 'menu'
            return True

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)

    def addWidget(self):
        texto = self.ids.texto.text
        self.ids.box.add_widget(Tarefa(text=texto))
        self.ids.texto.text = ''
        x = texto
        if x == 'bicicleta':
          foto = 'Foto2.jpg'
    
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
	im = Image(source = 'Resposta.png')
        im.reload()
    
        #plt.show() #faz em formato de arquivo

Test().run()

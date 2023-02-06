import customtkinter
import os
import subprocess
from PIL import Image
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
from time import sleep
import http.client
from datetime import datetime, timedelta
import time
import requests

#creamos las funciones principales
def sendMessage(para, mensaje):
    url = 'http://localhost:3001/lead'
    realone = int(para)
    data = {
        "message": mensaje,
        "phone": realone
    }
    headers = {
        'Content-Type':'application/json'
    }
    print(data)
    response = requests.post(url, json=data, headers=headers)
    time.sleep(10)
    return response

def iniciar_bot_turnos():
    df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSsDgSbzbApG4oRhjP7fMPzDZL1h23aLJlUUS-sRdEO43O0Fg6uKCFEDTgxnocSI_Z93_3r0I0N7jII/pub?gid=0&single=true&output=csv')
    group_size = 19
    # Crear lista para almacenar los grupos
    group_list = []
    # Iterar sobre los grupos
    for i in range(28):
        start = i * (group_size + 6)
        end = start + group_size
        df_group = df.iloc[start:end]
        group_list.append(df_group)
    # Asignar nombres a los grupos
    for i, df_group in enumerate(group_list, 1):
        globals()[f'df{i}'] = df_group
    for i in range(1,29):
        globals()[f'df{i}'] = globals()[f'df{i}'].rename(columns={"Fecha y Hora": "Hora"})
        globals()[f'df{i}'].insert(4, 'Hora1', globals()[f'df{i}']['Hora']) 
        globals()[f'df{i}'].insert(8, 'Hora2', globals()[f'df{i}']['Hora'])
        globals()[f'df{i}'].insert(12, 'Hora3', globals()[f'df{i}']['Hora'])
        fecha = [globals()[f'df{i}'].iloc[0]['Hora']] * 19
        globals()[f'df{i}'].insert(0, 'fecha', fecha)
        globals()[f'df{i}'].insert(5, 'fecha1', fecha)
        globals()[f'df{i}'].insert(10, 'fecha2', fecha)
        globals()[f'df{i}'].insert(15, 'fecha3', fecha)
        #globals()[f'df{i}'] = globals()[f'df{i}'].drop(0)
        aux1 = globals()[f'df{i}'].iloc[:, :5]
        aux2 = globals()[f'df{i}'].iloc[:, 5:10]
        aux3 = globals()[f'df{i}'].iloc[:, 10:15]
        aux4 = globals()[f'df{i}'].iloc[:, 15:20]
        aux2.columns = aux1.columns
        aux3.columns = aux1.columns
        aux4.columns = aux1.columns
        globals()[f'df{i}'] = pd.concat([aux1, aux2, aux3, aux4], ignore_index=True)
    for i in range(1,29):
        globals()[f'df{i}'] = globals()[f'df{i}'].drop(0)
    df_list = [eval("df" + str(i)) for i in range(1, 29)]
    # Concatena los 28 dataframes en un solo dataframe
    df = pd.concat(df_list, axis=0)
    # Obtener fecha actual
    ahora = datetime.now()
    # Calcular fechas para los próximos tres días
    fechas = [ahora + timedelta(days=x) for x in range(1,4)]
    # cambiamos el tipo de dato de fechas a datetime``
    fechas = [datetime.strftime(x, '%Y-%d-%m') for x in fechas]
    #cambiamos el tipo de dato de la columna fecha a datetime
    df['fecha'] = pd.to_datetime(df['fecha'])
    # Filtramos los datos para las fechas que nos interesan
    df = df[df['fecha'].isin(fechas)]
    #cambiamos el tipo de dato de la columna fecha a string
    df['fecha'] = df['fecha'].astype(str)
    #separamos la columna fecha por el espacio
    df['fecha'] = df['fecha'].str.split(' ', expand=True)
    #borramos las filas que no tienen datos en la columna de nombre y numero
    df = df.dropna(subset=['Nombre'])
    df = df.dropna(subset=['Numero'])
   
    #envia el mensaje a los numeros de whatsapp
    numbers = df['Numero'].head(72)
    def init(mensaje):
        for number in numbers:
            if isinstance(number, str):
                # Código a ejecutar si number es una cadena de texto
                sendMessage(str(number), f"{mensaje}")
            else:
                # Código a ejecutar si number no es una cadena de texto
                pass
    men='Hola, '+df.Nombre.head(1).values[0]+'! Te recordamos que tu turno es el '+df.fecha.head(1).values[0]+' a las '+df.Hora.head(1).values[0]+'. Te esperamos en Vuela! Saludos, Vuela.'
    init(men)
    

def iniciar_chatbot():
    import subprocess
    subprocess.Popen('./node/base-baileys-memory/base-bailey-memory-win32-x64/base-bailey-memory.exe')  
def ejecutar_comandos1():
    
    directorio = "C:/Users/Desarrollo/Desktop/botfinal"

   
    resultado1 = subprocess.run("npm install", cwd=directorio, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    salida1 = resultado1.stdout.decode("utf-8")
    print(salida1)
    print('PASO 1 TERMINADO')
def ejecutar_comandos2():
    directorio = "C:/Users/Desarrollo/Desktop/botfinal"
    resultado2 = subprocess.run("npm run build", cwd=directorio, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    salida2 = resultado2.stdout.decode("utf-8")
    print(salida2)
    print('PASO 2 TERMINADO')
def ejecutar_comandos3():
    directorio = "C:/Users/Desarrollo/Desktop/botfinal"
    print('PASO 3 COMENZO')
    resultado3 = subprocess.run("npm run dev", cwd=directorio, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    salida3 = resultado3.stdout.decode("utf-8")
    print(salida3)
    print('PASO 3 TERMINADO')


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Vuela_Bot.py")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./\\CustomTkinter-master\\examples\\test_images")

        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logovuela.png")), size=(70, 70))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  ", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Bot Turnos",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 3",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        
        
        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="Iniciar Bot Turnos",command=iniciar_bot_turnos)
        self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=100)
        self.home_frame_button_2 = customtkinter.CTkButton(self.home_frame, text="Iniciar Chatbot",command=iniciar_chatbot)
        self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)


        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=1)
        
        self.second_frame_button_1 = customtkinter.CTkButton(self.second_frame, text="Iniciar Bot Turnos",command=iniciar_bot_turnos)
        self.second_frame_button_1.grid(row=1, column=0, padx=20, pady=100)
        self.second_frame_button_2 = customtkinter.CTkButton(self.second_frame, text="Iniciar Chatbot",command=iniciar_chatbot)
        self.second_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        
        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame.grid_columnconfigure(0, weight=1)

        self.third_frame_button_1 = customtkinter.CTkButton(self.third_frame, text="Iniciar Sesion1",command=ejecutar_comandos1)
        self.third_frame_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.third_frame_button_2 = customtkinter.CTkButton(self.third_frame, text="Iniciar Sesion2",command=ejecutar_comandos2)
        self.third_frame_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.third_frame_button_3 = customtkinter.CTkButton(self.third_frame, text="Iniciar Sesion3",command=ejecutar_comandos3)
        self.third_frame_button_3.grid(row=3, column=0, padx=20, pady=10)


        



        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")
    
    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = App()
    app.mainloop()
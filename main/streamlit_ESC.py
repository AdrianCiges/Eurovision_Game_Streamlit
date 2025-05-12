import streamlit as st
import random
import numpy as np
import regex as re
import warnings
import time
import statistics as stats
from operator import itemgetter
import matplotlib.pyplot as plt
import plotly.colors
from wordcloud import WordCloud
import cv2 
warnings.filterwarnings("ignore")
# from sklearn.metrics import mean_squared_error as mse
# from sklearn.metrics import r2_score as r2
import pandas as pd
from pandas.api.types import is_numeric_dtype, is_datetime64_any_dtype, is_categorical_dtype
from catboost import CatBoostRegressor as CTR
from sklearn.model_selection import train_test_split as tts
from joblib import Parallel, delayed
import requests as req
from bs4 import BeautifulSoup as bs
import time
# import asyncio
# import websockets
import json
# from pytube import YouTube
import os
from IPython.display import HTML
import datetime
import plotly.graph_objects as go
import plotly.express as px
import plotly.subplots as sp
import bar_chart_race as bcr
import ffmpeg

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from statistics import mean
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from PIL import Image
import base64
import io

# chrome_options = Options()
# chrome_options.add_argument('--headless')  # Ejecutar en modo headless
# chrome_options.add_argument('--disable-gpu')  # Desactivar aceleración de GPU

# # Iniciar el navegador Chrome en modo "headless"
# PATH = ChromeDriverManager().install()
# driver = webdriver.Chrome(executable_path=PATH, options=chrome_options)

# URL de la página web con la tabla
url = 'https://eurovisionworld.com/odds/eurovision'

st.set_page_config(layout="wide", page_title="Eurovision Game", page_icon="./img/escicon.png")
st.write('')

def highlight_rows(s):
    '''
    Esta función aplica estilos CSS a las primeras tres filas de la tabla.
    '''
    if s.name == 1:
        return ['background-color: gold'] * len(s)
    elif s.name == 2:
        return ['background-color: silver'] * len(s)
    elif s.name == 3:
        return ['background-color: #e1c3b5'] * len(s)
    elif s.name in [4,5,6,7,8,9,10]:
        return ['background-color: #d5edf1'] * len(s)
    else:
        return [''] * len(s)

def get_songs(cancion):
    
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "3600",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    }
    label_codes = {
        "Albania 🇦🇱 ": 0,
        "Andorra 🇦🇩 ": 1,
        "Armenia 🇦🇲 ": 2,
        "Australia 🇦🇺 ": 3,
        "Austria 🇦🇹 ": 4,
        "Azerbaijan 🇦🇿 ": 5,
        "Belarus 🇧🇾 ": 6,
        "Belgium 🇧🇪 ": 7,
        "Bosnia and Herzegovina 🇧🇦 ": 8,
        "Bulgaria 🇧🇬 ": 9,
        "Croatia 🇭🇷 ": 10,
        "Cyprus 🇨🇾 ": 11,
        "Czechia 🇨🇿 ": 12,
        "Denmark 🇩🇰 ": 13,
        "Estonia 🇪🇪 ": 14,
        "Finland 🇫🇮 ": 15,
        "France 🇫🇷 ": 16,
        "Georgia 🇬🇪 ": 17,
        "Germany 🇩🇪 ": 18,
        "Greece 🇬🇷 ": 19,
        "Hungary 🇭🇺 ": 20,
        "Iceland 🇮🇸 ": 21,
        "Ireland 🇮🇪 ": 22,
        "Israel 🇮🇱 ": 23,
        "Italy 🇮🇹 ": 24,
        "Latvia 🇱🇻 ": 25,
        "Lithuania 🇱🇹 ": 26,
        "Malta 🇲🇹 ": 27,
        "Moldova 🇲🇩 ": 28,
        "Montenegro 🇲🇪 ": 30,
        "North Macedonia 🇲🇰 ": 31,
        "Norway 🇳🇴 ": 32,
        "Poland 🇵🇱 ": 33,
        "Portugal 🇵🇹 ": 34,
        "Romania 🇷🇴 ": 35,
        "Russia 🇷🇺 ": 36,
        "San Marino 🇸🇲 ": 37,
        "Serbia 🇷🇸 ": 38,
        "Slovakia 🇸🇰 ": 40,
        "Slovenia 🇸🇮 ": 41,
        "Spain 🇪🇸 ": 42,
        "Sweden 🇸🇪 ": 43,
        "Switzerland 🇨🇭 ": 44,
        "Netherlands 🇳🇱 ": 45,
        "Turkey 🇹🇷 ": 46,
        "Ukraine 🇺🇦 ": 47,
        "United Kingdom 🇬🇧 ": 48 }
    song = []
    pais = []
    views = []
    likes = []
    shazams = []


    st.write('Buscando en YouTube')

    try:
        url = ("https://www.youtube.com/results?search_query=" + cancion["song"].replace(' ','+').strip() +"+"+ cancion["singer"].replace(' ','+').strip() +"+"+ "Official")
        link_video = 'https://www.youtube.com/watch?v=' + (req.get(f"{url}").text).split('/watch?v=')[1].split(',')[0].replace('"', "")
        html = req.get(link_video, headers = {"Accept-Language": "es-ES,es;q=0.9"}).text
        video_likes = int(html.split("Me gusta en este vídeo junto con otras ")[1].split(" personas")[0].replace('.',''))
        video_views = int(re.search(r'"videoViewCountRenderer":\s*{.*?"simpleText":"([\d\.]+) visualizaciones"', html).group(1).replace('.', ''))
        song.append(cancion["song"] + " " + cancion["singer"]) # Añado la canción(just to see, después dropearé)
        pais.append(label_codes[cancion["country"]]) # Añado el label del país según mi dictio
        time.sleep(random.randint(5, 7))
        views.append(video_views)
        likes.append(video_likes)
    except:
        views.append(0)
        likes.append(0)
        song.append(cancion["song"] + " " + cancion["singer"]) # Añado la canción(just to see, después dropearé)
        pais.append(label_codes[cancion["country"]]) # Añado el label del país según mi dictio

    st.write('Buscando en Shazam')

    try:
        link_shazam_search = 'https://www.shazam.com/services/search/v4/es/ES/web/search?term='+cancion['song']+'%20'+cancion['singer']+'&numResults=1&offset=0&types=artists,songs&limit=1'
        json_shazam = json.loads(req.get(link_shazam_search).text)
        link_shazam_search = json_shazam['tracks']['hits'][0]['track']['url']
        json_shazam = req.get(link_shazam_search).text
        
        html = json_shazam.split('TrackPageHeader_floatingCount')[1]
        shazams_text = html.split('TrackPageHeader_count')[1].split('Text-module_fontWeightNormal')[1].split('>')[1].split('<')[0]
        
        shazams_count = int(shazams_text.replace(",", "").replace(".", ""))
        shazams_count

        #meter aqui la cantidad
        shazams.append(shazams_count)
    except:
        print(f"Cancion {cancion} no encontrada en Shazam")
        shazams.append(0)

    tabla0 = pd.DataFrame()
    tabla0["cancion"] = song
    tabla0["pais"] = pais
    tabla0["views"] = views
    tabla0["likes"] = likes
    tabla0["shazams"] = shazams

    return tabla0

def get_songs_ESC23(cancion):
    
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "3600",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    }
    label_codes = {
        "Albania 🇦🇱 ": 0,
        "Andorra 🇦🇩 ": 1,
        "Armenia 🇦🇲 ": 2,
        "Australia 🇦🇺 ": 3,
        "Austria 🇦🇹 ": 4,
        "Azerbaijan 🇦🇿 ": 5,
        "Belarus 🇧🇾 ": 6,
        "Belgium 🇧🇪 ": 7,
        "Bosnia and Herzegovina 🇧🇦 ": 8,
        "Bulgaria 🇧🇬 ": 9,
        "Croatia 🇭🇷 ": 10,
        "Cyprus 🇨🇾 ": 11,
        "Czechia 🇨🇿 ": 12,
        "Denmark 🇩🇰 ": 13,
        "Estonia 🇪🇪 ": 14,
        "Finland 🇫🇮 ": 15,
        "France 🇫🇷 ": 16,
        "Georgia 🇬🇪 ": 17,
        "Germany 🇩🇪 ": 18,
        "Greece 🇬🇷 ": 19,
        "Hungary 🇭🇺 ": 20,
        "Iceland 🇮🇸 ": 21,
        "Ireland 🇮🇪 ": 22,
        "Israel 🇮🇱 ": 23,
        "Italy 🇮🇹 ": 24,
        "Latvia 🇱🇻 ": 25,
        "Lithuania 🇱🇹 ": 26,
        "Malta 🇲🇹 ": 27,
        "Moldova 🇲🇩 ": 28,
        "Montenegro 🇲🇪 ": 30,
        "North Macedonia 🇲🇰 ": 31,
        "Norway 🇳🇴 ": 32,
        "Poland 🇵🇱 ": 33,
        "Portugal 🇵🇹 ": 34,
        "Romania 🇷🇴 ": 35,
        "Russia 🇷🇺 ": 36,
        "San Marino 🇸🇲 ": 37,
        "Serbia 🇷🇸 ": 38,
        "Slovakia 🇸🇰 ": 40,
        "Slovenia 🇸🇮 ": 41,
        "Spain 🇪🇸 ": 42,
        "Sweden 🇸🇪 ": 43,
        "Switzerland 🇨🇭 ": 44,
        "Netherlands 🇳🇱 ": 45,
        "Turkey 🇹🇷 ": 46,
        "Ukraine 🇺🇦 ": 47,
        "United Kingdom 🇬🇧 ": 48 }
    

    youtube_codes_dics = {  'Sweden 🇸🇪 ': 'https://www.youtube.com/watch?v=WK3HOMhAeQY',
                            'Austria 🇦🇹 ': 'https://www.youtube.com/watch?v=-ieSTNpxvio',
                            'France 🇫🇷 ': 'https://www.youtube.com/watch?v=Pj2DTSLcNnI',
                            'Israel 🇮🇱 ': 'https://www.youtube.com/watch?v=Q3BELu4z6-U',
                            'Netherlands 🇳🇱 ': 'https://www.youtube.com/watch?v=hEHwr5k9pd0',
                            'Finland 🇫🇮 ' : 'https://www.youtube.com/watch?v=Kg3QoTpnqyw',
                            'Estonia 🇪🇪 ': 'https://www.youtube.com/watch?v=5MS_Fczs_98',
                            'Belgium 🇧🇪 ': 'https://www.youtube.com/watch?v=oVrsnGFmuss',
                            'Ukraine 🇺🇦 ': 'https://www.youtube.com/watch?v=Dv4Zp_FG0qg',
                            'Albania 🇦🇱 ': 'https://www.youtube.com/watch?v=RNT1SmmxuIk',
                            'Malta 🇲🇹 ': 'https://www.youtube.com/watch?v=sLVSwfRRvMA',
                            'United Kingdom 🇬🇧 ': 'https://www.youtube.com/watch?v=-hu6R3ZnOdY',
                            'Italy 🇮🇹 ': 'https://www.youtube.com/watch?v=mfAf9-5Oevw',
                            'San Marino 🇸🇲 ': 'https://www.youtube.com/watch?v=Le3WpaLYRvE',
                            'Czechia 🇨🇿 ': 'https://www.youtube.com/watch?v=kpdQtYrEBTs',
                            'Lithuania 🇱🇹 ': 'https://www.youtube.com/watch?v=R2f2aZ6Fy58',
                            'Cyprus 🇨🇾 ': 'https://www.youtube.com/watch?v=rbfQqWyqgJw',
                            'Greece 🇬🇷 ': 'https://www.youtube.com/watch?v=ew1pujFTd1o',
                            'Australia 🇦🇺 ': 'https://www.youtube.com/watch?v=_08I6mjHSLA',
                            'Germany 🇩🇪 ': 'https://www.youtube.com/watch?v=zJplC4-9Scs',
                            'Ireland 🇮🇪 ': 'https://www.youtube.com/watch?v=-wnjg9jZEcM',
                            'Switzerland 🇨🇭 ': 'https://www.youtube.com/watch?v=dGX54zRExR8',
                            'Georgia 🇬🇪 ': 'https://www.youtube.com/watch?v=c3wu0dUNd4c',
                            'Norway 🇳🇴 ': 'https://www.youtube.com/watch?v=h7jkEmoBvU0',
                            'Portugal 🇵🇹 ': 'https://www.youtube.com/watch?v=-s1Cc2uEj3U',
                            'Poland 🇵🇱 ': 'https://www.youtube.com/watch?v=YXHHDjiclxA',
                            'Slovenia 🇸🇮 ': 'https://www.youtube.com/watch?v=qTS2L0VcaVI',
                            'Azerbaijan 🇦🇿 ': 'https://www.youtube.com/watch?v=upbiPJ9uA70',
                            'Denmark 🇩🇰 ': 'https://www.youtube.com/watch?v=gdCAgiSIOUc',
                            'Spain 🇪🇸 ': 'https://www.youtube.com/watch?v=BvVxhbCW9rw',
                            'Latvia 🇱🇻 ': 'https://www.youtube.com/watch?v=b1_t79mQkm4',
                            'Armenia 🇦🇲 ': 'https://www.youtube.com/watch?v=zm-Kil8Hm9Q',
                            'Romania 🇷🇴 ': 'https://www.youtube.com/watch?v=LVHu_KwHiKY',
                            'Serbia 🇷🇸 ': 'https://www.youtube.com/watch?v=18BCbtvDcag',
                            'Croatia 🇭🇷 ': 'https://www.youtube.com/watch?v=xOodVfY8hCs',
                            'Iceland 🇮🇸 ': 'https://www.youtube.com/watch?v=s9P83Nl6D1M',
                            'Montenegro 🇲🇪 ': 'https://www.youtube.com/watch?v=_zs0yq39aFA'
                            }

    song = []
    pais = []
    views = []
    likes = []
    shazams = []


    st.write('Buscando en YouTube')

    try:
        
       # link_video = 'https://www.youtube.com/watch?v=' + youtube_codes_dics[cancion['country']] + '&list=PLVf2bg851geTD_adqUqpSvGDVTqQwLZW6'
        link_video = youtube_codes_dics[cancion['country']]
        html = req.get(link_video, headers = {"Accept-Language": "es-ES,es;q=0.9"}).text
        video_likes = int(html.split("Me gusta en este vídeo junto con otras ")[1].split(" personas")[0].replace('.',''))
        video_views = int(re.search(r'"videoViewCountRenderer":\s*{.*?"simpleText":"([\d\.]+) visualizaciones"', html).group(1).replace('.', ''))
        song.append(cancion["song"] + " " + cancion["singer"]) # Añado la canción(just to see, después dropearé)
        pais.append(label_codes[cancion["country"]]) # Añado el label del país según mi dictio
        time.sleep(random.randint(5, 7))
        views.append(video_views)
        likes.append(video_likes)
    except:
        views.append(0)
        likes.append(0)
        song.append(cancion["song"] + " " + cancion["singer"]) # Añado la canción(just to see, después dropearé)
        pais.append(label_codes[cancion["country"]]) # Añado el label del país según mi dictio

    st.write('Buscando en Shazam')

    try:
        link_shazam_search = 'https://www.shazam.com/services/search/v4/es/ES/web/search?term='+cancion['song']+'%20'+cancion['singer']+'&numResults=1&offset=0&types=artists,songs&limit=1'
        json_shazam = json.loads(req.get(link_shazam_search).text)
        link_shazam_search = json_shazam['tracks']['hits'][0]['track']['url']
        json_shazam = req.get(link_shazam_search).text
        
        try: 
            html = json_shazam.split('TrackPageHeader_floatingCount')[1]
            shazams_text = html.split('TrackPageHeader_count')[1].split('Text-module_fontWeightNormal')[1].split('>')[1].split('<')[0]
        except:
            shazams_text = json_shazam.split('TrackPageHeader_floatingCount')[0].split('TrackPageHeader_count')[1].split('\\"className\\')[-2].split('\\')[-2]
        
        shazams_count = int(shazams_text.replace(",", "").replace(".", "").replace('"',''))
        shazams_count

        #meter aqui la cantidad
        shazams.append(shazams_count)
    except:
        print(f"Cancion {cancion} no encontrada en Shazam")
        shazams.append(0)

    tabla0 = pd.DataFrame()
    tabla0["cancion"] = song
    tabla0["pais"] = pais
    tabla0["views"] = views
    tabla0["likes"] = likes
    tabla0["shazams"] = shazams

    return tabla0

def row_data(user_songs):
    
    fecha_actual = datetime.datetime.now()
    fecha_actual_str = fecha_actual.strftime("%Y-%m-%d")
    hora_actual = fecha_actual.time()
    hora_actual_mas_2h = (datetime.datetime.combine(datetime.date.min, hora_actual) + datetime.timedelta(hours=2)).time()
    hora_actual_mas_2h_str = hora_actual_mas_2h.strftime("%H:%M:%S")

    st.write('')
    st.markdown(f'##### 🔎 Scrappeando visitas y likes (en YouTube) y shazams de las canciones seleccionadas a día {fecha_actual_str} a las {hora_actual_mas_2h_str} españolas')
    time.sleep(1)
    st.write('')
    st.markdown('##### 🤯 Esto puede tardar unos segundos. Interval act time!')
    
    time.sleep(1)
    st.write('')
    st.video('https://www.youtube.com/watch?v=Cv6tgnx6jTQ') 

    tablas_songs = Parallel(n_jobs=6, verbose=True)(delayed(get_songs)(d) for d in user_songs)

    tabla0 = pd.DataFrame()
    tabla0 = pd.concat(tablas_songs, axis=0)

    return tabla0

def row_data_ESC23(user_songs):

    fecha_actual = datetime.datetime.now()
    fecha_actual_str = fecha_actual.strftime("%Y-%m-%d")
    hora_actual = fecha_actual.time()
    hora_actual_mas_2h = (datetime.datetime.combine(datetime.date.min, hora_actual) + datetime.timedelta(hours=2)).time()
    hora_actual_mas_2h_str = hora_actual_mas_2h.strftime("%H:%M:%S")
    
    st.write('')
    st.markdown(f'##### 🔎 Scrappeando visitas y likes (en YouTube) y shazams de las canciones seleccionadas a día {fecha_actual_str} a las {hora_actual_mas_2h_str} españolas')
    time.sleep(1)
    st.write('')
    st.markdown('##### 🤯 Esto puede tardar unos segundos. Recap time!')
    
    time.sleep(1)
    st.write('')
    st.video('https://www.youtube.com/watch?v=ygniu2fDTkc') 

    tablas_songs = Parallel(n_jobs=6, verbose=True)(delayed(get_songs_ESC23)(d) for d in user_songs)

    tabla0 = pd.DataFrame()
    tabla0 = pd.concat(tablas_songs, axis=0)

    return tabla0

def puntos_reales(propo12, num_paises):
    return round(2*((0.0009984580569663269+11.961021107218633*propo12)*num_paises))

def predicciones(user_songs):

    tabla0 = row_data(user_songs)

    # LIMPIEZA

    # LIMPIEZA SHAZAMS

    int_shazams = []
    for shz in tabla0["shazams"]:
        if shz == "" or shz == 0:
            pass
        elif (type(shz) != int) and ("." in shz):
            int_shazams.append(int(shz.replace(".", "")))
        else:
            int_shazams.append(int(shz))

    shazams_bien = []
    for shz in tabla0["shazams"]:
        if type(shz) != int:
            shazams_bien.append(int(shz.replace(".", "")))
        elif (shz == 0 and type(shz) == int) or (shz == "" and type(shz) != int):
            shazams_bien.append(stats.mean(int_shazams))  # ← ERROR AQUÍ
        else:
            shazams_bien.append(int(shz))
            tabla0["shazams"] = shazams_bien

    # DAMOS DE APUESTA DE LA MEDIA HISTÓRICA (20 AÑOS) DEL PAÍS SELECCIONADO
    dictio_odds = {
        0: 342.37403011887017,
        1: 550.0,
        2: 190.04180672268907,
        3: 153.65840943043887,
        4: 303.57951388888887,
        5: 124.09745687748783,
        6: 355.31930026912727,
        7: 265.7936595875654,
        8: 72.9090909090909,
        9: 317.92552826510723,
        10: 304.23496732026143,
        11: 250.0217893876849,
        12: 419.6993137254902,
        13: 164.99074074074073,
        14: 255.3253267973856,
        15: 239.6154970760234,
        16: 116.43540161678706,
        17: 321.21309523809526,
        18: 162.8079961255047,
        19: 114.66420278637773,
        20: 216.79786324786326,
        21: 180.43704850361198,
        22: 270.40350877192986,
        23: 247.20045278637772,
        24: 35.95748225286925,
        25: 334.80882352941177,
        26: 268.8539251896511,
        27: 204.14866099071207,
        28: 234.4282765737874,
        29: 550.0,
        30: 446.10648148148147,
        31: 389.5522875816994,
        32: 68.06107384474257,
        33: 323.12762399077275,
        34: 351.8961076711387,
        35: 153.54299965600276,
        36: 58.391149810801515,
        37: 424.0443756449949,
        38: 300.6666666666667,
        40: 550.0,
        41: 387.5357920946156,
        42: 130.99342555735745,
        43: 14.644885706914343,
        44: 301.1869806094183,
        45: 142.5697150556129,
        46: 76.81818181818181,
        47: 63.61367202729045,
        48: 67.0881239250086}
    tabla0["bet_mean"] = [dictio_odds[c] for c in tabla0["pais"]]

    # REORDENO TABLA
    tabla0 = tabla0[["pais", "bet_mean", "views", "likes", "shazams"]]
    tabla0.rename(columns={"pais": "country","views": "views_propos","likes": "likes_propos","shazams": "shazams_propos",},inplace=True,)

    # CREANDO PROPORCIONES
    tabla0["views_propos"] = [v / tabla0["views_propos"].sum() for v in tabla0["views_propos"]]
    tabla0["likes_propos"] = [l / tabla0["likes_propos"].sum() for l in tabla0["likes_propos"]]
    tabla0["shazams_propos"] = [s / tabla0["shazams_propos"].sum() for s in tabla0["shazams_propos"]]
    #print(tabla0)

    # PREDICCIONES
    pred = list(ctr.predict(tabla0))
    participantes = len(user_songs)

    prediction_result = []
    for i, dictio in enumerate(user_songs):

        dictio["points"] = puntos_reales(pred[i], participantes-1)       
        prediction_result.append(dictio)

    prediction_result = sorted(prediction_result, key=itemgetter("points"), reverse=False)

    return prediction_result

def predicciones_now(user_songs):

    tabla0 = row_data_ESC23(user_songs)

    # LIMPIEZA

    # LIMPIEZA SHAZAMS

    int_shazams = []
    for shz in tabla0["shazams"]:
        if shz == "" or shz == 0:
            pass
        elif (type(shz) != int) and ("." in shz):
            int_shazams.append(int(shz.replace(".", "")))
        else:
            int_shazams.append(int(shz))

    shazams_bien = []
    for shz in tabla0["shazams"]:
        if type(shz) != int:
            shazams_bien.append(int(shz.replace(".", "")))
        elif (shz == 0 and type(shz) == int) or (shz == "" and type(shz) != int):
            if int_shazams:  # Verifica que no esté vacía
                shazams_bien.append(stats.mean(int_shazams))
            else:
                shazams_bien.append(0)  # o cualquier valor por defecto
        else:
            shazams_bien.append(int(shz))
    tabla0["shazams"] = shazams_bien

    # SCRAPPEO LA CUOTA DE APUESTAS ACTUALIZADA
    
    pais_odds = {'Albania 🇦🇱 ': 0, 'Andorra 🇦🇩 ': 1, 'Armenia 🇦🇲 ': 2, 'Australia 🇦🇺 ': 3, 'Austria 🇦🇹 ': 4, 'Azerbaijan 🇦🇿 ': 5, 'Belarus 🇧🇾 ': 6, 'Belgium 🇧🇪 ': 7, 'Bosnia and Herzegovina 🇧🇦 ': 8, 'Bulgaria 🇧🇬 ': 9, 'Croatia 🇭🇷 ': 10, 'Cyprus 🇨🇾 ': 11, 'Czechia 🇨🇿 ': 12, 'Denmark 🇩🇰 ': 13, 'Estonia 🇪🇪 ': 14, 'Finland 🇫🇮 ': 15, 'France 🇫🇷 ': 16, 'Georgia 🇬🇪 ': 17, 'Germany 🇩🇪 ': 18, 'Greece 🇬🇷 ': 19, 'Hungary 🇭🇺 ': 20, 'Iceland 🇮🇸 ': 21, 'Ireland 🇮🇪 ': 22, 'Israel 🇮🇱 ': 23, 'Italy 🇮🇹 ': 24, 'Latvia 🇱🇻 ': 25, 'Lithuania 🇱🇹 ': 26, 'Malta 🇲🇹 ': 27, 'Moldova 🇲🇩 ': 28, 'Monaco': 29, 'Montenegro 🇲🇪 ': 30, 'North Macedonia 🇲🇰 ': 31, 'Norway 🇳🇴 ': 32, 'Poland 🇵🇱 ': 33, 'Portugal 🇵🇹 ': 34, 'Romania 🇷🇴 ': 35, 'Russia 🇷🇺 ': 36, 'San Marino 🇸🇲 ': 37, 'Serbia 🇷🇸 ': 38, 'Slovakia 🇸🇰 ': 40, 'Slovenia 🇸🇮 ': 41, 'Spain 🇪🇸 ': 42, 'Sweden 🇸🇪 ': 43, 'Switzerland 🇨🇭 ': 44, 'Netherlands 🇳🇱 ': 45, 'Turkey 🇹🇷 ': 46, 'Ukraine 🇺🇦 ': 47, 'United Kingdom 🇬🇧 ': 48}
    

    fecha_actual = datetime.datetime.now()
    fecha_actual_str = fecha_actual.strftime("%Y-%m-%d")
    hora_actual_str = fecha_actual.strftime("%H:%M:%S")

    # st.markdown(f'##### Scrappeando visitas y likes (en YouTube) y shazams de las canciones seleccionadas a día {fecha_actual_str} a las {hora_actual_str}')

    scrap_odds =    {   'Sweden 🇸🇪 ': 2.13066666666667,
                        'Austria 🇦🇹 ': 4.35333333333333,
                        'France 🇫🇷 ': 13.2666666666667,
                        'Israel 🇮🇱 ': 19.9333333333333,
                        'Netherlands 🇳🇱 ': 27.8,
                        'Finland 🇫🇮 ': 27.1333333333333,
                        'Estonia 🇪🇪 ': 45.1333333333333,
                        'Belgium 🇧🇪 ': 23.8,
                        'Ukraine 🇺🇦 ': 118.266666666667,
                        'Albania 🇦🇱 ': 62.2666666666667,
                        'Malta 🇲🇹 ': 57.8666666666667,
                        'United Kingdom 🇬🇧 ': 144.533333333333,
                        'Italy 🇮🇹 ': 130.466666666667,
                        'San Marino 🇸🇲 ': 243.466666666667,
                        'Czechia 🇨🇿 ': 59.4,
                        'Lithuania 🇱🇹 ': 234.2,
                        'Cyprus 🇨🇾 ': 86.2,
                        'Greece 🇬🇷 ': 229.466666666667,
                        'Australia 🇦🇺 ': 164.133333333333,
                        'Germany 🇩🇪 ': 157.8,
                        'Ireland 🇮🇪 ': 164.8,
                        'Switzerland 🇨🇭 ': 38.6,
                        'Georgia 🇬🇪 ': 510.866666666667,
                        'Norway 🇳🇴 ': 240.8,
                        'Portugal 🇵🇹 ': 480.866666666667,
                        'Poland 🇵🇱 ': 227.533333333333,
                        'Slovenia 🇸🇮 ': 282.2,
                        'Azerbaijan 🇦🇿 ': 344.2,
                        'Denmark 🇩🇰 ': 314.2,
                        'Spain 🇪🇸 ': 158.6,
                        'Latvia 🇱🇻 ': 350.866666666667,
                        'Armenia 🇦🇲 ': 417.533333333333,
                        'Serbia 🇷🇸 ': 390.866666666667,
                        'Croatia 🇭🇷 ': 535.866666666667,
                        'Iceland 🇮🇸 ': 490.866666666667,
                        'Montenegro 🇲🇪 ': 494.2,
                        'Romania 🇷🇴 ': 460.866666666667
                    }

    dictio_odds = {pais_odds[key]: value for key, value in scrap_odds.items() if key in pais_odds}

    tabla0["bet_mean"] = [dictio_odds[c] for c in tabla0["pais"]]

    # REORDENO TABLA
    tabla0 = tabla0[["pais", "bet_mean", "views", "likes", "shazams"]]
    tabla0.rename(columns={"pais": "country","views": "views_propos","likes": "likes_propos","shazams": "shazams_propos",},inplace=True,)

    # st.write(tabla0)
    # CREANDO PROPORCIONES
    tabla0["views_propos"] = [v / tabla0["views_propos"].sum() for v in tabla0["views_propos"]]
    tabla0["likes_propos"] = [l / tabla0["likes_propos"].sum() for l in tabla0["likes_propos"]]
    tabla0["shazams_propos"] = [s / tabla0["shazams_propos"].sum() for s in tabla0["shazams_propos"]]
    #print(tabla0)

    st.write('')
    st.markdown('##### 🤔 Prediciendo resultados...')
    st.write('')

    # PREDICCIONES
    pred = list(ctr.predict(tabla0))
    participantes = len(user_songs)

    prediction_result = []
    for i, dictio in enumerate(user_songs):

        dictio["points"] = puntos_reales(pred[i], participantes-1)       
        prediction_result.append(dictio)

    prediction_result = sorted(prediction_result, key=itemgetter("points"), reverse=False)

    return prediction_result

def spotify_access_token():
    url = "https://accounts.spotify.com/api/token"

    payload=f"grant_type=refresh_token&refresh_token=AQAdp_4ZFLhLDSe3m6hvmqXfxZFWf2TQkfE35br2EGIFQ80N9t8BWihlDx-f21EgtWIff0TY95mEhNiwq_ryerMSIovlWfrd4q2CiWU-UfpP--UhnqeixNB6Wfj797bfV9M"
    headers = {
      'Authorization': 'Basic ZjA4ZTdkYjM3NTQzNGYzMjllNzMzMjkzMjIzNWFlOWM6YWE0NGE4YjhmODM4NGViYzhhMmNkMGFiYTY1Zjc4YjM=',
      'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = req.request("POST", url, headers=headers, data=payload).json()

    return response['access_token']

def create_playlist(name):
    token = spotify_access_token()
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : f"Bearer {token}"
        }
    data = {
        "name": name,
        "description": "Lista de reproducción autogenerada con las canciones de tu Eurovision Prediction Game",
        "public": False
        }
    response = req.post("https://api.spotify.com/v1/me/playlists", headers=headers, data=json.dumps(data))
    if response.status_code == 201:
        playlist_id = response.json()["id"]
        return playlist_id
    else:
        print(f"Failed to create playlist: {response.status_code} {response.reason}")

def add_to_playlist(tracks):
    tracks = list(reversed(tracks))
    token = spotify_access_token()
    playlist_id = create_playlist(list_name)
    
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : f"Bearer {token}"
        }
    
    
    params_search = {
        "type" : "track",
        "limit":"1"     
        }
    uris_raw = []
    for track in tracks:
        # print(f'adding track {track} to spotify playlist')
        params_search['q'] = track['song'] + " " + track['singer']
        
        try:
            response = req.get("https://api.spotify.com/v1/search", headers=headers, params=params_search)
        
            search_content = json.loads(response.text)
            uris_raw.append(search_content['tracks']['items'][0]['uri'])
        except:
            print(f'No es posible añadir canción {track} en lista de spoty')
            pass
        

    uris = ','.join(uris_raw)
    
    
    params_add_track = {
        "position" : "0",
        "uris" : uris # La uri de la canción (canciones)

    }
    playlist_id = playlist_id

    response = req.post(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=headers, params=params_add_track)
    
    link_spoty = f'https://open.spotify.com/playlist/{playlist_id}'
    #enlace_clicable = "<a href='" + link_spoty + "'>" + link_spoty + "</a>"
    return st.markdown(f'🎶 A disfrutar: [{link_spoty}]({link_spoty})')

countries = ['Albania 🇦🇱 ', 'Andorra 🇦🇩 ', 'Armenia 🇦🇲 ', 'Australia 🇦🇺 ', 'Austria 🇦🇹 ', 'Azerbaijan 🇦🇿 ', 'Belarus 🇧🇾 ', 'Belgium 🇧🇪 ', 'Bosnia and Herzegovina 🇧🇦 ', 'Bulgaria 🇧🇬 ', 'Croatia 🇭🇷 ', 'Cyprus 🇨🇾 ', 'Czechia 🇨🇿 ', 'Denmark 🇩🇰 ', 'Estonia 🇪🇪 ', 'Finland 🇫🇮 ', 'France 🇫🇷 ', 'Georgia 🇬🇪 ', 'Germany 🇩🇪 ', 'Greece 🇬🇷 ', 'Hungary 🇭🇺 ', 'Iceland 🇮🇸 ', 'Ireland 🇮🇪 ', 'Israel 🇮🇱 ', 'Italy 🇮🇹 ', 'Latvia 🇱🇻 ', 'Lithuania 🇱🇹 ', 'Malta 🇲🇹 ', 'Moldova 🇲🇩 ', 'Montenegro 🇲🇪 ', 'North Macedonia 🇲🇰 ', 'Norway 🇳🇴 ', 'Poland 🇵🇱 ', 'Portugal 🇵🇹 ', 'Romania 🇷🇴 ', 'Russia 🇷🇺 ', 'San Marino 🇸🇲 ', 'Serbia 🇷🇸 ', 'Slovakia 🇸🇰 ', 'Slovenia 🇸🇮 ', 'Spain 🇪🇸 ', 'Sweden 🇸🇪 ', 'Switzerland 🇨🇭 ', 'Netherlands 🇳🇱 ', 'Turkey 🇹🇷 ', 'Ukraine 🇺🇦 ', 'United Kingdom 🇬🇧 ']

num_part = [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48]


def get_available_countries(selected_countries):
    return [c for c in countries if c not in selected_countries]

@st.cache_data
def load_data_histo():
    df_histo = pd.read_excel('./data/data_to_race.xlsx')
    return df_histo


# ----------- PROBANDO FUNCION PARA FILTROS ⬇️------------------------------------------------------------------------------

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    modify = st.checkbox("👈 Añadir más filtros")
    if not modify:
        return df

    df = df.copy()

    # Cambiamos los nombres de columnas a las que queremos que salgan en los filtros -> Nombre USER FRIENDLY
    nuevos_nombres = ['key', 'country_id','País','Cantante/s','Canción','Año', 'Longitud letra', 'Palabras Únicas','Vecinos Participantes',
                      'Temática Amor', '1ª Palabra', '2ª Palabra', '3ª Palabra', '4ª Palabra', '5ª Palabra',
                      'Estructura','Finalista','Puntos','% Puntos','Clasificación','Orden actuación',
                      '1º Idioma','2º Idioma','3º Idioma','Views YT', 'Likes YT','Links','Estilo',
                      'Shazams','Duración Spotify','Duración ESC','PIB país','Ranking PIB','Ranking Influencia','Puntos Influencia','Ranking Reputación',
                      'reput_sci_tech','reput_cult','reput_peace_secur','reput_world_order','reput_planet_climate','reput_props_equal','reput_health_wellbeing',
                      'Cuota Apuestas']
    df.columns = nuevos_nombres

    modification_container = st.container()
    with modification_container:

        # Contenido del contenedor
        columnas_filtro = ['Cantante/s','Canción','Clasificación','Puntos','% Puntos','Finalista','Orden actuación','Estilo','1º Idioma','2º Idioma','3º Idioma','Temática Amor', 
                           '1ª Palabra', '2ª Palabra', '3ª Palabra', '4ª Palabra', '5ª Palabra', 'Estructura','Views YT', 'Likes YT', 'Shazams', 'Cuota Apuestas', 'Longitud letra', 'Palabras Únicas', 
                           'Duración ESC', 'Duración Spotify','PIB país', 'Ranking PIB', 'Ranking Influencia', 'Puntos Influencia', 'Ranking Reputación']
        to_filter_columns = st.multiselect("Filtrar por:", columnas_filtro, placeholder="Selecciona un campo")
        st.write('-----------')
        
        for column in to_filter_columns:
            # Si la columna es 'year', usa un widget especial
            if column == 'Año':
                left, right = st.columns((1, 20))
                # left.write("↳")
                min_year = int(df[column].min())
                max_year = int(df[column].max())
                user_year_input = right.slider(
                    f"Selecciona el año",
                    min_value=min_year,
                    max_value=max_year,
                    value=min_year,
                )
                st.write('-----------')
                df = df[df[column] == user_year_input]
            else:
                left, right = st.columns((1, 20))
                # left.write("↳")
                # Trata las columnas con < 10 valores únicos como categóricas
                if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                    user_cat_input = right.multiselect(
                        f"{column}",
                        sorted(df[column].unique()),
                        default=sorted(list(df[column].unique())),
                    )
                    st.write('-----------')
                    df = df[df[column].isin(user_cat_input)]

                elif column == 'Cuota Apuestas' or column == '% Puntos':
                    _min = float(df[column].min())
                    _max = float(df[column].max())
                    step = (_max - _min) / 100
                    user_num_input = right.slider(
                        f"{column}",
                        min_value=_min,
                        max_value=_max,
                        value=(_min, _max),
                        step=step,
                    )
                    st.write('-----------')

                elif is_numeric_dtype(df[column]):
                    _min = int(df[column].min())
                    _max = int(df[column].max())
                    step = (_max - _min) / 100
                    user_num_input = right.slider(
                        f"{column}",
                        min_value=_min,
                        max_value=_max,
                        value=(_min, _max),
                        step=1,
                    )
                    st.write('-----------')
                    df = df[df[column].between(*user_num_input)]
                elif is_datetime64_any_dtype(df[column]):
                    user_date_input = right.date_input(
                        f"{column}",
                        value=(
                            df[column].min(),
                            df[column].max(),
                        ),
                    )
                    st.write('-----------')
                    if len(user_date_input) == 2:
                        user_date_input = tuple(map(pd.to_datetime, user_date_input))
                        start_date, end_date = user_date_input
                        df = df.loc[df[column].between(start_date, end_date)]
                else:
                    user_text_input = right.text_input(
                        f"{column}",
                    )
                    st.write('-----------')
                    if user_text_input:
                        df = df[df[column].astype(str).str.contains(user_text_input)]

    # Cambiamos los nombres de columnas a los que entraros para que el código no se rompa -> Nombre ORIGINALES
    nuevos_nombres = ['key', 'country_id','country','artist','song','year', 'lyrics_long', 'unic_words','vecinos_participantes',
                      'love_song', 'top1word', 'top2word', 'top3word', 'top4word', 'top5word',
                      'estruc_resum','finalista','puntos_corregidos','propo_max_puntos','clasificacion','order_act',
                      'idioma1','idioma2','idioma3','views', 'likes','links','estilos',
                      'shazams','duracion_spoty','duracion_eurovision','GDP','orden_relativo_GDP','influ_ranking','influ_score','reput_ranking',
                      'reput_sci_tech','reput_cult','reput_peace_secur','reput_world_order','reput_planet_climate','reput_props_equal','reput_health_wellbeing',
                      'bet_mean']

    df.columns = nuevos_nombres

    return df
    
    
# ----------- PROBANDO FUNCION PARA FILTROS ⬆️------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------

tab1, tab2, tab3 = st.tabs(["🤖 Predicción Eurovisión 2025", "📊 Estadísticas 2002-2023", "🎶 Juego Eurovisión"])

# ---------------------------------------------------------------------------------------------------------------------------

with tab1:

    st.markdown('<h1 style="text-align:center"><span style="font-size: 40px;">📈</span> <u>PREDICCIONES EUROVISIÓN 2025</u></h1>', unsafe_allow_html=True)
    st.write('')
    st.write('')
    st.success('En este apartado podrás realizar una predicción en vivo de las canciones participantes en el Festival de Eurovisión del sábado 17 de mayo de 2025.')
    st.warning('⚠️ La fiabilidad de las predicciones es mayor conforme se acerca el festival y, sobretodo, después de las semifinales (13 y 15 de mayo de 2025).')

    # CARGAMOS DATA TO TRAIN
    @st.cache_data
    def load_data():
        data = pd.read_excel("./data/Data_to_train.xlsx")
        data.drop("Unnamed: 0", axis=1, inplace=True)
        return data

    @st.cache_data
    def split_data(data):
        X = data.drop("propo_puntos", axis=1)
        y = data.propo_puntos
        X_train, X_test, y_train, y_test = tts(
            X, y, train_size=0.99, test_size=0.01, random_state=22
        )
        return X_train, X_test, y_train, y_test

    @st.cache_data
    def train_model(X_train, y_train):
        ctr = CTR(iterations=5, verbose=False)
        ctr.fit(X_train, y_train)
        return ctr

    data = load_data()
    X_train, X_test, y_train, y_test = split_data(data)
    ctr = train_model(X_train, y_train)
    y_pred = ctr.predict(X_test)


    if __name__ == '__main__':
        st.write('')

        fecha_hoy = pd.Timestamp('today').date()
        fecha_formateada = fecha_hoy.strftime("%d/%m/%Y")

        if st.button(f'Predecir resultado a {fecha_formateada}'):
            user_songs = [  {'song': "Bara Bada Bastu", 'singer': "KAJ", 'country': "Sweden 🇸🇪 "},
                            {'song': "Wasted Love", 'singer': "JJ", 'country': "Austria 🇦🇹 "},
                            {'song': "Maman", 'singer': "Louane", 'country': "France 🇫🇷 "},
                            {'song': "New Day Will Rise", 'singer': "Yuval Raphael", 'country': "Israel 🇮🇱 "},
                            {'song': "C'est La Vie", 'singer': "Claude", 'country': "Netherlands 🇳🇱 "},
                            {'song': "Ich komme", 'singer': "Erika Vikman", 'country': "Finland 🇫🇮 "},
                            {'song': "Espresso macchiato", 'singer': "Tommy Cash", 'country': "Estonia 🇪🇪 "},
                            {'song': "Strobe Lights", 'singer': "Red Sebastian", 'country': "Belgium 🇧🇪 "},
                            {'song': "Bird of Pray", 'singer': "Ziferblat", 'country': "Ukraine 🇺🇦 "},
                            {'song': "Zjerm", 'singer': "Shkodra Elektronike", 'country': "Albania 🇦🇱 "},
                            {'song': "Kant", 'singer': "Miriana Conte", 'country': "Malta 🇲🇹 "},
                            {'song': "What The Hell Just Happened?", 'singer': "Remember Monday", 'country': "United Kingdom 🇬🇧 "},
                            {'song': "Volevo Essere Un Duro", 'singer': "Lucio Corsi", 'country': "Italy 🇮🇹 "},
                            {'song': "Tutta L'Italia", 'singer': "Gabry Ponte", 'country': "San Marino 🇸🇲 "},
                            {'song': "Kiss Kiss Goodbye", 'singer': "Adonxs", 'country': "Czechia 🇨🇿 "},
                            {'song': "Tavo akys", 'singer': "Katarsis", 'country': "Lithuania 🇱🇹 "},
                            {'song': "Shh", 'singer': "Theo Evan", 'country': "Cyprus 🇨🇾 "},
                            {'song': "Asteromata", 'singer': "Klavdia", 'country': "Greece 🇬🇷 "},
                            {'song': "Milkshake Man", 'singer': "Go-Jo", 'country': "Australia 🇦🇺 "},
                            {'song': "Baller", 'singer': "Abor & Tynna", 'country': "Germany 🇩🇪 "},
                            {'song': "Laika Party", 'singer': "Emmy", 'country': "Ireland 🇮🇪 "},
                            {'song': "Voyage", 'singer': "Zoë Më", 'country': "Switzerland 🇨🇭 "},
                            {'song': "Freedom", 'singer': "Mariam Shengelia", 'country': "Georgia 🇬🇪 "},
                            {'song': "Lighter", 'singer': "Kyle Alessandro", 'country': "Norway 🇳🇴 "},
                            {'song': "Deslocado", 'singer': "NAPA", 'country': "Portugal 🇵🇹 "},
                            {'song': "Gaja", 'singer': "Justyna Steczkowska", 'country': "Poland 🇵🇱 "},
                            {'song': "How Much Time Do We Have Left", 'singer': "Klemen", 'country': "Slovenia 🇸🇮 "},
                            {'song': "Run With U", 'singer': "Mamagama", 'country': "Azerbaijan 🇦🇿 "},
                            {'song': "Hallucination", 'singer': "Sissal", 'country': "Denmark 🇩🇰 "},
                            {'song': "Esa diva", 'singer': "Melody", 'country': "Spain 🇪🇸 "},
                            {'song': "Bur man laimi", 'singer': "Tautumeitas", 'country': "Latvia 🇱🇻 "},
                            {'song': "Survivor", 'singer': "Parg", 'country': "Armenia 🇦🇲 "},
                            {'song': "La poupée monte le son", 'singer': "Laura Thorn", 'country': "Romania 🇷🇴 "},
                            {'song': "Mila", 'singer': "Princ", 'country': "Serbia 🇷🇸 "},
                            {'song': "Poison Cake", 'singer': "Marko Bošnjak", 'country': "Croatia 🇭🇷 "},
                            {'song': "RÓA", 'singer': "VÆB", 'country': "Iceland 🇮🇸 "},
                            {'song': "Dobrodošli", 'singer': "Nina Žižić", 'country': "Montenegro 🇲🇪 "} ]

            resultado = predicciones_now(user_songs)

            df = pd.DataFrame(resultado)
            df_sorted = df.sort_values('points', ascending=False).reset_index(drop=True)

            # Hacemos la trampa de Romania = Luxemburgo
            df_sorted['country'] = df_sorted['country'].replace('Romania 🇷🇴 ', 'Luxemburgo 🇱🇺 ')

            puntos_maximos_posibles = (len(user_songs)-1)*58*2

            first_points = df_sorted['points'][0]
            last_points = df_sorted['points'][24]

            pendiente = first_points/(first_points-last_points)
            intercept = (first_points*last_points)/(first_points-last_points)

            total_points = df_sorted['points'].sum()

            for i,p in enumerate(df_sorted['points']):
                df_sorted.loc[i, 'points'] = round(pendiente*p-intercept)

            try:
                df_sorted.loc[26:, 'points'] = 0
            except:
                pass

            total_points = df_sorted['points'].sum()

            cociente = puntos_maximos_posibles/total_points

            for i,puntos in enumerate(df_sorted['points'][:26]):
                df_sorted.loc[i, 'points'] = round(puntos*cociente)

            total_points = df_sorted['points'].sum()

            diferencia = puntos_maximos_posibles-total_points

            # Me quedo con el último índice no nulo
            for i,p in enumerate(df_sorted['points']):
                if p <= 0:
                    last_nonull = i-1
                    break

            if diferencia > 0:
                for i in range(25-diferencia+1, 26):
                    df_sorted.loc[i, 'points'] = df_sorted['points'][i]+1

            elif diferencia < 0:
                for i in range(last_nonull+diferencia+1, last_nonull+1):
                    print(i)
                    df_sorted.loc[i, 'points'] = df_sorted['points'][i]-1

            total_points = df_sorted['points'].sum()

            df_sorted = df_sorted.sort_values('points', ascending=False).reset_index(drop=True)
            df_sorted = df_sorted[['song','singer','country','points']] 
            
            st.balloons()
            st.markdown('##### 😱 ¡Tenemos resultados! Y son los siguientes... 🥁🥁🥁🥁')
            time.sleep(4)
            
            st.write('')
            df_sorted_check = df_sorted.copy()
            df_sorted_check.reset_index(drop=True, inplace=True)
            df_sorted_check.index += 1
            
            # Asegurar que los puntos no sean negativos
            df_sorted_check["points"] = df_sorted_check["points"].apply(lambda x: max(x, 0))
            
            st.table(df_sorted_check.style.apply(highlight_rows, axis=1))

            #df_sorted['country1'] = [e.replace(' ','·') for e in df_sorted['country']]
            #df_sorted

            # Obtener la fecha de hoy
            fecha_hoy = pd.Timestamp('today').date()
            fecha_formateada = fecha_hoy.strftime("%d/%m/%Y")
           
            # Crear un diccionario para especificar las columnas y sus valores
            columnas = df_sorted['country'].tolist()  # Obtener los valores de la columna 'country'
            valores = df_sorted.set_index('country')['points'].to_dict()  # Crear un diccionario con los valores de 'points' indexados por 'country'
            data = {col: [valores.get(col, None)] for col in columnas}  # Crear un diccionario con los valores correspondientes a las columnas

# --------------------------------------------------------------------------------------
            # df_metricas = row_data_ESC23(user_songs) # Para ver las métricas
            # st.write(df_metricas)
            # pais_met = list(df_metricas['pais'])
            # views_met = list(df_metricas['views'])
            # likes_met = list(df_metricas['likes'])
            # shaz_met = list(df_metricas['shazams'])
            # st.write(pais_met)
            # st.write(views_met)
            # st.write(likes_met)
            # st.write(shaz_met)
# --------------------------------------------------------------------------------------

            # Crear un nuevo dataframe con la fecha de hoy como índice y las columnas y valores especificados
            df_nuevo = pd.DataFrame(data, index=[fecha_hoy])

            # @st.cache_data
            def load_data_graf():
                df_prueba = pd.read_excel('./data/prueba_predicc_dia_dia.xlsx')
                df_prueba.rename(columns= {'Unnamed: 0':'date'}, inplace=True)
                df_prueba = df_prueba.set_index('date')
                df_prueba.index = df_prueba.index.date.astype(str)
                df_prueba = df_prueba.astype(int)
                return df_prueba

            df_prueba = load_data_graf()
            
            df_prueba = pd.concat([df_nuevo, df_prueba])
            df_prueba.index = df_prueba.index.astype(str)
            df_prueba = df_prueba.sort_index(ascending=True)
            df_prueba = df_prueba.fillna(0)
            # st.write(df_prueba)
            
            # # Crear el gráfico de líneas con Plotly
            # fig = px.line(df_prueba, x=df_prueba.index, y=df_prueba.columns)

            # # Configurar formato de fecha en el eje X
            # fig.update_xaxes(title='Fecha', tickformat='%d/%m/%Y')
            # #fig.update_yaxes(title='Predicción de puntos')


            # # Configurar marcadores de puntos en las líneas
            # fig.update_traces(mode='markers+lines', marker=dict(size=6), showlegend=True)
            # fecha_actual = datetime.datetime.now()
            # fecha_actual_str = fecha_actual.strftime("%d/%m/%Y")
            # fig.update_layout(legend_title_text='País',title={'text': f"Evolución predicción desde 30/05/2025 hasta {fecha_formateada}",'font_size': 24},  xaxis_tickfont=dict(size=20), yaxis_tickfont=dict(size=20), yaxis_title=f'<b style="font-size:1em">Predicción de puntos</b>', xaxis_title=f'<b style="font-size:1em">Fecha de la predicción</b>', xaxis=dict(tickangle=-25), height=800) 
            
            # fig.update_layout(
            #     shapes=[
                    # dict(
                    #     type='line',
                    #     xref='x',
                    #     yref='y',
                    #     x0='2023-04-25',
                    #     y0=0,
                    #     x1='2023-04-25',
                    #     y1=max(list(df_prueba.max()))+100,
                    #     line=dict(color='black', width=1.4, dash='dash'),
                    # ),
                #     dict(
                #         type='line',
                #         xref='x',
                #         yref='y',
                #         x0='2024-05-07',
                #         y0=0,
                #         x1='2024-05-07',
                #         y1=max(list(df_prueba.max()))+100,
                #         line=dict(color='black', width=1.4, dash='dash'),
                #     ),
                #     dict(
                #         type='line',
                #         xref='x',
                #         yref='y',
                #         x0='2024-05-09',
                #         y0=0,
                #         x1='2024-05-09',
                #         y1=max(list(df_prueba.max()))+100,
                #         line=dict(color='black', width=1.4, dash='dash'),
                #     ),
                #     dict(
                #         type='line',
                #         xref='x',
                #         yref='y',
                #         x0='2024-05-10',
                #         y0=0,
                #         x1='2024-05-10',
                #         y1=max(list(df_prueba.max()))+100,
                #         line=dict(color='black', width=1.4, dash='dash'),
                #     ),
                #     dict(
                #         type='line',
                #         xref='x',
                #         yref='y',
                #         x0='2024-05-11',
                #         y0=0,
                #         x1='2024-05-11',
                #         y1=max(list(df_prueba.max()))+100,
                #         line=dict(color='black', width=1.4, dash='dash'),
                #     )
                # ], 
                # annotations=[
                    # dict(
                    #     x='2023-04-25',
                    #     y=max(list(df_prueba.max()))+50,
                    #     xref='x',
                    #     yref='y',
                    #     text='Cambio de algoritmo ',
                    #     showarrow=False,
                    #     font=dict(size=14, color='red'),
                    #     xanchor='right'
                    # ),
            #         dict(
            #             x='2024-05-07',
            #             y=max(list(df_prueba.max()))+50,
            #             xref='x',
            #             yref='y',
            #             text='1ª Semi ',
            #             showarrow=False,
            #             font=dict(size=14, color='red'),
            #             xanchor='right'
            #         ),
            #         dict(
            #             x='2024-05-09',
            #             y=max(list(df_prueba.max()))+50,
            #             xref='x',
            #             yref='y',
            #             text='2ª Semi ',
            #             showarrow=False,
            #             font=dict(size=14, color='red'),
            #             xanchor='right'
            #         ),
            #         dict(
            #             x='2024-05-10',
            #             y=max(list(df_prueba.max()))+50,
            #             xref='x',
            #             yref='y',
            #             text='Final ',
            #             showarrow=False,
            #             font=dict(size=14, color='red'),
            #             xanchor='right'
            #         ),
            #         dict(
            #             x='2024-05-11',
            #             y=max(list(df_prueba.max()))+50,
            #             xref='x',
            #             yref='y',
            #             text=' Final (real)',
            #             showarrow=False,
            #             font=dict(size=14, color='red'),
            #             xanchor='left'
            #         )
            #     ]
            # )


            # st.success('👇🏻 Puedes filtrar qué países ver en el gráfico pulsando sobre ellos en la leyenda: Si pulsas 1️⃣ vez, eliminas ese país del gráfico. Si pulsas 2️⃣ veces, verás solo ese país, y entonces, tocando 1️⃣ vez en otros, añadirás países a la visualización. Si quieres reestablecer la vista inicial, pulsa en "Autoscale", situado en tercera posición por la derecha en la parte superior del gráfico')
            # # Mostrar el gráfico
            # st.plotly_chart(fig, use_container_width=True)

            # Asegurarse de que los puntos no son negativos
            df_sorted_check["points"] = df_sorted_check["points"].apply(lambda x: max(x, 0))

            fig = px.bar(
                df_sorted_check,
                x="country",  # Ahora solo las banderas
                y="points",
                text="points",
                color="country",
                title="Predicción de puntos totales por país",
                labels={"country": "País", "points": "Puntos"},
            )
            
            fig.update_traces(textposition='outside')
            fig.update_layout(
                xaxis_tickangle=-45,
                yaxis_title="Puntos predichos",
                xaxis_title="País",
                title_font_size=24,
                height=700,
                showlegend=False
            )

            # Mostrar el gráfico
            st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------------------------------------------------------

with tab2:

    st.markdown('<h1 style="text-align:center"><span style="font-size: 40px;">📊</span> <u>ESTADÍSTICAS 2002-2023</u></h1>', unsafe_allow_html=True)

#     df_master = pd.read_excel('./data/MASTERTABLA.xlsx').drop('Unnamed: 0', axis = 1)
    # st.write(df_master)
    
    @st.cache_data
    def load_data_stats():
        df_master = pd.read_excel('./data/MASTERTABLA.xlsx').drop('Unnamed: 0', axis = 1)
        return df_master

    df_master = load_data_stats()
    
    st.write('')
    st.warning('⚠️ Si accedes desde un móvil rota la pantalla para poder visualizar los gráficos con una mejor adaptación.')
    st.write('')

    graf_names = ['Comportamiento Digital', 'Apuestas', 'Política', 'Aspectos Técnicos', 'Evolución Histórica']
    
    # Utilizando Markdown para añadir estilo al título
    st.markdown("<h4 style='margin-bottom: -50px;'> 🔎 Tipo de gráfico a visualizar</h4>", unsafe_allow_html=True)
    
    # Radio button para seleccionar el tipo de gráfico
    graf = st.radio(' ', graf_names)
    st.write('')

    
    # Markdown con estilo para el título
    st.markdown("<h4 style='margin-bottom: -40px;'>🗓 Selecciona un rango de años</h4>", unsafe_allow_html=True)


    # Filtro por año
    year_range = st.slider(' ', 
                           #min_value=df_master['year'].min(), 
                           min_value = 2002,
                           #max_value=df_master['year'].max(), 
                           max_value = 2023,
                           #value=(df_master['year'].min(), df_master['year'].max())
                           value = (2002, 2023)
                          )
    filtered_df = df_master[(df_master['year'] >= year_range[0]) & (df_master['year'] <= year_range[1])]
    st.write('')
    
    # Markdown con estilo para el título
    st.markdown("<h4 style='margin-bottom: -40px;'>🌍 Selecciona los países</h4>", unsafe_allow_html=True)
    
    # Filtro por país
    selected_country = st.multiselect(' ', options=sorted(df_master['country'].unique()), placeholder="Elige tantos como quieras")
    if selected_country:
        filtered_df = filtered_df[filtered_df['country'].isin(selected_country)]

        
# ----------- PROBANDO FUNCION PARA FILTROS ⬇️------------------------------------------------------------------------------

    # # st.write('')
    
    # # Markdown con estilo para el título
    # st.markdown("<h4 style='margin-bottom: -10px;'>🎯 ¿Quieres añadir más filtros?</h4>", unsafe_allow_html=True)
    
    # filtered_df = filter_dataframe(filtered_df)
    # st.write('Esta tabla debería filtrarse ⬇️')
    # st.write(filtered_df)

# ----------- PROBANDO FUNCION PARA FILTROS ⬆️------------------------------------------------------------------------------

    
    # crear un diccionario de reemplazo
    replace_dict = {
        'The Netherlands': 'Netherlands 🇳🇱 ',
        'Serbia and Montenegro': 'Serb. & Mont. 🇷🇸🇲🇪 ',
        'Bosnia and Herzegovina': 'Bosn. & Herz. 🇧🇦 ',
        'North Macedonia': 'N. Macedonia 🇲🇰 ',
        'Czech Republic': 'Czechia 🇨🇿 ',
        'United Kingdom': 'UK 🇬🇧 ',
        'Albania':'Albania 🇦🇱 ',
        'Andorra':"Andorra 🇦🇩 ",
        'Armenia':"Armenia 🇦🇲 ",
        'Australia':"Australia 🇦🇺 ",
        'Austria':"Austria 🇦🇹 ",
        'Azerbaijan':"Azerbaijan 🇦🇿 ",
        'Belarus':"Belarus 🇧🇾 ",
        'Belgium':"Belgium 🇧🇪 ",
        'Bulgaria':"Bulgaria 🇧🇬 ",
        'Croatia':"Croatia 🇭🇷 ",
        'Cyprus':"Cyprus 🇨🇾 ",
        'Denmark':"Denmark 🇩🇰 ",
        'Estonia':"Estonia 🇪🇪 ",
        'Finland':"Finland 🇫🇮 ",
        'France':"France 🇫🇷 ",
        'Georgia':"Georgia 🇬🇪 ",
        'Germany':"Germany 🇩🇪 ",
        'Greece':"Greece 🇬🇷 ",
        'Hungary':"Hungary 🇭🇺 ",
        'Iceland':"Iceland 🇮🇸 ",
        'Ireland':"Ireland 🇮🇪 ",
        'Israel':"Israel 🇮🇱 ",
        'Italy':"Italy 🇮🇹 ",
        'Latvia':"Latvia 🇱🇻 ",
        'Lithuania':"Lithuania 🇱🇹 ",
        'Malta':"Malta 🇲🇹 ",
        'Moldova':"Moldova 🇲🇩 ",
        'Monaco':"Monaco 🇲🇨 ",
        'Montenegro':"Montenegro 🇲🇪 ",
        'Norway':"Norway 🇳🇴 ",
        'Poland':"Poland 🇵🇱 ",
        'Portugal':"Portugal 🇵🇹 ",
        'Romania':"Romania 🇷🇴 ",
        'Russia':"Russia 🇷🇺 ",
        'San Marino':"San Marino 🇸🇲 ",
        'Serbia':"Serbia 🇷🇸 ",
        'Slovakia':"Slovakia 🇸🇰 ",
        'Slovenia':"Slovenia 🇸🇮 ",
        'Spain':"Spain 🇪🇸 ",
        'Sweden':"Sweden 🇸🇪 ",
        'Switzerland':"Switzerland 🇨🇭 ",
        'Turkey':"Turkey 🇹🇷 ",
        'Ukraine':"Ukraine 🇺🇦 "
    }
    # actualizar la columna 'country' utilizando el método replace
    filtered_df['country'] = filtered_df['country'].replace(replace_dict)

    replace_dict_likes = {
        '2,9 M': 2900000,
        '1,5 M': 1500000
    }
    filtered_df['likes'] = filtered_df['likes'].replace(replace_dict_likes)
    filtered_df['likes'] = [int(li) for li in filtered_df['likes']]

    if graf in ['Comportamiento Digital', 'Apuestas', 'Política', 'Aspectos Técnicos']:

        st.write('')
    
        # Markdown con estilo para el título
        st.markdown("<h4 style='margin-bottom: -10px;'>🎯 ¿Quieres añadir más filtros?</h4>", unsafe_allow_html=True)
        
        filtered_df = filter_dataframe(filtered_df)
        # st.write('Esta tabla debería filtrarse ⬇️')
        # st.write(filtered_df)

        # Muestra el DataFrame filtrado
        st.write('\n')
    
        st.markdown("<h4 style='margin-bottom: 5px;'>🔢 Tabla de datos </h4>", unsafe_allow_html=True)
        with st.expander('Ver Datos', expanded=False): 
            st.write('❗ A partir de 2016 los puntos se han corregido, dividiéndolos entre 2, para ser consistentes con el sistema de votación del periodo 2002-2015')

            # st.write(filtered_df)
            df_to_show = filtered_df[['links','country','year','artist','song','clasificacion','puntos_corregidos','propo_max_puntos','finalista','order_act',
                                     'estilos','idioma1','idioma2','idioma3','love_song', 'top1word', 'top2word', 'top3word', 'top4word', 'top5word', 'estruc_resum',
                                     'views', 'likes', 'shazams', 'bet_mean', 'lyrics_long', 'unic_words', 'duracion_eurovision', 'duracion_spoty',
                                     'vecinos_participantes','GDP', 'orden_relativo_GDP', 'influ_ranking', 'influ_score', 'reput_ranking' ]]
    
            nuevos_nombres = ['Link','País','Año','Cantante/s','Canción','Clasificación','Puntos','% Puntos','Finalista','Orden actuación',
                                     'Estilo','1º Idioma','2º Idioma','3º Idioma','Temática Amor', '1ª Palabra', '2ª Palabra', '3ª Palabra', '4ª Palabra', '5ª Palabra', 'Estructura',
                                     'Views YT', 'Likes YT', 'Shazams', 'Cuota Apuestas', 'Longitud letra', 'Palabras Únicas', 'Duración ESC', 'Duración Spotify',
                                     'Vecinos Participantes','PIB país', 'Ranking PIB', 'Ranking Influencia', 'Puntos Influencia', 'Ranking Reputación']
            df_to_show.columns = nuevos_nombres
    
            def corregir_numero(val):
                return int(val) 
    
            def corregir_text(val):
                try:
                    return val.strip()
                except:
                    return val
            def sustituir_valor_emoji(val):
                if val == "Yes":
                    return "✅"
                elif val == "No":
                    return "❌"
                else:
                    return val 
    
            columnas_a_modificar = ['Finalista', 'Temática Amor']
            for columna in columnas_a_modificar:
                df_to_show[columna] = df_to_show[columna].apply(sustituir_valor_emoji)
    
            columnas_a_modificar_2 = ['Cantante/s', 'Canción', 'Estilo', '1º Idioma', '2º Idioma', '3º Idioma', '1ª Palabra', '2ª Palabra', '3ª Palabra', '4ª Palabra', '5ª Palabra', 'Estructura']
            for columna in columnas_a_modificar_2:
                df_to_show[columna] = df_to_show[columna].apply(corregir_text)
                
            df_to_show['Likes YT'] = df_to_show['Likes YT'].apply(corregir_numero)
    
            df_to_show['% Puntos'] = df_to_show['% Puntos'].round(2)
    
            df_to_show['Cuota Apuestas'] = df_to_show['Cuota Apuestas'].round(2)
    
            df_to_show['Puntos Influencia'] = df_to_show['Puntos Influencia'].round(2)
    
            st.data_editor(
                df_to_show,
                column_config={
                    "Link": st.column_config.LinkColumn(
                        "🔗 Link", display_text = "🌐 Video YT"
                    ),
                    
                    "% Puntos": st.column_config.ProgressColumn(
                        "% Puntos",
                        format="%f",
                        min_value=0,
                        max_value=1,
                    ),
    
                    "Puntos Influencia": st.column_config.ProgressColumn(
                        "Puntos Influencia",
                        format="%f",
                        min_value=0,
                        max_value=100,
                    ),
    
                },
                hide_index=True,
            )
            # st.write(df_to_show)
        st.write('')
        
        st.write('')
        st.markdown("<h4 style='margin-bottom: 5px;'>📈 Gráficos</h4>", unsafe_allow_html=True)
        
        if graf == 'Comportamiento Digital':
            
        # ------ MÉTRICAS DIGITALES -----------------------------------------------------------------
          # ---- GRAFICOS PUNTOS VS YOUTUBE ---------------------------------------------------------
    
            with st.expander('PUNTOS vs YouTube 🔢📹', expanded=False): 
    
                st.write('')
                Acum = st.checkbox("Ver en datos acumulados")
                st.write('❗ Tenga en cuenta que los promedios se calculan dividiendo entre los años de participación, por lo que hay países con pocas participaciones pero buenos registros en ellas que muestran altos promedios')
    
                try:
                    if Acum:
    
                        grouped_df = filtered_df.groupby('country').sum().reset_index()
                        grouped_df = grouped_df.sort_values('puntos_corregidos', ascending=False)
    
                        # Crear figura con tres subplots
                        fig = sp.make_subplots(rows=1, cols=3, shared_yaxes=True, horizontal_spacing=0.01)
    
                        # Grafico 1: Acum de puntos
                        fig.add_trace(px.bar(grouped_df, x='puntos_corregidos', y='country',
                                              orientation='h', #text='puntos_corregidos',
                                              color='puntos_corregidos').data[0],
                                      row=1, col=1)
                        fig.update_xaxes(title='Acum. puntos', row=1, col=1)
    
                        # Grafico 2: Acum de reproducciones en YouTube
                        grouped_df = filtered_df.groupby('country').sum().reset_index()
                        grouped_df = grouped_df.sort_values('views', ascending=False)
    
                        fig.add_trace(px.bar(grouped_df, x='views', y='country',
                                              orientation='h', #text='views',
                                              color='views').data[0],
                                      row=1, col=2)
                        fig.update_xaxes(title='Acum. views YT', row=1, col=2)
    
                        # Grafico 3: Acum de likes en YouTube
                        grouped_df = filtered_df.groupby('country').sum().reset_index()
                        grouped_df = grouped_df.sort_values('likes', ascending=False)
    
                        fig.add_trace(px.bar(grouped_df, x='likes', y='country',
                                              orientation='h', #text='likes',
                                              color='likes').data[0],
                                      row=1, col=3)
                        fig.update_xaxes(title='Acum. likes YT', row=1, col=3)
                        fig.update_layout(title={'text': f'Acum. Puntos + Views y Likes en YT {year_range[0]}-{year_range[1]}', 'font_size': 24})
    
                        fig.update_yaxes(title='', row=1, col=1)
                        fig.update_traces(marker_color='#E97451')
                        fig.update_layout(showlegend=False, height=1100)
                        fig.update(layout_coloraxis_showscale = False)
                        fig.update_traces(hovertemplate='pais = %{label}<br>acumulado = %{value:.0f}')
    
                        st.plotly_chart(fig, use_container_width=True)
    
                    else:
    
                        grouped_df = filtered_df.groupby('country').mean().reset_index()
                        grouped_df = grouped_df.sort_values('puntos_corregidos', ascending=False)
    
                        # Crear figura con tres subplots
                        fig = sp.make_subplots(rows=1, cols=3, shared_yaxes=True, horizontal_spacing=0.01)
    
                        # Grafico 1: Promedio de puntos
                        fig.add_trace(px.bar(grouped_df, x='puntos_corregidos', y='country',
                                              orientation='h', #text='puntos_corregidos',
                                              color='puntos_corregidos').data[0],
                                      row=1, col=1)
                        fig.update_xaxes(title='Prom. puntos', row=1, col=1)
    
                        # Grafico 2: Promedio de reproducciones en YouTube
                        grouped_df = filtered_df.groupby('country').mean().reset_index()
                        grouped_df = grouped_df.sort_values('views', ascending=False)
    
                        fig.add_trace(px.bar(grouped_df, x='views', y='country',
                                              orientation='h', #text='views',
                                              color='views').data[0],
                                      row=1, col=2)
                        fig.update_xaxes(title='Prom. views YT', row=1, col=2)
                        fig.update_annotations(yshift=20)
    
                        # Grafico 3: Promedio de likes en YouTube
                        grouped_df = filtered_df.groupby('country').mean().reset_index()
                        grouped_df = grouped_df.sort_values('likes', ascending=False)
    
                        fig.add_trace(px.bar(grouped_df, x='likes', y='country',
                                              orientation='h', #text='likes',
                                              color='likes').data[0],
                                      row=1, col=3)
                        fig.update_xaxes(title='Prom. likes YT', row=1, col=3)
    
                        fig.update_layout(title={'text': f'Prom. Puntos + Views y Likes en YT {year_range[0]}-{year_range[1]}', 'font_size': 24})
    
                        fig.update_yaxes(title='', row=1, col=1)
                        fig.update_traces(marker_color='#E97451')
                        fig.update_layout(showlegend=False, height=1100)
                        fig.update(layout_coloraxis_showscale = False)
                        fig.update_traces(hovertemplate='pais = %{label}<br>promedio = %{value:.0f}')
    
                        st.plotly_chart(fig, use_container_width=True)
    
                except:
                    st.write('#### ❌ El gráfico no se ha podido generar debido a los filtros que has aplicado (has seleccionado un único país, un único año, 2020 sin concurso...)')
    
    
          # ---- GRAFICOS PUNTOS VS SHAZAM ---------------------------------------------------------
    
            with st.expander('PUNTOS vs SHAZAM 🔢🔊', expanded=False): 
    
                st.write('')
                Acum2 = st.checkbox("Ver en datos acumulados ")
                
                try:
    
                    if Acum2:
    
                        grouped_df = filtered_df.groupby('country').sum().reset_index()
                        grouped_df = grouped_df.sort_values('puntos_corregidos', ascending=False)
    
                        # Crear figura con tres subplots
                        fig = sp.make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.01)
    
                        # Grafico 1: Acum de puntos
                        fig.add_trace(px.bar(grouped_df, x='puntos_corregidos', y='country',
                                              orientation='h', #text='puntos_corregidos',
                                              color='puntos_corregidos').data[0],
                                      row=1, col=1)
                        fig.update_xaxes(title='Acum. puntos', row=1, col=1)
                        fig.update_layout(title={'text': f'Acum. Puntos vs Shazams {year_range[0]}-{year_range[1]}', 'font_size': 24})
    
                        # Grafico 2: Promedio de Shazams
                        grouped_df = filtered_df.groupby('country').sum().reset_index()
                        grouped_df = grouped_df.sort_values('shazams', ascending=False)
    
                        fig.add_trace(px.bar(grouped_df, x='shazams', y='country',
                                              orientation='h', #text='shazams',
                                              color='shazams').data[0],
                                      row=1, col=2)
                        fig.update_xaxes(title='Acum. shazams', row=1, col=2)
    
                        fig.update_yaxes(title='', row=1, col=1)
                        fig.update_traces(marker_color='#89CFF0')
                        fig.update_layout(showlegend=False, height=1100)
                        fig.update(layout_coloraxis_showscale = False)
                        fig.update_traces(hovertemplate='pais = %{label}<br>acumulado = %{value:.0f}')
    
                        st.plotly_chart(fig, use_container_width=True)
    
    
                    else:
    
                        grouped_df = filtered_df.groupby('country').mean().reset_index()
                        grouped_df = grouped_df.sort_values('puntos_corregidos', ascending=False)
    
                        # Crear figura con tres subplots
                        fig = sp.make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.01)
    
                        # Grafico 1: Acum de puntos
                        fig.add_trace(px.bar(grouped_df, x='puntos_corregidos', y='country',
                                              orientation='h', #text='puntos_corregidos',
                                              color='puntos_corregidos').data[0],
                                      row=1, col=1)
                        fig.update_xaxes(title='Prom. puntos', row=1, col=1)
    
                        # Grafico 2: Promedio de Shazams
                        grouped_df = filtered_df.groupby('country').mean().reset_index()
                        grouped_df = grouped_df.sort_values('shazams', ascending=False)
    
                        fig.add_trace(px.bar(grouped_df, x='shazams', y='country',
                                              orientation='h', #text='shazams',
                                              color='shazams').data[0],
                                      row=1, col=2)
                        fig.update_xaxes(title='Prom. shazams', row=1, col=2)
                        fig.update_layout(title={'text': f'Prom. Puntos vs Shazams {year_range[0]}-{year_range[1]}', 'font_size': 24})
    
                        fig.update_yaxes(title='', row=1, col=1)
                        fig.update_traces(marker_color='#89CFF0')
                        fig.update_layout(showlegend=False, height=1100)
                        fig.update(layout_coloraxis_showscale = False)
                        fig.update_traces(hovertemplate='pais = %{label}<br>promedio = %{value:.0f}')
    
                        st.plotly_chart(fig, use_container_width=True)
                        
                except:
                    st.write('#### ❌ El gráfico no se ha podido generar debido a los filtros que has aplicado (has seleccionado un único país, un único año, 2020 sin concurso...)')
                
    
        elif graf == 'Apuestas':
            
         # ----- APUESTAS --------------------------------------------------------------------------
          # ---- GRAFICOS PUNTOS VS APUESTAS ---------------------------------------------------------
    
            with st.expander('PUNTOS vs APUESTAS 🔢💸', expanded=False): 
    
                st.write('')
                Acum8 = st.checkbox("Ver en datos acumulados               ")
                
                try:
    
                    if Acum8:
    
                        grouped_df = filtered_df.groupby('country').sum().reset_index()
                        grouped_df = grouped_df.sort_values('puntos_corregidos', ascending=False)
    
                        # Crear figura con tres subplots
                        fig = sp.make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.01)
    
                        # Grafico 1: Acum de puntos
                        fig.add_trace(px.bar(grouped_df, x='puntos_corregidos', y='country',
                                              orientation='h', #text='puntos_corregidos',
                                              color='puntos_corregidos').data[0],
                                      row=1, col=1)
                        fig.update_xaxes(title='Acum. puntos', row=1, col=1)
                        fig.update_layout(title={'text': f'Acum. Puntos vs Apuestas {year_range[0]}-{year_range[1]}', 'font_size': 24})
    
                        # Grafico 2: Promedio de Shazams
                        grouped_df = filtered_df.groupby('country').sum().reset_index()
                        grouped_df = grouped_df.sort_values('bet_mean', ascending=False)
    
                        fig.add_trace(px.bar(grouped_df, x='bet_mean', y='country',
                                              orientation='h', #text='shazams',
                                              color='bet_mean').data[0],
                                      row=1, col=2)
                        fig.update_xaxes(title='Acum. Apuestas', row=1, col=2)
    
                        fig.update_yaxes(title='', row=1, col=1)
                        fig.update_traces(marker_color='#22BAB5')
                        fig.update_layout(showlegend=False, height=1100)
                        fig.update(layout_coloraxis_showscale = False)
                        fig.update_traces(hovertemplate='pais = %{label}<br>acumulado = %{value:.0f}')
    
                        st.plotly_chart(fig, use_container_width=True)
    
    
                    else:
    
                        grouped_df = filtered_df.groupby('country').mean().reset_index()
                        grouped_df = grouped_df.sort_values('puntos_corregidos', ascending=False)
    
                        # Crear figura con tres subplots
                        fig = sp.make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.01)
    
                        # Grafico 1: Acum de puntos
                        fig.add_trace(px.bar(grouped_df, x='puntos_corregidos', y='country',
                                              orientation='h', #text='puntos_corregidos',
                                              color='puntos_corregidos').data[0],
                                      row=1, col=1)
                        fig.update_xaxes(title='Prom. puntos', row=1, col=1)
    
                        # Grafico 2: Promedio de Apuestas
                        grouped_df = filtered_df.groupby('country').mean().reset_index()
                        grouped_df = grouped_df.sort_values('bet_mean', ascending=False)
    
                        fig.add_trace(px.bar(grouped_df, x='bet_mean', y='country',
                                              orientation='h', #text='shazams',
                                              color='bet_mean').data[0],
                                      row=1, col=2)
                        fig.update_xaxes(title='Prom. Apuestas', row=1, col=2)
                        fig.update_layout(title={'text': f'Prom. Puntos vs Apuestas {year_range[0]}-{year_range[1]}', 'font_size': 24})
    
                        fig.update_yaxes(title='', row=1, col=1)
                        fig.update_traces(marker_color='#22BAB5')
                        fig.update_layout(showlegend=False, height=1100)
                        fig.update(layout_coloraxis_showscale = False)
                        fig.update_traces(hovertemplate='pais = %{label}<br>promedio = %{value:.0f}')
    
                        st.plotly_chart(fig, use_container_width=True)
    
                except:
                    st.write('#### ❌ El gráfico no se ha podido generar debido a los filtros que has aplicado (has seleccionado un único país, un único año, 2020 sin concurso...)')
            
        elif graf == 'Política':
    
          # ---- GRAFICOS PUNTOS VS VECINOS ---------------------------------------------------------
    
            with st.expander('PUNTOS vs Nº de VECINOS 🔢🌍', expanded=False): 
    
                st.write('')
                Acum3 = st.checkbox("Ver en datos acumulados  ")
                st.write('❗ Los datos de "Nº Vecinos" se muestran siempre como valor promedio, ya que carece de sentido calcular un acumulado')
    
                try:
                    
                    if Acum3:
    
                        grouped_df = filtered_df.groupby('country').sum().reset_index()
                        grouped_df = grouped_df.sort_values('puntos_corregidos', ascending=False)
    
                        # Crear figura con tres subplots
                        fig = sp.make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.01)
    
                        # Grafico 1: Sum de puntos
                        fig.add_trace(px.bar(grouped_df, x='puntos_corregidos', y='country',
                                              orientation='h', #text='puntos_corregidos',
                                              color='puntos_corregidos').data[0],
                                      row=1, col=1)
                        fig.update_xaxes(title='Acum. puntos', row=1, col=1)
    
                        # Grafico 2: Nº de Vecinos
                        grouped_df = filtered_df.groupby('country').mean().reset_index()
                        grouped_df = grouped_df.sort_values('vecinos_participantes', ascending=False)
    
                        fig.add_trace(px.bar(grouped_df, x='vecinos_participantes', y='country',
                                              orientation='h', #text='likes',
                                              color='vecinos_participantes').data[0],
                                      row=1, col=2)
                        fig.update_xaxes(title='Nº vecinos participantes', row=1, col=2)
    
                        fig.update_layout(title={'text': f'Acum. Puntos vs Nº Vecinos {year_range[0]}-{year_range[1]}', 'font_size': 24})
    
                        fig.update_yaxes(title='', row=1, col=1)
                        fig.update_traces(marker_color='#DDA0DD')
                        fig.update_layout(showlegend=False, height=1100)
                        fig.update(layout_coloraxis_showscale = False)
                        fig.update_traces(hovertemplate='pais = %{label}<br>valor = %{value:.0f}')
    
                        st.plotly_chart(fig, use_container_width=True) 
    
    
                    else:
    
                        grouped_df = filtered_df.groupby('country').mean().reset_index()
                        grouped_df = grouped_df.sort_values('puntos_corregidos', ascending=False)
    
                        # Crear figura con tres subplots
                        fig = sp.make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.01)
    
                        # Grafico 1: Acum de puntos
                        fig.add_trace(px.bar(grouped_df, x='puntos_corregidos', y='country',
                                              orientation='h', #text='puntos_corregidos',
                                              color='puntos_corregidos').data[0],
                                      row=1, col=1)
                        fig.update_xaxes(title='Prom. puntos', row=1, col=1)
    
                        # Grafico 2: Nº de Vecinos
                        grouped_df = filtered_df.groupby('country').mean().reset_index()
                        grouped_df = grouped_df.sort_values('vecinos_participantes', ascending=False)
    
                        fig.add_trace(px.bar(grouped_df, x='vecinos_participantes', y='country',
                                              orientation='h', #text='likes',
                                              color='vecinos_participantes').data[0],
                                      row=1, col=2)
                        fig.update_xaxes(title='Nº vecinos participantes', row=1, col=2)
    
                        fig.update_layout(title={'text': f'Prom. Puntos vs Nº Vecinos {year_range[0]}-{year_range[1]}', 'font_size': 24})
    
                        fig.update_yaxes(title='', row=1, col=1)
                        fig.update_traces(marker_color='#DDA0DD')
                        fig.update_layout(showlegend=False, height=1100)
                        fig.update(layout_coloraxis_showscale = False)
                        fig.update_traces(hovertemplate='pais = %{label}<br>valor = %{value:.0f}')
    
                        st.plotly_chart(fig, use_container_width=True) 
    
                except:
                    st.write('#### ❌ El gráfico no se ha podido generar debido a los filtros que has aplicado (has seleccionado un único país, un único año, 2020 sin concurso...)')
    
         # -------ECONOMÍA ----------------------------------------------------------------------
          # ---- GRAFICOS PUNTOS VS PIB ---------------------------------------------------------
    
            with st.expander('PUNTOS vs PIB 🔢🪙', expanded=False): 
    
                st.write('')
                Acum4 = st.checkbox("Ver en datos acumulados   ")
                
                try:
    
                    if Acum4:
    
                        grouped_df = filtered_df.groupby('country').sum().reset_index()
                        grouped_df = grouped_df.sort_values('puntos_corregidos', ascending=False)
    
                        # Crear figura con tres subplots
                        fig = sp.make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.01)
    
                        # Grafico 1: Sum de puntos
                        fig.add_trace(px.bar(grouped_df, x='puntos_corregidos', y='country',
                                              orientation='h', #text='puntos_corregidos',
                                              color='puntos_corregidos').data[0],
                                      row=1, col=1)
                        fig.update_xaxes(title='Acum. puntos', row=1, col=1)
    
                        # Grafico 2: GDP
                        grouped_df = filtered_df.groupby('country').sum().reset_index()
                        grouped_df = grouped_df.sort_values('GDP', ascending=False)
    
                        fig.add_trace(px.bar(grouped_df, x='GDP', y='country',
                                              orientation='h', #text='likes',
                                              color='GDP').data[0],
                                      row=1, col=2)
                        fig.update_xaxes(title='Acum. PIB', row=1, col=2)
    
                        fig.update_layout(title={'text': f'Acum. Puntos vs PIB {year_range[0]}-{year_range[1]}', 'font_size': 24})
    
                        fig.update_yaxes(title='', row=1, col=1)
                        fig.update_traces(marker_color='#08B434')
                        fig.update_layout(showlegend=False, height=1100)
                        fig.update(layout_coloraxis_showscale = False)
                        fig.update_traces(hovertemplate='pais = %{label}<br>acumulado = %{value:.0f}')
    
                        st.plotly_chart(fig, use_container_width=True) 
    
    
                    else:
    
                        grouped_df = filtered_df.groupby('country').mean().reset_index()
                        grouped_df = grouped_df.sort_values('puntos_corregidos', ascending=False)
    
                        # Crear figura con tres subplots
                        fig = sp.make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.01)
    
                        # Grafico 1: Acum de puntos
                        fig.add_trace(px.bar(grouped_df, x='puntos_corregidos', y='country',
                                              orientation='h', #text='puntos_corregidos',
                                              color='puntos_corregidos').data[0],
                                      row=1, col=1)
                        fig.update_xaxes(title='Prom. puntos', row=1, col=1)
    
                        # Grafico 2: GDP
                        grouped_df = filtered_df.groupby('country').mean().reset_index()
                        grouped_df = grouped_df.sort_values('GDP', ascending=False)
    
                        fig.add_trace(px.bar(grouped_df, x='GDP', y='country',
                                              orientation='h', #text='likes',
                                              color='GDP').data[0],
                                      row=1, col=2)
                        fig.update_xaxes(title='Prom. PIB', row=1, col=2)
    
                        fig.update_layout(title={'text': f'Prom. Puntos vs PIB {year_range[0]}-{year_range[1]}', 'font_size': 24})
    
                        fig.update_yaxes(title='', row=1, col=1)
                        fig.update_traces(marker_color='#08B434')
                        fig.update_layout(showlegend=False, height=1100)
                        fig.update(layout_coloraxis_showscale = False)
                        fig.update_traces(hovertemplate='pais = %{label}<br>promedio = %{value:.0f}')
    
                        st.plotly_chart(fig, use_container_width=True) 
    
                except:
                    st.write('#### ❌ El gráfico no se ha podido generar debido a los filtros que has aplicado (has seleccionado un único país, un único año, 2020 sin concurso...)')
    
          # ---- GRAFICOS PUNTOS VS RANKING PIB ---------------------------------------------------------
    
            with st.expander('PUNTOS vs Ranking Relativo PIB 🔢🪙', expanded=False): 
    
                st.write('')
                Acum5 = st.checkbox("Ver en datos acumulados    ")
                
                try:
    
                    if Acum5:
    
                        grouped_df = filtered_df.groupby('country').sum().reset_index()
                        grouped_df = grouped_df.sort_values('puntos_corregidos', ascending=False)
    
                        # Crear figura con tres subplots
                        fig = sp.make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.01)
    
                        # Grafico 1: Sum de puntos
                        fig.add_trace(px.bar(grouped_df, x='puntos_corregidos', y='country',
                                              orientation='h', #text='puntos_corregidos',
                                              color='puntos_corregidos').data[0],
                                      row=1, col=1)
                        fig.update_xaxes(title='Acum. puntos', row=1, col=1)
    
                        # Grafico 2: Orden Relativo PIB
                        grouped_df = filtered_df.groupby('country').sum().reset_index()
                        grouped_df = grouped_df.sort_values('orden_relativo_GDP', ascending=False)
    
                        fig.add_trace(px.bar(grouped_df, x='orden_relativo_GDP', y='country',
                                              orientation='h', #text='likes',
                                              color='orden_relativo_GDP').data[0],
                                      row=1, col=2)
                        fig.update_xaxes(title='Acum. Ranking PIB', row=1, col=2)
    
                        fig.update_layout(title={'text': f'Acum. Puntos vs Ranking Relativo PIB {year_range[0]}-{year_range[1]}', 'font_size': 24})
    
                        fig.update_yaxes(title='', row=1, col=1)
                        fig.update_traces(marker_color='#053BB6')
                        fig.update_layout(showlegend=False, height=1100)
                        fig.update(layout_coloraxis_showscale = False)
                        fig.update_traces(hovertemplate='pais = %{label}<br>acumulado = %{value:.0f}')
    
                        st.plotly_chart(fig, use_container_width=True) 
    
    
                    else:
    
                        grouped_df = filtered_df.groupby('country').mean().reset_index()
                        grouped_df = grouped_df.sort_values('puntos_corregidos', ascending=False)
    
                        # Crear figura con tres subplots
                        fig = sp.make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.01)
    
                        # Grafico 1: Acum de puntos
                        fig.add_trace(px.bar(grouped_df, x='puntos_corregidos', y='country',
                                              orientation='h', #text='puntos_corregidos',
                                              color='puntos_corregidos').data[0],
                                      row=1, col=1)
                        fig.update_xaxes(title='Prom. puntos', row=1, col=1)
    
                        # Grafico 2: GDP
                        grouped_df = filtered_df.groupby('country').mean().reset_index()
                        grouped_df = grouped_df.sort_values('orden_relativo_GDP', ascending=False)
    
                        fig.add_trace(px.bar(grouped_df, x='orden_relativo_GDP', y='country',
                                              orientation='h', #text='likes',
                                              color='orden_relativo_GDP').data[0],
                                      row=1, col=2)
                        fig.update_xaxes(title='Prom. Ranking PIB', row=1, col=2)
    
                        fig.update_layout(title={'text': f'Prom. Puntos vs Ranking Relativo PIB {year_range[0]}-{year_range[1]}', 'font_size': 24})
    
                        fig.update_yaxes(title='', row=1, col=1)
                        fig.update_traces(marker_color='#053BB6')
                        fig.update_layout(showlegend=False, height=1100)
                        fig.update(layout_coloraxis_showscale = False)
                        fig.update_traces(hovertemplate='pais = %{label}<br>promedio = %{value:.0f}')
    
                        st.plotly_chart(fig, use_container_width=True) 
                        
                except:
                    st.write('#### ❌ El gráfico no se ha podido generar debido a los filtros que has aplicado (has seleccionado un único país, un único año, 2020 sin concurso...)')
    
    
          # ---- GRAFICOS PUNTOS VS INFLUENCIA ---------------------------------------------------------
    
            with st.expander('PUNTOS vs INFLUENCIA 🔢💪🏻', expanded=False): 
    
                st.write('')
                Acum6 = st.checkbox("Ver en datos acumulados      ")
                st.write('❗ La puntuación de INFLUENCIA no tiene evolución histórica como tal, si no que es un valor estimado sobre la influencia de cada país sobre el resto en los últimos 30 años a partir de encuestas de GlobeScan/PIPA')
    
                try:
                    
                    if Acum6:
    
                        grouped_df = filtered_df.groupby('country').sum().reset_index()
                        grouped_df = grouped_df.sort_values('puntos_corregidos', ascending=False)
    
                        # Crear figura con tres subplots
                        fig = sp.make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.01)
    
                        # Grafico 1: Sum de puntos
                        fig.add_trace(px.bar(grouped_df, x='puntos_corregidos', y='country',
                                              orientation='h', #text='puntos_corregidos',
                                              color='puntos_corregidos').data[0],
                                      row=1, col=1)
                        fig.update_xaxes(title='Acum. puntos', row=1, col=1)
    
                        # Grafico 2: Influencia
                        grouped_df = filtered_df.groupby('country').mean().reset_index()
                        grouped_df = grouped_df.sort_values('influ_score', ascending=False)
    
                        fig.add_trace(px.bar(grouped_df, x='influ_score', y='country',
                                              orientation='h', #text='likes',
                                              color='influ_score').data[0],
                                      row=1, col=2)
                        fig.update_xaxes(title='Puntuación de Influencia', row=1, col=2)
    
                        fig.update_layout(title={'text': f'Acum. Puntos vs Influencia {year_range[0]}-{year_range[1]}', 'font_size': 24})
    
                        fig.update_yaxes(title='', row=1, col=1)
                        fig.update_traces(marker_color='#D8D335')
                        fig.update_layout(showlegend=False, height=1100)
                        fig.update(layout_coloraxis_showscale = False)
                        fig.update_traces(hovertemplate='pais = %{label}<br>valor = %{value:.0f}')
    
                        st.plotly_chart(fig, use_container_width=True) 
    
                    else:
                        grouped_df = filtered_df.groupby('country').mean().reset_index()
                        grouped_df = grouped_df.sort_values('puntos_corregidos', ascending=False)
    
                        # Crear figura con tres subplots
                        fig = sp.make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.01)
    
                        # Grafico 1: Sum de puntos
                        fig.add_trace(px.bar(grouped_df, x='puntos_corregidos', y='country',
                                              orientation='h', #text='puntos_corregidos',
                                              color='puntos_corregidos').data[0],
                                      row=1, col=1)
                        fig.update_xaxes(title='Prom. puntos', row=1, col=1)
    
                        # Grafico 2: Influencia
                        grouped_df = filtered_df.groupby('country').mean().reset_index()
                        grouped_df = grouped_df.sort_values('influ_score', ascending=False)
    
                        fig.add_trace(px.bar(grouped_df, x='influ_score', y='country',
                                              orientation='h', #text='likes',
                                              color='influ_score').data[0],
                                      row=1, col=2)
                        fig.update_xaxes(title='Puntuación de Influencia', row=1, col=2)
    
                        fig.update_layout(title={'text': f'Prom. Puntos vs Influencia {year_range[0]}-{year_range[1]}', 'font_size': 24})
    
                        fig.update_yaxes(title='', row=1, col=1)
                        fig.update_traces(marker_color='#D8D335')
                        fig.update_layout(showlegend=False, height=1100)
                        fig.update(layout_coloraxis_showscale = False)
                        fig.update_traces(hovertemplate='pais = %{label}<br>valor = %{value:.0f}')
    
                        st.plotly_chart(fig, use_container_width=True) 
    
                except:
                    st.write('#### ❌ El gráfico no se ha podido generar debido a los filtros que has aplicado (has seleccionado un único país, un único año, 2020 sin concurso...)')
                    
                    
          # ---- GRAFICOS PUNTOS VS REPUTACIÓN ---------------------------------------------------------
    
            with st.expander('PUNTOS vs REPUTACIÓN 🔢👍🏻', expanded=False): 
    
                st.write('')
                Acum7 = st.checkbox("Ver en datos acumulados        ")
                st.write('❗ El Ranking de REPUTACIÓN Internacional no tiene evolución histórica como tal, si no que es un valor calculado sobre la reputación de cada país entorno a ciencia, tecnología, cultura, paz, seguridad, medio ambiente, política, derechos humanos, igualdad, salud y bienestar. Estos datos han sido extraídos a partir de los índices de TheGoodCountry')
    
                try:
                    
                    if Acum7:
                        grouped_df = filtered_df.groupby('country').sum().reset_index()
                        grouped_df = grouped_df.sort_values('puntos_corregidos', ascending=False)
    
                        # Crear figura con tres subplots
                        fig = sp.make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.01)
    
                        # Grafico 1: Sum de puntos
                        fig.add_trace(px.bar(grouped_df, x='puntos_corregidos', y='country',
                                              orientation='h', #text='puntos_corregidos',
                                              color='puntos_corregidos').data[0],
                                      row=1, col=1)
                        fig.update_xaxes(title='Acum. puntos', row=1, col=1)
    
                        # Grafico 2: Reputación
                        grouped_df = filtered_df.groupby('country').mean().reset_index()
                        grouped_df = grouped_df.sort_values('reput_ranking', ascending=False)
    
                        fig.add_trace(px.bar(grouped_df, x='reput_ranking', y='country',
                                              orientation='h', #text='likes',
                                              color='reput_ranking').data[0],
                                      row=1, col=2)
                        fig.update_xaxes(title='Ranking de Reputación', row=1, col=2)
    
                        fig.update_layout(title={'text': f'Acum. Puntos vs Ranking Reputación {year_range[0]}-{year_range[1]}', 'font_size': 24})
    
                        fig.update_yaxes(title='', row=1, col=1)
                        fig.update_traces(marker_color='#EDB753')
                        fig.update_layout(showlegend=False, height=1100)
                        fig.update(layout_coloraxis_showscale = False)
                        fig.update_traces(hovertemplate='pais = %{label}<br>valor = %{value:.0f}')
    
                        st.plotly_chart(fig, use_container_width=True) 
    
                    else:
                        grouped_df = filtered_df.groupby('country').mean().reset_index()
                        grouped_df = grouped_df.sort_values('puntos_corregidos', ascending=False)
    
                        # Crear figura con tres subplots
                        fig = sp.make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.01)
    
                        # Grafico 1: Sum de puntos
                        fig.add_trace(px.bar(grouped_df, x='puntos_corregidos', y='country',
                                              orientation='h', #text='puntos_corregidos',
                                              color='puntos_corregidos').data[0],
                                      row=1, col=1)
                        fig.update_xaxes(title='Prom. puntos', row=1, col=1)
    
                        # Grafico 2: Reputación
                        grouped_df = filtered_df.groupby('country').mean().reset_index()
                        grouped_df = grouped_df.sort_values('reput_ranking', ascending=False)
    
                        fig.add_trace(px.bar(grouped_df, x='reput_ranking', y='country',
                                              orientation='h', #text='likes',
                                              color='reput_ranking').data[0],
                                      row=1, col=2)
                        fig.update_xaxes(title='Ranking Reputación', row=1, col=2)
    
                        fig.update_layout(title={'text': f'Prom. Puntos vs Ranking Reputación {year_range[0]}-{year_range[1]}', 'font_size': 24})
    
                        fig.update_yaxes(title='', row=1, col=1)
                        fig.update_traces(marker_color='#EDB753')
                        fig.update_layout(showlegend=False, height=1100)
                        fig.update(layout_coloraxis_showscale = False)
                        fig.update_traces(hovertemplate='pais = %{label}<br>valor = %{value:.0f}')
    
                        st.plotly_chart(fig, use_container_width=True) 
                        
                except:
                    st.write('#### ❌ El gráfico no se ha podido generar debido a los filtros que has aplicado (has seleccionado un único país, un único año, 2020 sin concurso...)')
                    
                    
        elif graf == 'Aspectos Técnicos':
            
        # -------TÉCNICOS ----------------------------------------------------------------------
          # ---- GRAFICOS ESTILOS ---------------------------------------------------------
    
            with st.expander('ESTILOS vs PAÍS 🤘🏻🌍', expanded=False):
                
                st.write('')
                sin_pop = st.checkbox("Visualizar sin POP")
                
                try:
                
                    if sin_pop:
    
                        concat_df = filtered_df.copy()
    
                        concat_df2 = concat_df.loc[concat_df['estilos'] != 'Pop']
    
                        concat_df2['entry'] = concat_df2['song'] + ' - ' + concat_df2['artist'] + ' (' + concat_df2['year'].astype(str) + ')'
    
                        df_count = concat_df2.groupby(['estilos', 'country', 'entry']).size().reset_index(name='count')
    
                        fig = px.treemap(df_count, path=[px.Constant('TODOS'), 'estilos', 'country', 'entry'], 
                                         values='count', height = 1000 
                                         )
                        fig.update_traces(root_color="lightgrey", hovertemplate='<b>%{label} </b> <br> Canciones: %{value}<br>')
    
                        fig.update_layout(title={'text': f'Cantidad de Países + Canciones por Estilo {year_range[0]}-{year_range[1]}', 'font_size': 24})
    
    
                        st.plotly_chart(fig, use_container_width=True) 
    
    
                    else:
    
                        concat_df = filtered_df.copy()
    
                        concat_df['entry'] = concat_df['song'] + ' - ' + concat_df['artist'] + ' (' + concat_df['year'].astype(str) + ')'
    
                        df_count = concat_df.groupby(['estilos', 'country', 'entry']).size().reset_index(name='count')
    
                        fig = px.treemap(df_count, path=[px.Constant('TODOS'), 'estilos', 'country', 'entry'], 
                                         values='count', height = 1000 
                                         )
                        fig.update_traces(root_color="lightgrey", hovertemplate='<b>%{label} </b> <br> Canciones: %{value}<br>')
    
                        fig.update_layout(title={'text': f'Cantidad de Países + Canciones por Estilo {year_range[0]}-{year_range[1]}', 'font_size': 24})
    
                        st.plotly_chart(fig, use_container_width=True) 
                        
                except:
                    st.write('#### ❌ El gráfico no se ha podido generar debido a los filtros que has aplicado (has seleccionado un único país, un único año, 2020 sin concurso...)')
    
            
            with st.expander('PAÍS vs ESTILOS 🌍🤘🏻', expanded=False):
                
                st.write('')
                sin_pop2 = st.checkbox("Visualizar sin POP ")
                
                try:
                
                    if sin_pop2:
    
                        concat_df = filtered_df.copy()
    
                        concat_df2 = concat_df.loc[concat_df['estilos'] != 'Pop']
    
                        concat_df2['entry'] = concat_df2['song'] + ' - ' + concat_df2['artist'] + ' (' + concat_df2['year'].astype(str) + ')'
    
                        df_count = concat_df2.groupby(['country', 'estilos', 'entry']).size().reset_index(name='count')
    
                        fig = px.treemap(df_count, path=[px.Constant('TODOS'), 'country', 'estilos', 'entry'], 
                                         values='count', height = 1000 
                                         )
                        fig.update_traces(root_color="lightgrey", hovertemplate='<b>%{label} </b> <br> Canciones: %{value}<br>')
    
                        fig.update_layout(title={'text': f'Cantidad de Estilos por País {year_range[0]}-{year_range[1]}', 'font_size': 24})
    
                        st.plotly_chart(fig, use_container_width=True) 
    
    
                    else:
    
                        concat_df = filtered_df.copy()
    
                        concat_df['entry'] = concat_df['song'] + ' - ' + concat_df['artist'] + ' (' + concat_df['year'].astype(str) + ')'
    
                        df_count = concat_df.groupby(['country', 'estilos', 'entry']).size().reset_index(name='count')
    
                        fig = px.treemap(df_count, path=[px.Constant('TODOS'), 'country', 'estilos', 'entry'], 
                                         values='count', height = 1000 
                                         )
                        fig.update_traces(root_color="lightgrey", hovertemplate='<b>%{label} </b> <br> Canciones: %{value}<br>')
    
                        fig.update_layout(title={'text': f'Cantidad de Estilos por País {year_range[0]}-{year_range[1]}', 'font_size': 24})
    
    
                        st.plotly_chart(fig, use_container_width=True) 
    
                except:
                    st.write('#### ❌ El gráfico no se ha podido generar debido a los filtros que has aplicado (has seleccionado un único país, un único año, 2020 sin concurso...)')
                          
        # ---- GRAFICOS PALABRAS ---------------------------------------------------------
    
            with st.expander('Palabras más usadas 🔤', expanded=False):
                st.write('')
                st.write('❗ La imagen que observarás abajo se acaba de generar de manera dinámica con las palabras más usadas (si filtras los datos se generará una nueva)')
                st.write(f'<p style="font-size: 24px; text-align: left;">Palabras más usadas {year_range[0]}-{year_range[1]}</p>', unsafe_allow_html=True)
                
    #             image_eu = Image.open("./img/palabras_UE-removebg.png")
    #             with io.BytesIO() as output:
    #                 image_eu.save(output, format="PNG")
    #                 b64_2 = base64.b64encode(output.getvalue()).decode()
    #             st.image(f"data:image/png;base64,{b64_2}", use_column_width=True) 
    
                try:
                    words_df = pd.concat([filtered_df['top1word'], filtered_df['top2word'], filtered_df['top3word'], filtered_df['top4word'], filtered_df['top5word']])
                    words = words_df.tolist()
                    dict_prueba = {word: words_df.tolist().count(word) for word in words}            
                    img = cv2.imread('./img/europe.jpg')
                    gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    wordcloud = WordCloud(width = 1000, height = 500, background_color='white', mask=gray_img).generate_from_frequencies(dict_prueba)
                    #plt.figure(figsize=(40,20))
                    plt.axis("off")
                    img_pil = Image.fromarray(wordcloud.to_array())
                    st.image(img_pil, use_column_width=True)
    
                except:
                    st.write('#### ❌ El gráfico no se ha podido generar debido a los filtros que has aplicado (has seleccionado un único país, un único año, 2020 sin concurso...)')
            
    
        # ---- GRAFICOS LONGITUD ---------------------------------------------------------
    
            with st.expander('Longitud de la canción ⏩', expanded=False):
    
                st.write('')
                Acum9 = st.checkbox("Ver en datos acumulados                    ")
                
                try:
    
                    if Acum9:
    
                        grouped_df = filtered_df.groupby('country').sum().reset_index()
                        grouped_df = grouped_df.sort_values('lyrics_long', ascending=False)
    
                        # Crear figura con tres subplots
                        fig = sp.make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.01)
    
                        # Grafico 1: Acum de Palabras
                        fig.add_trace(px.bar(grouped_df, x='lyrics_long', y='country',
                                              orientation='h',
                                              color='lyrics_long').data[0],
                                      row=1, col=1)
                        fig.update_xaxes(title='Acum. Palabras', row=1, col=1)
                        fig.update_layout(title={'text': f'Acum. Palabras + Palabras Únicas {year_range[0]}-{year_range[1]}', 'font_size': 24})
    
                        # Grafico 2: Acum de Palabras Únicas
                        grouped_df = filtered_df.groupby('country').sum().reset_index()
                        grouped_df = grouped_df.sort_values('unic_words', ascending=False)
    
                        fig.add_trace(px.bar(grouped_df, x='unic_words', y='country',
                                              orientation='h',
                                              color='unic_words').data[0],
                                      row=1, col=2)
                        fig.update_xaxes(title='Acum. Palabras Únicas', row=1, col=2)
    
                        fig.update_yaxes(title='', row=1, col=1)
                        fig.update_traces(marker_color='#2277BA')
                        fig.update_layout(showlegend=False, height=1100)
                        fig.update(layout_coloraxis_showscale = False)
                        fig.update_traces(hovertemplate='pais = %{label}<br>acumulado = %{value:.0f}')
    
                        st.plotly_chart(fig, use_container_width=True)
    
    
                    else:
    
                        grouped_df = filtered_df.groupby('country').mean().reset_index()
                        grouped_df = grouped_df.sort_values('lyrics_long', ascending=False)
    
                        # Crear figura con tres subplots
                        fig = sp.make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.01)
    
                        # Grafico 1: Acum de Palabras
                        fig.add_trace(px.bar(grouped_df, x='lyrics_long', y='country',
                                              orientation='h', #text='puntos_corregidos',
                                              color='lyrics_long').data[0],
                                      row=1, col=1)
                        fig.update_xaxes(title='Prom. Palabras', row=1, col=1)
    
                        # Grafico 2: Promedio de Palabras Únicas
                        grouped_df = filtered_df.groupby('country').mean().reset_index()
                        grouped_df = grouped_df.sort_values('unic_words', ascending=False)
    
                        fig.add_trace(px.bar(grouped_df, x='unic_words', y='country',
                                              orientation='h',
                                              color='unic_words').data[0],
                                      row=1, col=2)
                        fig.update_xaxes(title='Prom. Palabras Únicas', row=1, col=2)
                        fig.update_layout(title={'text': f'Prom. Palabras + Palabras Únicas {year_range[0]}-{year_range[1]}', 'font_size': 24})
    
                        fig.update_yaxes(title='', row=1, col=1)
                        fig.update_traces(marker_color='#2277BA')
                        fig.update_layout(showlegend=False, height=1100)
                        fig.update(layout_coloraxis_showscale = False)
                        fig.update_traces(hovertemplate='pais = %{label}<br>promedio = %{value:.0f}')
    
                        st.plotly_chart(fig, use_container_width=True)
                        
                except:
                    st.write('#### ❌ El gráfico no se ha podido generar debido a los filtros que has aplicado (has seleccionado un único país, un único año, 2020 sin concurso...)')
                    
    
            with st.expander('Top 20 Canciones según LONGITUD PALABRAS🔝', expanded=False):
                
                try:
                
                    concat_df = filtered_df.copy()
                    concat_df['entry'] = concat_df['song'] + ' - ' + concat_df['artist']
                    concat_df['paisano'] = concat_df['country'] + ' ' + concat_df['year'].astype(str) 
    
                    largestP_df = concat_df.sort_values('lyrics_long', ascending=False)[:20].reset_index()
                    shortestP_df = concat_df.sort_values('lyrics_long', ascending=True)[:20].reset_index()
                    largestU_df = concat_df.sort_values('unic_words', ascending=False)[:20].reset_index()
                    shortestU_df = concat_df.sort_values('unic_words', ascending=True)[:20].reset_index()  
    
                    # -- Grafico Largest ---
                    fig = px.bar(largestP_df, x='lyrics_long', y='paisano', hover_data=['entry', 'lyrics_long'],
                        orientation='h', height=600)
    
                    fig.update_layout(title={'text': f'Top 20 Canciones con MÁS PALABRAS {year_range[0]}-{year_range[1]}', 'font_size': 24}, xaxis_title='Palabras Únicas')
                    fig.update_traces(marker_color='#BB34AD')
                    fig.update_yaxes(title='')
                    fig.update_traces(hovertemplate='Canción = %{customdata[0]}<br>Palabras = %{value:.0f}')
    
                    st.plotly_chart(fig, use_container_width=True)
    
    
                    # -- Grafico Shortest ---
                    fig = px.bar(shortestP_df, x='lyrics_long', y='paisano', hover_data=['entry', 'lyrics_long'],
                        orientation='h', height=600)
    
                    fig.update_layout(title={'text': f'Top 20 Canciones con MENOS PALABRAS {year_range[0]}-{year_range[1]}', 'font_size': 24}, xaxis_title='Palabras Únicas')
                    fig.update_traces(marker_color='#1F9CC4')
                    fig.update_yaxes(title='')
                    fig.update_traces(hovertemplate='Canción = %{customdata[0]}<br>Palabras = %{value:.0f}')
    
                    st.plotly_chart(fig, use_container_width=True)
    
                    # -- Grafico Largest Unics ---
                    fig = px.bar(largestU_df, x='unic_words', y='paisano', hover_data=['entry', 'unic_words'],
                        orientation='h', height=600)
    
                    fig.update_layout(title={'text': f'Top 20 Canciones con MÁS PALABRAS ÚNICAS {year_range[0]}-{year_range[1]}', 'font_size': 24}, xaxis_title='Palabras Únicas')
                    fig.update_traces(marker_color='#BB34AD')
                    fig.update_yaxes(title='')
                    fig.update_traces(hovertemplate='Canción = %{customdata[0]}<br>Palabras Únicas = %{value:.0f}')
    
                    st.plotly_chart(fig, use_container_width=True)
    
    
                    # -- Grafico Shortest Unics---
                    fig = px.bar(shortestU_df, x='unic_words', y='paisano', hover_data=['entry', 'unic_words'],
                        orientation='h', height=600)
    
                    fig.update_layout(title={'text': f'Top 20 Canciones con MENOS PALABRAS ÚNICAS {year_range[0]}-{year_range[1]}', 'font_size': 24}, xaxis_title='Palabras Únicas')
                    fig.update_traces(marker_color='#1F9CC4')
                    fig.update_yaxes(title='')
                    fig.update_traces(hovertemplate='Canción = %{customdata[0]}<br>Palabras Únicas= %{value:.0f}')
    
                    st.plotly_chart(fig, use_container_width=True)
                    
                except:
                    st.write('#### ❌ El gráfico no se ha podido generar debido a los filtros que has aplicado (has seleccionado un único país, un único año, 2020 sin concurso...)')
    
    
            with st.expander('Top 20 Canciones según LONGITUD TIEMPO ⏱️', expanded=False):
    
                shortestT_df = concat_df.sort_values('duracion_eurovision', ascending=True).reset_index()
                shortestT_df = shortestT_df[shortestT_df['duracion_eurovision'] != '0:00'][:20]
                shortestT_df['segundos'] = [int(s.split(':')[0])*60 + int(s.split(':')[1]) for s in shortestT_df['duracion_eurovision']]
                # st.write(shortestT_df)
                
                try:
    
                    # -- Grafico Shortest Tiempo ---
                    fig = px.bar(shortestT_df, x='segundos', y='paisano', hover_data=['entry', 'segundos', 'duracion_eurovision'],
                        orientation='h', height=600)
    
                    fig.update_layout(title={'text': f'Top 20 Canciones con MENOR DURACIÓN {year_range[0]}-{year_range[1]}', 'font_size': 24}, xaxis_title='Segundos')
                    fig.update_layout(xaxis=dict(range=[0, 180]))
                    fig.update_traces(marker_color='#ECB94B')
                    fig.update_yaxes(title='')
                    fig.update_traces(hovertemplate='Canción = %{customdata[0]}<br>Duración = %{customdata[1]}')
    
                    st.plotly_chart(fig, use_container_width=True)
                    
                except:
                    st.write('#### ❌ Los gráficos no se han podido generar debido a los filtros que has aplicado (has seleccionado un único país, un único año, 2020 sin concurso...)')
                
                
      # ---- GRAFICOS IDIOMAS ---------------------------------------------------------
    
            with st.expander('IDIOMAS vs PAÍS 🗣️🌍', expanded=False):
                
                st.write('')
                sin_ing = st.checkbox("Visualizar sin INGLÉS")
                st.write('❗ Solo se ha podido registrar el idioma de las canciones finalistas debido a que no existían datos consistentes de todas las canciones')
    
                try: 
                    if sin_ing:
                    
                        concat_df = filtered_df.copy()
                    
                        concat_df2 = concat_df.loc[concat_df['idioma1'] != 'English']
                    
                        concat_df2['entry'] = concat_df2['song'] + ' - ' + concat_df2['artist'] + ' (' + concat_df2['year'].astype(str) + ')'
    
                        df_count = concat_df2.groupby(['idioma1', 'country', 'entry']).size().reset_index(name='count')
    
                        fig = px.treemap(df_count, path=[px.Constant('TODOS'), 'idioma1', 'country', 'entry'], 
                                     values='count', height = 1000 
                                     )
                        fig.update_traces(root_color="lightgrey", hovertemplate='<b>%{label} </b> <br> Canciones: %{value}<br>')
                    
                        fig.update_layout(title={'text': f'Idiomas por País {year_range[0]}-{year_range[1]}', 'font_size': 24})
     
                        st.plotly_chart(fig, use_container_width=True) 
                    
                    
                    else:
                
                        concat_df = filtered_df.copy()
    
                        concat_df['entry'] = concat_df['song'] + ' - ' + concat_df['artist'] + ' (' + concat_df['year'].astype(str) + ')'
    
                        df_count = concat_df.groupby(['idioma1', 'country', 'entry']).size().reset_index(name='count')
    
                        fig = px.treemap(df_count, path=[px.Constant('TODOS'), 'idioma1', 'country', 'entry'], 
                                     values='count', height = 1000 
                                     )
                        fig.update_traces(root_color="lightgrey", hovertemplate='<b>%{label} </b> <br> Canciones: %{value}<br>')
                                             
                        fig.update_layout(title={'text': f'Idiomas por País {year_range[0]}-{year_range[1]}', 'font_size': 24})
    
                        st.plotly_chart(fig, use_container_width=True) 
    
                except:
                    st.write('#### ❌ El gráfico no se ha podido generar debido a los filtros que has aplicado (has seleccionado un único país, un único año, 2020 sin concurso...)')
                    
        # ---- GRAFICOS ESTRUCTURA ---------------------------------------------------------
    
            with st.expander('ESTRUCTURA vs PAÍS 🔠🌍', expanded=False):
                
                st.write('')
                st.write('❗ En este gráfico solo se visualizan aquellas canciones cuya estructura ha podido ser registrada, dado que no existían datos consistentes sobre ello')
                st.write('❗ Los valores del gráfico son acrónimos de Introducció (I), Verso (V), Estrofa (E), Puente (P), Coda (C) e Instrumental (B)')
    
                concat_df = filtered_df.copy()
    
                concat_df2 = concat_df.loc[concat_df['estruc_resum'] != 'UNKNOWN']
    
                concat_df2['entry'] = concat_df2['song'] + ' - ' + concat_df2['artist'] + ' (' + concat_df2['year'].astype(str) + ')'
                
                try:
    
                    df_count = concat_df2.groupby(['estruc_resum', 'country', 'entry']).size().reset_index(name='count')
    
                    fig = px.treemap(df_count, path=[px.Constant('TODOS'), 'estruc_resum', 'country', 'entry'], 
                                     values='count', height = 1000 
                                     )
                    fig.update_traces(root_color="lightgrey", hovertemplate='<b>%{label} </b> <br> Canciones: %{value}<br>')
    
                    fig.update_layout(title={'text': f'Estructura de la canción por País {year_range[0]}-{year_range[1]}', 'font_size': 24})
    
                    st.plotly_chart(fig, use_container_width=True) 
                    
                except:
                    st.write('#### ❌ El gráfico no se ha podido generar debido a los filtros que has aplicado (has seleccionado un único país, un único año, 2020 sin concurso...)')
    else:
        # Muestra el DataFrame filtrado
        st.write('\n')
    
        st.markdown("<h4 style='margin-bottom: 5px;'>🔢 Tabla de datos </h4>", unsafe_allow_html=True)
        with st.expander('Ver Datos', expanded=False): 
            st.write('❗ A partir de 2016 los puntos se han corregido, dividiéndolos entre 2, para ser consistentes con el sistema de votación del periodo 2002-2015')

            # st.write(filtered_df)
            df_to_show = filtered_df[['links','country','year','artist','song','clasificacion','puntos_corregidos','propo_max_puntos','finalista','order_act',
                                     'estilos','idioma1','idioma2','idioma3','love_song', 'top1word', 'top2word', 'top3word', 'top4word', 'top5word', 'estruc_resum',
                                     'views', 'likes', 'shazams', 'bet_mean', 'lyrics_long', 'unic_words', 'duracion_eurovision', 'duracion_spoty',
                                     'vecinos_participantes','GDP', 'orden_relativo_GDP', 'influ_ranking', 'influ_score', 'reput_ranking' ]]
    
            nuevos_nombres = ['Link','País','Año','Cantante/s','Canción','Clasificación','Puntos','% Puntos','Finalista','Orden actuación',
                                     'Estilo','1º Idioma','2º Idioma','3º Idioma','Temática Amor', '1ª Palabra', '2ª Palabra', '3ª Palabra', '4ª Palabra', '5ª Palabra', 'Estructura',
                                     'Views YT', 'Likes YT', 'Shazams', 'Cuota Apuestas', 'Longitud letra', 'Palabras Únicas', 'Duración ESC', 'Duración Spotify',
                                     'Vecinos Participantes','PIB país', 'Ranking PIB', 'Ranking Influencia', 'Puntos Influencia', 'Ranking Reputación']
            df_to_show.columns = nuevos_nombres
    
            def corregir_numero(val):
                return int(val) 
    
            def corregir_text(val):
                try:
                    return val.strip()
                except:
                    return val
            def sustituir_valor_emoji(val):
                if val == "Yes":
                    return "✅"
                elif val == "No":
                    return "❌"
                else:
                    return val 
    
            columnas_a_modificar = ['Finalista', 'Temática Amor']
            for columna in columnas_a_modificar:
                df_to_show[columna] = df_to_show[columna].apply(sustituir_valor_emoji)
    
            columnas_a_modificar_2 = ['Cantante/s', 'Canción', 'Estilo', '1º Idioma', '2º Idioma', '3º Idioma', '1ª Palabra', '2ª Palabra', '3ª Palabra', '4ª Palabra', '5ª Palabra', 'Estructura']
            for columna in columnas_a_modificar_2:
                df_to_show[columna] = df_to_show[columna].apply(corregir_text)
                
            df_to_show['Likes YT'] = df_to_show['Likes YT'].apply(corregir_numero)
    
            df_to_show['% Puntos'] = df_to_show['% Puntos'].round(2)
    
            df_to_show['Cuota Apuestas'] = df_to_show['Cuota Apuestas'].round(2)
    
            df_to_show['Puntos Influencia'] = df_to_show['Puntos Influencia'].round(2)
    
            st.data_editor(
                df_to_show,
                column_config={
                    "Link": st.column_config.LinkColumn(
                        "🔗 Link", display_text = "🌐 Video YT"
                    ),
                    
                    "% Puntos": st.column_config.ProgressColumn(
                        "% Puntos",
                        format="%f",
                        min_value=0,
                        max_value=1,
                    ),
    
                    "Puntos Influencia": st.column_config.ProgressColumn(
                        "Puntos Influencia",
                        format="%f",
                        min_value=0,
                        max_value=100,
                    ),
    
                },
                hide_index=True,
            )
            # st.write(df_to_show)
        st.write('')
        if graf == 'Evolución Histórica':

            st.markdown("<h4 style='margin-bottom: 5px;'>📈 Gráficos</h4>", unsafe_allow_html=True)

    
        # -------HISTÓRICOS ----------------------------------------------------------------------
            
            # st.write('En desarrollo...')
    
            df_to_evol = filtered_df[['country','year','clasificacion','puntos_corregidos','propo_max_puntos',
                                     'views', 'likes', 'shazams', 'bet_mean']]
    
            df = df_to_evol.copy()
            df = df.sort_values(by = ["country", "year"], ascending=True).fillna(0)
            
            # st.write(df)

            with st.expander('Evolución Histórica de Puntos por Año 🔢⏳', expanded=False): 
    
                # -------PUNTOS POR AÑO ----------------------------------------------------------------------
        
                fig1 = px.line(df, x='year', y='puntos_corregidos', color='country', 
                       title='',
                       labels={'puntos_corregidos': 'Puntos', 'year': 'Año'},
                       hover_name='country', markers=True)
                
                # Configuración del eje y para incluir ceros
                fig1.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='black')
                fig1.update_layout(title={'text': f'Puntos por país {year_range[0]}-{year_range[1]}', 'font_size': 24})
                
                st.plotly_chart(fig1, use_container_width=True)

                # -------PUNTOS POR AÑO BARRAS ----------------------------------------------------------------------
                
                st.markdown(f'#### Puntos por país {year_range[0]}-{year_range[1]} - Barras')

                # Agregar un checkbox para cambiar entre puntos y escala porcentual
                porcentaje = st.checkbox("Ver en escala porcentual")
                
                # Si el checkbox está marcado, convertir los datos a porcentajes
                if porcentaje:
                    total_por_anio = df.groupby('year')['puntos_corregidos'].transform('sum')
                    df['puntos_corregidos'] = (df['puntos_corregidos'] / total_por_anio) * 100
        
                # Creamos el gráfico de barras apiladas

                colors = {'Albania 🇦🇱 ': '#1f67b4', 'Andorra 🇦🇩 ': '#ff6f0e', 'Armenia 🇦🇲 ': '#64DA39', 'Australia 🇦🇺 ': '#d62528',
                'Austria 🇦🇹 ': '#9467bd', 'Azerbaijan 🇦🇿 ': '#24E19C', 'Belarus 🇧🇾 ': '#e377c2', 'Belgium 🇧🇪 ': '#C4A4BC',
                'Bosnia and Herzegovina 🇧🇦 ': '#E7F77C','Bosn. & Herz. 🇧🇦 ': '#E7F77C', 'Bulgaria 🇧🇬 ': '#A2EFBE', 'Croatia 🇭🇷 ': '#1f27b4', 'Cyprus 🇨🇾 ': '#ff7f0e',
                'Czechia 🇨🇿 ': '#2ca12c', 'Denmark 🇩🇰 ': '#d62628', 'Estonia 🇪🇪 ': '#9447bd', 'Finland 🇫🇮 ': '#60FDED',
                'France 🇫🇷 ': '#B69BF3', 'Georgia 🇬🇪 ': '#7f7f6f', 'Germany 🇩🇪 ': '#bcbd52', 'Greece 🇬🇷 ': '#16becf',
                'Hungary 🇭🇺 ': '#1f57b4', 'Iceland 🇮🇸 ': '#ff5f0e', 'Ireland 🇮🇪 ': '#2ca22c', 'Israel 🇮🇱 ': '#d62428',
                'Italy 🇮🇹 ': '#8BFD8F', 'Latvia 🇱🇻 ': '#E856A4', 'Lithuania 🇱🇹 ': '#e357c2', 'Malta 🇲🇹 ': '#50AB5C',
                'Moldova 🇲🇩 ': '#F39BEA', 'Montenegro 🇲🇪 ': '#14becf', 'North Macedonia 🇲🇰 ': '#5F6EF2','N. Macedonia 🇲🇰 ':'#5F6EF2' ,'Norway 🇳🇴 ': '#F77CEB',
                'Poland 🇵🇱 ': '#C644B9', 'Portugal 🇵🇹 ': '#FD5B7C', 'Romania 🇷🇴 ': '#9437bd', 'Russia 🇷🇺 ': '#EFB1B1',
                'San Marino 🇸🇲 ': '#e347c2', 'Serbia 🇷🇸 ': '#AAB2FD', 'Slovakia 🇸🇰 ': '#bcbd62', 'Slovenia 🇸🇮 ': '#12becf',
                'Spain 🇪🇸 ': '#1f77b4', 'Sweden 🇸🇪 ': '#ff3f0e', 'Switzerland 🇨🇭 ': '#2ca42c', 'Netherlands 🇳🇱 ': '#F6BE76','The Netherlands 🇳🇱 ': '#F6BE76',
                'Turkey 🇹🇷 ': '#E626B3', 'Ukraine 🇺🇦 ': '#F9F919', 'United Kingdom 🇬🇧 ': '#EED55B', 'UK 🇬🇧 ': '#EED55B', 
                'Luxemburgo 🇱🇺 ': '#7f7f3f','Serb. & Mont. 🇷🇸🇲🇪 ':'#6AEB66', 'Monaco 🇲🇨 ':'#EC21D8'
                }


                # Creamos una lista vacía para almacenar los datos de las barras
                data = []
                                    
                # Configuración del diseño del gráfico
                if porcentaje:
                    for year in df['year'].unique():
                        # Filtramos el DataFrame por año
                        df_year = df[df['year'] == year]
                        
                        # Ordenamos las filas por puntos corregidos en orden descendente
                        df_year_sorted = df_year.sort_values(by='puntos_corregidos', ascending=False)
                        
                        # Creamos una lista de nombres de países ordenados
                        sorted_countries = df_year_sorted['country'].tolist()
                        
                        # Creamos una lista de valores de puntos corregidos ordenados
                        sorted_points = df_year_sorted['puntos_corregidos'].tolist()
                        
                        # Creamos una lista de colores para las barras de cada país
                        bar_colors = [colors[country] for country in sorted_countries]
                        
                        # Añadimos una barra para cada país en el año actual
                        for country, points, color in zip(sorted_countries, sorted_points, bar_colors):
                            data.append(go.Bar(x=[year], y=[points], name=country, marker=dict(color=color), legendgroup=country, showlegend=False,
                                                hoverinfo='skip',
                                                hovertemplate=f"<b>{country}</b><br>% Puntos: {points:.2f}%<extra></extra>",
                                                hoverlabel=dict(font=dict(color='black'))))
                    layout = dict(barmode='stack',
                                  yaxis={'title': '% Puntos','title_standoff': 0},
                                  xaxis={'title': 'Año'},
                                  margin=dict(t=0),
                                  legend={'title': {'text': 'Países', 'font': {'color': 'black'}}})  # Ajustar el color del título de la leyenda a negro
                else:
                    for year in df['year'].unique():
                        # Filtramos el DataFrame por año
                        df_year = df[df['year'] == year]
                        
                        # Ordenamos las filas por puntos corregidos en orden descendente
                        df_year_sorted = df_year.sort_values(by='puntos_corregidos', ascending=False)
                        
                        # Creamos una lista de nombres de países ordenados
                        sorted_countries = df_year_sorted['country'].tolist()
                        
                        # Creamos una lista de valores de puntos corregidos ordenados
                        sorted_points = df_year_sorted['puntos_corregidos'].tolist()
                        
                        # Creamos una lista de colores para las barras de cada país
                        bar_colors = [colors[country] for country in sorted_countries]
                        
                        # Añadimos una barra para cada país en el año actual
                        for country, points, color in zip(sorted_countries, sorted_points, bar_colors):
                            data.append(go.Bar(x=[year], y=[points], name=country, marker=dict(color=color), legendgroup=country, showlegend=False,
                                                hoverinfo='skip',
                                                hovertemplate=f"<b>{country}</b><br>Puntos: {points}<extra></extra>",
                                                hoverlabel=dict(font=dict(color='black'))))
                    layout = dict(barmode='stack',
                                  yaxis={'title': 'Puntos','title_standoff': 0},
                                  xaxis={'title': 'Año'},
                                  margin=dict(t=0),
                                  legend={'title': {'text': 'Países', 'font': {'color': 'black'}}})  # Ajustar el color del título de la leyenda a negro

                
                # Creamos la figura
                fig = go.Figure(data=data, layout=layout)
                
                # Mostramos el gráfico en Streamlit
                # fig.update_layout(title={'text': f'Puntos por país {year_range[0]}-{year_range[1]} - BARRAS', 'font_size': 24})
                st.plotly_chart(fig, use_container_width=True)
        
                # -------PUNTOS ACUMULADOS POR AÑO -----------------------------------------------------------
                
                df_histo = load_data_histo()
                
                # Seleccionar las columnas que representan los años dentro del rango especificado
                cols_in_range = [int(year) for year in range(year_range[0], year_range[1] + 1)]
                
                # Filtrar el DataFrame para incluir solo las columnas dentro del rango de años
                cols_filter = ['country', 'Image URL']
                cols_filter.extend(cols_in_range)
        
                df_histo = df_histo.loc[:, df_histo.columns.isin(cols_filter)]
                
                # Si también necesitas filtrar por países seleccionados:
                if selected_country:
                    df_histo = df_histo[df_histo['country'].isin(selected_country)]
                
                # st.write(df_histo)
                
                # Derretir el DataFrame para convertir los años en filas
                df_melted = df_histo.melt(id_vars=['country', 'Image URL'], var_name='year', value_name='valor')
                
                # Convertir la columna 'year' al tipo de dato adecuado
                df_melted['year'] = pd.to_datetime(df_melted['year'], format='%Y')
                
                # Gráfico de líneas
                fig = px.line(df_melted, x='year', y='valor', color='country',
                              title='Valor de cada país en cada año',
                              labels={'valor': 'Puntos', 'year': 'Año'},
                              hover_name='country', line_group='country', markers=True)

                fig.update_layout(title={'text': f'Puntos acum. (desde 2002) para {year_range[0]}-{year_range[1]}', 'font_size': 24})
                st.plotly_chart(fig, use_container_width=True)

            with st.expander('Acumulados Histórico 🔢🛒', expanded=False): 

                st.write('❗ Los siguientes gráficos no se filtrarán por país y/o año ya que el cálculo acumulado carecería de sentido.')
                st.write('')

                # # -------CARRERA PUNTOS ACUMULADOS POR AÑO TOP20----------------------------------------------------
        
                html_code1 = """
                <div class="flourish-embed flourish-bar-chart-race" data-src="visualisation/17473996"><script src="https://public.flourish.studio/resources/embed.js"></script></div>
                """
                
                # Establecer un margen inferior negativo para minimizar el espacio
                st.markdown('#### Evolución dinámica puntos acumulados 2002-2023 - TOP20')
                st.components.v1.html(html_code1, width=600, height=600)
                
                # # -------PUNTOS ACUMULADOS POR AÑO Por CANCIÓN----------------------------------------------------
                
                # Establecer un margen superior negativo para minimizar el espacio
                html_code2 = """
                    <div class="flourish-embed flourish-hierarchy" data-src="visualisation/17597991"><script src="https://public.flourish.studio/resources/embed.js"></script></div>                
                    """
                st.markdown("<h4 style='margin-bottom: -10px; margin-top: -80px;'>Repartos acumulados por canción 2002-2023</h4>", unsafe_allow_html=True)
                # st.markdown('#### Reparto puntos acumulados por canción 2002-2023')
                st.components.v1.html(html_code2, width=600, height=600)
                
# ---------------------------------------------------------------------------------------------------------------------------------------------

with tab3:
    
    st.markdown('<h1 style="text-align:center"><span style="font-size: 40px;">🎙️</span> <u>THE EUROVISION GAME</u></h1>', unsafe_allow_html=True)

    st.markdown('<h2 style="text-align:center"><span style="font-size: 15px;"></span> ¡Bienvenidos al juego de Eurovision! ¿Con quién tenemos el placer de jugar?</h2>', unsafe_allow_html=True)
    
    participante = st.text_input("Me llamo...")
    list_name = participante + " The Eurovision Game"

    # CARGAMOS DATA TO TRAIN
    @st.cache_data
    def load_data():
        data = pd.read_excel("./data/Data_to_train.xlsx")
        data.drop("Unnamed: 0", axis=1, inplace=True)
        return data

    @st.cache_data
    def split_data(data):
        X = data.drop("propo_puntos", axis=1)
        y = data.propo_puntos
        X_train, X_test, y_train, y_test = tts(
            X, y, train_size=0.99, test_size=0.01, random_state=22
        )
        return X_train, X_test, y_train, y_test

    @st.cache_data
    def train_model(X_train, y_train):
        ctr = CTR(iterations=5, verbose=False)
        ctr.fit(X_train, y_train)
        return ctr

    data = load_data()
    X_train, X_test, y_train, y_test = split_data(data)
    ctr = train_model(X_train, y_train)
    y_pred = ctr.predict(X_test)

    # y_pred = ctr.predict(X_test)

# ---------------------------------------------------------------------------

    st.write('')
    #st.write('### Elige el nº de participantes')
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)


    if participante:
        
        st.success('🧡 Introduce las canciones que desees para jugar a The Eurovision Game. Las canciones **no tienen por qué haber participado** en el festival. El objetivo del juego es aplicar un modelo de machine learning entrenado con los últimos 20 años de concurso y simular cómo quedaría cualquier selección de canciones en caso de participar hoy en Eurovisión')
        
        participantes = col1.selectbox('Nº participantes', options=num_part)

        if participantes < 11:
            st.warning('⚠️ Las puntuaciones no serán 100% representativas al haber menos de 11 participantes, pero sí lo serán las posiciones obtenidas')
            
        try:
            
            def create_form():
                selected_countries = []
                user_songs = []
                for i in range(participantes):
                    col1, col2, col3, col4 = st.columns(4)
                    song = col1.text_input(f'Canción {i+1}')
                    singer = col2.text_input(f'Cantante {i+1}')
                    available_countries = get_available_countries(selected_countries)
                    country = col3.selectbox(f'País {i+1}', options=available_countries)
                    selected_countries.append(country)
                    manager = col4.text_input(f'Jugador {i+1}')
                    user_songs.append({'song': song, 'singer': singer, 'country': country, 'manager': manager})
                    st.write('-----')
                return user_songs

            if __name__ == '__main__':
                st.title('🗒️ Registro de canciones')
                st.write('')
              
                user_songs = create_form()
                st.write('')
                st.write('')
                if st.button('Enviar'):
                    user_songs = [song for song in user_songs if all(song.values())]
                    if len(user_songs) < 3:
                        st.warning('⚠️ No puede haber un concurso "modo Eurovisión" con menos de 3 participantes.')
                        #st.write(user_songs)
                    else:
                        try:
                            #st.write(user_songs)
                            resultado = predicciones(user_songs)
                            df = pd.DataFrame(resultado)
                            df_sorted = df.sort_values('points', ascending=False).reset_index(drop=True)
                            # df_sorted
                            # df_sorted['country1'] = [e.replace(' ','·') for e in df_sorted['country']]

                            if len(df_sorted) > 26:
                                first_points = df_sorted['points'][0]
                                last_points = df_sorted['points'][26]

                                pendiente = first_points/(first_points-last_points)
                                intercept = (first_points*last_points)/(first_points-last_points)

                                total_points = df_sorted['points'].sum()

                                for i,p in enumerate(df_sorted['points']):
                                    df_sorted.loc[i, 'points'] = round(pendiente*p-intercept)

                                df_sorted.loc[26:, 'points'] = 0

                                total_points = df_sorted['points'].sum()

                                cociente = (116*len(df_sorted))/total_points

                                for i,puntos in enumerate(df_sorted['points'][:26]):
                                    df_sorted.loc[i, 'points'] = round(puntos*cociente)

                                total_points = df_sorted['points'].sum()

                                diferencia = 116*len(df_sorted)-total_points

                                # Me quedo con el último índice no nulo
                                for i,p in enumerate(df_sorted['points']):
                                    if p <= 0:
                                        last_nonull = i-1
                                        break

                                if diferencia > 0:
                                    for i in range(25-diferencia+1, 26):
                                        df_sorted.loc[i, 'points'] = df_sorted['points'][i]+1

                                elif diferencia < 0:
                                    for i in range(last_nonull+diferencia+1, last_nonull+1):
                                        print(i)
                                        df_sorted.loc[i, 'points'] = df_sorted['points'][i]-1

                                total_points = df_sorted['points'].sum()

                                df_sorted = df_sorted.sort_values('points', ascending=False).reset_index(drop=True)

                            elif len(df_sorted) > 10:

                                total_points = df_sorted['points'].sum()

                                cociente = (116*len(df_sorted))/total_points

                                for i,puntos in enumerate(df_sorted['points'][:len(df_sorted)]):
                                    df_sorted.loc[i, 'points'] = round(puntos*cociente)

                                total_points = df_sorted['points'].sum()

                                diferencia = 116*len(df_sorted)-total_points

                                # Me quedo con el último índice no nulo
                                for i,p in enumerate(df_sorted['points']):
                                    if p <= 0:
                                        last_nonull = i-1
                                        break

                                if diferencia > 0:
                                    for i in range((len(df_sorted)-1)-diferencia+1, len(df_sorted)):
                                        df_sorted.loc[i, 'points'] = df_sorted['points'][i]+1

                                elif diferencia < 0:
                                    for i in range(last_nonull+diferencia+1, last_nonull+1):
                                        print(i)
                                        df_sorted.loc[i, 'points'] = df_sorted['points'][i]-1

                                total_points = df_sorted['points'].sum()

                                df_sorted = df_sorted.sort_values('points', ascending=False).reset_index(drop=True)

                            df_sorted.rename(columns = {'manager':'jugador'}, inplace=True)
                            df_sorted = df_sorted[['song','singer','country','jugador','points']]
                            st.write('')
                            st.markdown('#### 🖐🏻 Europe, stop scrapping now! Tenemos resultados... 🥁🥁🥁🥁')
                            st.write('')
                            time.sleep(4)
                            song = df_sorted['song'][0].replace(' ','+')
                            singer = df_sorted['singer'][0].replace(' ','+')
                            winner_url = ("https://www.youtube.com/results?search_query=" + song +"+"+ singer + "+official")
                            winner_link_video = 'https://www.youtube.com/watch?v=' + (req.get(f"{winner_url}").text).split('/watch?v=')[1].split(',')[0].replace('"', "")
                            st.balloons()
                            st.markdown(f"### 🥳 Enhorabuena a {df_sorted['jugador'][0]}, ganadora con {df_sorted['song'][0]} de {df_sorted['singer'][0]} representando a {df_sorted['country'][0]}")
                            st.write('')
                            df_sorted_check = df_sorted.copy()
                            df_sorted_check.reset_index(drop=True, inplace=True)
                            df_sorted_check.index += 1
                            st.table(df_sorted_check.style.apply(highlight_rows, axis=1))
                            st.video(winner_link_video)

                            st.markdown('#### 🎁 De regalo, aquí te dejamos una lista de reproducción con las canciones que has elegido para jugar a The Eurovision Game 😊')
                            add_to_playlist(resultado)
                        except:
                            st.markdown('##### 😥 Ha habido algún error con las canciones que has introducido')
                            
        except:
            pass

import streamlit as st
import random
import warnings
import time
import statistics as stats
from operator import itemgetter

warnings.filterwarnings("ignore")
# from sklearn.metrics import mean_squared_error as mse
# from sklearn.metrics import r2_score as r2
import pandas as pd
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
        url = ("https://www.youtube.com/results?search_query=" + cancion["song"].replace(' ','+') +"+"+ cancion["singer"].replace(' ','+') +"+"+ "Official")
        link_video = 'https://www.youtube.com/watch?v=' + (req.get(f"{url}").text).split('/watch?v=')[1].split(',')[0].replace('"', "")
        html = req.get(link_video, headers = {"Accept-Language": "es-ES,es;q=0.9"}).text
        video_likes = int(html.split(" Me gusta")[0].split(":")[-1].replace('"', "").replace(".", ""))
        video_views = int((bs(html)).select_one('meta[itemprop="interactionCount"][content]')["content"])
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

        song_id = json_shazam['tracks']['hits'][0]['track']['key']
        print(song_id)
        link_shazam_search = 'https://www.shazam.com/services/count/v2/web/track/'+song_id

        json_shazam = json.loads(req.get(link_shazam_search).text)
        shazams_count = json_shazam['total']

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

    youtube_codes_dics = {'Sweden 🇸🇪 ': 'b3vJfR81xO0',
         'Finland 🇫🇮 ': 'rJHe-iZ5HSI',
         'Ukraine 🇺🇦 ': 'q6QFVqWX2gM',
         'Norway 🇳🇴 ': 'zt7U0-N1mlk',
         'Spain 🇪🇸 ': 'yxuO0qZITko',
         'Israel 🇮🇱 ': 'r4wbdKmM3bQ',
         'Austria 🇦🇹 ': 'ZMmLeV47Au4',
         'Czechia 🇨🇿 ': '-y78qgDlzAM',
         'France 🇫🇷 ': 'GWfbEFH9NvQ',
         'United Kingdom 🇬🇧 ': 'tJ21grjN6wU',
         'Italy 🇮🇹 ': 'N4HBDAbdXUg',
         'Armenia 🇦🇲 ': 'Co8ZJIejXBA',
         'Switzerland 🇨🇭 ': '_8-Sbc_GZMc&',
         'Georgia 🇬🇪 ': 'E8kO-QPippo',
         'Netherlands 🇳🇱 ': 'UOf-oKDlO6A',
         'Serbia 🇷🇸 ': 'oeIVwYUge8o',
         'Australia 🇦🇺 ': 'aqtu2GspT80',
         'Croatia 🇭🇷 ': 'O_tmsim6lPY',
         'Moldova 🇲🇩 ': 'se9LDgFW6ak',
         'Germany 🇩🇪 ': 'lnAliSmSI1A',
         'Slovenia 🇸🇮 ': 'vfTiuZaESKs',
         'Estonia 🇪🇪 ': 'lbEj29AjB-c',
         'Ireland 🇮🇪 ': 'ak5Fevs424Y',
         'Cyprus 🇨🇾 ': 'zrFUKqTy4zI',
         'Poland 🇵🇱 ': 'ANM4CwbE0Is',
         'Iceland 🇮🇸 ': 'BhlJXcCv7gw',
         'Portugal 🇵🇹 ': 'wa3suiOzAAk',
         'Denmark 🇩🇰 ': 'kY5QNC2LkG8',
         'Greece 🇬🇷 ': 'qL0EkId_sTY',
         'Azerbaijan 🇦🇿 ': '5dvsr-L3HgY',
         'Belgium 🇧🇪 ': 'uYWhh-E_VPo',
         'Lithuania 🇱🇹 ': '68lbEUDuWUQ',
         'Malta 🇲🇹 ': 'h5wfKv4p8uA',
         'San Marino 🇸🇲 ': 'Hjfq-T-8WHw',
         'Latvia 🇱🇻 ': 'PQkKJNLuO_Y',
         'Romania 🇷🇴 ': 'NRxv-AUCinQ',
         'Albania 🇦🇱 ': 'aZxe3Ce6yEI'}

    song = []
    pais = []
    views = []
    likes = []
    shazams = []


    st.write('Buscando en YouTube')

    try:
        
        link_video = 'https://www.youtube.com/watch?v=' + youtube_codes_dics[cancion['country']] + '&list=PLVf2bg851geTD_adqUqpSvGDVTqQwLZW6'
        html = req.get(link_video, headers = {"Accept-Language": "es-ES,es;q=0.9"}).text
        video_likes = int(html.split(" Me gusta")[0].split(":")[-1].replace('"', "").replace(".", ""))
        video_views = int((bs(html)).select_one('meta[itemprop="interactionCount"][content]')["content"])
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

        song_id = json_shazam['tracks']['hits'][0]['track']['key']
        print(song_id)
        link_shazam_search = 'https://www.shazam.com/services/count/v2/web/track/'+song_id

        json_shazam = json.loads(req.get(link_shazam_search).text)
        shazams_count = json_shazam['total']

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
    hora_actual_str = fecha_actual.strftime("%H:%M:%S")

    st.write('')
    st.markdown(f'##### 🔎 Scrappeando visitas y likes (en YouTube) y shazams de las canciones seleccionadas a día {fecha_actual_str} a las {hora_actual_str}')
    time.sleep(1)
    st.write('')
    st.markdown('##### 🤯 Esto puede tardar unos minutos. Interval act time!')
    
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
    hora_actual_str = fecha_actual.strftime("%H:%M:%S")
    
    st.write('')
    st.markdown(f'##### 🔎 Scrappeando visitas y likes (en YouTube) y shazams de las canciones seleccionadas a día {fecha_actual_str} a las {hora_actual_str}')
    time.sleep(1)
    st.write('')
    st.markdown('##### 🤯 Esto puede tardar unos minutos. Interval act time!')
    
    time.sleep(1)
    st.write('')
    st.video('https://www.youtube.com/watch?v=Cv6tgnx6jTQ') 

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
            shazams_bien.append(stats.mean(int_shazams))
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
            shazams_bien.append(stats.mean(int_shazams))
        else:
            shazams_bien.append(int(shz))
    tabla0["shazams"] = shazams_bien

    # SCRAPPEO LA CUOTA DE APUESTAS ACTUALIZADA
    
    pais_odds = {'Albania 🇦🇱 ': 0, 'Andorra 🇦🇩 ': 1, 'Armenia 🇦🇲 ': 2, 'Australia 🇦🇺 ': 3, 'Austria 🇦🇹 ': 4, 'Azerbaijan 🇦🇿 ': 5, 'Belarus 🇧🇾 ': 6, 'Belgium 🇧🇪 ': 7, 'Bosnia and Herzegovina 🇧🇦 ': 8, 'Bulgaria 🇧🇬 ': 9, 'Croatia 🇭🇷 ': 10, 'Cyprus 🇨🇾 ': 11, 'Czechia 🇨🇿 ': 12, 'Denmark 🇩🇰 ': 13, 'Estonia 🇪🇪 ': 14, 'Finland 🇫🇮 ': 15, 'France 🇫🇷 ': 16, 'Georgia 🇬🇪 ': 17, 'Germany 🇩🇪 ': 18, 'Greece 🇬🇷 ': 19, 'Hungary 🇭🇺 ': 20, 'Iceland 🇮🇸 ': 21, 'Ireland 🇮🇪 ': 22, 'Israel 🇮🇱 ': 23, 'Italy 🇮🇹 ': 24, 'Latvia 🇱🇻 ': 25, 'Lithuania 🇱🇹 ': 26, 'Malta 🇲🇹 ': 27, 'Moldova 🇲🇩 ': 28, 'Monaco': 29, 'Montenegro 🇲🇪 ': 30, 'North Macedonia 🇲🇰 ': 31, 'Norway 🇳🇴 ': 32, 'Poland 🇵🇱 ': 33, 'Portugal 🇵🇹 ': 34, 'Romania 🇷🇴 ': 35, 'Russia 🇷🇺 ': 36, 'San Marino 🇸🇲 ': 37, 'Serbia 🇷🇸 ': 38, 'Slovakia 🇸🇰 ': 40, 'Slovenia 🇸🇮 ': 41, 'Spain 🇪🇸 ': 42, 'Sweden 🇸🇪 ': 43, 'Switzerland 🇨🇭 ': 44, 'Netherlands 🇳🇱 ': 45, 'Turkey 🇹🇷 ': 46, 'Ukraine 🇺🇦 ': 47, 'United Kingdom 🇬🇧 ': 48}
    

    fecha_actual = datetime.datetime.now()
    fecha_actual_str = fecha_actual.strftime("%Y-%m-%d")
    hora_actual_str = fecha_actual.strftime("%H:%M:%S")

    # st.markdown(f'##### Scrappeando visitas y likes (en YouTube) y shazams de las canciones seleccionadas a día {fecha_actual_str} a las {hora_actual_str}')

    scrap_odds =    {'Sweden 🇸🇪 ': 1.858235294117647,
                     'Finland 🇫🇮 ': 3.044705882352941,
                     'France 🇫🇷 ': 9.088235294117647,
                     'Ukraine 🇺🇦 ': 13.0,
                     'Spain 🇪🇸 ': 19.176470588235293,
                     'Norway 🇳🇴 ': 21.58823529411765,
                     'Israel 🇮🇱 ': 33.94117647058823,
                     'Italy 🇮🇹 ': 45.76470588235294,
                     'United Kingdom 🇬🇧 ': 61.0,
                     'Austria 🇦🇹 ': 75.58823529411765,
                     'Armenia 🇦🇲 ': 105.05882352941177,
                     'Czechia 🇨🇿 ': 123.3529411764706,
                     'Australia 🇦🇺 ': 144.64705882352942,
                     'Switzerland 🇨🇭 ': 177.05882352941177,
                     'Germany 🇩🇪 ': 171.41176470588235,
                     'Croatia 🇭🇷 ': 200.52941176470588,
                     'Serbia 🇷🇸 ': 205.52941176470588,
                     'Slovenia 🇸🇮 ': 199.64705882352942,
                     'Moldova 🇲🇩 ': 211.7058823529412,
                     'Ireland 🇮🇪 ': 209.7058823529412,
                     'Netherlands 🇳🇱 ': 232.88235294117646,
                     'Cyprus 🇨🇾 ': 230.8235294117647,
                     'Georgia 🇬🇪 ': 268.7647058823529,
                     'Poland 🇵🇱 ': 270.2352941176471,
                     'Portugal 🇵🇹 ': 296.70588235294116,
                     'Estonia 🇪🇪 ': 299.6470588235294,
                     'Lithuania 🇱🇹 ': 311.4117647058824,
                     'Belgium 🇧🇪 ': 323.1764705882353,
                     'Iceland 🇮🇸 ': 355.52941176470586,
                     'Denmark 🇩🇰 ': 361.4117647058824,
                     'Greece 🇬🇷 ': 387.88235294117646,
                     'Malta 🇲🇹 ': 411.4117647058824,
                     'Azerbaijan 🇦🇿 ': 414.3529411764706,
                     'Albania 🇦🇱 ': 446.70588235294116,
                     'San Marino 🇸🇲 ': 446.70588235294116,
                     'Latvia 🇱🇻 ': 464.3529411764706,
                     'Romania 🇷🇴 ': 476.11764705882354}

    dictio_odds = {pais_odds[key]: value for key, value in scrap_odds.items() if key in pais_odds}

    tabla0["bet_mean"] = [dictio_odds[c] for c in tabla0["pais"]]

    # REORDENO TABLA
    tabla0 = tabla0[["pais", "bet_mean", "views", "likes", "shazams"]]
    tabla0.rename(columns={"pais": "country","views": "views_propos","likes": "likes_propos","shazams": "shazams_propos",},inplace=True,)

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

app_mode = st.sidebar.selectbox('Ir a:',['🎶 Juego Eurovisión', '🤖 Predicción Eurovisión 2023', '📊 Estadísticas 2002-2022'])

# ---------------------------------------------------------------------------------------------------------------------------

if app_mode == '🎶 Juego Eurovisión':
    
    image_inicio = Image.open("./img/panel.png")
    with io.BytesIO() as output:
        image_inicio.save(output, format="PNG")
        b64_1 = base64.b64encode(output.getvalue()).decode()

    st.markdown('<h1 style="text-align:center"><span style="font-size: 40px;">🎙️</span> <u>THE EUROVISION GAME</u></h1>', unsafe_allow_html=True)
    
    st.write('')
    with st.expander('Cómo usar la página adecuadamente', expanded=False):
        st.write('⬅️ Utiliza el **panel de la izquierda** para navegar por las diferentes secciones de la página')
        st.image(f"data:image/png;base64,{b64_1}", use_column_width=True) 
        st.write('')
        st.write('🔁 Si accedes desde un móvil **rota la pantalla** para una mejor visibilidad')
        st.write('')
        st.write('🗒 Introduce las canciones que desees para jugar a The Eurovision Game. Las canciones **no tienen por qué haber participado** en el festival. El objetivo del juego es aplicar un modelo de machine learning entrenado con los últimos 20 años de concurso y simular cómo quedaría cualquier selección de canciones en caso de participar hoy en Eurovisión')
    

    st.markdown('<h2 style="text-align:center"><span style="font-size: 15px;"></span> ¡Bienvenidos al juego de Eurovision! ¿Con quién tenemos el placer de jugar?</h2>', unsafe_allow_html=True)
    
    participante = st.text_input("Me llamo...")
    list_name = participante + " The Eurovision Game"

    # CARGAMOS DATA TO TRAIN
    data = pd.read_excel("./data/Data_to_train.xlsx")
    data.drop("Unnamed: 0", axis=1, inplace=True)

    # PARTIMOS DATA
    X = data.drop("propo_puntos", axis=1)
    y = data.propo_puntos
    X_train, X_test, y_train, y_test = tts(
        X, y, train_size=0.99, test_size=0.01, random_state=22
    )
    # X_train.shape, X_test.shape, y_train.shape, y_test.shape

    # ENTRENAMOS
    ctr = CTR(iterations=5, verbose=False)
    ctr.fit(X_train, y_train)
    y_pred = ctr.predict(X_test)

    st.write('')
    #st.write('### Elige el nº de participantes')
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

    if participante:
    
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

# ---------------------------------------------------------------------------------------------------------------------------

elif app_mode == '🤖 Predicción Eurovisión 2023':

    st.markdown('<h1 style="text-align:center"><span style="font-size: 40px;">📈</span> <u>PREDICCIONES 30 DÍAS ANTES</u></h1>', unsafe_allow_html=True)
    st.write('')
    st.write('')
    st.success('En este apartado podrás realizar una predicción en vivo de las canciones participantes en el Festival de Eurovisión del sábado 13 de mayo de 2023. Visualizarás la predicción en fecha y hora actual y un gráfico con la evolución de dicha predicción a lo largo de los 30 días previos al concurso.')
    
    # CARGAMOS DATA TO TRAIN
    data = pd.read_excel("./data/Data_to_train.xlsx")
    data.drop("Unnamed: 0", axis=1, inplace=True)

    # PARTIMOS DATA
    X = data.drop("propo_puntos", axis=1)
    y = data.propo_puntos
    X_train, X_test, y_train, y_test = tts(
        X, y, train_size=0.99, test_size=0.01, random_state=22
    )
    # X_train.shape, X_test.shape, y_train.shape, y_test.shape

    # ENTRENAMOS
    ctr = CTR(iterations=5, verbose=False)
    ctr.fit(X_train, y_train)
    y_pred = ctr.predict(X_test)

    if __name__ == '__main__':
        st.write('')

        fecha_actual = datetime.datetime.now()
        fecha_formateada = fecha_actual.strftime("%d/%m/%Y")

        if st.button(f'Predecir resultado a {fecha_formateada}'):
            user_songs = [{'song': 'Duje', 'singer': 'Albina & Familja Kelmendi', 'country': 'Albania 🇦🇱 ', 'manager': 'J1'}, {'song': 'Blood & Glitter', 'singer': 'Lord of the Lost', 'country': 'Germany 🇩🇪 ', 'manager': 'J2'}, {'song': 'Future Lover', 'singer': 'Brunette', 'country': 'Armenia 🇦🇲 ', 'manager': 'J3'}, {'song': 'Promise', 'singer': 'Voyager', 'country': 'Australia 🇦🇺 ', 'manager': 'J4'}, {'song': 'Who the hell is Edgar?', 'singer': 'Teya & Selena', 'country': 'Austria 🇦🇹 ', 'manager': 'J5'}, {'song': 'Tell me more', 'singer': 'TuralTuranX', 'country': 'Azerbaijan 🇦🇿 ', 'manager': 'J6'}, {'song': 'Because of you', 'singer': 'Gustaph', 'country': 'Belgium 🇧🇪 ', 'manager': 'J7'}, {'song': "My Sister's Crown", 'singer': 'Vesna', 'country': 'Czechia 🇨🇿 ', 'manager': 'J8'}, {'song': 'Break a Broken Heart', 'singer': 'Andrew Lambrou', 'country': 'Cyprus 🇨🇾 ', 'manager': 'J9'}, {'song': 'Mama ŠČ!', 'singer': 'Let3', 'country': 'Croatia 🇭🇷 ', 'manager': 'J10'}, {'song': 'Breaking My Heart', 'singer': 'Reiley', 'country': 'Denmark 🇩🇰 ', 'manager': 'J11'}, {'song': 'Carpe Diem', 'singer': 'Joker Out', 'country': 'Slovenia 🇸🇮 ', 'manager': 'J12'}, {'song': 'EaEa', 'singer': 'BlancaPaloma', 'country': 'Spain 🇪🇸 ', 'manager': 'J13'}, {'song': 'Bridges', 'singer': 'Alika', 'country': 'Estonia 🇪🇪 ', 'manager': 'J14'}, {'song': 'ChaChaCha', 'singer': 'Käärijä', 'country': 'Finland 🇫🇮 ', 'manager': 'J15'}, {'song': 'Évidemment', 'singer': 'Zarra', 'country': 'France 🇫🇷 ', 'manager': 'J16'}, {'song': 'Echo', 'singer': 'Iru', 'country': 'Georgia 🇬🇪 ', 'manager': 'J17'}, {'song': 'What They Say', 'singer': 'Victor Vernicos', 'country': 'Greece 🇬🇷 ', 'manager': 'J18'}, {'song': 'We are one', 'singer': 'Wild Youth', 'country': 'Ireland 🇮🇪 ', 'manager': 'J19'}, {'song': 'Power', 'singer': 'Diljá', 'country': 'Iceland 🇮🇸 ', 'manager': 'J20'}, {'song': 'Unicorn', 'singer': 'Noa Kirel', 'country': 'Israel 🇮🇱 ', 'manager': 'J21'}, {'song': 'Due Vite', 'singer': 'MarcoMengoni', 'country': 'Italy 🇮🇹 ', 'manager': 'J22'}, {'song': 'Aijā', 'singer': 'Sudden Lights', 'country': 'Latvia 🇱🇻 ', 'manager': 'J23'}, {'song': 'Stay', 'singer': 'Monika Linkytė', 'country': 'Lithuania 🇱🇹 ', 'manager': 'J24'}, {'song': 'Dance (Our Own Party)', 'singer': 'The Busker', 'country': 'Malta 🇲🇹 ', 'manager': 'J25'}, {'song': 'Soarele şi Luna', 'singer': 'Pasha Parfeni', 'country': 'Moldova 🇲🇩 ', 'manager': 'J26'}, {'song': 'Queen of kings', 'singer': 'Alessandra', 'country': 'Norway 🇳🇴 ', 'manager': 'J27'}, {'song': 'Burning Daylight', 'singer': 'Mia Nicolai & Dion Cooper', 'country': 'Netherlands 🇳🇱 ', 'manager': 'J28'}, {'song': 'Solo', 'singer': 'Blanka', 'country': 'Poland 🇵🇱 ', 'manager': 'J29'}, {'song': 'AiCoração', 'singer': 'Mimicat', 'country': 'Portugal 🇵🇹 ', 'manager': 'J30'}, {'song': 'I Wrote a Song', 'singer': 'MaeMuller', 'country': 'United Kingdom 🇬🇧 ', 'manager': 'J31'}, {'song': 'D.G.T. (Off and On)', 'singer': 'Theodor Andrei', 'country': 'Romania 🇷🇴 ', 'manager': 'J32'}, {'song': 'Like an Animal', 'singer': 'Piqued Jacks', 'country': 'San Marino 🇸🇲 ', 'manager': 'J33'}, {'song': 'Samo mi se spava', 'singer': 'Luke Black', 'country': 'Serbia 🇷🇸 ', 'manager': 'J34'}, {'song': 'Tattoo', 'singer': 'Loreen', 'country': 'Sweden 🇸🇪 ', 'manager': 'J35'}, {'song': 'Watergun', 'singer': 'Remo Forrer', 'country': 'Switzerland 🇨🇭 ', 'manager': 'J36'}, {'song': 'Heart of steel', 'singer': 'Tvorchi', 'country': 'Ukraine 🇺🇦 ', 'manager': 'J37'}]

            resultado = predicciones_now(user_songs)

            df = pd.DataFrame(resultado)
            df_sorted = df.sort_values('points', ascending=False).reset_index(drop=True)

            first_points = df_sorted['points'][0]
            last_points = df_sorted['points'][26]

            pendiente = first_points/(first_points-last_points)
            intercept = (first_points*last_points)/(first_points-last_points)

            total_points = df_sorted['points'].sum()

            for i,p in enumerate(df_sorted['points']):
                df_sorted.loc[i, 'points'] = round(pendiente*p-intercept)

            df_sorted.loc[26:, 'points'] = 0

            total_points = df_sorted['points'].sum()

            cociente = 4292/total_points

            for i,puntos in enumerate(df_sorted['points'][:26]):
                df_sorted.loc[i, 'points'] = round(puntos*cociente)

            total_points = df_sorted['points'].sum()

            diferencia = 4292-total_points

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
            st.table(df_sorted_check.style.apply(highlight_rows, axis=1))

            #df_sorted['country1'] = [e.replace(' ','·') for e in df_sorted['country']]
            #df_sorted

            # Obtener la fecha de hoy
            fecha_hoy = pd.Timestamp('today').date()

            # Crear un diccionario para especificar las columnas y sus valores
            columnas = df_sorted['country'].tolist()  # Obtener los valores de la columna 'country'
            valores = df_sorted.set_index('country')['points'].to_dict()  # Crear un diccionario con los valores de 'points' indexados por 'country'
            data = {col: [valores.get(col, None)] for col in columnas}  # Crear un diccionario con los valores correspondientes a las columnas

# --------------------------------------------------------------------------------------
            # st.write(row_data_ESC23(user_songs)) # Para ver las métricas
# --------------------------------------------------------------------------------------

            # Crear un nuevo dataframe con la fecha de hoy como índice y las columnas y valores especificados
            df_nuevo = pd.DataFrame(data, index=[fecha_hoy])
            df_nuevo = df_nuevo.sort_index(axis=1)
            #df_nuevo

            df_prueba = pd.read_excel('./data/prueba_predicc_dia_dia.xlsx')
            df_prueba.rename(columns= {'Unnamed: 0':'date'}, inplace=True)
            df_prueba = df_prueba.set_index('date')
            # Cambiar el índice de fecha+hora a solo fecha
            df_prueba.index = df_prueba.index.date.astype(str)
            # Cambiar los valores numéricos de float a int
            df_prueba = df_prueba.astype(int)
            #df_prueba

            df_prueba = pd.concat([df_nuevo, df_prueba])
            df_prueba.index = df_prueba.index.astype(str)
            df_prueba = df_prueba.sort_index(ascending=True)
            #df_prueba    

            # Crear el gráfico de líneas con Plotly
            fig = px.line(df_prueba, x=df_prueba.index, y=df_prueba.columns)

            # Configurar formato de fecha en el eje X
            fig.update_xaxes(title='Fecha', tickformat='%d/%m/%Y')
            #fig.update_yaxes(title='Predicción de puntos')


            # Configurar marcadores de puntos en las líneas
            fig.update_traces(mode='markers+lines', marker=dict(size=6), showlegend=True)
            fecha_actual = datetime.datetime.now()
            fecha_actual_str = fecha_actual.strftime("%d/%m/%Y")
            fig.update_layout(legend_title_text='País',title={'text': f"Evolución predicción desde 12/04/2023 hasta {fecha_actual_str}",'font_size': 24},  xaxis_tickfont=dict(size=20), yaxis_tickfont=dict(size=20), yaxis_title=f'<b style="font-size:1em">Predicción de puntos</b>', xaxis_title=f'<b style="font-size:1em">Fecha de la predicción</b>', xaxis=dict(tickangle=-25), height=800) 

            st.success('👇🏻 Puedes filtrar qué países ver en el gráfico pulsando sobre ellos en la leyenda: Si pulsas 1️⃣ vez, eliminas ese país del gráfico. Si pulsas 2️⃣ veces, verás solo ese país, y entonces, tocando 1️⃣ vez en otros, añadirás países a la visualización. Si quieres reestablecer la vista inicial, pulsa en "Autoscale", situado en tercera posición por la derecha la parte superior del gráfico')
            
            # Mostrar el gráfico
            st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------------------------------------------------------

elif app_mode == '📊 Estadísticas 2002-2022':

    st.markdown('<h1 style="text-align:center"><span style="font-size: 40px;">📊</span> <u>ESTADÍSTICAS 2002-2022</u></h1>', unsafe_allow_html=True)

    df_master = pd.read_excel('./data/MASTERTABLA.xlsx').drop('Unnamed: 0', axis = 1)
    # st.write(df_master)
    
    st.write('')
    st.warning('⚠️ Si accedes desde un móvil rota la pantalla para poder visualizar los gráficos con una mejor adaptación.')
    st.write('')
    
    # Filtro por año
    year_range = st.slider('Selecciona un rango de años', 
                           #min_value=df_master['year'].min(), 
                           min_value = 2002,
                           #max_value=df_master['year'].max(), 
                           max_value = 2022,
                           #value=(df_master['year'].min(), df_master['year'].max())
                           value = (2002, 2022)
                          )
    filtered_df = df_master[(df_master['year'] >= year_range[0]) & (df_master['year'] <= year_range[1])]

    # Filtro por país
    selected_country = st.multiselect('Selecciona los países', options=df_master['country'].unique())
    if selected_country:
        filtered_df = filtered_df[filtered_df['country'].isin(selected_country)]

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

    # Muestra el DataFrame filtrado
    st.write('\n')
    st.write('\n')
    with st.expander('👀 Ver Datos', expanded=False): 
        st.write(filtered_df)
    st.write('')
    
    graf_names = ['Comportamiento Digital', 'Apuestas', 'Política', 'Aspectos Técnicos']
    graf = st.radio('Tipo de gráfico a visualizar', graf_names)
    st.write('')
    

    if graf == 'Comportamiento Digital':
        
    # ------ MÉTRICAS DIGITALES -----------------------------------------------------------------
      # ---- GRAFICOS PUNTOS VS YOUTUBE ---------------------------------------------------------

        with st.expander('PUNTOS vs YouTube 🔢📹', expanded=True): 

            st.write('')
            Acum = st.checkbox("Ver en datos acumulados")

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
                fig.update_layout(title={'text': 'Acum. Puntos + Views y Likes en YT 2002-2022', 'font_size': 24})

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

                fig.update_layout(title={'text': 'Prom. Puntos + Views y Likes en YT 2002-2022', 'font_size': 24})

                fig.update_yaxes(title='', row=1, col=1)
                fig.update_traces(marker_color='#E97451')
                fig.update_layout(showlegend=False, height=1100)
                fig.update(layout_coloraxis_showscale = False)
                fig.update_traces(hovertemplate='pais = %{label}<br>promedio = %{value:.0f}')

                st.plotly_chart(fig, use_container_width=True)


      # ---- GRAFICOS PUNTOS VS SHAZAM ---------------------------------------------------------

        with st.expander('PUNTOS vs SHAZAM 🔢🔊', expanded=True): 

            st.write('')
            Acum2 = st.checkbox("Ver en datos acumulados ")

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
                fig.update_layout(title={'text': 'Acum. Puntos vs Shazams 2002-2022', 'font_size': 24})

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
                fig.update_layout(title={'text': 'Prom. Puntos vs Shazams 2002-2022', 'font_size': 24})

                fig.update_yaxes(title='', row=1, col=1)
                fig.update_traces(marker_color='#89CFF0')
                fig.update_layout(showlegend=False, height=1100)
                fig.update(layout_coloraxis_showscale = False)
                fig.update_traces(hovertemplate='pais = %{label}<br>promedio = %{value:.0f}')

                st.plotly_chart(fig, use_container_width=True)
            

    elif graf == 'Apuestas':
        
     # ----- APUESTAS --------------------------------------------------------------------------
      # ---- GRAFICOS PUNTOS VS APUESTAS ---------------------------------------------------------

        with st.expander('PUNTOS vs APUESTAS 🔢💸', expanded=True): 

            st.write('')
            Acum8 = st.checkbox("Ver en datos acumulados               ")

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
                fig.update_layout(title={'text': 'Acum. Puntos vs Apuestas 2002-2022', 'font_size': 24})

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
                fig.update_layout(title={'text': 'Prom. Puntos vs Apuestas 2002-2022', 'font_size': 24})

                fig.update_yaxes(title='', row=1, col=1)
                fig.update_traces(marker_color='#22BAB5')
                fig.update_layout(showlegend=False, height=1100)
                fig.update(layout_coloraxis_showscale = False)
                fig.update_traces(hovertemplate='pais = %{label}<br>promedio = %{value:.0f}')

                st.plotly_chart(fig, use_container_width=True)

        
    elif graf == 'Política':

      # ---- GRAFICOS PUNTOS VS VECINOS ---------------------------------------------------------

        with st.expander('PUNTOS vs Nº de VECINOS 🔢🌍', expanded=True): 

            st.write('')
            Acum3 = st.checkbox("Ver en datos acumulados  ")

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

                fig.update_layout(title={'text': 'Acum. Puntos vs Nº Vecinos 2002-2022', 'font_size': 24})

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

                fig.update_layout(title={'text': 'Prom. Puntos vs Nº Vecinos 2002-2022', 'font_size': 24})

                fig.update_yaxes(title='', row=1, col=1)
                fig.update_traces(marker_color='#DDA0DD')
                fig.update_layout(showlegend=False, height=1100)
                fig.update(layout_coloraxis_showscale = False)
                fig.update_traces(hovertemplate='pais = %{label}<br>valor = %{value:.0f}')

                st.plotly_chart(fig, use_container_width=True) 


     # -------ECONOMÍA ----------------------------------------------------------------------
      # ---- GRAFICOS PUNTOS VS PIB ---------------------------------------------------------

        with st.expander('PUNTOS vs GDP (PIB) 🔢🪙', expanded=True): 

            st.write('')
            Acum4 = st.checkbox("Ver en datos acumulados   ")

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
                fig.update_xaxes(title='Acum. GDP', row=1, col=2)

                fig.update_layout(title={'text': 'Acum. Puntos vs GDP 2002-2022', 'font_size': 24})

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
                fig.update_xaxes(title='Prom. GDP', row=1, col=2)

                fig.update_layout(title={'text': 'Prom. Puntos vs GDP 2002-2022', 'font_size': 24})

                fig.update_yaxes(title='', row=1, col=1)
                fig.update_traces(marker_color='#08B434')
                fig.update_layout(showlegend=False, height=1100)
                fig.update(layout_coloraxis_showscale = False)
                fig.update_traces(hovertemplate='pais = %{label}<br>promedio = %{value:.0f}')

                st.plotly_chart(fig, use_container_width=True) 


      # ---- GRAFICOS PUNTOS VS RANKING PIB ---------------------------------------------------------

        with st.expander('PUNTOS vs Ranking Relativo GDP (PIB) 🔢🪙', expanded=True): 

            st.write('')
            Acum5 = st.checkbox("Ver en datos acumulados    ")

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

                # Grafico 2: Orden Relativo GDP
                grouped_df = filtered_df.groupby('country').sum().reset_index()
                grouped_df = grouped_df.sort_values('orden_relativo_GDP', ascending=False)

                fig.add_trace(px.bar(grouped_df, x='orden_relativo_GDP', y='country',
                                      orientation='h', #text='likes',
                                      color='orden_relativo_GDP').data[0],
                              row=1, col=2)
                fig.update_xaxes(title='Acum. Ranking GDP', row=1, col=2)

                fig.update_layout(title={'text': 'Acum. Puntos vs Ranking Relativo GDP (PIB) 2002-2022', 'font_size': 24})

                fig.update_yaxes(title='', row=1, col=1)
                fig.update_traces(marker_color='#5CC176')
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
                fig.update_xaxes(title='Prom. Ranking GDP', row=1, col=2)

                fig.update_layout(title={'text': 'Prom. Puntos vs Ranking Relativo GDP (PIB) 2002-2022', 'font_size': 24})

                fig.update_yaxes(title='', row=1, col=1)
                fig.update_traces(marker_color='#5CC176')
                fig.update_layout(showlegend=False, height=1100)
                fig.update(layout_coloraxis_showscale = False)
                fig.update_traces(hovertemplate='pais = %{label}<br>promedio = %{value:.0f}')

                st.plotly_chart(fig, use_container_width=True) 


      # ---- GRAFICOS PUNTOS VS INFLUENCIA ---------------------------------------------------------

        with st.expander('PUNTOS vs INFLUENCIA 🔢💪🏻', expanded=True): 

            st.write('')
            Acum6 = st.checkbox("Ver en datos acumulados      ")
            st.write('❗ La puntuación de INFLUENCIA no tiene evolución histórica como tal, si no que es un valor estimado sobre la influencia de cada país sobre el resto en los últimos 30 años')

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

                fig.update_layout(title={'text': 'Acum. Puntos vs Influencia 2002-2022', 'font_size': 24})

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

                fig.update_layout(title={'text': 'Prom. Puntos vs Influencia 2002-2022', 'font_size': 24})

                fig.update_yaxes(title='', row=1, col=1)
                fig.update_traces(marker_color='#D8D335')
                fig.update_layout(showlegend=False, height=1100)
                fig.update(layout_coloraxis_showscale = False)
                fig.update_traces(hovertemplate='pais = %{label}<br>valor = %{value:.0f}')

                st.plotly_chart(fig, use_container_width=True) 


      # ---- GRAFICOS PUNTOS VS REPUTACIÓN ---------------------------------------------------------

        with st.expander('PUNTOS vs REPUTACIÓN 🔢👍🏻', expanded=True): 

            st.write('')
            Acum7 = st.checkbox("Ver en datos acumulados        ")
            st.write('❗ El Ranking de REPUTACIÓN Internacional no tiene evolución histórica como tal, si no que es un valor calculado sobre la reputación de cada país entorno a ciencia, tecnología, cultura, paz, seguridad, medio ambiente, política, derechos humanos, igualdad, salud y bienestar')

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

                fig.update_layout(title={'text': 'Acum. Puntos vs Ranking Reputación 2002-2022', 'font_size': 24})

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

                fig.update_layout(title={'text': 'Prom. Puntos vs Ranking Reputación 2002-2022', 'font_size': 24})

                fig.update_yaxes(title='', row=1, col=1)
                fig.update_traces(marker_color='#EDB753')
                fig.update_layout(showlegend=False, height=1100)
                fig.update(layout_coloraxis_showscale = False)
                fig.update_traces(hovertemplate='pais = %{label}<br>valor = %{value:.0f}')

                st.plotly_chart(fig, use_container_width=True) 
                
                
    elif graf == 'Aspectos Técnicos':
        
    # -------ECONOMÍA ----------------------------------------------------------------------
      # ---- GRAFICOS PUNTOS VS PIB ---------------------------------------------------------

        with st.expander('ESTILOS 🤘🏻', expanded=True):
            
            concat_df = filtered_df.copy()
            concat_df['entry'] = concat_df['song'] + ' - ' + concat_df['artist'] + ' ' + concat_df['country'] + ' ' + concat_df['year'].astype(str)
            
            df_count = concat_df.groupby(['estilos', 'entry']).size().reset_index(name='count')
            
            fig = px.treemap(df_count, path=[px.Constant('TODOS'), 'estilos', 'entry'], values='count')

            st.plotly_chart(fig, use_container_width=True) 

        



#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Modo de uso
Argumentos:
    1 - [lista de palavras] - Arquivo com a lista de palavras
    2 - [idioma]            - en, pt-br, la, ja, ko...

./audiodownload.py 1 2

Exemplo:
    ./audiodownload.py lista.txt en
'''

import sys
import os
from requests import get

def __save_audio(audio: bytes, name: str) -> str:
    if not os.path.exists("audio/"):
        try:
            os.mkdir("audio")
        except Exception as e:
            raise Exception("Não foi possível criar a pasta de destino")
    
    save = open(f"audio/{name}.mp3", "wb")
    save.write(audio)
    save.close()

    return os.path.realpath(save.name)

def __download(word: str, lang: str) -> bytes:
    '''
    :param arquivo: string - Lista de palavras para serem baixadas
    :idioma idioma: en, pt-br, la, ja, ko ... sigla do idioma a ser baixado
    :return: conteudo em bytes
    '''
    url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={word}&tl={lang}&total=1&idx=0&tk=350535.255567&client=webapp&prev=input"
    audio = get(url)
    
    if audio.status_code != 200:
        raise Exception(f"Erro ao transferir a palavra {word}: status_code {audio.status_code}")
    else:
        return audio.content

def download_from_list(lista: list, lang: str) -> list:

    files_path = {}

    for word in lista:
        audio = __download(word, lang)
        path = __save_audio(audio, word)
        files_path.update({word: path})
    
    return files_path

def download_from_arquive(arquive: str, lang: str) -> map:
    if not os.path.exists(arquive):
        raise Exception(f"Não foi possível abrir: {arquive}")

    with open(arquive, "r") as file:
        word_list = list((word.rstrip("\n") for word in file.readlines()))
        files_path = download_from_list(word_list, lang)
        return files_path

if __name__ == "__main__":
    try:
        path = download_from_arquive(sys.argv[1], sys.argv[2])
    except Exception as e:
        print(e)
        print(__doc__)

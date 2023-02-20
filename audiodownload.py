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

def download(arquivo, idioma):
    '''
    :param arquivo: string - Lista de palavras para serem baixadas
    :idioma idioma: en, pt-br, la, ja, ko ... sigla do idioma a ser baixado
    '''

    with open(arquivo) as file:
        palavras = [word.rstrip("\n") for word in file.readlines()]

        for palavra in palavras:
            url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={palavra}&tl={idioma}&total=1&idx=0&tk=350535.255567&client=webapp&prev=input"
            audio = get(url)
            
            if audio.status_code != 200:
                print(f"Erro ao baixar palavra {palavra}: code {audio.status_code}")
                raise Exception

            if not os.path.exists("audio/"):
                os.mkdir("audio")
            
            save = open(f"audio/{palavra}.mp3", "wb")
            save.write(audio.content)
            save.close()
    
if __name__ == "__main__":
    try:
        download(sys.argv[1], sys.argv[2])
        
    except Exception as e:
        print(e)
        print(__doc__)
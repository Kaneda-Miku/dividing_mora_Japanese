import pykakasi
import re
import csv

def hiragana2mora(hiraganaWord):
    moraresult = []
    
    if "ん" or "ン" in hiraganaWord:
        hiraganaWord = hiraganaWord.replace('ん', 'N')
        hiraganaWord = hiraganaWord.replace('ン', 'N')
    if "ー" or "～" in hiraganaWord:
        hiraganaWord = hiraganaWord.replace('ー', 'R')
        hiraganaWord = hiraganaWord.replace('～', 'R')
    if "っ" or "ッ" in hiraganaWord:
        hiraganaWord = hiraganaWord.replace('っ', 'Q')
        hiraganaWord = hiraganaWord.replace('ッ', 'Q')
    
    hiraganaWord = re.sub('ぁ', 'la', hiraganaWord)
    hiraganaWord = re.sub('ぃ', 'li', hiraganaWord)
    hiraganaWord = re.sub('ぅ', 'lu', hiraganaWord)
    hiraganaWord = re.sub('ぇ', 'le', hiraganaWord)
    hiraganaWord = re.sub('ぉ', 'lo', hiraganaWord)
    
    kks = pykakasi.kakasi()
    result_conv = kks.convert(hiraganaWord)
    
    for item in result_conv:
        itemconv = re.split(r"([aeiou])",item["hepburn"])
        moraresult = moraresult + itemconv

    return moraresult


def moraDividStart():
    with open('formoradividing.csv') as f:
        with open('moraresult.csv', 'w') as rf:
            reader = csv.reader(f)
            writer = csv.writer(rf)
            for row in reader:
                writer.writerow(moradivid(row))
            

def moradivid(moraWord):
    if type(moraWord) is str:
        moraWord = moraWord.split()
    
    itemconv = hiragana2mora(moraWord[0])
    itemconv = NRQdivid(itemconv)
   
    return itemconv


def NRQdivid(itemconv):
    moraresult = []
    addlist = [""]
    
    for item in itemconv:
        if re.search(r"([NRQ])", item):
            for listcontent in item:
                moraresult = moraresult + list(listcontent)
                if re.search(r"([NRQ])", listcontent):
                    moraresult.extend(addlist)
            #splitresult = re.split(r"([NRQ])", item)
            #del splitresult[0]
            #moraresult = moraresult + splitresult
        else:
            moraresult.append(item)
            
    return moraresult


#課題　数えられるようにする
#条件ごとに数えられたらカラースケールにするのが簡単
#githubにあげる
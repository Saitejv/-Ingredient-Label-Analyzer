import cv2
import pytesseract
import easyocr
import torch
import numpy as np
import string 
from textblob import TextBlob
import csv
import pandas as pd
import re



def readImage():
    imagepath = "iPhoto.jpg" #for real use
    #imagepath = "carbohydrate-nutrition-facts-label.png" #for testing use

    img = cv2.imread(imagepath)

    #used to transform the image and improve accuracy
    img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    cv2.threshold(cv2.GaussianBlur(img, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


    reader = easyocr.Reader(["en"], gpu = False)

    readerOut = reader.readtext(img)
    ocrRawFileWrite = open("outputOCRRaw.txt", "w")

    reachedIngredients = False


    for i in readerOut:
        bbox, text , score = i
        #lowercase the text and than run autocorrect 
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        

        

        #only adds to file if the ingredients label has started
        if reachedIngredients:
            #print(text)
            ocrRawFileWrite.write(text + " ")



        ###########################################################################
        ########################THIS MIGHT CAUSE AN ISSUE##########################
        #############################REMOVE IF IT DOES#############################
        ###########################################################################
        #ordered like this to avoid ingredients from being added to the file id the ingrediets
        #label has not been reached
        if (("ingredient" in text) or ("ingredients" in text)):
            
            reachedIngredients = True
    


    ocrRawFileWrite.close()
    ocrRawFileRead = open("outputOCRRaw.txt", "r")
    ocrCleanFileWrite = open("outputOCRClean.txt", "w")


    text = ocrRawFileRead.read()
    text = TextBlob(text)
    
    text = str(text.correct())

    text = text.replace(" and ", " ")
    text = text.replace(" or ", " ")
    text = text.replace(" with ", " ")
    text = text.replace(" so ", " soy ")

    ocrCleanFileWrite.write(text)
    print(text)


def contains_word(s, w):
    return (' ' + w + ' ') in (' ' + s + ' ')


def compareList():
    csvFile = pd.read_csv(r"D:\Learn\ingredients\p65chemicalslist.csv")

    ingredientsList = open("outputOCRClean.txt", "r").read()

    ingredientsList = ingredientsList.split(" ")

    
    hazardIngredients = csvFile[csvFile['STATE OF CALIFORNIA'].notna()]

    

    hazardIngredientsInItem = []

    

    for ingredient in ingredientsList:
        for index,row in hazardIngredients.iterrows():
            
            csvIngredent = row['STATE OF CALIFORNIA']
            csvIngredent = re.sub(r'\(.*?\)', '', csvIngredent)
            csvIngredent = csvIngredent.strip()



            if contains_word(ingredient, csvIngredent ):
                hazardIngredientsInItem.append((row['STATE OF CALIFORNIA'],row['Unnamed: 1']))
                print(row['STATE OF CALIFORNIA'])
            

    return hazardIngredientsInItem
            
        




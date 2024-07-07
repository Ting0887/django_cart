import requests
from bs4 import BeautifulSoup
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import tkinter as tk
from tkinter.ttk import *
from PIL import Image,ImageTk
from functools import partial
import pandas as pd

def read_image_url():
    df = pd.read_csv('D:/django_cart/data.csv')
    imgs_link = df['image']
    for img_link in imgs_link:
        if img_link:
            img_name = img_link.split('/')[-1]
            download_image(img_link, 'D:/django_cart/static/images/'+img_name)

def download_image(image_url, file_name):
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # 检查请求是否成功
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"Image successfully downloaded: {file_name}")
    except Exception as e:
        print(f"Failed to download image. Error: {e}")
        
read_image_url()
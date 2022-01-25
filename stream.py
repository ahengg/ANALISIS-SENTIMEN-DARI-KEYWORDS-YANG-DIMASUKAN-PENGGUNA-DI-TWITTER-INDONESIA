#boostrap
from threading import activeCount
import streamlit.components.v1 as components
#
import streamlit as st 
import pandas as pd 
from PIL import Image 
##

#from keras.preprocessing.text import Tokenizer
#from keras.preprocessing.sequence import pad_sequences
import pandas as pd
import re
#import matplotlib.pyplot as plt
import string
from nltk.corpus import stopwords
import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from collections import Counter
#from wordcloud import WordCloud 
import nltk
from gensim.utils import simple_preprocess 
import gensim
from sklearn.model_selection import train_test_split
  
import seaborn as sns
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt  
import keras
import numpy as np
import pandas as pd

import string
import nltk 
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
##
import urllib
from bs4 import BeautifulSoup
import time
from time import sleep
from datetime import date, timedelta
import requests
import pandas as pd  
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
##

import snscrape.modules.twitter as sntwitter 
 
##
 
# Creating list to append tweet data to
# Creating a dataframe from the tweets list above 
##
totalImpressionPerAccount=[]
st.set_option('deprecation.showPyplotGlobalUse', False)
#  
st.markdown("<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css' rel='stylesheet' integrity='sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3' crossorigin='anonymous'>", unsafe_allow_html=True)
st.markdown("<center><img src='https://rekreartive.com/wp-content/uploads/2018/10/Logo-Petra-Universitas-Kristen-Petra-Original-PNG.png' style='width:200px;height:200px'></center>", unsafe_allow_html=True)
st.markdown("<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'>", unsafe_allow_html=True)
sentence = st.text_input('Massukan kata yang di analisa:') 
col1,col2=st.columns(2)
with col1:
    awal=st.date_input("Pilih Tanggal Awal Tweet")
with col2:
    akhir=st.date_input("Pilih Tanggal Akhir Tweet") 
result=st.button("Submit")
#ini bakal Detik,Kompas, Merdeka,Tribunnews 
inputUser=sentence.replace(" ", "+")
keyword=sentence
keywordUI=sentence
##
siteHeader = st.container() 
dataExploration = st.container() 
newFeatures = st.container() 
modelTraining = st.container()

#st.write(result)

#cara bikin enak 
if (result):
  tgl_awal="01/12/2021"
  tgl_akhir="13/01/2022"

  urlLiputan6= "https://www.liputan6.com/search?q=anime" #gagal
  urlDetik ="https://www.detik.com/search/searchall?query=" + inputUser +"&siteid=2&sortby=time&fromdatex="+str(awal)+"&todatex="+str(akhir) #bisa reqeust biasa
  print(urlDetik)
  inputUser=inputUser+" after:"+str(awal)+" before:"+str(akhir)
  
  urlKompas="https://search.kompas.com/search/?q="+inputUser+"&submit=Submit" #selenium
  urlMerdeka="https://www.merdeka.com/cari/?q="+inputUser #seelnium
  urlTribun="https://www.tribunnews.com/search?q="+inputUser #selenium 
  ##
  #khusus selenium
  s=Service(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=s) 

  driver.get(urlKompas) 
  sentence=driver.page_source
  soupKompas = BeautifulSoup(str(sentence), 'html.parser')

  driver.get(urlMerdeka) 
  sentence=driver.page_source
  soupMerdeka = BeautifulSoup(sentence, 'html.parser')

  driver.get(urlTribun) 
  sentence=driver.page_source
  soupTribun = BeautifulSoup(sentence, 'html.parser')

  driver.quit()
  ##
  # URL Studentsite UG 
  user_agent = 'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36'
  # header variable
  headers = { 'User-Agent' : user_agent }
  laman_ss = requests.get(urlLiputan6, headers=headers)
  laman_ssDetik = requests.get(urlDetik)
  # jika sukses, maka status query ini adalah 200, alias OK
  print(f'Status GET laman SS UG: {laman_ss.status_code}')
  ##
  soup = BeautifulSoup(laman_ss.content, 'html.parser') 
  soupDetik = BeautifulSoup(laman_ssDetik.content, 'html.parser') 
  kontainer_berita = soup.find_all('article', class_='articles--iridescent-list--item articles--iridescent-list--text-item')
  kontainer_beritaDetik = soupDetik.find_all('div', class_='list media_rows list-berita')
  kontainer_beritaKompas=soupKompas.find_all('div', class_='gsc-expansionArea')
  kontainer_beritaTribun=soupTribun.find_all('div', class_='gsc-expansionArea')
  kontainer_beritaMerdeka=soupMerdeka.find_all('div', class_='gsc-expansionArea')
  
  ##
  
  lineGraphX=[]
  lineGraphY=[]
  # siapkan list kosong untuk menampung judul dan rangkuman detik.com
  judul_list = []
  isi_list = []
  img_list=[]
  link_list=[]
  tgl_list=[]
  website_list=[]
  for berita in kontainer_beritaDetik:
      tanggal=''
      for rangkuman in berita.find_all('h2', class_='title'):
          rangkuman_rapi = ' '.join(str(rangkuman.get_text()).strip().split()) 
          judul_list.append(rangkuman_rapi)
      for rangkuman in berita.find_all('p'):
          rangkuman_rapi = ' '.join(str(rangkuman.get_text()).strip().split()) 
          isi_list.append(rangkuman_rapi)
      for rangkuman in berita.find_all('img'):
          rangkuman_rapi = ' '.join(str(rangkuman.get('src')).strip().split()) 
          img_list.append(rangkuman_rapi)
      for rangkuman in berita.find_all('a'):
          rangkuman_rapi = ' '.join(str(rangkuman.get('href')).strip().split())  
          link_list.append(rangkuman_rapi)
      for rangkuman in berita.find_all('span', class_='date'):
          rangkuman_rapi = ' '.join(str(rangkuman.get_text()).strip().split()) 
          hasilSplit = rangkuman_rapi.split(", ") 

          tgl_list.append(hasilSplit[1])
  for i in isi_list:
      website_list.append('detik') 
  ##
  # siapkan list kosong untuk menampung judul dan rangkuman tribun.com
  i=0
  for berita in kontainer_beritaTribun:
      tanggal=''
      for rangkuman in berita.find_all('div', class_='gs-title'):
          if(i==0 or i%2==0):
              rangkuman_rapi = ' '.join(str(rangkuman.get_text()).strip().split())  
              judul_list.append(rangkuman_rapi)
              website_list.append('tribun') 
          i=i+1
      i=0
      for rangkuman in berita.find_all('div', class_='gs-bidi-start-align gs-snippet'):
          rangkuman_rapi = ' '.join(str(rangkuman.get_text()).strip().split()) 
          hasilSplit = rangkuman_rapi.split(" ... ") 
          if(len(hasilSplit)<2):
              tgl_list.append('')
              isi_list.append(hasilSplit[0])
          else:
              tgl_list.append(hasilSplit[0])
              isi_list.append(hasilSplit[1])
          # append teks rangkuman ke list 
          #
      i=0    
      for rangkuman in berita.find_all('img', class_='gs-image'):
          rangkuman_rapi = ' '.join(str(rangkuman.get('src')).strip().split()) 
          #print(rangkuman_rapi)
          # append teks rangkuman ke list 
          img_list.append(rangkuman_rapi)
      for rangkuman in berita.find_all('a', class_='gs-title'):
          if(i==0 or i%2==0):
              rangkuman_rapi = ' '.join(str(rangkuman.get('href')).strip().split()) 
              #print(rangkuman_rapi)
              # append teks rangkuman ke list 
              link_list.append(rangkuman_rapi) 
          i=i+1
      i=0
  ##
  # siapkan list kosong untuk menampung judul dan rangkuman Merdeka.com
  i=0
  for berita in kontainer_beritaMerdeka: 
      for rangkuman in berita.find_all('a', class_='gs-title'):
          if(i==0 or i%2==0):
              rangkuman_rapi = ' '.join(str(rangkuman.get_text()).strip().split()) 
              #print(rangkuman_rapi)
              # append teks rangkuman ke list
              judul_list.append(rangkuman_rapi)
              website_list.append('merdeka') 
          i=i+1
      i=0
      for rangkuman in berita.find_all('div', class_='gs-bidi-start-align gs-snippet'):
          rangkuman_rapi = ' '.join(str(rangkuman.get_text()).strip().split()) 
          hasilSplit = rangkuman_rapi.split(" ... ") 
          if(len(hasilSplit)<2):
              #tgl_list.append(hasilSplit[0])
              isi_list.append(hasilSplit[0])
          else:
              tgl_list.append(hasilSplit[0])
              isi_list.append(hasilSplit[1])
          # append teks rangkuman ke list 
          #
          
      for rangkuman in berita.find_all('img', class_='gs-image'):
          rangkuman_rapi = ' '.join(str(rangkuman.get('src')).strip().split()) 
          #print(rangkuman_rapi)
          # append teks rangkuman ke list 
          img_list.append(rangkuman_rapi)
      for rangkuman in berita.find_all('a', class_='gs-title'):
          if(i==0 or i%2==0):
              rangkuman_rapi = ' '.join(str(rangkuman.get('href')).strip().split()) 
              #print(rangkuman_rapi)
              # append teks rangkuman ke list 
              link_list.append(rangkuman_rapi)
          i=i+1
      for berita in kontainer_beritaKompas: 
        for rangkuman in berita.find_all('a', class_='gs-title'):
            if(i==0 or i%2==0):
                rangkuman_rapi = ' '.join(str(rangkuman.get_text()).strip().split()) 
                #print(rangkuman_rapi)
                # append teks rangkuman ke list
                judul_list.append(rangkuman_rapi)
                website_list.append('kompas') 
            i=i+1
        i=0
        for rangkuman in berita.find_all('div', class_='gs-bidi-start-align gs-snippet'):
            rangkuman_rapi = ' '.join(str(rangkuman.get_text()).strip().split()) 
            hasilSplit = rangkuman_rapi.split(" ... ")
            print((hasilSplit))
            if(len(hasilSplit)<2):
                #tgl_list.append(hasilSplit[0])
                isi_list.append(hasilSplit[0])
            else:
                tgl_list.append(hasilSplit[0])
                isi_list.append(hasilSplit[1])
        for rangkuman in berita.find_all('img', class_='gs-image'):
            rangkuman_rapi = ' '.join(str(rangkuman.get('src')).strip().split()) 
            #print(rangkuman_rapi)
            # append teks rangkuman ke list 
            img_list.append(rangkuman_rapi)
        for rangkuman in berita.find_all('a', class_='gs-title'):
            if(i==0 or i%2==0):
                rangkuman_rapi = ' '.join(str(rangkuman.get('href')).strip().split()) 
                #print(rangkuman_rapi)
                # append teks rangkuman ke list 
                link_list.append(rangkuman_rapi)
            i=i+1        
  ##
  # siapkan list kosong untuk menampung judul dan rangkuman kompas.com
  i=0 
  ##
  dfBerita = pd.DataFrame()  
  dfBerita['website']=website_list
  dfBerita['judul']=judul_list
  dfBerita['isi']=isi_list
  dfBerita['tgl']=tgl_list
  dfBerita['link']=link_list
  dfBerita['gambar']=img_list

  #st.dataframe(dfBerita)
  #tokenizer = Tokenizer(num_words=19)
  #tokenizer.fit_on_texts(data)
  #sequences = tokenizer.texts_to_sequences(data)
  #tweets = tweepy.Cursor(api.search_tweets, q=keyword,lang = 'id').items(100) 
  tweet=[]
  users=[]
  userAuthor=[]
  createdAt=[]
  place=[]
  qoute=[]
  retweet=[]
  favorite=[]
  typeTweet=[] 
  proPic=[]
  screenName=[]
  totalImpressionPerAccount=[]  
  totalImpression=0
  keyword=keyword+" since:"+str(awal)+" until:"+str(akhir)+" lang:id"
  for count,t in enumerate(sntwitter.TwitterSearchScraper(keyword).get_items()): 
    if count>1000:
        break 
    tweet.append(t.content)  
    proPic.append(t.user.profileImageUrl)
    userAuthor.append(t.user.displayname)
    createdAt.append(t.date)
    #print(t.user.location)
    screenName.append(t.user.displayname)
    users.append(t.user.username)
    place.append(t.user.location)
    retweet.append(t.retweetCount)
    favorite.append(t.likeCount) 
    totalImpressionPerAccount.append([t.likeCount+t.replyCount+t.likeCount+t.quoteCount+t.retweetCount,t.user.displayname])
    totalImpression=totalImpression+t.likeCount+t.replyCount+t.likeCount+t.quoteCount+t.retweetCount
    i=i+1
    #st.text(t.text)
    #st.text(' ') 
  #for tweet in strings: 
    #sequence = tokenizer.texts_to_sequences(tweet)
    #test = pad_sequences(sequence, maxlen=19)
    #st.text(tweet+" :"+sentiment[np.around(model3.predict(test), decimals=0).argmax(axis=1)[0]])
#Matplot 


#    

col1,col2=st.columns([3,1])
with col1:
    import matplotlib.pyplot as plt
    from datetime import datetime
    MyList=[]
    for a in createdAt:
        MyList.append(a.strftime("%m/%d/%Y") )

    my_dict = {i:MyList.count(i) for i in MyList}
    dates=[]
    value=[]
    for i in my_dict:
        dates.append(i)
        value.append(my_dict[i])
    fig, ax = plt.subplots(figsize=(50, 20)) 
    st.subheader('Perkembangan Tweet dari '+keywordUI)
    df = pd.DataFrame({
    'date': dates,
    'second column': value
    })

    df = df.rename(columns={'date':'index'}).set_index('index')
 
    st.line_chart(df) 
with col2:
    import matplotlib.pyplot as plt
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    st.subheader('Perbandingan Sentiment dari '+keywordUI)
    labels = 'Negative', 'Neutral', 'Positive'
    sizes = [15, 30, 45]# only "Neutral" the 2nd slice (i.e. 'Hogs')
    explode = (0, 0.1, 0) 
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode,labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90,radius=0.5)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig1, use_container_width=True)
    
    col2.metric("Total Impression", str(totalImpression))

from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, ArrayDictionary, StopWordRemover
 
factory = StopWordRemoverFactory() 

stopword = factory.create_stop_word_remover()
data = factory.get_stop_words()+['dengan', 'ia','bahwa','oleh','co','rt','t',"gue","yg","aku"] 
dictionary = ArrayDictionary(data)
stopword = StopWordRemover(dictionary)
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
factory = StemmerFactory()
stemmer = factory.create_stemmer()
#
wordFreq=[]
import re
from wordcloud import WordCloud, STOPWORDS
comment_words = ''
for val in tweet:
    
    # typecaste each val to string 
    val=stemmer.stem(val)
    
    val = re.sub(r"http\S+", "", val)
    
    val=stopword.remove(val)
    # split the value
    tokens = val.split()
     
    # Converts each token into lowercase
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()
        wordFreq.append(tokens[i])
    comment_words += " ".join(tokens)+" "
    
wordcloud = WordCloud(width = 800, height = 800,background_color ='white',   min_font_size = 10).generate(comment_words)
 


#
from collections import Counter

counts = Counter(wordFreq)
freq=Counter(wordFreq).most_common(5) 
col1,col2,col3=st.columns(3)
with col1: 
    st.header("5 hasil kata yang paling sering muncul atau berelasi dengan " + keywordUI)
    for i in range(0,5):
        st.caption(str(i+1)+". "+str(freq[i][0])+": "+str(freq[i][1]))
    i=0
with col2: 
    st.header("World Cloud dari "+ keywordUI)
    # plot the WordCloud image                      
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    st.pyplot()
    
with col3:
    totalImpressionPerAccount.sort(reverse=True)
    st.header("5 Account total impression terbanyak "+ keywordUI)
    for i in range(0,5):
        st.caption(str(i+1)+". "+str(totalImpressionPerAccount[i][1])+": "+str(totalImpressionPerAccount[i][0]))
    i=0

col1, col2 = st.columns([1, 1])
with col1:
  with st.expander("Twitter tentang "+keywordUI +" "):
    st.write(""" Berikut tweet-tweet yang ada : """) 
    for j in range(5):  
        st.markdown("<div class='card'><div class='card-header'>"+str(createdAt[j].strftime("%d %b %Y, %H:%M:%S"))+"</div><div class='card-body'><div class='container'><div class='row'><div class='col-2'><img src='"+str(proPic[j])+"' style='display: inline-block;border-radius:50%;background-repeat: no-repeat;background-position: center center;background-size: cover;'></div><div class='col-10'><h5 class='card-title'>"+str(users[j])+"</h5><p style='color: darkgray;margin-top: -20px;'>@"+str(screenName[j])+"</p></div></div></div><p class='card-text'>"+str(tweet[j])+"</p></div> <div class='card-footer''><i class='fa fa-retweet'></i>"+" "+str(retweet[j])+"  "+"<i class='fa fa-heart'></i> "+str(favorite[j])+"</div></div><br>", unsafe_allow_html=True)
with col2:
  with st.expander("Media online tentang "+keywordUI +" "):
    st.write(""" Berikut berita-berita yang ada : """) 
    
    if (len(website_list)>=5):
        lengthWeb=5
    else :
        lengthWeb=len(website_list)
    for j in range(lengthWeb):  
        st.markdown("<div class='card mb-3' style='max-width: 540px;margin:auto;'><div class='row no-gutters' ><div class='col-md-4'><img src='"+str(img_list[j])+"' class='card-img' alt='...' style='margin-left: 1rem;margin-top: 1rem;'> </div><div class='col-md-8'><div class='card-body'><h5 class='card-title'><a href='"+str(link_list[j])+"'>"+str(judul_list[j])+"</a></h5><p class='card-text'>"+str(isi_list[j])+"</p> <p class='card-text'><small class='text-muted'>"+str(tgl_list[j])+" by "+str(website_list[j])+" </small></p></div> </div></div></div>", unsafe_allow_html=True)


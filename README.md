# News Headline Filter


## 01. Introduction
Nowadays, unsuitable news content for under 12-year-old children is increasing in Taiwan. Those violent, bloody, and pornographic content should be restricted. To protect these young audiences' mental health, I build a deep learning model that can avoid them from reaching these types of news. All news headlines are in **Mandarin**.
***
## 02. Setup
### 1. Google Colaboratory
This project is built on Google Colab. First of all, you need to new a folder named `Colab Notebooks` in your google drive. Then, import your drive from google.colab to access the folder.
```python
%cd '/content/drive/My Drive/Colab Notebooks'
```
### 2. Import text data
Upload the CSV file named `NewsTitle2` to the folder you have built.
***
## 03. Test and Application
You can copy and paste any news headlines to test.  
*Prediction probability means the accuracy of the prediction.  
*Prediction will show banned or passed.
```python
predict('<news_headline>')
```


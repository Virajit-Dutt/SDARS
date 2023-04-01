
# import module
import requests
import openai
openai.api_key = "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"
from bs4 import BeautifulSoup
  
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
  
# user define function
# Scrape the data
def getdata(url):
    r = requests.get(url, headers=HEADERS)
    return r.text

# Use ChatGPT to summarize the review
def chatgpt_summarize(review):
    # from transformers import pipeline
    # summarizer = pipeline("summarization")
    # summary = summarizer(review, max_length=100, min_length=30, do_sample=False)
    summary = "This is a summary"
    return summary
  
  
def html_code(url):
  
    # pass the url
    # into getdata function
    htmldata = getdata(url)
    soup = BeautifulSoup(htmldata, 'html.parser')
  
    # display html code
    return (soup)

def cus_data(soup):
    # find the Html tag
    # with find()
    # and convert into string
    data_str = ""
    cus_list = []
  
    for item in soup.find_all("span", class_="a-profile-name"):
        data_str = data_str + item.get_text()
        cus_list.append(data_str)
        data_str = ""
    return cus_list
  
  

def cus_rev(soup):
    # find the Html tag
    # with find()
    # and convert into string
    data_str = ""
  
    for item in soup.find_all("div", class_="a-expander-content reviewText review-text-content a-expander-partial-collapse-content"):
        data_str = data_str + item.get_text()
    
    result = data_str.split("\n")
    # print(result)
    return (result)


  
  

def product_info(soup):
  
    # find the Html tag
    # with find()
    # and convert into string
    data_str = ""
    pro_info = []
  
    for item in soup.find_all("ul", class_="a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"):
        data_str = data_str + item.get_text()
        pro_info.append(data_str.split("\n"))
        data_str = ""
    return pro_info
  
  
def rev_img(soup):
  
    # find the Html tag
    # with find()
    # and convert into string
    data_str = ""
    cus_list = []
    images = []
    for img in soup.findAll('img', class_="cr-lightbox-image-thumbnail"):
        images.append(img.get('src'))
    return images
  
#Classify the review sentiment using model.h5
def review_sentiment(review):
    # from tensorflow.keras.models import load_model
    # model = load_model('models\model.h5')
    # review = review.reshape(1, -1)
    # review = review.astype('float32')
    # review = review / 255
    # prediction = model.predict(review)
    prediction = 1
    return prediction

def summarizer(review):
    reviews_text = '\n'.join(review)

    # Use the GPT API to generate a summary of the reviews
    model_engine = "text-davinci-002"
    summary = openai.Completion.create(
        engine=model_engine,
        prompt=f"Please summarize the following customer reviews:\n{reviews_text}\n\nSummary:",
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Print the summary
    print(summary.choices[0].text.strip())
    return summary.choices[0].text.strip()   
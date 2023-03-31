#Flask App
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask import session as login_session
from flask import make_response
from sqlalchemy import create_engine
from scraperbs import getdata, html_code, cus_data, cus_rev, product_info, rev_img, review_sentiment

app = Flask(__name__)

#First Page Render - Home Page

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    link = ""
    #Request for link from index.html
    if request.method == 'POST':
        link = request.form['link']
        #redirect to scrape route
        return redirect(url_for('scrape', link=link))
    return render_template('index.html')

# Web Scraping route
@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    #return to scrape.html 
    link = request.args.get('link')
    #Go to the product reviews and scrape the data
    data = html_code(link)
    #return customer data
    cus_res = cus_data(data)
    rev_data = cus_rev(data)
    rev_result = []
    for i in rev_data:
        if i == "":
            pass
        else:
            rev_result.append(i)

    pro_result = product_info(data)
    #parse list items into strings in product_info
    pro_result = ['\n'.join(i) for i in pro_result]

    #Show images from rev_img
    images = rev_img(data)

    #Classify the review sentiment of the product
    sentiment = review_sentiment(rev_result)
    
    

    return render_template('scrape.html', link=link, cus_res=cus_res, cus_rev=rev_result, pro_result=pro_result, rev_img=images)

    


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    # Run on port 3000
    app.run(debug=True, port=3000)

    

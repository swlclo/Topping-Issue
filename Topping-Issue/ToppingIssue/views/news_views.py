from ToppingIssue import app
from flask import render_template, request
import sqlite3 as sql
import pandas as pd
from ast import literal_eval
import json
from numpyencoder import NumpyEncoder

@app.route('/news', methods = ['GET'])
def news():
    selectCategory = request.args.get('subCategory')
    
    with sql.connect("ToppingIssue/ToppingIssue.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM news_data_" + str(selectCategory))
        rows = cur.fetchall()
        cols = [column[0] for column in cur.description]
        news_df = pd.DataFrame.from_records(data=rows, columns=cols)
    conn.close()

    news_df['Title'] = news_df['Title'].apply(lambda x: literal_eval(x))
    news_df['Link'] = news_df['Link'].apply(lambda x: literal_eval(x))

    newsData = {}
    N_sentimentData = []
    D_sentimentData = []

    for i in range(0, len(news_df)):
        mainClusterName = i
        newsData[mainClusterName] = [news_df['Title'][i][0:3], news_df['Link'][i][0:3]]
        N_sentimentData.append([news_df['N_Good'][i], news_df['N_Bad'][i], news_df['N_Neut'][i]])
        D_sentimentData.append([news_df['D_Good'][i], news_df['D_Bad'][i], news_df['D_Neut'][i]])

    return render_template("news.html", newsData=newsData, subCategory='하이',
        N_sentimentData=json.dumps(N_sentimentData, cls=NumpyEncoder), D_sentimentData=json.dumps(D_sentimentData, cls=NumpyEncoder))
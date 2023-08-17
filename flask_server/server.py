from flask import Flask, jsonify, redirect, request, url_for
from collections import Counter
import pandas as pd
import re
import requests
import urllib.parse

app = Flask(__name__)

@app.route('/api')
def api():
    try:
        # Reddit API
        client_id = "NO7eW0Y94TRDka_g7zVb2A"
        secret_key = "xU5reQOGKgWbFFy8AZljDjnCxthqug"
        user_agent = "stocks_api"
        username = "Daiiki"

        auth = requests.auth.HTTPBasicAuth(client_id, secret_key)

        with open("pwd.txt", "r") as f:
            password = f.read()

        data = {"grant_type": "password", "username": username, "password": password}

        headers = {"User-Agent": user_agent}

        res = requests.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=auth,
            data=data,
            headers=headers,
            timeout=10,
        )

        TOKEN = res.json()["access_token"]
        headers["Authorization"] = f"bearer {TOKEN}"
        requests.get("https://oauth.reddit.com/api/v1/me", headers=headers, timeout=10)


        # Reddit Data
        subred = "wallstreetbets"
        category = "hot"

        res = requests.get(
            f"https://oauth.reddit.com/r/{subred}/{category}",
            headers=headers,
            params={"limit": "100"},
            timeout=10,
        )

        # Putting some relevant data into a spreadsheet
        df_reddit_data = []

        for post in res.json()["data"]["children"]:
            data = {
                "title": post["data"]["title"],
                "selftext": post["data"]["selftext"],
                "upvotes": post["data"]["ups"],
                "downvotes": post["data"]["downs"],
                "upvotes_ratio": post["data"]["upvote_ratio"],
                "score": post["data"]["score"],
            }
            df_reddit_data.append(data)

        df_reddit = pd.DataFrame(df_reddit_data)
            
            
        # Collecting data based on a pattern
        search_pattern = r"(?<![A-Z])[A-Z]{2,4}(?![A-Z])"
        res = []

        for row in df_reddit.selftext:
            matches = re.finditer(search_pattern, row)
            for match in matches:
                res.append(match.group())

        for row in df_reddit.title:
            matches = re.finditer(search_pattern, row)
            for match in matches:
                if match.group() not in res:
                    res.append(match.group())
        
        
        #Filtering out none-tickers
        df_company = pd.read_excel('company_list.xlsx')
        symbols = df_company['Symbol'].values.tolist()
        
        reddit_tickers = []
        for i in range(len(res)):
            if res[i] in symbols:
                reddit_tickers.append(res[i])

        # Count the ticker occurrences
        ticker_counts = Counter(reddit_tickers)
        
        #Deleting commonly used but irrelevant tickers
        try:
            del ticker_counts['AI']
        except:
            print('AI not in tickers')
        try:
            del ticker_counts['CEO']
        except:
            print('CEO not in Tickers')
        try:
            del ticker_counts['NEW']
        except:
            print('NEW not in Tickers')
        try:
            del ticker_counts['AM']
        except:
            print('AM not in Tickers')

        # Getting the top 10 tickers
        # top_tickers = {ticker: {"count": count} for ticker, count in ticker_counts.most_common(10)}
        top_tickers = [ticker for ticker, count in ticker_counts.most_common(7)]
        
        # Redirect to the 'prices' endpoint with the top_tickers as query parameters
        query_params = {'tickers': top_tickers}
        query_string = urllib.parse.urlencode(query_params, doseq=True)
        return redirect(url_for('prices') + '?' + query_string)


        # return jsonify(top_tickers)

    except Exception as e:
        # Handle any exceptions
        error_message = f"An error occurred: {str(e)}"
        return jsonify(error=error_message), 500
    


@app.route('/prices', methods=['GET'])
def prices():
    
    try:
        # Get the ticker symbols from the query parameters
        tickers = request.args.getlist('tickers')
        
        TDKEY = "71f03e968def41da843befd7b52604f4"
        tdurl = 'https://api.twelvedata.com/price?symbol=' + ','.join(tickers) + '&apikey=' + TDKEY

        response = requests.get(tdurl, headers={'User-agent': 'request'})
        data = response.json()

        if response.status_code != 200:
            print('Status:', response.status_code)
        else:
            print(data)

        return jsonify(data)
    
    except Exception as e:
        # Handle any exceptions
        error_message = f"An error occurred: {str(e)}"
        return jsonify(error=error_message), 500




if __name__ == "__main__":
    app.run(debug=True)

import json
import requests


def read_google_key():
    google_api_key = None
    try:
        with open('google-custom-search-api.key', 'r') as f:
            google_api_key = f.readline().strip()
    except:
        try:
            with open('../google-custom-search-api.key') as f:
                google_api_key = f.readline().strip()
        except:
            raise IOError('bing.key file not found')
    if not google_api_key:
        raise KeyError('Bing key not found')
    return google_api_key


def run_query(search_terms):
    google_api_key = read_google_key()
    api_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": google_api_key,
        "cx": "87c25690b11d50b5f",
        "q": search_terms,
    }

    response = requests.get(api_url, params=params)

    response.raise_for_status()
    search_results = response.json()

    results = []
    for result in search_results['items']:
        results.append({
            'title': result['title'],
            'link': result['link'],
            'summary': result['snippet'],
        })

    return results

def main():
    search_terms = input("Enter your query terms: ")
    results = run_query(search_terms)

    for result in results:
        print(result['title'])
        print(result['link'])
        print(result['summary'])
        print('===============')

if __name__ == '__main__':
    main()
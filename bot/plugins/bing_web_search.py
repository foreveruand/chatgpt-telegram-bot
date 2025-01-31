import os
from itertools import islice
from typing import Dict
import requests
from .plugin import Plugin
import logging

class BINGWebSearchPlugin(Plugin):
    """
    A plugin to search the web for a given query, using Bing
    """
    def __init__(self):
        self.subscription_key = os.getenv('BING_API_KEY', '')

    def get_source_name(self) -> str:
        return "Bing"

    def get_spec(self) -> [Dict]:
        return [{
            "name": "web_search",
            "description": "Execute a web search for the given query and return a list of results",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "the user query"
                    }
                },
                "required": ["query"],
            },
        }]

    async def execute(self, function_name, helper, **kwargs) -> Dict:
        endpoint = "https://api.bing.microsoft.com" + "/v7.0/search"
        # Construct a request
        mkt = 'zh-CN'
        params = { 'q': kwargs['query'], 'mkt': mkt }
        headers = { 'Ocp-Apim-Subscription-Key': self.subscription_key }
        results = ''
        # Call the API
        try:
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            results = response.json()
        except Exception as ex:
            logging.error(ex)
        results = results['webPages']['value'][:2]
        if results is None or len(results) == 0:
            return {"Result": "No good Bing Search Result was found"}

        def to_metadata(result: Dict) -> Dict[str, str]:
            return {
                "snippet": result["snippet"],
                "link": result["url"],
            }
        logging.info({"result": [to_metadata(result) for result in results]})    
        # return {"Result": "No good Bing Search Result was found"}
        return {"result": [to_metadata(result) for result in results]}

# def bing_search(query):
#     subscription_key = os.environ['BING_API_KEY']
#     # search_url = 
#     # headers = {"Ocp-Apim-Subscription-Key": subscription_key}
#     # params = {"q": query, "textDecorations": True, "textFormat": "HTML"}
#     # response = requests.get(search_url, headers=headers, params=params)
#     # response.raise_for_status()

#     endpoint = "https://api.bing.microsoft.com" + "/v7.0/search"
#     # Construct a request
#     mkt = 'zh-CN'
#     params = { 'q': query, 'mkt': mkt }
#     headers = { 'Ocp-Apim-Subscription-Key': subscription_key }
#     # Call the API
#     try:
#         response = requests.get(endpoint, headers=headers, params=params)
#         response.raise_for_status()
#         return response.json()
#     except Exception as ex:
#         raise ex
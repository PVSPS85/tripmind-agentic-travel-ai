import os
import json
import requests
from crewai.tools import tool

class SearchTools:
    @tool("Search the internet")
    def search_internet(query: str) -> str:
        """Useful to search the internet about a given topic and return relevant results."""
        top_result_to_return = 2
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': os.environ.get('SERPER_API_KEY', ''),
            'content-type': 'application/json'
        }
        
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            response.raise_for_status() # Catches HTTP errors (404, 500, etc.)
        except requests.exceptions.RequestException as e:
            return f"Failed to fetch search results: {e}"
            
        results = response.json().get('organic', [])
        string = []
        
        # Parse and format the top organic Google search results
        for result in results[:top_result_to_return]:
            if 'title' in result and 'link' in result and 'snippet' in result:
                string.append('\n'.join([
                    f"Title: {result['title']}",
                    f"Link: {result['link']}",
                    f"Snippet: {result['snippet']}",
                    "---"
                ]))
                
        return '\n'.join(string) if string else "No relevant search results found."

import requests
import json

class TextDB:
    def search_db_ref(self, title: str) -> str:
        search = f'https://en.wikipedia.org/w/rest.php/v1/search/title?q={title}&limit1'
        search_response = requests.get(search)

        search_response_json = json.loads(search_response.text)

        searched_term = ""

        if len(search_response_json["pages"]) > 0:
            searched_term = search_response_json["pages"][0]["title"]
        else:
            raise Exception("Couldn't find searched term")

        return searched_term

    def search_from_text_db(self, title: str) -> str:
        searched_term = self.search_db_ref(title)

        url = f'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exlimit=max&explaintext&titles={searched_term}&redirects='
        response = requests.get(url)

        response_json = json.loads(response.text)

        content = ""

        sub_str = "=="

        for page in response_json["query"]["pages"].keys():
            content = response_json["query"]["pages"][page]["extract"]

        content = content[:content.index(sub_str) + len(sub_str)]

        content = content.lower()

        return content
import requests
import json

class TextDB:
    def search_for_term(self, title: str, limit: int):
        search = f'https://en.wikipedia.org/w/rest.php/v1/search/title?q={title}&limit={limit}'
        search_response = requests.get(search)

        return json.loads(search_response.text)
    
    def get_db_ref(self, title: str) -> str:
        search_response_json = self.search_for_term(title, 1)

        searched_term = ""

        if len(search_response_json["pages"]) > 0:
            searched_term = search_response_json["pages"][0]["title"]
        else:
            raise Exception("Couldn't find searched term")

        return searched_term
    
    def get_search_options(self, title: str, limit: int) -> [str]:
        search_response_json = self.search_for_term(title, limit)

        results = []

        num_of_pages = len(search_response_json["pages"])

        if num_of_pages > 0:
            for i in range(num_of_pages):
                results.append(search_response_json["pages"][i]["title"])
        else:
            raise Exception("Couldn't find searched term")

        return results


    def search_from_text_db(self, title: str) -> (str, str, str, str):
        searched_term = self.get_db_ref(title)

        return self.get_content(searched_term)

    def get_content(self, title: str) -> (str, str, str, str):
        url = f'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exlimit=max&explaintext&titles={title}&redirects='
        response = requests.get(url)

        response_json = json.loads(response.text)

        content = ""

        sub_str = "=="

        for page in response_json["query"]["pages"].keys():
            content = response_json["query"]["pages"][page]["extract"]
        full_text = content
        content = content[:content.index(sub_str) + len(sub_str)]

        content = content.lower()

        return content, full_text, url, title
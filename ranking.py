import google.generativeai as genai

class Ranking:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.0-pro-latest')

    def get_ranks(self, theme, terms):
        terms = ';'.join(terms)
        prompt = f"For the following Theme: {theme}, classify the importance of each term to the theme from 1 (most important) to 5 (less important) and return a tuple with (term|grade) format for every following term: {terms}"

        text = self.model.generate_content(prompt,
            generation_config = genai.GenerationConfig(
                temperature=0.5
            )
        ).text

        return self.response_treatment(text)

    def response_tuple_to_dict(self, tuple):
        if tuple.startswith("(") and tuple.endswith(")"):
            tuple = tuple[1:len(tuple)-1]
            term, grade = tuple.split("|")
            return {
                "term": term,
                "level": int(grade)
            }

    def response_treatment(self, response):
        response = response.split("\n")
        return list(map(self.response_tuple_to_dict, response))

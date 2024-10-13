from transformers import pipeline
import numpy

class Ranking:
    def __init__(self):
        self.classifier = pipeline('zero-shot-classification', model='roberta-large-mnli')

    def get_ranks(self, theme, terms):
        sequence_to_classify = f"to learn about {theme}"
        hypothesis_template = "learning about {} is really important"

        result = self.classifier(sequence_to_classify, terms, hypothesis_template=hypothesis_template)

        return self.format_response(result)

    def response_tuple_to_dict(self, term, level):
        
        return {
            "term": term,
            "level": level
        }

    def format_response(self, response):
        return list(map(self.response_tuple_to_dict, response["labels"], response["scores"]))

from transformers import pipeline
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
class Ranking:
    def __init__(self):
        self.classifier = pipeline('zero-shot-classification', model='roberta-large-mnli')

    def get_ranks(self, theme, terms):
        if (len(terms) <= 0): return []
        elif (len(terms) == 1): return [{ "term": terms[0], "level": 1 }]
        else:
            sequence_to_classify = f"to learn about {theme}"
            hypothesis_template = "learning about {} is important"

            result = self.classifier(sequence_to_classify, terms, hypothesis_template=hypothesis_template)

            return self.format_response(result)
    
    def group_scores(self, scores, terms):
        standard_deviation = np.std(scores)
        labels = [1]

        clusters = [{
            "leader": scores[0],
            "scores": [scores[0]]
        }]

        cluster_number = 0

        for score in scores[1:]:
            if clusters[cluster_number]["leader"] - score - standard_deviation <= 0:
                clusters[cluster_number]["scores"].append(score)
                
            else:
                clusters.append({
                    "leader": score,
                    "scores": [score]
                })
                cluster_number += 1
            labels.append(cluster_number + 1)

        return [{ "term": terms[i], "level": labels[i] } for i in range(len(labels))]

    def format_response(self, response):
        return self.group_scores(response["scores"], response["labels"])
    

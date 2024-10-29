from transformers import pipeline
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
class Ranking:
    def __init__(self):
        self.classifier = pipeline('zero-shot-classification', model='roberta-large-mnli')

    def get_ranks(self, theme, terms):
        sequence_to_classify = f"to learn about {theme}"
        hypothesis_template = "learning about {} is really important"

        result = self.classifier(sequence_to_classify, terms, hypothesis_template=hypothesis_template)

        return self.format_response(result)
    
    def group_scores(self, scores, terms):
        X = np.array(scores).reshape(-1, 1)
        bandwidth = estimate_bandwidth(X, quantile=0.3)
        ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
        ms.fit(X)
        labels = ms.labels_

        labels_unique = np.unique(labels)
        n_clusters_ = len(labels_unique)

        return [{ "term": terms[i], "level": n_clusters_ - labels[i].item() } for i in range(len(labels))]

    def format_response(self, response):
        return self.group_scores(response["scores"], response["labels"])

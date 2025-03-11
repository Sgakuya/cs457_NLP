from typing import Dict, List
from util import *
from collections import defaultdict, Counter


class NBLangIDModel:
    def __init__(self, ngram_size: int = 2, extension: bool = False):
        """
        NBLangIDModel constructor

        Args:
            ngram_size (int, optional): size of char n-grams. Defaults to 2.
            extension (bool, optional): set to True to use extension code. Defaults to False.
        """
        self._priors = None
        self._likelihoods = None
        self.ngram_size = ngram_size
        self.extension = extension

    def fit(self, train_sentences: List[str], train_labels: List[str]):
        """
        Train the Naive Bayes model (by setting self._priors and self._likelihoods)

        Args:
            train_sentences (List[str]): sentences from the training data
            train_labels (List[str]): labels from the training data
        """
        self._priors = defaultdict(dict)
        vocab = set()
        n_gram_counts = defaultdict(Counter)

        # Collect vocab and n-gram counts
        for sent, lang in zip(train_sentences, train_labels):
            sentence = sent.lower() if self.extension else sent # lowercase if extension is True
            ngrams = get_char_ngrams(sentence, self.ngram_size)
            vocab.update(ngrams)
            n_gram_counts[lang].update(ngrams)

        # Ensure all languages have all n-grams in vocab with at least zero count
        for lang in n_gram_counts.keys():
            n_gram_counts[lang].update({ngram: 0 for ngram in vocab if ngram not in n_gram_counts[lang]})

        # print("vocab=", vocab)
        # print("n_gram_counts=", n_gram_counts)

        # Come up with the priors
        equal_priors = False
        langCounts = Counter(train_labels)
        self._priors = {lang: 1/len(langCounts) for lang in langCounts.keys()} if equal_priors else normalize(langCounts, log_prob=False)

        # # make priors the same i.e, 1/num_langs
        # self._priors = {lang: 1/len(langCounts) for lang in langCounts.keys()}
        # print("my priors=", self._priors)

        # for lang in langCounts.keys():
        #     self._priors[lang] = langCounts[lang] / len(train_labels)
        # print("my priors=", self._priors)

        # Come up with the likelihoods
        self._likelihoods = defaultdict(Counter)
        V = len(vocab)
        k = .05 if self.extension else 1
        # for lang in n_gram_counts.keys():
        #     for ngram in n_gram_counts[lang].keys():
        #         self._likelihoods[lang][ngram] = (n_gram_counts[lang][ngram]+k) / (sum(n_gram_counts[lang].values())+ (V*k))
        for lang, counts in n_gram_counts.items():
            total_count = sum(counts.values())
            self._likelihoods[lang] = {ngram: (count + k) / (total_count + V * k) for ngram, count in counts.items()}
        # print("likelihoods=", self._likelihoods)        

    def predict(self, test_sentences: List[str]) -> List[str]:
        """
        Predict labels for a list of sentences

        Args:
            test_sentences (List[str]): the sentence to predict the language of

        Returns:
            List[str]: the predicted languages (in the same order)
        """
        new_test_sentences = [sentence.lower() if self.extension else sentence for sentence in test_sentences]
        return [argmax(self.predict_one_log_proba(sentence)) for sentence in new_test_sentences]
        # return [argmax(self.predict_one_log_proba(sentence.lower())) for sentence in test_sentences]

    def predict_one_log_proba(self, test_sentence: str) -> Dict[str, float]:
        """
        Computes the log probability of a single sentence being associated with each language

        Args:
            test_sentence (str): the sentence to predict the language of

        Returns:
            Dict[str, float]: mapping of language --> probability
        """
        assert not (self._priors is None or self._likelihoods is None), \
            "Cannot predict without a model!"
        ngrams = get_char_ngrams(test_sentence, self.ngram_size)
        log_probs = defaultdict(float)
        for lang in self._priors.keys():
            log_probs[lang] = math.log(self._priors[lang])
            for ngram in ngrams:
                if ngram in self._likelihoods[lang]:
                    log_probs[lang] += math.log(self._likelihoods[lang][ngram])
        return log_probs

# if __name__ == "__main__":
#     model = NBLangIDModel(ngram_size=2)
#     model.fit(["ablaze", "hablo", "learn"], ["eng", "spa", "eng"])
#     print(model.predict_one_log_proba("able"))
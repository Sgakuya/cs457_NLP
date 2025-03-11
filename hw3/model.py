import abc
from collections import Counter, defaultdict
import itertools
import json
import math
import random
from typing import Dict, List, Set, Tuple


PREDICTIONS_FILENAME = "predicted_tags.json"
UNK_TOKEN = "<UNK>"


def get_tokens(file_path: str) -> List[List[Tuple[str, str]]]:
    """
    Get the tokens and tags from a file.
    The file is expected to have sentences separated by newline.
    Each sentence is formatted as token1/tag1 token2/tag2 ... tokenn tagn

    Args:
        file_path (str): path to a file with the given format

    Returns:
        List[List[Tuple[str, str]]]: outer list represents sentences,
            inner list is tuples of (token, tag) pairs
    """
    sentences = []
    with open(file_path) as f:
        for line in f.readlines():
            tokens = []
            for token_tag_pair in line.split(" "):
                # str.rsplit("/", 1) returns splits once based on the last
                # occurrence of / this is important if the token has / in it
                token, tag = token_tag_pair.strip().rsplit("/", 1)
                tokens.append((token, tag))
            sentences.append(tokens)
    return sentences


class POSTagger(abc.ABC):
    def __init__(self):
        """
        Initialize a POS tagger object
        """
        self._trained = False
        random.seed(457)

    def train(self, train_data_path: str):
        """
        Should be overridden by child classes - sets self._trained to true to
        indicate that the model can be used for prediction

        Args:
            train_data_path (str): path to test data, format should be the
                format accepted by get_tokens
        """
        self._trained = True

    def predict(self, test_data_path: str, report_accuracy: bool = True,
                save_results: bool = True) -> float:
        """
        Method to predict POS tags from a test set and calculate tag-level
        accuracy

        Args:
            test_data_path (str): path to test data, format should be the
                format accepted by get_tokens
            report_accuracy (bool, optional): print the tag-level accuracy
                score. Defaults to True.
            save_results (bool, optional): save the results of incorrectly
                predicted sentences as a json file. Defaults to True.

        Returns:
            float: the tag-level accuracy
        """
        self.check_trained()
        test_sentences = get_tokens(test_data_path)

        correct = 0
        total = 0
        incorrect = []
        for sentence in test_sentences:
            # separate tags from tokens
            tokens = [token for token, _ in sentence]
            golden_tags = [tag for _, tag in sentence]
            # predict and update results
            predicted_tags = self.predict_one(tokens)
            correct += sum(1 for correct, predicted in
                           zip(golden_tags, predicted_tags)
                           if correct == predicted)
            total += len(golden_tags)
            if golden_tags != predicted_tags:
                incorrect.append((tokens, golden_tags, predicted_tags))

        accuracy = correct / total
        if report_accuracy:
            print("Tag level accuracy: {0:.2%}".format(accuracy))

        # save tags in a file
        if save_results:
            with open(PREDICTIONS_FILENAME, "w") as f:
                json.dump(incorrect, f)

        return accuracy

    @abc.abstractmethod
    def predict_one(self, tokens: List[str]) -> List[str]:
        """
        Predict a tag sequence given tokens

        Args:
            tokens (List[str]): a list of tokens

        Returns:
            List[str]: tags for each token
        """
        pass

    def check_trained(self):
        """
        Checks if the model has been trained before predicting.
        Should call before calling _predict_one.

        Raises:
            Exception: model hasn't been trained
        """
        if not self._trained:
            raise Exception("Must train before predicting")


class BaselinePOSTagger(POSTagger):
    def __init__(self):
        """
        Initialize a BaselinePOSTagger
        """
        super().__init__()
        self._token_to_tag = None
        self._tags = Counter()

    def train(self, train_data_path: str):
        """
        Train POS tagger, saving the most probable token for each tag and
        counts of tags

        Args:
            train_data_path (str): path to test data, format should be the
                format accepted by get_tokens
        """
        super().train(train_data_path)
        sentences = get_tokens(train_data_path)
        token_tag_counts = defaultdict(Counter)
        for sentence in sentences:
            for token, tag in sentence:
                token_tag_counts[token][tag] += 1
                self._tags[tag] += 1

        self._token_to_tag = {}
        for token, token_counts in token_tag_counts.items():
            # Counter.most_common(k) returns a list of tuples ordered by count
            # the tuple format is (key, count)
            self._token_to_tag[token] = token_counts.most_common(1)[0][0]

    def predict_one(self, tokens: List[str]):
        """
        Strong baseline:
        * pick the most common tag for the token
        * if the token does not appear in the data, pick the most common tag
          overall

        Args:
            tokens (List[str]): a list of tokens

        Returns:
            List[str]: tags for each token
        """
        # note: python guarantees that .keys() and .values() return data in
        #       the same order
        tags = []
        for token in tokens:
            if token in self._token_to_tag:
                tags.append(self._token_to_tag[token])
            else:
                tags.append(self._tags.most_common(1)[0][0])

        return tags


class HMMPOSTagger(POSTagger):
    def __init__(self, k_transition: float = .01,
                 k_emission: float = .01, extension: bool = False):
        """
        Initialize a HMMPOSTagger

        Args:
            k_transition (float, optional): the alpha value to use for
                laplace smoothing of the transition probabilities.
                Defaults to 1.
            k_emission (float, optional): the alpha value of use for
                laplace smoothing of the emission probabilities. Defaults to 1.
            extension (bool, optional): use an extension that weights emission
                smoothing. Defaults to False.
        """
        super().__init__()
        self.k_transition = k_transition
        self.k_emission = k_emission
        self.extension = extension

        # you might find these to be useful in your predict_one method
        self._init_log_probs = Counter()
        self._transition_log_probs = defaultdict(dict)
        self._emission_log_probs = defaultdict(dict)
        self._tags = set()

        # keep track of most uncommon tag
        self.most_uncommon_tag = None

    def train(self, train_data_path: str):
        """
        Train POS tagger, saving initial, transition, and emission
        probabilities

        Args:
            train_data_path (str): path to test data, format should be the
                format accepted by get_tokens
        """
        super().train(train_data_path)

        init_counts = Counter()
        transition_counts = defaultdict(Counter)
        emission_counts = defaultdict(Counter)

        sentences = get_tokens(train_data_path)
        for sentence in sentences:
            prev_tag = None
            for token, tag in sentence:
                if prev_tag is None:
                    init_counts[tag] += 1
                else:
                    transition_counts[prev_tag][tag] += 1
                emission_counts[tag][token] += 1
                self._tags.add(tag)
                prev_tag = tag

        # use laplace smoothing with self.k_transition for initial
        # probabilities
        self._init_log_probs = self._smooth_normalize_log(
            init_counts, self._tags, self.k_transition)
        
        # use laplace smoothing with self.k_transition for transition
        # probabilities
        for tag, tag_counts in transition_counts.items():
            self._transition_log_probs[tag] = self._smooth_normalize_log(
                tag_counts, self._tags, self.k_transition)

        # get tag with most single occurrences
        most_uncommon_tag = None
        uncommon_count = 0
        for tag, tag_counts in emission_counts.items():
            curr_tag_count = 0
            for token, count in tag_counts.items():
                if count == 1:
                    curr_tag_count += 1
            if curr_tag_count > uncommon_count:
                most_uncommon_tag = tag
                uncommon_count = curr_tag_count

        self.most_uncommon_tag = most_uncommon_tag
                    

        # add <UNK> token with self.k_emission for emission
        # probabilities
        for tag, tag_counts in emission_counts.items():
            vocab = set(tag_counts.keys()) | {UNK_TOKEN}
            self._emission_log_probs[tag] = self._smooth_normalize_log(
                tag_counts, vocab, self.k_emission)


    def predict_one(self, tokens: List[str]):
        """
        Predict a tag for tokens using a HMM and smoothing
        Should use self._init_log_probs, self._transition_log_probs and self._emission_log_probs

        Args:
            tokens (List[str]): a list of tokens

        Returns:
            List[str]: tags for each token
        """
        # raise NotImplementedError("You need to implement this method")
        # Initialize the viterbi matrix and backpointer matrix
        viterbi = defaultdict(list)
        backpointer = defaultdict(list)


        # Initialize the first column of the viterbi matrix
        for tag in self._tags:
            uncommon_tag = self.possible_tag(tokens[0]) if self.extension else tag
            uncommon_prob = self._emission_log_probs[uncommon_tag].get(UNK_TOKEN)
            viterbi[tag].append(self._init_log_probs.get(tag, float("-inf")) 
                                + self._emission_log_probs[tag].get(tokens[0], uncommon_prob))
            backpointer[tag].append(None)
        # print("viterbi: ", viterbi)
        # print("backpointer: ", backpointer)

        # Fill in the rest of the viterbi matrix
        for i in range(1, len(tokens)):
            for tag in self._tags:
                max_prob = float("-inf")
                max_tag = None
                for prev_tag in self._tags:
                    prob = viterbi[prev_tag][i - 1] + self._transition_log_probs[prev_tag].get(tag, float("-inf"))
                    if prob > max_prob:
                        max_prob = prob
                        max_tag = prev_tag
                uncommon_tag = self.possible_tag(tokens[i]) if self.extension else prev_tag
                uncommon_prob = self._emission_log_probs[uncommon_tag].get(UNK_TOKEN)
                viterbi[tag].append(max_prob + self._emission_log_probs[tag].get(tokens[i], uncommon_prob))
                backpointer[tag].append(max_tag)
        # print("viterbi: ", viterbi)
        # print("backpointer: ", backpointer)

        bestPathProb = float("-inf")
        bestPathPointer = None
        for tag in self._tags:
            if viterbi[tag][-1] > bestPathProb:
                bestPathProb = viterbi[tag][-1]
                bestPathPointer = tag   
        # print("bestPathProb: ", bestPathProb)
        # print("bestPathPointer: ", bestPathPointer)

        bestPath = [bestPathPointer]
        for i in range(len(backpointer[bestPathPointer]) - 1, 0, -1):
            bestPathPointer = backpointer[bestPathPointer][i]
            bestPath.append(bestPathPointer)
        bestPath.reverse()
        # print("bestPath: ", bestPath)

        return bestPath
    
    def possible_tag(self, token: str) -> str:
        """
        Get possible tags for an unknown token
        """
        ly_ending = token[-2:].lower() == "ly"
        ing_ending = token[-3:].lower() == "ing"
        ed_ending = token[-2:].lower() == "ed"
        capitalized = token[0].isupper()
        all_caps = token.isupper()

        if ly_ending:
            return "ADV"
        elif ing_ending or ed_ending:
            return "VERB"
        elif capitalized:
            return "NOUN"
        elif all_caps:
            return "PROPN"
        else:
            return self.most_uncommon_tag

    
    
    def set_model_params(self, init: Dict[str, float], transition: Dict[str, Dict[str, float]], \
                      emission: Dict[str, Dict[str, float]]):
        """
        Set log probability values directly rather than learning them from data

        Args:
            init (Dict[str, float]): initial probabilities
            transition (Dict[str, Dict[str, float]]): transition probabilities.
                The keys of the dictionary are prior POS tags, and the values
                are dictionaries mapping the next tags to probabilities
            emission (Dict[str, Dict[str, float]]): emission probabilities. 
                The keys of the dictionary are POS tags and the values are 
                dictionaries mapping the words to probabilities.
        """
        self._tags = set(emission.keys())
        self._init_log_probs = init
        self._emission_log_probs = emission
        self._transition_log_probs = transition

    @staticmethod
    def _smooth_normalize_log(counts: Dict[str, int], vocab: Set[str], k: float) \
        -> Dict[str, float]:
        """
        From counts, creates smoothed log probabilities

        Args:
            counts (Dict[str, int]): dictionary storing counts
            vocab (Set[str]): the entire vocab (used for smoothing)
            k (float): the k value for add-k smoothing

        Returns:
            Dict[str, float]: the log probabilities after smoothing
        """
        result_dict = {}
        denominator = sum(counts.values()) + k * len(vocab)
        for item in vocab:
            prob = (counts.get(item, 0) + k) / denominator
            if prob > 0:
                result_dict[item] = math.log(prob)
            else:
                result_dict[item] = float("-inf")
        return result_dict

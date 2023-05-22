import math
import string
import typing as tp
from collections import defaultdict


class NaiveBayesClassifier:
    def __init__(self, alpha):
        self.alpha = alpha
        self._class_freq: tp.Dict[str, float] = defaultdict(lambda: 0.0)
        self._separated_words_in_class: tp.Dict[tp.Tuple[str, str], int] = defaultdict(lambda: 0)
        self._words_in_class: tp.Dict[str, int] = defaultdict(lambda: 0)
        self._word_set: tp.Set[str] = set()

    def fit(self, X, y):
        for feature, label in zip(X, y):
            self._class_freq[label] += 1
            for value in feature.split():
                self._separated_words_in_class[(value, label)] += 1
                self._words_in_class[label] += 1
                self._word_set.add(value)

        num_samples = len(X)
        for k in self._class_freq:
            self._class_freq[k] /= num_samples

    def predict(self, X):
        result = []
        for x in X:
            result.append(max(self._class_freq.keys(), key=lambda c: self.__calculate_class_freq(x, c)))
        return result

    def __calculate_class_freq(self, X: str, my_class: str) -> float:
        freq = math.log(self._class_freq[my_class])

        for feat in X.split():
            freq += math.log(
                (self._separated_words_in_class[feat, my_class] + self.alpha)
                / (self._words_in_class[my_class] + self.alpha * len(self._word_set))
            )
        return freq

    def score(self, X_test, y_test):
        results = self.predict(X_test)
        correct_predictions = sum(y_test[x] == results[x] for x in range(len(y_test)))
        accuracy = correct_predictions / len(y_test)
        return accuracy

    def clean(self, s: str) -> str:
        translator = str.maketrans("", "", string.punctuation)
        cleaned_string = s.translate(translator)
        return cleaned_string

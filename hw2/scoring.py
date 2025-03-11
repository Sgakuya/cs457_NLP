from typing import Any, List
from itertools import combinations


def accuracy_score(y_true: List[Any], y_pred: List[Any]) -> float:
    """
    Compute the accuracy given true and predicted labels

    Args:
        y_true (List[Any]): true labels
        y_pred (List[Any]): predicted labels

    Returns:
        float: accuracy score
    """
    # check that the lengths of y_true and y_pred are the same
    assert len(y_true) == len(y_pred), "y_true and y_pred must have the same length"
    
    num_correct = 0
    for true, pred in zip(y_true, y_pred):
        if true == pred:
            num_correct += 1
    return num_correct / len(y_true)
    

def confusion_matrix(y_true: List[Any], y_pred: List[Any], labels: List[Any]) \
    -> List[List[int]]:
    """
    Builds a confusion matrix given predictions
    Uses the labels variable for the row/column order

    Args:
        y_true (List[Any]): true labels
        y_pred (List[Any]): predicted labels
        labels (List[Any]): the column/rows labels for the matrix

    Returns:
        List[List[int]]: the confusion matrix
    """
    # check that all of the labels in y_true and y_pred are in the header list
    for label in y_true + y_pred:
        assert label in labels, \
            f"All labels from y_true and y_pred should be in labels, missing {label}"
    
    all_combinations = [(label, label2) for label in labels for label2 in labels]
    # print(all_combinations)
    # create dict to map (pred, true) to count
    confusion_dict = {comb: 0 for comb in all_combinations}
    # print(confusion_dict)
    for pred, true in zip(y_pred, y_true):
        confusion_dict[(pred, true)] += 1
    # print(confusion_dict)

    # create a list of lists to represent the confusion matrix
    confusion_matrix = [[confusion_dict[(pred, true)] for true in labels] for pred in labels]
    return confusion_matrix
        


# if __name__ == "__main__":
#     y_true = ["spa", "eng", "spa"]
#     y_pred = ["eng", "eng", "spa"]
#     print(accuracy_score(y_true, y_pred))  

#     labels = ["spa", "eng", "fra"]
#     print(confusion_matrix(y_true, y_pred, labels))
#     # [[1, 1],
#     #  [0, 3]]

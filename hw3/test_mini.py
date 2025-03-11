from model import HMMPOSTagger


def main():
    """
    Train/test your model WITHOUT SMOOTHING on the basic examples we saw in class.
    """

    print("Please note that this script tests the basic functionality of your code with no smoothing on two very small test sets!")

    tagger = HMMPOSTagger(k_emission=0, k_transition=0)
    # instead of training the model, this test script will use the set_prob method
    # IF you want to test your model using this, you"ll need to implement that method
    # otherwise, you may skip it, but I do think that this will be helpful for debugging!
    # it tests the two examples that we saw in class

    print("Example 1: 'bear is on the move.'")

    # the initial, transition and emission log probabilities in the "bear is on the move" example
    emission_1 = {
        "AT": {"the": -1, "bear": float("-inf"), "is": float("-inf"), "on": float("-inf"), "move": float("-inf"), ".": float("-inf")},
        "BEZ": {"the": float("-inf"), "bear": float("-inf"), "is": 0, "on": float("-inf"), "move": float("-inf"), ".": float("-inf")},
        "IN": {"the": float("-inf"), "bear": float("-inf"), "is": float("-inf"), "on": -3, "move": float("-inf"), ".": float("-inf")},
        "NN": {"the": float("-inf"), "bear": -10, "is": float("-inf"), "on": float("-inf"), "move": -8, ".": float("-inf")},
        "VB": {"the": float("-inf"), "bear": -8, "is": float("-inf"), "on": float("-inf"), "move": -5, ".": float("-inf")},
        "PERIOD": {"the": float("-inf"), "bear": float("-inf"), "is": float("-inf"), "on": float("-inf"), "move": float("-inf"), ".": 0}
    }

    init_1 = {"AT": -2, "BEZ": float("-inf"), "IN": -2, "NN": -1, "VB": -2, "PERIOD": float("-inf")}

    transition_1 = {
        "AT": {"IN": float("-inf"), "VB": float("-inf"), "NN": -1, "AT": float("-inf"), "BEZ": float("-inf"), "PERIOD": -8},
        "BEZ": {"IN": -2, "VB": float("-inf"), "NN": -3, "AT": -1, "BEZ": float("-inf"), "PERIOD": -4},
        "IN": {"IN": -4, "VB": float("-inf"), "NN": -2, "AT": -1, "BEZ": float("-inf"), "PERIOD": -6},
        "NN": {"IN": -1, "VB": -5, "NN": -2, "AT": -4, "BEZ": -3, "PERIOD": -1},
        "VB": {"IN": -1, "VB": -5, "NN": -2, "AT": -1, "BEZ": -6, "PERIOD": -1},
        "PERIOD": {"IN": -1, "VB": -3, "NN": -2, "AT": -1, "BEZ": -5, "PERIOD": float("-inf")}
    }

    tagger.set_model_params(init_1, transition_1, emission_1)
    predictions = tagger.predict_one(["bear", "is", "on", "the", "move", "."])
    print("Should be NN BEZ IN AT NN PERIOD:", predictions)

    print("Example 2: 'ski on snow'")
    # the initial, emission and transition log probabilities in the "ski on snow" example

    init_2 = {"V": -3, "N": -3, "P": -4}

    transition_2 = {
        "V": {"V": -4, "N": -2, "P": -2},
        "N": {"V": -3, "N": -2, "P": -1},
        "P": {"V": -5, "N": -2, "P": -4}
    }

    emission_2 = {
        "V": {"ski": -6, "on": float("-inf"), "snow": -5},
        "N": {"ski": -5, "on": float("-inf"), "snow": -3},
        "P": {"ski": float("-inf"), "on": -1, "snow": float("-inf")}
    }

    tagger.set_model_params(init_2, transition_2, emission_2)
    predictions = tagger.predict_one(["ski", "on", "snow"])
    print("Should be N P N:", predictions)


if __name__ == "__main__":
    main()

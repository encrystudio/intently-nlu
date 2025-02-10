"""Utils for feature extraction"""

import re

from intently_nlu.constants import NONE_LABEL
from intently_nlu.dataset.entity import Entity


def extract_features(sentence: list[str], i: int) -> dict[str, str | bool]:
    """Extract features for a given token in a sentence

    Args:
        sentence (list[str]): List of words in a sentence.
        i (int): Index of the current word.

    Returns:
        dict[str, str | bool]: Dictionary of features for the token.
    """
    word = sentence[i]
    features: dict[str, str | bool] = {
        "word": word,
        "is_first": i == 0,
        "is_last": i == len(sentence) - 1,
        "is_capitalized": word[0].isupper(),
        "is_all_caps": word.isupper(),
        "is_all_lower": word.islower(),
        "prefix-1": word[0],
        "prefix-2": word[:2],
        "suffix-1": word[-1],
        "suffix-2": word[-2:],
        "has_hyphen": "-" in word,
        "is_numeric": word.isdigit(),
    }
    if i > 0:
        features.update(
            {
                "-1:word": sentence[i - 1],
                "-1:is_capitalized": sentence[i - 1][0].isupper(),
            }
        )
    else:
        features["BOS"] = True  # Beginning of Sentence

    if i < len(sentence) - 1:
        features.update(
            {
                "+1:word": sentence[i + 1],
                "+1:is_capitalized": sentence[i + 1][0].isupper(),
            }
        )
    else:
        features["EOS"] = True  # End of Sentence

    return features


def sentence_to_features(sentence: list[str]) -> list[dict[str, str | bool]]:
    """Convert a sentence into a list of feature dictionaries, one per token

    Args:
        sentence (list[str]): The sentence to extract features from.

    Returns:
        list[dict[str, str | bool]]: A list of feature dictionaries.
    """
    return [extract_features(sentence, i) for i in range(len(sentence))]


def prepare_utterance(
    utterance: str, all_slots: dict[str, Entity]
) -> tuple[list[str], list[str]]:
    """Convert an utterance into a list of tokens and a list of labels

    Args:
        utterance (str): The utterance to prepare.
        all_slots (dict[str, Entity]): All slots in the utterance.

    Returns:
        tuple[list[str], list[str]]: List of tokens and list of labels.
    """
    utterance = re.sub(r"\[(.*?)\]", r" [\1] ", utterance)
    utterance_as_list = utterance.split()
    labels_as_list: list[str] = []
    slots = all_slots
    for word in utterance_as_list:
        found = False
        for slot in slots:
            if f"[{slot}]" == word:
                labels_as_list.append(slot)
                found = True
                break
        if not found:
            labels_as_list.append(NONE_LABEL)
    return utterance_as_list, labels_as_list


def utterance_data_augmentation(
    utterances: list[str], all_slots: dict[str, Entity]
) -> list[tuple[list[str], list[str]]]:
    """Augments the utterances by filling slots with examples and converts sentences to training data with labels

    Args:
        utterances (list[str]): Utterances of the intent.
        all_slots (dict[str, Entity]): All slots of the intent.

    Returns:
        list[tuple[list[str], list[str]]]: Augmented utterances as training data with slots filled
    """
    data: list[tuple[list[str], list[str]]] = []
    for utterance in utterances:
        start = prepare_utterance(utterance, all_slots)
        replaced_utterances: list[tuple[list[str], list[str]]] = [start]
        for slot, entity in all_slots.items():
            for replaced_utterance in replaced_utterances.copy():
                found = False
                for index, label in enumerate(replaced_utterance[1]):
                    if slot == label:
                        found = True
                        for value in entity.values:
                            utterance_to_replace = replaced_utterance[0][:]
                            utterance_to_replace[index] = value
                            replaced_utterances.append(
                                (utterance_to_replace, replaced_utterance[1][:])
                            )
                if found:
                    replaced_utterances.remove(replaced_utterance)
        data += replaced_utterances
    return data

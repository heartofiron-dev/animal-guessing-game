"""An animal guessing game using the UCI Zoo dataset."""

import argparse
import csv
import random
from pathlib import Path


DATA_FILE = Path(__file__).parent / "data" / "zoo.data"
FIELD_NAMES = (
    "animal_name", "hair", "feathers", "eggs", "milk", "airborne",
    "aquatic", "predator", "toothed", "backbone", "breathes",
    "venomous", "fins", "legs", "tail", "domestic", "catsize", "type",
)

# Fixed mode follows this order. Random mode picks from this same list.
QUESTIONS = (
    ("milk", 1, "Does it produce milk?"),
    ("feathers", 1, "Does it have feathers?"),
    ("fins", 1, "Does it have fins?"),
    ("legs", 4, "Does it have four legs?"),
    ("legs", 2, "Does it have two legs?"),
    ("legs", 6, "Does it have six legs?"),
    ("legs", 0, "Does it have no legs?"),
    ("hair", 1, "Does it have hair?"),
    ("aquatic", 1, "Does it live in water?"),
    ("eggs", 1, "Does it lay eggs?"),
    ("predator", 1, "Is it a predator?"),
    ("airborne", 1, "Can it fly?"),
    ("venomous", 1, "Is it venomous?"),
    ("toothed", 1, "Does it have teeth?"),
    ("backbone", 1, "Does it have a backbone?"),
    ("breathes", 1, "Does it breathe air?"),
    ("tail", 1, "Does it have a tail?"),
    ("domestic", 1, "Is it domesticated?"),
    ("catsize", 1, "Is it at least the size of a cat?"),
    ("legs", 5, "Does it have five legs?"),
    ("legs", 8, "Does it have eight legs?"),
)
MAX_QUESTIONS = 12
ANSWER_ACCURACY = 0.9
STOP_PROBABILITY = 0.8


def load_animals(filepath=DATA_FILE):
    """Read the original 18-column UCI Zoo file."""
    animals = []
    with open(filepath, newline="", encoding="utf-8") as source:
        for row_number, row in enumerate(csv.reader(source), start=1):
            if len(row) != len(FIELD_NAMES):
                raise ValueError(f"Row {row_number} has {len(row)} columns, not 18.")
            animal = {"animal_name": row[0]}
            for name, value in zip(FIELD_NAMES[1:], row[1:]):
                animal[name] = int(value)
            animals.append(animal)
    if not animals:
        raise ValueError("The dataset is empty.")
    return animals


def next_question(animals, asked, method="fixed", rng=None):
    """Choose an unused question that can split the dataset."""
    available = []
    for index, (feature, expected, wording) in enumerate(QUESTIONS):
        if index in asked:
            continue
        answers = {animal[feature] == expected for animal in animals}
        if len(answers) == 2:
            available.append((index, feature, expected, wording))
    if not available:
        return None
    if method == "random":
        return (rng or random).choice(available)
    return available[0]


def update_probabilities(animals, probabilities, feature, expected, answer):
    """Give matching records more weight, then make the weights sum to one."""
    updated = []
    for animal, probability in zip(animals, probabilities):
        matches = (animal[feature] == expected) == answer
        likelihood = ANSWER_ACCURACY if matches else 1 - ANSWER_ACCURACY
        updated.append(probability * likelihood)
    total = sum(updated)
    return [probability / total for probability in updated]


def name_probabilities(animals, probabilities):
    """Combine records that have the same animal name, such as the two frogs."""
    totals = {}
    for animal, probability in zip(animals, probabilities):
        name = animal["animal_name"]
        totals[name] = totals.get(name, 0) + probability
    return totals


def play(method="fixed", seed=None):
    animals = load_animals()
    probabilities = [1 / len(animals)] * len(animals)
    asked = set()
    rng = random.Random(seed)
    print("Think of an animal in the UCI Zoo dataset. Answer yes or no.")

    while len(asked) < MAX_QUESTIONS:
        scores = name_probabilities(animals, probabilities)
        if max(scores.values()) >= STOP_PROBABILITY:
            break
        question = next_question(animals, asked, method, rng)
        if question is None:
            break
        index, feature, expected, wording = question
        answer = input(f"Question {len(asked) + 1}: {wording} [y/n] ").strip().lower()
        while answer not in ("y", "yes", "n", "no"):
            answer = input("Please answer y or n: ").strip().lower()
        probabilities = update_probabilities(
            animals, probabilities, feature, expected, answer in ("y", "yes")
        )
        asked.add(index)
        scores = name_probabilities(animals, probabilities)
        best_name = max(scores, key=scores.get)
        print(f"Current best guess: {best_name} ({scores[best_name]:.1%})")

    scores = name_probabilities(animals, probabilities)
    best_name = max(scores, key=scores.get)
    if scores[best_name] >= STOP_PROBABILITY:
        print(f"My guess: {best_name} ({scores[best_name]:.1%})")
    else:
        print(f"Best guess: {best_name} ({scores[best_name]:.1%})")
        top_three = sorted(scores, key=scores.get, reverse=True)[:3]
        print("Top three candidates: " + ", ".join(
            f"{name} ({scores[name]:.1%})" for name in top_three
        ))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Guess an animal from the UCI Zoo dataset.")
    parser.add_argument("--method", choices=("fixed", "random"), default="fixed")
    parser.add_argument("--seed", type=int, help="Repeat the same random question order.")
    options = parser.parse_args()
    play(options.method, options.seed)

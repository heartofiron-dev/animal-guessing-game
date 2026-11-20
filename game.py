"""A fixed-order animal guessing game using the UCI Zoo dataset."""

import csv
from pathlib import Path


DATA_FILE = Path(__file__).parent / "data" / "zoo.data"
FIELD_NAMES = (
    "animal_name", "hair", "feathers", "eggs", "milk", "airborne",
    "aquatic", "predator", "toothed", "backbone", "breathes",
    "venomous", "fins", "legs", "tail", "domestic", "catsize", "type",
)

# The order is fixed. A question is skipped if every remaining record
# would give the same answer to it.
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


def next_question(animals, asked):
    """Take the next fixed-order question that can split the candidates."""
    for index, (feature, expected, wording) in enumerate(QUESTIONS):
        if index in asked:
            continue
        answers = {animal[feature] == expected for animal in animals}
        if len(answers) == 2:
            return index, feature, expected, wording
    return None


def matching_animals(animals, feature, expected, answer):
    """Keep records whose stored trait agrees with a yes or no answer."""
    return [
        animal for animal in animals
        if (animal[feature] == expected) == answer
    ]


def play():
    animals = load_animals()
    asked = set()
    names = set(animal["animal_name"] for animal in animals)
    print("Think of an animal in the UCI Zoo dataset. Answer yes or no.")

    while len(names) > 1 and len(asked) < MAX_QUESTIONS:
        question = next_question(animals, asked)
        if question is None:
            break
        index, feature, expected, wording = question
        answer = input(f"Question {len(asked) + 1}: {wording} [y/n] ").strip().lower()
        while answer not in ("y", "yes", "n", "no"):
            answer = input("Please answer y or n: ").strip().lower()
        animals = matching_animals(animals, feature, expected, answer in ("y", "yes"))
        asked.add(index)
        names = set(animal["animal_name"] for animal in animals)
        print(f"Possible animals: {len(names)}")

    if len(names) == 1:
        print(f"My guess: {next(iter(names))}")
    elif names:
        print("I cannot identify one animal from these answers.")
        print("Possible animals: " + ", ".join(sorted(names)))
    else:
        print("No animal in this dataset matches all of those answers.")


if __name__ == "__main__":
    play()

# Animal Guessing Game

This is an animal guessing game for the COMP 3106 project. It reads the UCI Zoo dataset and asks yes/no questions. Each animal record starts with equal probability. After an answer, records that match it get a 0.9 likelihood; other records get a 0.1 likelihood. The game normalizes the probabilities after each question.

It stops after 12 questions, when one animal name reaches 80% probability, or when no unused question can split the dataset. The two `frog` records have separate probabilities, which are added together when the game guesses a name.

Run it with Python 3 from this folder:

```text
python game.py
```

The default mode asks questions in a fixed order. To pick unused questions at random, run:

```text
python game.py --method random
```

Add `--seed 42` to repeat the same random question order. Choose an animal listed in the dataset and answer each question with `y` or `n`. If no name reaches 80%, the game shows its best guess and the top three names. Information-gain question selection is planned for a later stage of the project.

## Dataset

`data/zoo.data` is the original 101-record Zoo dataset from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/111/zoo). It has 16 traits and seven animal types. The file has no header; `game.py` assigns the column names in the order published by UCI. The two `frog` records remain separate records, although they share the same displayed animal name.

Forsyth, R. (1990). *Zoo* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5R59V. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

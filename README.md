# Animal Guessing Game

This is a fixed-order baseline for the COMP 3106 project. It reads the UCI Zoo dataset, asks yes/no questions, and removes animal records that disagree with each answer. It stops after 12 questions, when one animal name remains, or when no remaining question can split the candidates.

Run it with Python 3 from this folder:

```text
python game.py
```

Choose an animal listed in the dataset and answer each question with `y` or `n`. If several animals still fit, the game shows their names. This version uses exact matching; probability updates and other question-selection methods are planned for later stages of the project.

## Dataset

`data/zoo.data` is the original 101-record Zoo dataset from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/111/zoo). It has 16 traits and seven animal types. The file has no header; `game.py` assigns the column names in the order published by UCI. The two `frog` records remain separate records, although they share the same displayed animal name.

Forsyth, R. (1990). *Zoo* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5R59V. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

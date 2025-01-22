
# SD-DFPTRee

Python source code associated to the paper:

J. M. Luna, H. M. Fardoun, F. Padillo, C. Romero & S. Ventura (2022) Subgroup discovery in MOOCs: a big data application for describing different types of learners, Interactive Learning Environments, 30:1, 127-145, [https://doi.org/10.1080/10494820.2019.1643742](https://doi.org/10.1080/10494820.2019.1643742)

## Structure

- `README.md`: Description and usage instructions
- `requirements.txt`: Python dependencies
- `src/`: Source code
  - `preprocess_data.py`: Script for data preprocessing
  - `discover_rules.py`: Sequential SD-DFPTRee script to discover rules
  - `sd_dfptree.py`: SD-DFPTRee Spark script to discover rules
  - `postprocess_rules.py`: Script for postprocessing rules
- `data/`: Datasets used

## Installation

Clone the repository:

```
git clone https://github.com/in1romocgmail/SD-DFPTRee.git
```

## Requirements

Install the dependencies using:

```
pip install -r requirements.txt
```

Copy the dataset to be used into the `data` directory.

## Usage

### Step 1: Preprocess Data

```
python src/preprocess_data.py --input data/input/raw_data.csv --output data/output/preprocessed_data.csv
```

### Step 2: Discover Rules

```
python src/discover_rules.py --input data/output/preprocessed_data.csv --output data/output/rules.csv
```

### Step 3: Discover Rules with Spark

```
python src/sd_dfptree.py --input data/output/preprocessed_data.csv --output data/output/spark_rules.csv
```

### Step 4: Postprocess Rules

```
python src/postprocess_rules.py --input data/output/spark_rules.csv --output data/output/final_rules.csv
```

## Reference

J. M. Luna, H. M. Fardoun, F. Padillo, C. Romero & S. Ventura (2022) Subgroup discovery in MOOCs: a big data application for describing different types of learners, Interactive Learning Environments, 30:1, 127-145, [https://doi.org/10.1080/10494820.2019.1643742](https://doi.org/10.1080/10494820.2019.1643742)

```
@article{luna2022subgroup,
  title={Subgroup discovery in MOOCs: a big data application for describing different types of learners},
  author={Luna, Jos{\'e} Mar{\'\i}a and Fardoun, Habib M and Padillo, Francisco and Romero, Crist{\'o}bal and Ventura, Sebasti{\'a}n},
  journal={Interactive Learning Environments},
  volume={30},
  number={1},
  pages={127--145},
  year={2022},
  publisher={Taylor \& Francis}
}
```

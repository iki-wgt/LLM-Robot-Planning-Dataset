# LLM Robot Planning Dataset

This repo offers the dataset of the this [paper]() and the possibility to create new datasets. 

## Dataset
The dataset can be found [here](https://drive.google.com/drive/folders/10ocT59q-CzqNAOLwHQQTokxN-ECO3asS)

## The Dataset Structure
The dataset is structured as follows:
1. Each sentence has an associated JSON file containing the ground truth movements.
2. The `sentence.json` file contains all sentences along with additional information about the sentences.

## Create new Dataset
To create a new dataset several files are important: 

1. `objects.json`: This JSON file describes the rules, for each rule the corresponding objects and the location. 
2. `gt_paraml.yml` : This file contains all config parameters that are needed to create the dataset. *Hint:* The rule names in this file should be the same as in the objects.json file.

After the setup of these files run the script `create_gt.py` to start the dataset creation.
*Hint:* In this file you can choose the directory name and the path. 

```bash
python3 src/create_gt.py 
```

## Read the Dataset
The script `gt_reader.py` is used to read the dataset.
Adjust the dataset path in the script.

```bash
python3 src/gt_reader.py
```

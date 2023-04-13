# FPS Anti Cheat Detection

## 1. About the FPS Anti Cheat Detection





## 2. Environment

- Python >= 3.9
- Go >= 1.18 (manually install)

```shell
# install python packages under the root directory of the project
pip install -r requirements.txt
```

- Before using tensorflow gpu, you should follow the instructions in the below link
  - https://www.tensorflow.org/install/pip

## 3. Use the sample data

- Classification data
  - Need to install the `weka`
    - Install the weka package `Auto-Weka`
  - Already trained model `mlp.model`
  - Train by yourself
    - Sample training data can be found under the root directory. You can modify the classification_all_feature_data.csv and convert it to .arff, or just use the provided feature .arff file. 
      - Put the .arff training data into the weka, and generate a trained model
      - Use provided test set to test the model, or you can pick random records from the training data and convert to .arff file to test.





## 4. Run the code

Due to time limitation, the codes needs further optimization. Currently you need to manually do some preparation to run the code successfully.

- Classification

  - Before running classification, make sure that no folder named `data_to_combine `and `angle_data` under the `classification` directory.
  - Change the value of `data_path` variable in the `classification_main.py` to the path of demo you prepared.
  - After successfully running the code, the training data `classification_all_feature_data_trained.csv` will be generated under the root directory.

  

## 5. Contact

Email: ``

Phone: ``

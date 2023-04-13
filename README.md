# FPS Anti-Cheat Detection

## 1. About the FPS Anti-Cheat Detection

This project aims at identifying the cheaters in First-Person Shooter (FPS) Games by constructing two subsystems featuring in-game performance and behavior properties respectively which are essential for identifying dishonest players from the honest ones. Initially, find a new approach to extract and preprocess in-game data without cooperating with the game developers. Discover potential new patterns from in-game data for configuring different features for two different subsystems. Afterward, design the MLP classification and LSTM subsystems respectively, feature selection and parameter tuning for each property is the key enabler for characterizing the cheaters from the honest players. To increase the final accuracy, cross validate two prediction results, and yield a final determination.



The contributions of this project are 

1. finding new aiming or shooting patterns and behavior or performance features of cheaters that are distinctive from the honest players;
2. designing a brand-new multi-subsystem architecture for identifying the cheaters;
3. obtaining a generalized approach and more accurate model to identify the cheats for FPS games.
4. providing massive preprocessing and feature extraction approach as well as their relevant codes.



## 2. Environment

- Python >= 3.9
- Go >= 1.18 (manually install)

```shell
# install python packages under the root directory of the project
pip install -r requirements.txt
```

- Before using tensorflow gpu, you should follow the instructions in the below link
  - https://www.tensorflow.org/install/pip



## 3. Use the sample provided data

Need to install the `weka` (https://www.cs.waikato.ac.nz/ml/weka/)

- Classification data

  - Use current trained model
    - Already trained model `mlp.model`

  - Train by yourself

    - Install the weka package `Auto-Weka`

    - Sample training data can be found under the root directory. You can modify the `classification_all_feature_data.csv` and convert it to `.arff`, or just use the provided feature `classification_all_feature_data.arff` file. 

      - Put the .arff training data into the weka, and generate a tuned parameters with the following parameters:
        - `weka.classifiers.meta.AutoWEKAClassifier -seed 123 -timeLimit 90 -memLimit 4000 -nBestConfigs 5 -metric fMeasure -parallelRuns 4`
        - You can obtain the best parameters settings as follows:
          - `weka.classifiers.functions.MultilayerPerceptron -L 0.4856237075132298 -M 0.45855923991991865 -H i -S 1`
      - Use provided test set `classification_testset.arff` to test the model, or you can pick random records from the training data and convert to .arff file to test.

      

- LSTM data

  - Use current trained model

    - Already trained model `RandomTree_LSTM_Raw_Output_Classification.model`

  - Train by yourself

    - Set the training set as `Train_LSTM_RAW_Output.arff`, and the testing set as `Test_LSTM_RAW_Output.arff`.

    - Use the following parameters to run in the weka:

      - `weka.classifiers.trees.RandomTree -K 3 -M 1.0 -V 0.001 -S 1`

      

## 4. Run the code

Because of the limited time, a small part of the code is still not very user-friendly to run on a different environment. That is the exactly reason why we provide a higher-level testing and training set data for you to run it more smoothly. However, if you insist to run everything from the very beginning, it would take very long time and memory. Also, you may encounter some slight problems for MLP preprocessing. If you encounter any problem you can contact with [jiayi719@connect.hku.hk](mailto:jiayi719@connect.hku.hk), [magimaki@connect.hku.hk](mailto:magimaki@connect.hku.hk). We will try to work it out for you. Thanks a lot.

- Classification
  - Before running classification, make sure that no folder named `data_to_combine `and `angle_data` under the `classification` directory.
  - Change the value of `data_path` variable in the `classification_main.py` to the path of demo you prepared.
  - After successfully running the code, the training data `classification_all_feature_data_trained.csv` will be generated under the root directory.
- LSTM
  - If you want to use our trained model directly on testing set, you just simply need to unzip two zip files, and merge them into one. The file structure must be 
    - -First_Folder
      --Second_Folder
      ---your unzipped files here
    - Otherwise, you cannot run the code successfully.
    - After unzipping, you should also change the directory into your first folder path in the `last_main.py`, and pass the second parameter as `'test'`.
    - You will obtain a .txt file which contains the raw prediction result of LSTM. If you want to use weka, you need to convert the text file into csv first, you can use `lstm_txt_to_csv.py`, in which you need to change the directory as your text file. Also, you need to manually change the parameter(numbers of players) at line 8 (in range()).
      - Test Mode: 20
      - Train Mode: The number of your players, can be calculated by checking the text file rows: ((#rows - 1) / 10) - 1

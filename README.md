# Estimation of the Energy Budget of Privacy-Enhancing Technologies

> **Read this before doing anything.** <br>
For any questions, contact via socials on my GitHub profile (first state where are you from and why are you interested).

## Contents
<!-- For instructions, [press here!](#instructions) -->

1. [About the project](#1-about-the-project) 
2. [Requirements](#2-requirements) 
3. [Research files](#3-research) 
4. [Estimation Framework](#4-estimation-framework) 
5. [(Bonus) Measurement Tool Combination Framework](#5-bonus-measurement-tool-combination-framework) 
## 1. About the project: <a name="about"></a>
This is a MSc Thesis Project that explored the estimation of the energy consumption of the Privacy-Enhancing Technologies (PET), as well as privacy risks and utility of the dataset after PET treatment. The estimation is based on the dataset properties, which is used by Gradient Boosting Model. 

The datasets and their sources are listed in the csv file `all_datasets_and_their_sources.csv`

## 2. Requirements <a name="requirements"></a>
Make sure your Python version is the following:<br>
Python 3.10.12 -  3.10.14 (pip 22.0 - 24.0)<br>

Run the following line from the terminal:<br>

`pip install -r requirements.txt`<br>

## 3. Research <a name="research"></a>
All research conducted can be located in the folder `research_files`.
It includes:
1. Cleaned datasets folder
2. Figures folder
3. 8 Notebooks for feature selections
4. 2 dataset properties and measurement datasets
5. Measurement files (main file is called `data_collection_main.py`)

## 4. Estimation Framework <a name="estimation"></a>
### Precautions
Before launching the framework:
1. It's necessary to clean your file.<br>
2. Plus, it's necessary to preprocess the target attribute for classification purposes.<br>
3. For other attributes, please do not modify them in a way, that would change their values. <br>
4. After synthetic data has been generated, the framework will apply MinMaxScaler and One-Hot encoding for ML tasks.<br>

<strong>Running on Terminal:</strong><br>
Linux (or WSL):<br>
`python3 main_project.py`<br>

Windows:<br>
`python main_project.py`<br>

MacOS:<br>
`python3 main_project.py`<br>

<strong>Running on Jupyter Notebook:</strong><br>
`jupyter notebook`<br>

Then, run the notebook, like you normally would a function:<br>

    launch_estimation(filename = None, continuous_to_categorical = None, target = None, epsilon = None)




### What input to provide?
1. Name of the csv file, that is in the `put_your_dataset_here` folder <br>
2. Attributes, that are categorical, but because of their numerical format, could be mistaken for continuous<br>
3. Target attribute <br>

<strong>For terminal:</strong> <br>
Follow the instructions in the terminal!


<strong>For Jupyter Notebook: </strong>  
1. The filename needs to be just a filename. No additional path is necessary. <br>
2. The `continuous_to_categorical` must be a list of strings.
3. Input for epsilon can be either `0` for No Differential Privacy or `1` for Differential Privacy with epsilon value of 0.1.









## 5. (Bonus) Measurement Tool Combination Framework <a name="bonus"></a>
Before launching the framework:
1. It's necessary to clean your file.<br>
2. Plus, it's necessary to preprocess the target attribute for classification purposes.<br>
3. For other attributes, please do not modify them in a way, that would change their values. <br>
4. After synthetic data has been generated, the framework will apply MinMaxScaler and One-Hot encoding for ML tasks.<br>

<strong>Running on Terminal:</strong><br>
Linux (or WSL):<br>
`sudo python3 main_single_measurement.py`*<br>

Windows:<br>
`runas /user:Administrator "python main_single_measurement.py"`*<br>

MacOS:<br>
`sudo python3 main_single_measurement.py`*<br>

<strong>Running on Jupyter Notebook:</strong><br>
`sudo jupyter notebook --allow-root`*<br>
Then, run the notebook, like you normally would a function.<br>

    launch_measurement(input_filename=None, target_attribute_ML=None, num_to_categ = None, possible_known_attributes = None, secret_mode = None,  save_my_report_to_csv = None)

    # Note: possible_known_attributes and secret_mode are disabled. 

*<em>It is necessary to run with the administrator rights in order to perform all hardware measurements of energy consumption. Otherwise, it won't work.</em>

### What input to provide?
1. Name of the csv file, that is in the `put_your_dataset_here` folder <br>
2. Attributes, that are categorical, but because of their numerical format, could be mistaken for continuous<br>
3. Target attribute<br>

Note: The Linkability and Inference risk measurements are disabled.



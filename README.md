# Framework for determining energy budget


## Contents
<!-- For instructions, [press here!](#instructions) -->

1. About the project
2. [Requirements](#requirements) 
3. Experimentations
4. Estimation Framework
5. (Bonus) Measurement Tool Combination Framework
## About the project:
This is a MSc Thesis Project that explored the estimation of the energy consumption of the Privacy-Enhancing Technologies (PET), as well as privacy risks and utility of the dataset after PET treatment. The estimation is based on the dataset properties, which is used by Gradient Boosting Model. 
..


## Requirements <a name="requirements"></a>
Make sure your Python version is the following:<br>
Python 3.10.12 -  3.10.14 (pip 22.0 - 24.0)<br>

Run the following line from the terminal:<br>

`pip install -r requirements.txt`<br>


# Estimation Framework
### What input to provide?
1. Name of the csv file, that is in the `put_your_dataset_here` folder <br>
2. Attributes, that are categorical, but because of their numerical format, could be mistaken for continuous<br>
3. Target attribute <br>









# Validation Framework
Before launching the framework:<br>
It's necessary to clean your file.<br>
Plus, it's necessary to preprocess the target attribute for classification purposes.<br>
For other attributes, please do not modify them in a way, that would change their values. <br>
After synthetic data has been generated, the framework will apply MinMaxScaler and One-Hot encoding for ML tasks.<br>

<strong>Running on Terminal:</strong><br>
Linux (or WSL):<br>
`sudo python3 main_validation.py`*<br>

Windows:<br>
`runas /user:Administrator "python main_validation.py"`*<br>

MacOS:<br>
`sudo python3 main_validation.py`*<br>

<strong>Running on Jupyter Notebook:</strong><br>
`sudo jupyter notebook --allow-root`*<br>
Then, run the notebook, like you normally would.<br>

*<em>It is necessary to run with the administrator rights in order to perform all hardware measurements of energy consumption. Otherwise, it won't work.</em>

### What input to provide?
1. Name of the csv file, that is in the `put_your_dataset_here` folder <br>
2. Attributes, that are categorical, but because of their numerical format, could be mistaken for continuous<br>
3. Target attribute<br>

The Linkability and Inference risk measurements are disabled.



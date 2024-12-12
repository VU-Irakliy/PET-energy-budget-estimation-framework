# Framework for determining energy budget
This is the MSc project for my thesis that is dedicated to helping make the decision on energy budget.

For instructions, [press here!](#instructions)

## About the project:




## Instructions for usage
Make sure your Python version is the following:<br>
Python 3.10.12 -  3.10.14 (pip 22.0 - 24.0)<br>
%Install libomp1
Run the following line from the terminal:<br>

`pip install -r requirements.txt`<br>

Before launching the framework:<br>
It's necessary to clean your file.<br>
Plus, it's necessary to preprocess the target attribute for classification purposes.<br>
For other attributes, please do not modify them in a way, that would change their values. <br>
After synthetic data has been generated, the framework will apply MinMaxScaler and One-Hot encoding for ML tasks.<br>

<strong>Running on Terminal:</strong><br>
Linux (or WSL):<br>
`sudo python3 main.py`*<br>

Windows:<br>
`runas /user:Administrator "python main.py"`*<br>

MacOS:<br>
`sudo python3 main.py`*<br>

<strong>Running on Jupyter Notebook:</strong><br>
`sudo jupyter notebook --allow-root`*<br>
Then, run the notebook, like you normally would.<br>

### What input to provide?




*<em>It is necessary to run with the administrator rights in order to perform all hardware measurements of energy consumption. Otherwise, it won't work.</em>

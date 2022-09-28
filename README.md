# Current car prices and other relevant parameters from bazos.cz

## [Daniel Brosko](mailto:89227653@fsv.cuni.cz), [Vojtěch Suchánek](mailto:92048987@fsv.cuni.cz)

In this project, we scrape the bazos.cz website and collect recent car advertisements. Based on the user input (car brand, model, etc.), we filter all the recent advertisements, and get the price, milage, and the year of manufacture.

We found this to be useful filter, since there are over 15 thousand advertisements added every day, but there is no unified form for adding/providing the respective parameters that buyers are interrested in - hence, it is pretty time consuming and over the human power to check all of the advertisements.

Initially, based on the user input (usually brand and model specification), we get the number of relevant advertisements found. Then we run over all of the advertisement previews and collect their URLs + date when the particular adv. was added. In the next step, we filter out only the advertisements that were added in last few days - user is able to specify the number of recent days (1 to 5 days). Then, we follow the URL of each of the advertisements that match \"date-added\" condition, scrape its content, and use data-mining algorithm to get the milage (in km), year of manufacture, and price.

We save all those parameter, along with the respective URL, into a dataframe using pandas library.

## Which files are relavant in this repository?

The core of the project is Jupyter Notebook [final_project_submit.ipynb](https://github.com/Vojtas52/Python-project/blob/037af6a1e8ab453c98ce490891db56d40d1f02ff/final_project_submit.ipynb).

Then we also use two python scripts that contains functions that we have written, but to make the Jupyter Ntb. more concise, we saved them as separate files and we load them in the process - these scripts are [model_search.py](https://github.com/Vojtas52/Python-project/blob/037af6a1e8ab453c98ce490891db56d40d1f02ff/model_search.py) and [n_days_search.py](https://github.com/Vojtas52/Python-project/blob/037af6a1e8ab453c98ce490891db56d40d1f02ff/n_days_search.py).

Another relevant file is [requirements.txt](https://github.com/Vojtas52/Python-project/blob/3ecfddd04d22bbf45240c4e08cc9764e5b79e2ce/requirements.txt) which specifies packages/libraries that are required for running our project, and also [.gitignore](https://github.com/Vojtas52/Python-project/blob/d465bfc4f743c0c9cae26dcce547690954eb5273/.gitignore).

Apart from that (and the illustration displayed below), other files were used mainly during the project development as testing and debugging files, before putting it together into [final_project_submit.ipynb](https://github.com/Vojtas52/Python-project/blob/037af6a1e8ab453c98ce490891db56d40d1f02ff/final_project_submit.ipynb).

[UPDATE]
In further project development, we created a flask application - the source code is in [__main__.py](https://github.com/Vojtas52/Python-project/blob/a27758cef387553ca0a911c98756c0c0362e7708/__main__.py). Since there were some troubles with the obtaining responses from bazos.cz server on our requests, we solved this problem by creating [cache.py](https://github.com/Vojtas52/Python-project/blob/a27758cef387553ca0a911c98756c0c0362e7708/cache.py) that saves the responses that got through successfully (200). Also, the main part of the project that flask visualizes is in [templates/index.j2](https://github.com/Vojtas52/Python-project/blob/a98e3750847e787a42b21d7bb0c8f77ae763217a/templates/index.j2), where we list several of the ads and also some graphical comparison between Price vs Milage, and Year of Manufacture, respectively.

Also, we tried to make a code a little more readable - we put data-mining functions into [data_mining.py](https://github.com/Vojtas52/Python-project/blob/a27758cef387553ca0a911c98756c0c0362e7708/data_mining.py) script. What's more, we adjusted many lines to be more concise, efficient (e.g., when raising errors, or comparing the types of used variables) in the entire source code (even though I am sure it can still be done much better somehow).



[//]: <> (TO BE DONE: specify in which file is what, and etc. ... basically how to operate the .py script or jupyter ntb.)

![alt text](https://github.com/Vojtas52/Python-project/blob/1154eacc407364256ca560b80cddab04bb6b34ad/process_diagram.png)

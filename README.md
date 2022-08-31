# Getting current car prices and other relevant parameters from bazos.cz 

In this project, we scrape the bazos.cz website and collect recent car advertisements. Based on the user input (car brand, model, etc.), we filter all the recent advertisements, and get the price, milage, and the year of manufacture.

We found this to be useful filter, since there are over 15 thousand advertisements added every day, but there is no unified form for adding/providing the respective parameters that buyers are interrested in - hence, it is pretty time consuming and over the human power to check all of the advertisements.

Initially, based on the user input (usually brand and model specification), we get the number of relevant advertisements found. Then we run over all of the advertisement previews and collect their URLs + date when the particular adv. was added. In the next step, we filter out only the advertisements that were added in last few days - user is able to specify the number of recent days (1 to 5 days). Then, we follow the URL of each of the advertisements that match \"date-added\" condition, scrape its content, and use data-mining algorithm to get the milage (in km), year of manufacture, and price.

We save all those parameter, along with the respective URL, into a dataframe using pandas library.

TO BE DONE: specify in which file is what, and etc. ... basically how to operate the .py script or jupyter ntb.

![alt text](https://github.com/Vojtas52/Python-project/blob/c3b7dea95ff38be8ca3adabfa22066c54422db40/process_diagram.png)
from datetime import date, datetime, timedelta
import time

#FILTER for advertisements added in last n_days 
def n_days_search(n_days: int, soup_list : list[str]):
    """
    Function n_days_search behaves as a filter, and consider only the advertisements that have been added
    within the selected time range.
    
    It takes two arguments - n_days, and soup_list.
    The in_days should be integer from 0 to 5 - where 0 means no past days (just today),
    and the 5 means today and 5 days before.
    The soup_list is the list of html code where we will search for the advertisements
     - the output of search_model function.
    
    The date is scraped from each adv. source code, converted into datetime object and then challenged
    by condition based on input of n_days_search provided by user.
    
    Function returns list of URLs of all advertisements that satisfied the required condition,
    and prepared for further processing - scraping and data-mining of the desired parameters.
    """
    number_of_accepted_past_days = n_days #range (0:5) - if more,

    n_days = int(n_days) #TODO - co robit ked do input nedam cislo? 

    if not isinstance(n_days, int):
        raise TypeError('First argument (n_days) should be an integer. However, it is: '.type(n_days))

    if n_days > 5:
        raise ValueError('First argument (n_days) should be less than or equal to 5. Your input was:'.format(n_days))


    today = date.today()
    accepted_days = list()

    for i in list(range(0, min(number_of_accepted_past_days + 1, 6), 1)):
        i_days_ago = today - timedelta(days=i)
        accepted_days.append(i_days_ago)

    # by the following code, we get the urls of each advertisement /offer/ (listed in the tabs we work with),
    # and save it to "list_of_offers_url"
    list_of_offers_url = list()

    for element in soup_list:
        #print(f"{element=}")
        x = element.find_all('div', {'class':'inzeraty inzeratyflex'})

        for sub_element in x:
            y = sub_element.find('div', {'class':'inzeratynadpis'})
            attribute_a = y.find('a')
            w = attribute_a.get('href')
            attribute_span = y.find('span')

            #here we just obtain the date from the particular advertisement to make sure we analyze only ads added today
            date_str = str(attribute_span.text)
            date_str = date_str.replace(" ","")
            date_str = date_str.strip("-[]")
            date_str = date_str.strip("TOP-[]")
            date_object = datetime.strptime(date_str,'%d.%m.%Y')
            date_object = date_object.date()

            if not date_object in accepted_days:
                continue

            list_of_offers_url.append(f'https://auto.bazos.cz{w}')

    print(f'The number of found advertisements matching the criteria: {len(list_of_offers_url)}.')
    #logger / take a look on logging library

    return list_of_offers_url
import re

# firstly, we define the input variable so the user can search according to their preference
def search_model(user_input):
    """
    Function search_model takes string input, hence it has to be in quotes ("").
    The input should be the name of the car model you would like to get results for,
    e.g. "octávia 3" - there should be no problem even when full Czech alphabet is used.
    
    Then the string is stripped of the characters that are not supposed to be in the search input,
    and if there are more than single word in the input, they are connected by '+' (plus) sign,
    since that is the format that bazos.cz use in their URLs.
    
    Then, the prepared string is paste into the common URL format that bazos.cz use.
    
    The very next step is obtaining the number of found advertisements for user's input from the html source code.
    This number of advertisements is used to select the proper length of the adv. tabs list that we will scrape.
    
    The function returns "soup_list" - the list of html codes for each adv. tab that we process with function 
    n_days_search.
    """
    
    user_search_input = str(user_input)
    user_search_input = re.sub(r"[^\w\s]", '', user_search_input)
    user_search_input = re.sub(r"\s+", '+', user_search_input)

    no_of_adv_url = 'https://auto.bazos.cz/0/?hledat=' + user_search_input + '&hlokalita=&humkreis=25&cenaod=&cenado=&order='

    page = requests.get(no_of_adv_url)
    no_of_adv_html = BeautifulSoup(page.text, 'html')

    get_no_adv = no_of_adv_html.find('div', {'class':'listainzerat inzeratyflex'})
    get_no_adv = get_no_adv.find('div', {'class':'inzeratynadpis'})
    get_no_adv = get_no_adv.text
    get_no_adv = get_no_adv.split("z ")[-1]
    number_adv = get_no_adv.replace(" ","")
    number_adv = int(number_adv)
    # works properly, "number_adv" represents total number of advertisements for particular search input,
    # however, we modify it so that it correspondents correctly to the structure of page
    no_of_ad_lists = number_adv // 20
    if number_adv % 20 == 0:
        number_adv = no_of_ad_lists * 19
    else:
        number_adv = no_of_ad_lists * 20


    number_sequence = range(0, number_adv, 20) #start, stop (not included), step
    # we create empty list for saving the urls,
    # and then append other tabs with offers (since there are only 20 offers per tab by default)
    main_url_list = list()

    for i in range(0,len(number_sequence)):
        url = f'https://auto.bazos.cz/{number_sequence[i]}/'
        url = url + '?hledat=' + user_search_input + '&hlokalita=&humkreis=25&cenaod=&cenado=&order='
        main_url_list.append(url)
    # here we can check the list of urls for particular tabs
    #print(main_url_list)

    # in the next step, we get the text of each of those tabs using the BeautifulSoup function,
    # and save it as elements of the "soup_list"
    soup_list = list()
    for url in main_url_list:
        page = requests.get(url)

        ## MAYBE SLOW DOWN LATER by 0.3s per iteration
        soup_list.append(BeautifulSoup(page.text, 'html'))

    # filter to cut-off pseudo-empty elements in main_url_list to prevent the unwanted behaviour of the code
    res_soup_list = []
    for element in soup_list:
        if "html" in element:
            res_soup_list.append(element)
    soup_list = res_soup_list
    
    print("Initial search for your model successfully finished.")
    return soup_list
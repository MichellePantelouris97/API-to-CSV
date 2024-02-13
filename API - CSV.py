import requests
import csv

def get_content(): # define the function'
    api_url = 'https://content.guardianapis.com/search?section=politics&q=%22brexit%22' # api endpoint with api query
    payload = {
        'api-key': '128ebb73-cead-4d69-9243-542a238a4962', # api key
        'page-size': 200, # number of results returned
        'show-fields': 'wordcount', # return the wordcount for later
        'order-by': 'newest' # order of results by newest first
    }
    response = requests.get(api_url, params=payload) # calls the API with the payload from above
    data = response.json() # stores the request as a variable 'data' in json format so python can understand it

    # Extract relevant information from the response
    results = data.get('response', {}).get('results', [])
    if results: # if theres a response:
        with open('brexit.csv', 'w', newline='') as csvfile: # create a csv file 
            fieldnames = ['ID','Type','SectionID','SectionName','PubDate', 'Title','ApiURL','Is Hosted?','PillarID','Pillar Name','Wordcount', 'Web URL','Year','formatted_date'] # field names for the csv file
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames) # setup the csv file
            writer.writeheader() # write the headers

            for result in results:# for every result in the results
                wordcount = result.get('fields', {}).get('wordcount', 0) # get the wordcount
                wordcount=int(wordcount) # convert the wordcount to an integer 
                web_url = result.get('webUrl', '') # grabbing the fields in the API request and preparing to write
                ID = result.get('id')
                Type = result.get('type')
                SectionID = result.get('sectionId')
                SectionName = result.get('sectionName')
                PubDate = result.get('webPublicationDate')
                Title = result.get('webTitle')
                APIURL = result.get('apiUrl')
                Hosted = result.get('isHosted')
                PillarID = result.get('pillarId')
                PillarName = result.get('pillarName')
                year = PubDate[0:4] # string slicing 
                fdate = PubDate[8:10]+('/')+PubDate[5:7]+('/')+PubDate[0:4] # slicing/formatting of string
                
                if wordcount > 1000: # only write the data if the 'wordcount' value is above 1000 

                    # write to the file 
                    writer.writerow({'ID': ID, 'Type': Type, 'SectionID': SectionID, 'SectionName': SectionName,
                                 'PubDate': PubDate, 'Title': Title, 'ApiURL':APIURL, 'Is Hosted?':Hosted, 'PillarID':PillarID, 'Pillar Name': PillarName,
                                     'Wordcount': wordcount, 'Web URL': web_url,'Year':year, 'formatted_date':fdate})

        print("Data has been written!")
    else:
        print(":error!:")

get_content() # calls the function

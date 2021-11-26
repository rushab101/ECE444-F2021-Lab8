import requests
import time
from prettytable import PrettyTable

url = "http://lab8-env.eba-cbgftieq.eu-west-1.elasticbeanstalk.com/news"


#Response == 1 --> Article is fake
#Response == 0 --> Article is real

test_cases = [
    {
        "Test Input": "Emperor of Mars has declared war on Earth",
        "Expected Response": 1  
        
    },
    {
        "Test Input": "The Trump campaign has confirmed to Hannity.com that Mr. Trump did indeed send his plane to make two trips from North Carolina to Miami, \
            Florida to transport over 200 Gulf War Marines back home.",
        "Expected Response": 1  

    },
    {
        #URL for Article = https://www.thestar.com/politics/provincial/2021/11/25/students-need-to-get-back-in-the-classroom-ontarios-minister-of-colleges-and-universities-says.html
        "Test Input": "Students need to have classes on campus and the Ontario government is working with post-secondary schools \
                “to provide support for institutions as they prepare for winter 2022 to safely reopen,” \
                says Colleges and Universities Minister Jill Dunlop.",
        "Expected Response": 0  
    },
    {
        #URL for article = https://www.thestar.com/news/canada/2021/11/25/covid-19-coronavirus-updates-toronto-canada-november-25.html
        "Test Input": "A new coronavirus variant has been detected in South Africa that scientists say is a concern because of its high number of mutations \
                and rapid spread among young people in Gauteng, the country’s most populous province, \
                Health Minister Joe Phaahla announced Thursday",
        "Expected Response": 0  
    }   
]


def predict_news(text):
    text = "{\n\t\"text\": \"" + text + "\"\n}"
    headers = {
        'Content-Type': "application/json"
    }
    response = requests.request("GET", url, data=text.encode('utf-8'), headers=headers)
    return response.json()

def run_time(text):
    start = time.time()
    for i in range(100):
        predict_news(text)
    time_elapsed = time.time() - start
    return round(time_elapsed / 100,2)*1000

def main():
    for i,test in enumerate(test_cases):
        table = PrettyTable(["Test Case #" , str(i+1)])
        current_text = test['Test Input']
        remove_tabs = current_text.split()
        table.add_row(["Test Input", " " .join(remove_tabs)])
        table.add_row(["Expected Response", test['Expected Response']])
        table.add_row(["Actual Response", predict_news(test['Test Input']).split(':')[1]])
        table.add_row(["Average Latency Over 100 Calls", str(run_time(test['Test Input'])) + " ms"])
        print(table)
        print()
    


if __name__ == "__main__":
    main()
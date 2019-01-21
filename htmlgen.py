# python default imports
import requests, json,sys,math

# project related imports
import location,weather,news
#setting up logging info
import log
from datetime import datetime, timezone
from pathlib import Path


log_handle=log.setup()

html_header1 = '<!DOCTYPE html><html><head><meta name="viewport"  \
content="width=device-width, initial-scale=1.0"><style>* \
{  box-sizing: border-box;}.row::after {  content: "";  \
clear: both;  display: table;}[class*="col-"] {float: left;padding: 15px;} \
.col-1 {width: 8.33%;} \
.col-2 {width: 16.66%;} \
.col-3 {width: 25%;}\
.col-4 {width: 33.33%;}\
.col-5 {width: 41.66%;}\
.col-6 {width: 50%;}\
.col-7 {width: 58.33%;}\
.col-8 {width: 66.66%;}\
.col-9 {width: 75%;}\
.col-10 {width: 83.33%;}\
.col-11 {width: 91.66%;}\
.col-12 {width: 100%;}\
\
html {\
  font-family: "Lucida Sans", sans-serif;\
}\
\
.header {\
  background-color: #9933cc;\
  color: #ffffff;\
  text-align: center;\
  padding: 15px;\
}\
\
.menu ul {\
  list-style-type: none;\
  margin: 0;\
  padding: 0;\
}\
\
.menu li {\
  padding: 8px;\
  margin-bottom: 7px;\
  background-color: #33b5e5;\
  color: #ffffff;\
  box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);\
}\
\
.menu li:hover {\
  background-color: #0099cc;\
}'
html_header = '<!DOCTYPE html><html lang="en"><head><title>CSS Template</title><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><style> \
* {  box-sizing: border-box;}body {  font-family: Arial, Helvetica, sans-serif;}/* Style the header */header {  background-color: #666;  padding: 30px;  text-align: center; \
font-size: 35px;  color: white;}/* Create two columns/boxes that floats next to each other */nav {  float: left;  width: 30%; \
  background: #ccc;  padding: 20px;}/* Style the list inside the menu */ \
nav ul {  list-style-type: none;  padding: 0;}article {  float: left;  padding: 20px;  width: 70%;  background-color: #f1f1f1; \
}/* Clear floats after the columns */section:after {  content: "";  display: table;  clear: both;} \
/* Style the footer */ footer { background-color: #777; padding: 10px; text-align: center; color: white;} \
/* Responsive layout - makes the two columns/boxes stack on top of each other instead of next to each other, on small screens */ \
@media (max-width: 600px) { nav, article {   width: 100%;  height: auto;}}'

def save_file(html,name):
    data_folder = Path("output/")

    file_to_open = data_folder / name
    with open(file_to_open, 'w') as file:
        file.write(html)
    
def make_url_tag(url,title):
    #<a href="url">link text</a>
    # <li><a href="#">London</a></li>
    return '<li><a href="%s">%s</a></li>' % (url,title)
def make_url_tags(urls,titles):
    html_string = '<div class="row"><div class="col-3 menu"><h1>Top News</h1><ul>'
    for u,t in zip(urls,titles):
        html_string = html_string + make_url_tag(u,t)
    return html_string + "    </ul> </div>"
def builder_header(city):
    return '</style></head><body><div class="header"><h1>%s</h1></div>' %(city)
def get_news_urls_titles(data):
    urls = []
    titles = []
    for a in data['articles']:
        titles.append(a['title'])
        urls.append(a['url'])
    return urls,titles
def remove_tag(html):
    return html[4:-5]
def build_news_section(data):
    urls,titles = get_news_urls_titles(data)
    return make_url_tags(urls,titles)
def change_to_f(degree):
    #(0K − 273.15) × 9/5 + 32 = -459.7°F
    ans = ((degree) - 273.15) * 9/5 + 32
    return round(ans,3)
def addimage(word):
    #http://openweathermap.org/img/w/10d.png
    #<img src="http://openweathermap.org/img/w/%s.png" alt="Trulli" width="500" height="333" %(word)>

    return  '<img src="http://openweathermap.org/img/w/% s.png" >' %(word)
def build_current_weather(data):
    html_string ='<div class="col-9"> <h1>Current Weather</h1>'
    for key in data['main'].keys():
        if 'temp' in key:
            html_string = html_string + '<p>' + str(key) + " (F) : " + str(change_to_f(data['main'][key])) +  '</p>'
        else:
            html_string = html_string + '<p>' + str(key) + " : " + str(data['main'][key]) +  '</p>'
    html_string = html_string +  '<p>' + 'weather : ' + str(data['weather'][0]['main']) + addimage(data['weather'][0]['icon']) + '</p>'
    sunrise = data['sys']['sunrise'] 
    sunset = data['sys']['sunset'] 
    formatsunrise=datetime.fromtimestamp(sunrise) 
    formatsunset = datetime.fromtimestamp(sunset)
    html_string = html_string +  '<p>' + 'sunrise : ' + str(formatsunrise) + '</p>'
    html_string = html_string +  '<p>' + 'sunset : ' + str(formatsunset) + '</p>'
    return html_string + '</div>'
def num_to_day(num):
    days = ["Mon","Tue","Wed","Thur","Fri","Sat","Sun"]
    return days[num]


def build_weather_map(url):
    html_string = ""
    html_string = '<div class="col-8"><h1>' + remove_tag(make_url_tag(url,'Weather Map')) + '</h1>'
    return html_string
def build_forecast(data):
    html_string ='<div class="col-9"><h1>5 day Forecast</h1><title>Forecast</title><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css"><body>'
    #html_string = html_string + '<div class="w3-container w3-red w3-cell">'
    new_row = False
    old_date = None
    color = 'red'
    for d in data['list']:
        if old_date !=(d['dt_txt'].split(' ')[0].split('-')[2]):
            
            if new_row:
                html_string = html_string +  '</div>'
                if color == 'red':
                    color = 'green'
                else:
                    color = 'red'

            new_row = True
            formatdate=datetime.fromtimestamp(d['dt']+ 50000)
            day_of_week=formatdate.weekday()
            html_string = html_string + '<div class="w3-container w3-%s w3-cell"><h1>%s</h1>' %(color,num_to_day(day_of_week))
        old_date = (d['dt_txt'].split(' ')[0].split('-')[2])
        html_string = html_string + '<p> temp (F) : '+ str(change_to_f(d['main']['temp'])) + addimage(d['weather'][0]['icon'])  + str(d['dt_txt'].split(' ')[-1]) + '</p>'
                                                                                                             
        
    return html_string + '</div>'
def main():
    city = None
    name = None
    #pass no args to use the ip of the machine running this pass extra args and it will
    # default to Brentwood
    if len(sys.argv) == 3:
        loc = sys.argv[1]
        if loc == 'local':
            name = 'local_test.html'
            city = location.get_location_by_ip()
        elif loc == 'default':
            city=location.get_location()
            name = 'brentwood_test.html'
        else:
            print('usage:\n python htmlgen.py local newsapikey\n python htmlgen.py default newsapikey\n')
            sys.exit(0)
        newsapi =sys.argv[2]
        try:
             news_data = news.build_url_call(None,newsapi)
        except:
            print('bad key try again')
            sys.exit(1)
                  
                  
            
            
            
        
         
      
       
       
    
        
    else:
        print('usage:\n python htmlgen.py local newsapikey\n python htmlgen.py default newsapikey\n')
        sys.exit(0)
       
    current_weather=weather.get_current_weather(city=city)
    forecast=weather.get_forecast(city=city)
   
    x,y = weather.get_coord( current_weather)
    weather_url=weather.get_map_url(y,x)
    # get the top headline news
    url = news.build_url_call(None,newsapi)
    news_data = news. get_data(url)
    html = html_header1 +  builder_header(city) + build_news_section(news_data) +  build_current_weather(current_weather) +  build_forecast(forecast) +  build_weather_map(weather_url)
    save_file(html,name)
main()


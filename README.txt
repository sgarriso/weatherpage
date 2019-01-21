This project creates an HTML page to get the current weather. you may supply a location or it will use your ip address to guess your location. 
in order for this app to work you will need to install geocoder
sources:
https://newsapi.org/
https://geocoder.readthedocs.io/api.html#house-addresses for gecoder
https://www.geeksforgeeks.org/python-find-current-weather-of-any-city-using-openweathermap-api/ (for weather api)
the command below will create an html file called local_test.html it will be stored in a folder called output
python htmlgen.py local apinewskey
the command below will create an html file called brentwood_test.html and it will be stored in a folder called output
python htmlgen.py default apinewskey
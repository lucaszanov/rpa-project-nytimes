# rpa-project-nytimes
Automation to extract informations from news in NY Times website.

Your challenge is to automate the process of extracting data from the news site. Link to the news site: [www.nytimes.com](http://www.nytimes.com/)

You must have 3 configured variables (you can save them in the configuration file, but it is better to put them to the Robocorp Cloud [Work Items](https://robocorp.com/docs/libraries/rpa-framework/rpa-robocorp-workitems/keywords#get-work-item-variable)):

- search phrase
- news category or section
- number of months for which you need to receive news
    
    > Example of how this should work: 0 or 1 - only the current month, 2 - current and previous month, 3 - current and two previous months, and so on
    > 

The main steps:

1. Open the site by following the link
2. Enter a phrase in the search field
3. On the result page, apply the following filters:
    - select a news category or section
        
        > your automation should have the option to choose from none to any number of categories/sections. This should be specified via the config file or/and Robocorp Cloud Work Items
        > 
    - choose the latest (i.e., newest) news
4. Get the values: title, date, and description.
5. Store in an Excel file:
    - title
    - date
    - description (if available)
    - picture filename
    - count of search phrases in the title and description
    - True or False, depending on whether the title or description contains any amount of money
    
    >    Possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD
    > 
6. Download the news picture and specify the file name in the Excel file
7. Follow steps 4-6 for all news that falls within the required time period

# Project structure
The project is divided in three folders:
<ul>
<li><code>config</code>: configuration files;</li>
<li><code>outputs</code>: output folders generated using current datetime for unique folders
and containing the Excel file, a log file and the images folder with all images
downloaded;</li>
<li><code>src</code>: folder containing all scripts</li>
</ul>

# Libraries
Main libraries used in this project (also available in <code>requirements.txt</code>):
- openpyxl==3.1.2
- pandas==2.0.2
- selenium==4.9.1
- tqdm==4.65.0
- urllib3==2.0.2
- webdriver-manager==3.8.6

Python version: 3.11

# Configuration file
The <code>config.ini</code> file is located in the <code>config</code> folder
and contains all the configuration parameters divided by section:

<ul>
<li>website_parameters: URLs, xpaths, ids and parameters related to the 
website <url>http://www.nytimes.com</url>;</li>
<li>input_parameters: the configured variables by user:
    <ul>
        <li>search phrase: must be separated by space;</li>
        <li>news category or section: must be a list, eg: [Books,Fashion,Movies,Opinion,U.S.];</li>
        <li>number of months for which you need to receive news: must be an integer</li>
    </ul></li>
<li>browser_parameters: basically the chrome version;</li>
<li>general_parameters: folders path, time to wait on clicks and
regex structures</li>
</ul>

# Future improvements
- Generate an .exe file to be more user-friendly with a Tkinter Interface;
- Use Docker to ensure functional application in other environments;
- Improve exception handling in code to avoid robot crashes.
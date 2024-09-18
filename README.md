UD Webscraper

This project is a web scraper built using Selenium and Python that logs into the Underdog Fantasy website to extract MLB strikeout projections. The scraper navigates through the website, gathers player names and strikeout values, and saves the extracted data into a CSV file. It sorts the strikeout lines neatly in the CSV.

Features:

Automates login to the Underdog Fantasy website.
Extracts MLB player names and their strikeout projections.
Organizes and sorts the extracted data in a CSV file.
Uses Selenium for web scraping and pandas for data handling.

Requirements:

Python 
Selenium
pandas
Microsoft Edge WebDriver (or preferred webdriver)

Download Edge WebDriver:

Download the appropriate WebDriver for your version of Microsoft Edge from here.
Extract the downloaded WebDriver and update the edge_driver_path in the script to point to the location of msedgedriver.exe.

Update Credentials:

Open the script file and update the login credentials with your Underdog Fantasy account's email and password.

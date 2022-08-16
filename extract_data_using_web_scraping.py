
# Install the required modules and functions
! wget -O miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-py37_4.10.3-Linux-x86_64.sh
! chmod +x miniconda.sh
! bash ./miniconda.sh -b -f -p /usr/local
! rm miniconda.sh
! conda config --add channels conda-forge
! conda install -y mamba
! mamba update -qy --all
! mamba clean -qafy
import sys
sys.path.append('/usr/local/lib/python3.7/site-packages/')

# Import the required modules and functions
from bs4 import BeautifulSoup
import html5lib
import requests
import pandas as pd

# Extract Data Using BeautifulSoup
response = requests.get("https://en.wikipedia.org/wiki/List_of_largest_banks")
html_data = response.content

html_data[101:124]

soup = BeautifulSoup(html_data, "html5lib")

#Getting some error because of \n and [6]
data = pd.DataFrame(columns=["Name", "Market Cap (US$ Billion)"])

for row in soup.find_all('tbody')[3].find_all('tr'):
    col = row.find_all('td')
    if col:
        bank_name = col[1].find_all("a")[1].text
        market_cap = float(col[2].text)
        data = data.append({"Name": bank_name,
                            "Market Cap (US$ Billion)": market_cap},
                           ignore_index=True)

data.head()

# Extract and Load Data Using Pandas
data = pd.read_html("https://en.wikipedia.org/wiki/List_of_largest_banks", header=0, flavor='bs4')[3]
data = data[["Bank name", "Market cap(US$ billion)"]]

data.to_json('bank_market_cap.json')
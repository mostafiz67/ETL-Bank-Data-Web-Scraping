# Required Packages
#!mamba install pandas==1.3.3 -y
#!mamba install requests==2.26.0 -y

# Imports
import glob
import pandas as pd
from datetime import datetime

# As the exchange rate fluctuates, we will download the same dataset to make marking simpler. This will be in the same format as the dataset you used in the last section
!wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0221EN-SkillsNetwork/labs/module%206/Lab%20-%20Extract%20Transform%20Load/data/bank_market_cap_1.json
!wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0221EN-SkillsNetwork/labs/module%206/Lab%20-%20Extract%20Transform%20Load/data/bank_market_cap_2.json
!wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0221EN-SkillsNetwork/labs/module%206/Final%20Assignment/exchange_rates.csv

# Extract
#JSON Extract Function
# This function will extract JSON files.

def extract_from_json(file_to_process):
    dataframe = pd.read_json(file_to_process)
    return dataframe

"""## 
Define the extract function that finds JSON file `bank_market_cap_1.json` and calls the function created above to extract data from them. Store the data in a `pandas` dataframe. Use the following list for the columns.
"""
columns=['Name','Market Cap (US$ Billion)']
market_cap_file = 'bank_market_cap_1.json'
exchange_rate_file = 'exchange_rates.csv'
load_to_file = 'bank_market_cap_gbp.csv'

def extract(market_cap_file):
    extracted_data = pd.DataFrame(columns=columns)
    
    #process the json files
    extracted_data = extracted_data.append(extract_from_json(market_cap_file), ignore_index=True)
    
    return extracted_data

# Write your code here
exchange_rate_data = pd.read_csv("exchange_rates.csv", index_col=0)
# exchange_rate = exchange_rate_data.at["GBP", "Rates"]
exchange_rate = exchange_rate_data.loc["GBP"].at["Rates"]
exchange_rate

# Transform
def transform(extracted_df, exchange_rate):
    # Write your code here
    transformed_df = extracted_df.rename(columns={"Market Cap (US$ Billion)": "Dollar"})
    transformed_df["Dollar"] = round(transformed_df.Dollar * exchange_rate)
    transformed_df = transformed_df.rename(columns={"Dollar": "Market Cap (GBP$ Billion)"})
    
    return transformed_df

# Load
def load(df_to_load, filename):
    # Write your code here
    df_to_load.to_csv(filename)

# Logging Function
def log(message):
    # Write your code here
    timestamp_format = '%d-%h-%Y-%H:%M:%S'
    time = datetime.now()
    timestamp = time.strftime(timestamp_format)
    with open("logfile.txt", "a") as f:
        f.write(f'{timestamp}, {message}\n')

# Running the ETL Process

log('ETL Job Started')
log('Exract Phase Started')


# Call the function here
extracted_data = extract(market_cap_file)

# Print the rows here
extracted_data

log('Extract Phase Ended')
log('Transform Phase Started')
transformed_data = transform(extracted_data, exchange_rate)
transformed_data.head()
log('Transform phase Ended')
log('Load phase Started')
load(transformed_data, load_to_file)
log('Load phase Ended')

"""## 

Copyright © 2020 IBM Corporation. This notebook and its source code are released under the terms of the [MIT License](https://cognitiveclass.ai/mit-license?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkPY0221ENSkillsNetwork23455645-2022-01-01&cm_mmc=Email_Newsletter-\_-Developer_Ed%2BTech-\_-WW_WW-\_-SkillsNetwork-Courses-IBM-DA0321EN-SkillsNetwork-21426264&cm_mmca1=000026UJ&cm_mmca2=10006555&cm_mmca3=M12345678&cvosrc=email.Newsletter.M12345678&cvo_campaign=000026UJ).
"""
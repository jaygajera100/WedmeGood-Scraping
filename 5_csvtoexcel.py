import pandas as pd
import numpy as np


# Reading the csv file
with open('city.txt') as f:
    cities = f.readlines()
    cities = [x.strip() for x in cities]
    for y in cities:
        file_name = f'All_done\\{y}.csv'

        df_new = pd.read_csv(file_name)

        # saving xlsx file
        GFG = pd.ExcelWriter(f'All_excel\\{y}.xlsx')
        df_new.to_excel(GFG, index=False)

        GFG.save()

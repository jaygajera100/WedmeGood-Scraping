import pandas as pd

with open('city.txt') as f:
    cities = f.readlines()
    cities = [x.strip() for x in cities]
    for x in cities:
        city = f"specific_city\\{x}.csv"
        df = pd.read_csv(city, encoding='ISO-8859-1')
        df['Email_id'] = ''
        df['Contact'] = ''
        df['Instagram Link'] = ''
        df['Facebook Link'] = ''
        df['Website Link'] = ''

        df.head()
        attach = f"new\\{x}.csv"
        df.to_csv(attach, index=False)


# file_name = 'new\\ahmedabad.csv'
# df = pd.read_csv(file_name)
# photographer = list(df['Photography'])

# print(photographer)

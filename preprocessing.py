import pandas as pd

df = pd.read_csv(r'C:\Users\HP\Downloads\startup_funding.csv')
print(df)
df.drop(columns=['Remarks'], inplace=True)
df.head()

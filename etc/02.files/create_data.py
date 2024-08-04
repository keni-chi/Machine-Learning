import pandas as pd
import random


random.seed(0)
row_length = 100
dataframe_dict = {
    "x1":[ random.randint(0,10) for i in range(row_length) ],
    "x2":[ random.randint(0,10) for i in range(row_length) ],
    "x3":[ random.randint(0,10) for i in range(row_length) ]
}
df = pd.DataFrame(dataframe_dict)
print(df)
df["y"] = df["x1"] + df["x2"] + df["x3"] + [ random.normalvariate(mu=0,sigma=1) for i in range(row_length) ]
print(df)

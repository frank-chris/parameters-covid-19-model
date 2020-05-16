import pandas as pd
import os

folder = "data/"

files = os.listdir(folder)

print("\n", len(files), " files found\n")

states = pd.read_csv(folder + files[0],  delimiter=" ", header=1)

del states["Day"]

states = states.columns

errors = pd.DataFrame(index=files, columns = states)
errors.fillna(0, inplace=True)

state_wise_daily = pd.read_csv('state_wise_daily.csv')
del state_wise_daily["DN"]
del state_wise_daily["DD"]
del state_wise_daily["ML"]
del state_wise_daily["MZ"]
del state_wise_daily["NL"]

# Rename column TT as Total
state_wise_daily.rename(columns={"TT" : "Total"}, inplace=True)

# Move the column Total to the end
column_total = state_wise_daily.pop("Total") 
state_wise_daily["Total"] = column_total

state_wise_daily = state_wise_daily[state_wise_daily.Status == "Confirmed"]
del state_wise_daily["Status"]
del state_wise_daily["Date"]
state_wise_daily["index"]=[i for i in range(len(state_wise_daily.index))]
state_wise_daily.set_index("index", inplace = True)

for i in range(1,len(state_wise_daily.index)):
    for column in state_wise_daily.columns:
        state_wise_daily.loc[i, column] += state_wise_daily.loc[i-1, column]

state_wise_daily = state_wise_daily.iloc[9:]
state_wise_daily["index"]=[i for i in range(len(state_wise_daily.index))]
state_wise_daily.set_index("index", inplace = True)


for file in files:
    df = pd.read_csv(folder + file,  delimiter=" ", header=1)
    for state in states:
        error_count = 0
        for i in range(min(len(state_wise_daily.index),len(df.index))):
            error_count += (state_wise_daily.loc[i, state] - df.loc[i, state])*(state_wise_daily.loc[i, state] - df.loc[i, state])
        errors.loc[file, state] = error_count


errors = errors.append(errors.idxmin(axis=0), ignore_index=True)

best_parameters = pd.DataFrame()
best_parameters["state"] = list(errors.columns)
best_parameters["file"] = list(errors.iloc[-1])

best_parameters.to_csv('best_parameters.data', sep=" ", index=False)

print("\nData written to best_parameters.data\n")
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm
import folium

from folium import plugins

file1 = "review.json"
file2 = "business.json"
cols1 = ["business_id","date"]
cols2 = ["business_id","name","city","neighborhood","latitude","longitude"]

data1 = []
data2 = []
# read in the review data
with open(file1, 'r') as f:
    for line in f:
        selected_info = []
        lines = json.loads(line)
        for item in cols1:
            selected_info.append(lines[item])
        data1.append(selected_info)

# read in the business data
with open(file2, 'r') as f:
    for line in f:
        selected_info = []
        lines = json.loads(line)
        for item in cols2:
            selected_info.append(lines[item])
        data2.append(selected_info)

# save the data used in this analysis: business ID and data, to dataframe.
review_date = pd.DataFrame(data1,columns = cols1)
review_date['date'] = pd.to_datetime(review_date['date'])

new_df = review_date.groupby(["business_id",review_date.date.dt.year]).size().to_frame(name = 'count').reset_index()
df_table = pd.pivot_table(new_df,values='count',index=['business_id'],columns=['date'])
df_table.reset_index(inplace=True)

# save the data used in this analysis: "business_id","name","city","neighborhood","latitude","longitude"
# to dataframe.
yelp_business = pd.DataFrame(data2, columns = cols2)
PGH = yelp_business[yelp_business['city'] == "Pittsburgh"]

# Combine these two data frames together
df_combo = pd.merge(PGH,df_table,how = 'left', on ='business_id')
df_combo['Count Total']= df_combo.iloc[:,6:20].sum(axis=1)
df_combo.loc['Year Total'] = pd.Series(df_combo.iloc[:,6:21].sum(axis=0))

# Plot 1: showing the number of reviews increases dramatically for Pittsburgh's businesses.
df_combo.columns
df_combo.columns.get_loc(2004)
df_combo.columns.get_loc(2017)
plt.plot(df_combo.columns[6:20], df_combo.loc["Year Total"][6:20],linestyle='--', marker='o', color='r')
plt.xlabel("Year")
plt.ylabel("Number of Reviews")
plt.title('Pittsburgh Review Summary')
#plt.show()
plt.savefig("annual_review_count.png")


# Plot 2: interactive map of Pittsburgh businesses with yelp reviews since 2004.
pgh_map = folium.Map(location=[40.4, -80], zoom_start=11)
marker_cluster = folium.MarkerCluster().add_to(pgh_map)
for each in df_combo.iloc[:-1].iterrows():
    folium.CircleMarker([each[1]["latitude"], each[1]["longitude"]], popup=each[1]["name"],
                        radius = each[1]["Count Total"], color='crimson').add_to(marker_cluster)

pgh_map.save('pittsburgh_business.html')
pgh_map

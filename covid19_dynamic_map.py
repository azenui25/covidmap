# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 15:47:21 2020

@author: Asanga Nicholas
"""
import pandas as pd
import geopandas as gpd
import PIL
import io
# reading the csv data
data = pd.read_csv('time_series_covid19_confirmed_global.csv')

# group data by country
data=data.groupby('Country/Region').sum()

# Drop latitude and longitude colomns
data = data.drop(columns = ['Lat', 'Long'])

# create a transpose of the data frame
data_transposed = data.T
data_transposed.plot(y = ['Australia', 'Cameroon', 'Germany', 'Spain'], use_index = True,
                         figsize =(6,6))

# read in the world shapefile
world = gpd.read_file(r'E:/COVID-19-master/World_Map.shp')

world.replace('Viet Nam', 'Vietnam', inplace = True)
world.replace('Brunei Darussalam', 'Brunei', inplace = True)
world.replace('Cape Verde', 'Cabo Verde', inplace = True)
world.replace('Democratic Republic of the Congo', 'Congo (Kinshasa)', inplace = True)
world.replace('Congo', 'Congo (Brazzaville)', inplace = True)
world.replace('Czech Republic', 'Czechia', inplace = True)
world.replace('Swaziland', 'Eswatini', inplace = True)
world.replace('Iran (Islamic Republic of)', 'Iran', inplace = True)
world.replace('Korea, Republic of', 'Korea, South', inplace = True)
world.replace("Lao People's Democratic Republic", 'Laos', inplace = True)
world.replace('Libyan Arab Jamahiriya', 'Libya', inplace = True)
world.replace('Republic of Moldova', 'Moldova', inplace = True)
world.replace('The former Yugoslav Republic of Macedonia', 'North Macedonia', inplace = True)
world.replace('Syrian Arab Republic', 'Syria', inplace = True)
world.replace('Taiwan', 'Taiwan*', inplace = True)
world.replace('United Republic of Tanzania', 'Tanzania', inplace = True)
world.replace('United States', 'US', inplace = True)
world.replace('Palestine', 'West Bank and Gaza', inplace = True)

#merging data with world map
merge = world.join(data, on = 'NAME', how = 'right')

image_frames = []


for dates in merge.columns.to_list()[2:143]:


 # Plot 
    ax = merge.plot(column = dates, 
                    cmap = 'OrRd', 
                    figsize = (8,8), 
                    legend = True,
                    scheme = 'user_defined', 
                    classification_kwds = {'bins':[10, 20, 50, 100, 500, 1000, 5000, 10000, 500000]}, 
                    edgecolor = 'black',
                    linewidth = 0.4)
    
    # Add a title to the map 
    ax.set_title('Total Confirmed Coronavirus Cases: '+ dates, fontdict = 
                 {'fontsize':20}, pad = 12.5)
    
    # Removing the axes
    ax.set_axis_off()
    
    # Move the legend 
    ax.get_legend().set_bbox_to_anchor((0.18, 0.6))
    
    img = ax.get_figure()
    
    f = io.BytesIO()
    img.savefig(f, format = 'png', bbox_inches = 'tight')
    f.seek(0)
    image_frames.append(PIL.Image.open(f))


# Create a GIF animation 
image_frames[0].save('Dynamic COVID-19 Map.gif', format = 'GIF',
            append_images = image_frames[1:], 
            save_all = True, duration = 300, 
            loop = 3)

f.close()



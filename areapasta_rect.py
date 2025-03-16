import os
import math
import numpy as np
from PIL import Image


def Get_ar(file):
    im = Image.open(file)
    if im.mode == 'P' or im.mode == 'PA':
        im = im.convert()
    ar = np.asarray(im)
    return ar

def Get_File():
    path = ''#os.path.join(os.path.dirname(__file__), '')   #messes with the .exe version, not sure it's even necessary
    while True:
        filen = path + input('Equirectangular image filename: ')
        if os.path.exists(filen):
            try:
                ar = Get_ar(filen)
                tot_area = float(input('Total map area (any unit, input 0 to skip): '))
                return ar, tot_area
            except:
                print('Failed to load file, try again')
        else:
            print('File not found, try again')

def Find_Areas(in_map):
    if isinstance(in_map, str):
        in_map = Get_ar(in_map) #find array if passed filepath directly
    res = in_map.shape

    #get map of pixel arrays
    lat = np.linspace(-math.pi/2 + math.pi/res[0], math.pi/2 - math.pi/res[0], res[0])  #latitudes
    area = np.cos(lat)  #cosine correction for area
    area = area * 100 / (np.sum(area) * res[1]) #convert to percent of total area
    area = np.broadcast_to(np.expand_dims(area,1), (res[0],res[1]))   #broadcast to map shape

    col_val = []    #array of colors in map
    col_per = []    #array of color percents
    
    for idx in np.ndindex(res[:2]): #iterate over maps first 2 dimensions
        if len(res) > 2:
            col = tuple(in_map[idx])
        else:
            col = in_map[idx]
        if col not in col_val:  #if color not already found, add it and start counting area
            col_val.append(col)
            col_per.append(area[idx])
        else:                   #if color has been found, increase area count
            col_i = col_val.index(col)
            col_per[col_i] = col_per[col_i] + area[idx]

    return col_val, col_per

def To_Text(col_val, col_per, tot_area=0):
    col_val_t = [str(val) for val in col_val]
    max_len = 10 #always at least 10 characters for proper spacing
    for val in col_val_t:
        max_len = max(max_len, len(val))    #fnd maximum length of color string
    if tot_area > 0:
        max_per_len = 10
        for per in col_per:
            max_per_len = max(max_per_len, len(str(per)))
        
        
    lines = [f'Found {len(col_val)} colors',
             '  Color' + ' ' * (max_len) + 'Area (%)']
    if tot_area > 0:
        lines[1] = lines[1] + ' ' * (max_per_len - 3) + 'Area (units)'
    
    for val, per in zip(col_val_t, col_per):
        line = (val + ' ' * (max_len + 5 - len(val)) + str(per))
        if tot_area > 0:
            line = line + ' ' * (max_per_len + 5 - len(str(per))) + str(per*tot_area/100)
        lines.append(line)
    return lines


if __name__ == "__main__":
    in_map, tot_area = Get_File()
    print('Finding areas...')
    col_val, col_per = Find_Areas(in_map)
    lines = To_Text(col_val, col_per, tot_area)
    for l in lines:
        print(l)
    maketxt = input('Print to text? (y/n): ')
    if 'y' in maketxt or 'Y' in maketxt or '1' in maketxt:
        print('Writing to area_counts.txt...')
        f = open('area_counts.txt', 'w')
        f.writelines(['\n' + l for l in lines])
        f.close()
    maketxt = input('Print to csv? (y/n): ')
    if 'y' in maketxt or 'Y' in maketxt or '1' in maketxt:
        print('Writing to area_counts.csv...')
        lines = []
        for val,per in zip(col_val, col_per):
            valt = str(val)
            valt = valt.replace('(','')
            valt = valt.replace(')','')
            line = ('\n'+valt+','+str(per))
            if tot_area > 0:
                line = line + ',' + str(per*tot_area/100)
            lines.append(line)
        f = open('area_counts.csv', 'w')
        f.writelines(lines)
        f.close()
    a = input('Done; press enter to close')
    
    
        



    
    
        

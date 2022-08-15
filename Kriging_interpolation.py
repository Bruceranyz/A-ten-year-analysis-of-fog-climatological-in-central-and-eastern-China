# -*- codeing = utf-8 -*-
# @Time : 2022/8/15 19:25
# @Author : Ranyinze
# @File : Kriging_interpolation.py.py
# @Software: PyCharm

import pandas as pd, os, h5py
import numpy as np, time
from pykrige.ok import OrdinaryKriging
import datetime
import plotnine
from plotnine import *
# import geopandas as gpd
import shapefile
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
# import cmaps
from matplotlib.path import Path
from matplotlib.patches import PathPatch

def ReadHDF5SDS(filename, sds):
    if os.path.exists(filename):
        with h5py.File(filename, 'r') as f:
            data = f[sds][:]
    else:
        print("%s is not exists, Read HDF Data fileld!" % (filename))
    return data

def Fog_writer(filename111, FPI_Kriging, start1):
    # 获取输出的文件名
    outfilefullpath = filename111

    # 输出数据
    with h5py.File(outfilefullpath, "w") as savehdf:
        # data_fog
        data_fog = savehdf.create_dataset('Fog_Lat_Lon_DEM_Vis_Temp', data=FPI_Kriging)
        data_fog.attrs['units'] = 'NONE'
        data_fog.attrs['valid_range'] = '0, 1'
        data_fog.attrs['FillValue'] = 'NAN'
        data_fog.attrs['long_name'] = 'Fog Frequency after kriging interpolation'
        data_fog.attrs['Slope'] = float(1)
        data_fog.attrs['Intercept'] = float(0)
        data_fog.attrs['Description'] = 'Fog Frequency after kriging interpolation'

        # 全局属性文件
        # 全局属性文件
        savehdf.attrs['L1 Name'] = 'Micaps Data'
        savehdf.attrs['Dataset Name'] = 'Fog Frequency Product of Monthly'
        savehdf.attrs['File Name'] = ''

        savehdf.attrs['Data Level'] = 'L2'
        savehdf.attrs['Version Of Software'] = 'V1.0.0'
        savehdf.attrs['Software Revision Date'] = '2022-08-15'

        savehdf.attrs['Data Creating Date'] = datetime.datetime.now().date().strftime("%Y-%m-%d")
        savehdf.attrs['Data Creating Time'] = datetime.datetime.now().time().strftime("%H:%M:%S")
        savehdf.attrs['Time Of Data Composed'] = time.time() - start1

        savehdf.attrs['Number Of Data Level'] = 2
        savehdf.attrs['Projection Type'] = 'GLL'

        savehdf.attrs['Product Creator'] = 'Ranyz'
        savehdf.attrs['Programmer'] = 'Ranyz'
        savehdf.attrs['Additional Annotation'] = 'Product Creator:Ranyz, Tel:(86)010-12345678,Email:ranyinze@163.com'
    print('......Writing Fog HDF file success!......')
    return 0

if __name__=="__main__":
    start = time.time()

    filepath = r'D:\future_study\FPI\MONTH\201501\201501.HDF'
    outfilepath = r'D:\future_study\FPI\MONTH\201501\201501_Kriging.HDF'
    # 读取数据
    df = ReadHDF5SDS(filepath, 'Fog_Lat_Lon_DEM_Vis_Temp')
    # 读取站点经度
    lons = df[:, 0]
    # 读取站点纬度
    lats = df[:, 1]
    # 读取雾频率数据
    data = df[:, -1]
    # 生成经纬度网格点, 分辨率设置为0.02 或者 0.01
    cols = (123.5 - 104.5)/0.02
    lines = (41.5 - 20.5)/0.02
    print(cols,lines)
    # 950, 1000
    grid_lon = np.linspace(104.5, 123.5, int(cols)).astype(np.float32)
    grid_lat = np.linspace(20.5, 41.5, int(lines)).astype(np.float32)

    OK = OrdinaryKriging(lons, lats, data, variogram_model='gaussian',nlags=6)
    # z1 为插值结果， ss1 为每个网格对应的方差
    FPI_Kriging, ss1 = OK.execute('grid', grid_lon, grid_lat)

    # 输出插值结果为新的hdf
    Fog_writer(outfilepath, FPI_Kriging, start)
    end = time.time()

    print("Cost time: ", end-start)
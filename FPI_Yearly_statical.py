# -*- codeing = utf-8 -*-
# @Time : 2022/4/17 21:20
# @Author : Ranyinze
# @File : FPI_Yearly_statical.py.py
# @Software: PyCharm
import os, h5py,openpyxl
import numpy as np
import datetime,time
import matplotlib.pyplot as plt
import matplotlib.figure
import shapefile
import matplotlib.ticker as ticker
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_agg import FigureCanvasAgg
import pandas as pd
'''
# 读取一个HDF文件所有数据到一个矩阵，然后对矩阵中每行数据进行操作
# 将一年每个月所有的文件合并到一起，并去掉第一列和第二列都相同的数据所在的行
# 存储为新的hdf文件，方便访问：要素包括：经度，纬度，海拔高度，能见度，度
'''
# 读取hdf文件
def ReadHDF5SDS(filename, sds):
    if os.path.exists(filename):
        with h5py.File(filename, 'r') as f:
            data = f[sds][:]
    else:
        print("%s is not exists, Read HDF Data fileld!" % ('filename'))
    return data

# 将一个月的hdf数据全部存储到列表中，30个array
def GetYearfog(filepath):
    # 获取该年所有月数文件夹名称
    filepath_month = []
    for root, dirs, files in os.walk(filepath):
        # dirs: Month
        for i in dirs:
            month_filepath = os.path.join(filepath, i)
            print(month_filepath)
            filepath_month.append(month_filepath)
    # 获取该年每个月的hdf文件名称
    filename_year = []
    for ii in filepath_month:
        for root1, dirs1, files1 in os.walk(ii):
            for iii in files1:
                if os.path.splitext(iii)[1]=='.HDF':
                    filename_year.append(os.path.join(ii,iii))
    print(filename_year)
    # 循环读取这年的所有hdf文件到一个矩阵，并将矩阵添加到列表中存储
    year_data = []
    for j in filename_year:
        data = ReadHDF5SDS(j, 'Fog_Lat_Lon_DEM_Vis_Temp')
        year_data.append(data)
    return year_data

# 输出数据为矩阵hdf，方便以后读取
def Fog_writer(filename111,curr_data1, data_fog_arr,start1):
    # 获取输出的文件名

    name1 = curr_data1
    outfilefullpath = filename111

    # 输出数据
    with h5py.File(outfilefullpath, "w") as savehdf:
        # data_fog
        data_fog = savehdf.create_dataset('Fog_Lat_Lon_DEM_Vis_Temp', data=data_fog_arr)
        data_fog.attrs['units'] = 'degree; degree; meter; kilometer; celsius degree'
        data_fog.attrs['valid_range'] = 'NAN'
        data_fog.attrs['FillValue'] = 'NAN'
        data_fog.attrs['long_name'] = 'Fog of stations'
        data_fog.attrs['Slope'] = float(1)
        data_fog.attrs['Intercept'] = float(0)
        data_fog.attrs['Description'] = 'fog stations in study area from Micaps data'

        # 全局属性文件
        # 全局属性文件
        savehdf.attrs['L1 Name'] = 'Micaps Data'
        savehdf.attrs['Dataset Name'] = 'Fog stations Product of Monthly'
        savehdf.attrs['File Name'] = name1

        savehdf.attrs['Data Level'] = 'L0'
        savehdf.attrs['Version Of Software'] = 'V1.0.0'
        savehdf.attrs['Software Revision Date'] = '2022-04-17'

        savehdf.attrs['Data Creating Date'] = datetime.datetime.now().date().strftime("%Y-%m-%d")
        savehdf.attrs['Data Creating Time'] = datetime.datetime.now().time().strftime("%H:%M:%S")
        savehdf.attrs['Time Of Data Composed'] = time.time() - start1

        savehdf.attrs['Number Of Data Level'] = 3
        savehdf.attrs['Projection Type'] = 'GLL'

        savehdf.attrs['Product Creator'] = 'Ranyz'
        savehdf.attrs['Programmer'] = 'Ranyz'
        savehdf.attrs['Additional Annotation'] = 'Product Creator:Ranyz, Tel:(86)010-12345678,Email:ranyinze@163.com'

    print('......Writing Fog HDF file success!......')
    # 出能见度的图
    out_fullname1 = os.path.splitext(filename111)[0]+'_vis.png'
    print(out_fullname1)
    Plot_FSS(data_fog_arr, out_fullname1)
    # 出FPI雾频统计的图
    out_fullname2 = os.path.splitext(filename111)[0] + '_FPI.png'
    print(out_fullname1)
    Plot_FPI_Month(data_fog_arr, out_fullname2)
    return 0

# 输出可视化出图结果--插值图，用于绘制频率
# 目前还不支持一维数据
def Plot_FPI(data, outfullname):
    # 设置画图句柄
    figure = matplotlib.figure.Figure()
    FigureCanvasAgg(figure)
    # 定义绘图属性
    figsize = (6, 6)
    dpi = 300
    fig = plt.figure(figsize=figsize, dpi=dpi)
    # 解析数据，从数据中读取站点经度，纬度，能见度
    lon = data[:, 0]
    lat = data[:, 1]
    vis = data[:, 3]
    # 定义投影 投影范围 投影分辨率
    map = Basemap(projection='cyl', llcrnrlon=104.5, llcrnrlat=21.5, urcrnrlon=123.5, urcrnrlat=42.5, resolution='l')

    # 读取shp文件 并画出区域shp叠加图
    shpfile = r'D:\paper_figure\china_basic_map\bou2_4l'

    map.readshapefile(shpfile, 'states', drawbounds=True, linewidth=1.)
    map.drawmapboundary()
    # 绘制插值图
    lon, lat = map(lon, lat)
    cs = map.contourf(lon, lat, vis, cmap='jet', levels=np.linspace(0, 100,100), vmin=0, vmax=100)
    # 纬度和标识
    map.drawparallels(np.arange(-90, 90, 2), labels=[1, 0, 0, 0])
    # 经度和标识
    map.drawmeridians(np.arange(-180, 180, 2), labels=[0, 0, 0, 1])

    # 设置colorbar
    position = fig.add_axes([0.1, 0.06, 0.5, 0.025])
    # (第一个参数控制水平位置(左减右加)，第二个参数控制垂直位置（上加下减），第三个参数控制宽度，第四个参数控制高度)
    colorbar = plt.colorbar(cs, 'right', cax=position, fraction=0.01, orientation='horizontal')
    # 设置色标卡的刻度个数
    colorbar.locator = ticker.MaxNLocator(nbins=11)
    # 设置色标卡的标签字体大小，字体与色标卡间距，刻度方向,刻度大小，刻度的宽度
    colorbar.ax.tick_params(labelsize=8, pad=2, direction="in", size=2, width=0.3)
    # 设置色标卡的刻度单位 第一个参数控制水平方向，第二个参数控制垂直方向
    plt.text(48, -42, '℃', fontsize=8)
    colorbar.update_ticks()
    # 保存图像
    plt.savefig(outfullname)
    fig.clear()
    plt.close()

    return 0

# 输出可视化出图结果--散点图，用于绘制频率
def Plot_FSS(data, outfullname):
    # 设置画图句柄
    figure = matplotlib.figure.Figure()
    FigureCanvasAgg(figure)
    # 定义绘图属性
    figsize = (6, 6)
    dpi = 300
    fig = plt.figure(figsize=figsize, dpi=dpi)
    # 解析数据，从数据中读取站点经度，纬度，能见度
    lon = data[:, 0]
    lat = data[:, 1]
    vis = data[:, 3]
    # 定义投影 投影范围 投影分辨率
    map = Basemap(projection='cyl', llcrnrlon=104.5, llcrnrlat=21.5, urcrnrlon=123.5, urcrnrlat=42.5, resolution='l')

    # 读取shp文件 并画出区域shp叠加图
    shpfile = r'D:\paper_figure\china_basic_map\bou2_4l'

    map.readshapefile(shpfile, 'states', drawbounds=True, linewidth=0.5)
    map.drawmapboundary()
    # 绘制插值图
    lon, lat = map(lon, lat)
    # 绘制散点图
    cs = map.scatter(lon, lat, s=50, c=vis, marker='.', cmap='jet', vmin=0, vmax=1)
    # 纬度和标识
    map.drawparallels(np.arange(21.5, 41.5, 4), labels=[1, 0, 0, 0],linewidth=.5)
    # 经度和标识
    map.drawmeridians(np.arange(104.5, 123.5, 5), labels=[0, 0, 0, 1],linewidth=.5)

    # 设置colorbar
    position = fig.add_axes([0.166, 0.04, 0.62, 0.02])
    # (第一个参数控制水平位置(左减右加)，第二个参数控制垂直位置（上加下减），第三个参数控制宽度，第四个参数控制高度)
    bounds = [round(elem, 2) for elem in np.linspace(0, 1, 11)]
    colorbar = plt.colorbar(cs, cax=position, boundaries = [-0.1] + bounds + [1],extend='both',
                            fraction=0.01,orientation='horizontal')
    # 设置色标卡的刻度个数
    colorbar.locator = ticker.MaxNLocator(nbins=11)
    # 设置色标卡的标签字体大小，字体与色标卡间距，刻度方向,刻度大小，刻度的宽度
    colorbar.ax.tick_params(labelsize=8, pad=2, direction="in", size=4, width=0.3)
    # 设置色标卡的刻度单位 第一个参数控制水平方向，第二个参数控制垂直方向
    plt.text(1.08, 0, 'km', fontsize=10)
    colorbar.update_ticks()
    # 保存图像
    plt.savefig(outfullname)
    fig.clear()
    plt.close()

    return 0

# 输出可视化出图结果--雾频散点图，用于绘制频率
def Plot_FPI_Month(data, outfullname):
    # 设置画图句柄
    figure = matplotlib.figure.Figure()
    FigureCanvasAgg(figure)
    # 定义绘图属性
    figsize = (6, 6)
    dpi = 300
    fig = plt.figure(figsize=figsize, dpi=dpi)
    # 解析数据，从数据中读取站点经度，纬度，能见度
    lon = data[:, 0]
    lat = data[:, 1]
    fpi = data[:, 6]
    # 定义投影 投影范围 投影分辨率
    map = Basemap(projection='cyl', llcrnrlon=104.5, llcrnrlat=21.5, urcrnrlon=123.5, urcrnrlat=42.5, resolution='l')

    # 读取shp文件 并画出区域shp叠加图
    shpfile = r'D:\paper_figure\china_basic_map\bou2_4l'

    map.readshapefile(shpfile, 'states', drawbounds=True, linewidth=0.5)
    map.drawmapboundary()
    # 绘制插值图
    lon, lat = map(lon, lat)
    # 绘制散点图
    cs = map.scatter(lon, lat, s=50, c=fpi, marker='.', cmap='PRGn', vmin=0, vmax=1)
    # 纬度和标识
    map.drawparallels(np.arange(21.5, 41.5, 4), labels=[1, 0, 0, 0],linewidth=.5)
    # 经度和标识
    map.drawmeridians(np.arange(104.5, 123.5, 5), labels=[0, 0, 0, 1],linewidth=.5)

    # 设置colorbar
    position = fig.add_axes([0.166, 0.04, 0.62, 0.02])
    # (第一个参数控制水平位置(左减右加)，第二个参数控制垂直位置（上加下减），第三个参数控制宽度，第四个参数控制高度)
    bounds = [round(elem, 2) for elem in np.linspace(0, 1, 11)]
    colorbar = plt.colorbar(cs, cax=position, boundaries = [-0.1] + bounds + [1],extend='both',
                            fraction=0.01,orientation='horizontal')
    # 设置色标卡的刻度个数
    colorbar.locator = ticker.MaxNLocator(nbins=11)
    # 设置色标卡的标签字体大小，字体与色标卡间距，刻度方向,刻度大小，刻度的宽度
    colorbar.ax.tick_params(labelsize=8, pad=2, direction="in", size=4, width=0.3)
    # 设置色标卡的刻度单位 第一个参数控制水平方向，第二个参数控制垂直方向
    plt.text(1.08, 0, '', fontsize=10)
    colorbar.update_ticks()
    # 保存图像
    plt.savefig(outfullname)
    fig.clear()
    plt.close()

    return 0

if __name__=="__main__":
    # 具体路径到每个月份
    start = time.time()
    filepath = r'D:\future_study\FPI\MONTH'
    outpath = r'D:\future_study\FPI\YEAR'
    # 读取一年的数据矩阵到列表, 将每个月的hdf数据全部存储到列表中，12个array
    data_yearly = GetYearfog(filepath)
    print(data_yearly[0].shape)
    lines = 0
    for jj in range(len(data_yearly)):
        lines = len(data_yearly[jj]) + lines
    # 年合成的所有站点，其中有重复的站点
    year_data = np.empty((lines,7))
    print(year_data.shape)
    curr_line = 0
    for jjj in range(len(data_yearly)):
        # print(len(data_yearly[jjj]))
        # print(curr_line+data_yearly[jjj].shape[0])
        year_data[curr_line: curr_line+data_yearly[jjj].shape[0],:] = data_yearly[jjj]
        curr_line = curr_line + len(data_yearly[jjj])
    # 对年合成站点 month_data 统计 出现的次数，最大值应该为当年的天数
    # 1. 取出经纬度
    lon_lat_arr = year_data[:,0:2]
    # 2. 统计出现相同站点的次数，对应位置的索引
    x1, index, counts = np.unique(lon_lat_arr, return_index=True, return_counts=True, axis=0)
    print("stations counts: ", lon_lat_arr.shape[0])
    print("unique stations counts: ", index.shape[0])
    # 3. 赋值
    # 1-5列表示之前的属性值，第6列表示该站点在该年出现雾的天数，第7列表是频率 = 天数/365
    Year_Fog = np.zeros((len(index), 7))
    for s in range(len(index)):
        Year_Fog[s, 0:5] = year_data[index[s], 0:5]
        Year_Fog[s, 5:6] = counts[s]+year_data[index[s], 5]
        print(counts[s] + year_data[index[s], 5])
    Year_Fog[:,-1] = Year_Fog[:,-2]/365
    print(Year_Fog)

    # 开始输出每月的文件
    curr_month = filepath[-6:]
    outpath = os.path.join(outpath,curr_month)
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    outname = curr_month + '.HDF'

    outfullname = os.path.join(outpath,outname)
    print('outfullname: ', outfullname)
    # 输出hdf
    Fog_writer(outfullname,outname, Month_Fog,start)
    # 输出excel
    data_df = pd.DataFrame(Month_Fog)
    Excel_name = curr_month + '.xls'

    print(Excel_name)
    writer = pd.ExcelWriter(os.path.join(outpath,Excel_name))
    data_df.to_excel(writer,float_format='%.2f')
    writer.save()




    end = time.time()
    print("cost time: ", end-start)

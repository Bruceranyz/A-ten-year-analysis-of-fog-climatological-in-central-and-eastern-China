import os, h5py
import numpy as np
import datetime,time
import matplotlib.pyplot as plt
import matplotlib.figure
import shapefile
import matplotlib.ticker as ticker
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_agg import FigureCanvasAgg

'''
micaps数据简介：
区站号，经度，纬度，海拔，站点级别，总云量，风向，风速，
海平面气压，3小时变压，过去天气1，过去天气2，6小时降雨，低云状，低云量，低云高，
露点，能见度，现在天气，温度，中云状，高云状，标志1，标志2

预处理后，保留的要素为：
经度、纬度、海拔、总云量、风向、风速、海平面气压、过去天气1、过去天气2、低云状、低云高、露点、能见度、现在天气、温度
对应的索引
1，2，3，5，6，7，8，10，11，13，15，16，17，18，19，
后续可以通过 露点温度、空气温度 计算相对湿度：

# 读取一个micaps文件所有数据到一个矩阵，然后对矩阵中每行数据进行操作
# 首先将研究区外的数据全部删除；21.5-42.5，104.5-123.5
# 填充值，不合理的值全部删除，只保留有雾的站点
# 存储为新的hdf文件，方便访问和进一步研究
'''

# 获取文件夹下所有文件
def file_name(file_dir):
    for root,dirs, files in os.walk(file_dir):
        # root: 返回当前目录路径
        # dirs： 返回当前路径下所有子目录
        # files：返回当前路径下所有非目录子文件
        return files

# 读取txt文本中行列号，并存储到矩阵里面，filename为txt文件全路径名
def Readmicaps(filename):
    path, name = os.path.split(filename)
    if os.path.exists(filename):
        fp = open(filename, 'r')
        print("-----Read micaps file: %s success!------"%(name))
        lines = fp.readlines()

        text_lon = []  # longitude
        text_lat = []  # latitude
        text_dem = []  # altitude
        text_tcc = []  # total cloud cover
        text_wid = []  # wind direction
        text_wis = []  # wind speed
        text_sap = []  # site air pressure
        text_pw1 = []  # past weather 1
        text_pw2 = []  # past weather 2
        text_lcs = []  # low cloud shape
        text_lch = []  # low cloud height
        text_dpt = []  # dew point temperature
        text_vis = []  # visibility
        text_cuw = []  # current weather
        text_tmp = []  # air temperature
        for line in lines:
            if line.isspace():
                continue
            elif len(line.split()) !=24 :
                # print(len(line.split()))
                continue
            else:
                line1 = line.split()
                '''
                
                经度、纬度、海拔、总云量、风向、风速、海平面气压、过去天气1、过去天气2、低云状、低云高、露点、能见度、现在天气、温度
                对应的索引
                1，2，3，5，6，7，8，10，11，13，15，16，17，18，19，
                后续可以通过 露点温度、空气温度 计算相对湿度：
                '''
                # 经度
                text_lon.append(line1[1])
                # 纬度
                text_lat.append(line1[2])
                # 站点海拔
                text_dem.append(line1[3])
                # 总云量
                text_tcc.append(line1[5])
                # 风向
                text_wid.append(line1[6])
                # 风速
                text_wis.append(line1[7])
                # 海平面气压
                text_sap.append(line1[8])
                # 过去天气1
                text_pw1.append(line1[10])
                # 过去天气2
                text_pw2.append(line1[11])
                # 低云状
                text_lcs.append(line1[13])
                # 低云高
                text_lch.append(line1[15])
                # 露点
                text_dpt.append(line1[16])
                # 能见度
                text_vis.append(line1[17])
                # 现在天气
                text_cuw.append(line1[18])
                # 温度
                text_tmp.append(line1[19])

        if len(text_lon)<1:
            print("-----There is no stations need to process, program will exit!-----")
            return -1
        else:
            print("-----Start process all stations now!------")
            arr_fog = np.ones((len(text_lon),15),dtype=float)
            arr_fog = arr_fog * -9999

            for i in range(len(text_lon)):

                arr_fog[i,0] = text_lon[i]
                arr_fog[i, 1] = text_lat[i]
                arr_fog[i,2] = text_dem[i]
                arr_fog[i, 3] = text_tcc[i]
                arr_fog[i,4] = text_wid[i]
                arr_fog[i,5] = text_wis[i]
                arr_fog[i,6] = text_sap[i]
                arr_fog[i,7] = text_pw1[i]
                arr_fog[i,8] = text_pw2[i]
                arr_fog[i,9] = text_lcs[i]
                arr_fog[i,10] = text_lch[i]
                arr_fog[i,11] = text_dpt[i]
                arr_fog[i,12] = text_vis[i]
                arr_fog[i,13] = text_cuw[i]
                arr_fog[i,14] = text_tmp[i]

            print("arr_fog shape:", arr_fog.shape[0],arr_fog.shape[1])
            # print(arr_fog)
            print("-----process all stations success!------")
            return arr_fog
    else:
        print("-----%s is not exist!-----"%(filename))
        return -1

# 获取研究区域的有雾的站点，有霾的站点；需要对经纬度控制，能见度vis范围满足【0，1】fog； 【1，3】haze
def GetStudyAreaFog(arr_fog,lon_start,lon_end,lat_start,lat_end,starttime):
    # 构造一个索引矩阵储存满足条件的那一行，即该站点所在的索引
    # print(arr_fog)
    fog_index = np.zeros((arr_fog.shape[0]),dtype=int)
    index_lines = []
    for i in range(arr_fog.shape[0]):
        if lon_start<=arr_fog[i,0]<=lon_end and lat_end<=arr_fog[i,1]<=lat_start:
                if 0<=arr_fog[i,12]<= 3:
                    fog_index[i] = 1
                    index_lines.append(i)
                    # print("fog lines = %d"%(i))
                    # print(arr_fog[i,:])
    print("-----------Curr time fog stations have %d-----------"%np.sum(fog_index))
    data = np.empty((np.sum(fog_index),15))
    for ii in range(data.shape[0]):
        data[ii,:] = arr_fog[index_lines[ii]]

    print("-----------Get study fog stations success!-----------")

    return data

# 输出数据为矩阵hdf，方便以后读取
def Fog_writer(filename,outfilepath,data_fog_arr):
    # 获取输出的文件名
    path1, name1 = os.path.split(filename)

    name2 = os.path.splitext(name1)[0] + '.HDF'
    name_day = name2[0:6]
    outfilepath = os.path.join(outfilepath, name_day)
    if not os.path.exists(outfilepath):
        os.mkdir(outfilepath)

    outfilefullpath = os.path.join(outfilepath, name2)

    print("Input file name: %s"%(name1))
    print("Output file name: %s"%(name2))

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
        savehdf.attrs['Dataset Name'] = 'Fog stations Product'
        savehdf.attrs['File Name'] = name2

        savehdf.attrs['Data Level'] = 'L0'
        savehdf.attrs['Version Of Software'] = 'V1.0.0'
        savehdf.attrs['Software Revision Date'] = '2022-04-15'

        savehdf.attrs['Data Creating Date'] = datetime.datetime.now().date().strftime("%Y-%m-%d")
        savehdf.attrs['Data Creating Time'] = datetime.datetime.now().time().strftime("%H:%M:%S")
        savehdf.attrs['Time Of Data Composed'] = time.time() - start

        savehdf.attrs['Number Of Data Level'] = 6
        savehdf.attrs['Projection Type'] = 'GLL'

        savehdf.attrs['Product Creator'] = 'Ranyz'
        savehdf.attrs['Programmer'] = 'Ranyz'
        savehdf.attrs['Additional Annotation'] = 'Product Creator:Ranyz, Tel:(86)010-12345678,Email:ranyinze@163.com'

    print('......Writing Fog HDF file success!......')
    if int(data_fog_arr.shape[0]) >=15:
        out_fullname = os.path.join(outfilepath, os.path.splitext(name1)[0]+'.png')
        Plot_FSS(data_fog_arr, out_fullname)
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
    vis = data[:, 12]
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

# 输出可视化出图结果--插值图，用于绘制频率
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
    vis = data[:, 12]
    # 定义投影 投影范围 投影分辨率
    map = Basemap(projection='cyl', llcrnrlon=104.5, llcrnrlat=21.5, urcrnrlon=123.5, urcrnrlat=42.5, resolution='l')

    # 读取shp文件 并画出区域shp叠加图
    shpfile = r'D:\paper_figure\china_basic_map\bou2_4l'

    map.readshapefile(shpfile, 'states', drawbounds=True, linewidth=0.5)
    map.drawmapboundary()
    # 绘制插值图
    lon, lat = map(lon, lat)
    # 绘制散点图
    cs = map.scatter(lon, lat, s=150, c=vis, marker='.', cmap='jet', vmin=0, vmax=3)
    # 纬度和标识
    map.drawparallels(np.arange(21.5, 41.5, 4), labels=[1, 0, 0, 0],linewidth=.5)
    # 经度和标识
    map.drawmeridians(np.arange(104.5, 123.5, 5), labels=[0, 0, 0, 1],linewidth=.5)

    # 设置colorbar
    position = fig.add_axes([0.166, 0.04, 0.62, 0.02])
    # (第一个参数控制水平位置(左减右加)，第二个参数控制垂直位置（上加下减），第三个参数控制宽度，第四个参数控制高度)
    bounds = [round(elem, 2) for elem in np.linspace(0, 3, 11)]
    colorbar = plt.colorbar(cs, cax=position, boundaries = [-0.1] + bounds + [3],extend='both',
                            fraction=0.01,orientation='horizontal')
    # 设置色标卡的刻度个数
    colorbar.locator = ticker.MaxNLocator(nbins=11)
    # 设置色标卡的标签字体大小，字体与色标卡间距，刻度方向,刻度大小，刻度的宽度
    colorbar.ax.tick_params(labelsize=8, pad=2, direction="in", size=4, width=0.3)
    # 设置色标卡的刻度单位 第一个参数控制水平方向，第二个参数控制垂直方向
    plt.text(3.08, -3, 'km', fontsize=10)
    colorbar.update_ticks()
    # 保存图像
    plt.savefig(outfullname)
    fig.clear()
    plt.close()

    return 0

if __name__=="__main__":
    start = time.time()
    year = '2020'
    month111=['01','02','03','04','05','06','07','08','09','10','11','12']
    if int(year) == 2018 or int(year) ==2019:
        filename1 = r'E:\data_sorting\dataset\地面验证数据\YYYY\YYYYMM'
    # month111=['08','09','10','11','12']
    elif int(year) == 2012 or int(year) ==2013 or int(year) ==2014:
        filename1 = r'E:\data_sorting\dataset\地面验证数据\YYYY\YYYYMM\data\surface\plot-pc'
    elif int(year) == 2021:
        filename1 = r'E:\data_sorting\dataset\地面验证数据\YYYY\YYYY\MICAPS_DATA\data\surface\plot\YYYYMM\MICAPS_DATA\data\surface\plot'
    # month111=['08','09','10','11','12']
    else:
        filename1 = r'E:\data_sorting\dataset\地面验证数据\YYYY\YYYYMM\MICAPS_DATA\data\surface\plot'
    for ym in range(len(month111)):
        print("----------------------------------------------------------------------------------")
        filename1 = filename1.replace('YYYY',year)
        filename1 = filename1.replace('MM',month111[ym])
        print(filename1)
        output_month = filename1[36:42]
        print(output_month)
        files = file_name(filename1)
        print(files)
        for i in files:
            filename = os.path.join(filename1,i)
            print(filename)
            try:
                # 获得所有的站点信息
                arr_fog = Readmicaps(filename)

                # 设置研究区域的经纬度范围
                # 左经度
                lon_start = 104.5
                # 右经度
                lon_end = 123.5
                # 上纬度
                lat_start = 41.5
                # 下纬度
                lat_end = 21.5

                # 获得Fog 站点数据
                data_fog = GetStudyAreaFog(arr_fog, lon_start, lon_end, lat_start, lat_end, start)
                # 设置输出路径
                outfilepath = r'E:\Analysis_fog_haze\Dataset\Hourly'
                outfilepath = os.path.join(outfilepath,output_month)
                if not os.path.exists(outfilepath):
                    os.mkdir(outfilepath)

                # 输出数据为HDF
                return_code = Fog_writer(filename, outfilepath, data_fog)
            except:
                print('\033[1;31m')
                print("****************************************")
                print("-----There is problem: %s !!!-----"%(i))
                print("****************************************")
                print('\033[0m')
        if int(year) == 2018 or int(year) == 2019:
            filename1 = r'E:\data_sorting\dataset\地面验证数据\YYYY\YYYYMM'
        # month111=['08','09','10','11','12']
        elif int(year) == 2012 or int(year) == 2013 or int(year) == 2014:
            filename1 = r'E:\data_sorting\dataset\地面验证数据\YYYY\YYYYMM\data\surface\plot-pc'
        elif int(year)==2021:
            filename1 = r'E:\data_sorting\dataset\地面验证数据\YYYY\YYYY\MICAPS_DATA\data\surface\plot\YYYYMM\MICAPS_DATA\data\surface\plot'

        else:
            filename1 = r'E:\data_sorting\dataset\地面验证数据\YYYY\YYYYMM\MICAPS_DATA\data\surface\plot'
    end =time.time()
    print("cost time: ", end-start)


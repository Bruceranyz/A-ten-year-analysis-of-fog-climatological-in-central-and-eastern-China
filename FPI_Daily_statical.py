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
# 读取一个HDF文件所有数据到一个矩阵，然后对矩阵中每行数据进行操作
# 将一天所有的文件合并到一起，并去掉第一列和第二列都相同的数据所在的行
# 存储为新的hdf文件，方便访问：要素包括：经度，纬度，海拔高度，能见度，度
'''

# 读取hdf文件
def ReadHDF5SDS(filename, sds):
    if os.path.exists(filename):
        with h5py.File(filename, 'r') as f:
            data = f[sds][:]
    else:
        print("%s is not exists, Read HDF Data fileld!" % (filename))
    return data

# 获取当天的雾的数据矩阵
def Getcurrday(filepath):
    return 0

#  获得日产品
def GetDailyfog(filepath):
    # 获取月份下文件夹的名称，存储为一个列表
    for root, dirs, files in os.walk(filepath):
        # dirs: 151130
        for i in dirs:
            daily_filepath = os.path.join(filepath, i)
            print(daily_filepath)
            filename = []
            # 每一天中所有HDF文件的文件名
            for root1, dirs1, files1 in os.walk(daily_filepath):
                for ii in files1:
                    if os.path.splitext(ii)[1] == '.HDF':
                        filename.append(os.path.join(daily_filepath, ii))
            if len(filename) == 2:
                arr_fog = ReadHDF5SDS(filename[0], 'Fog_Lat_Lon_DEM_Vis_Temp')
                arr_fog_new = np.vstack((arr_fog, ReadHDF5SDS(filename[1], 'Fog_Lat_Lon_DEM_Vis_Temp')))
            elif len(filename) == 3:
                arr_fog = ReadHDF5SDS(filename[0], 'Fog_Lat_Lon_DEM_Vis_Temp')
                a1 = np.vstack((arr_fog, ReadHDF5SDS(filename[1], 'Fog_Lat_Lon_DEM_Vis_Temp')))
                arr_fog_new = np.vstack((a1, ReadHDF5SDS(filename[2], 'Fog_Lat_Lon_DEM_Vis_Temp')))
            elif len(filename) == 4:
                arr_fog = ReadHDF5SDS(filename[0], 'Fog_Lat_Lon_DEM_Vis_Temp')
                a1 = np.vstack((arr_fog, ReadHDF5SDS(filename[1], 'Fog_Lat_Lon_DEM_Vis_Temp')))
                a2 = np.vstack((a1, ReadHDF5SDS(filename[2], 'Fog_Lat_Lon_DEM_Vis_Temp')))
                arr_fog_new = np.vstack((a2, ReadHDF5SDS(filename[3], 'Fog_Lat_Lon_DEM_Vis_Temp')))
            elif len(filename) == 5:
                arr_fog = ReadHDF5SDS(filename[0], 'Fog_Lat_Lon_DEM_Vis_Temp')
                a1 = np.vstack((arr_fog, ReadHDF5SDS(filename[1], 'Fog_Lat_Lon_DEM_Vis_Temp')))
                a2 = np.vstack((a1, ReadHDF5SDS(filename[2], 'Fog_Lat_Lon_DEM_Vis_Temp')))
                a3 = np.vstack((a2, ReadHDF5SDS(filename[3], 'Fog_Lat_Lon_DEM_Vis_Temp')))
                arr_fog_new = np.vstack((a3, ReadHDF5SDS(filename[4], 'Fog_Lat_Lon_DEM_Vis_Temp')))
            elif len(filename) == 6:
                arr_fog = ReadHDF5SDS(filename[0], 'Fog_Lat_Lon_DEM_Vis_Temp')
                a1 = np.vstack((arr_fog, ReadHDF5SDS(filename[1], 'Fog_Lat_Lon_DEM_Vis_Temp')))
                a2 = np.vstack((a1, ReadHDF5SDS(filename[2], 'Fog_Lat_Lon_DEM_Vis_Temp')))
                a3 = np.vstack((a2, ReadHDF5SDS(filename[3], 'Fog_Lat_Lon_DEM_Vis_Temp')))
                a4 = np.vstack((a3, ReadHDF5SDS(filename[4], 'Fog_Lat_Lon_DEM_Vis_Temp')))
                arr_fog_new = np.vstack((arr_fog, ReadHDF5SDS(filename[5], 'Fog_Lat_Lon_DEM_Vis_Temp')))
            elif len(filename) == 7:
                arr_fog = ReadHDF5SDS(filename[0], 'Fog_Lat_Lon_DEM_Vis_Temp')
                a1 = np.vstack((arr_fog, ReadHDF5SDS(filename[1], 'Fog_Lat_Lon_DEM_Vis_Temp')))
                a2 = np.vstack((a1, ReadHDF5SDS(filename[2], 'Fog_Lat_Lon_DEM_Vis_Temp')))
                a3 = np.vstack((a2, ReadHDF5SDS(filename[3], 'Fog_Lat_Lon_DEM_Vis_Temp')))
                a4 = np.vstack((a3, ReadHDF5SDS(filename[4], 'Fog_Lat_Lon_DEM_Vis_Temp')))
                a5 = np.vstack((a4, ReadHDF5SDS(filename[5], 'Fog_Lat_Lon_DEM_Vis_Temp')))
                arr_fog_new = np.vstack((arr_fog, ReadHDF5SDS(filename[6], 'Fog_Lat_Lon_DEM_Vis_Temp')))
            elif len(filename) == 8:
                arr_fog = ReadHDF5SDS(filename[0], 'Fog_Lat_Lon_DEM_Vis_Temp')
                a1 = np.vstack((arr_fog, ReadHDF5SDS(filename[1], 'Fog_Lat_Lon_DEM_Vis_Temp')))
                a2 = np.vstack((a1, ReadHDF5SDS(filename[2], 'Fog_Lat_Lon_DEM_Vis_Temp')))
                a3 = np.vstack((a2, ReadHDF5SDS(filename[3], 'Fog_Lat_Lon_DEM_Vis_Temp')))
                a4 = np.vstack((a3, ReadHDF5SDS(filename[4], 'Fog_Lat_Lon_DEM_Vis_Temp')))
                a5 = np.vstack((a4, ReadHDF5SDS(filename[5], 'Fog_Lat_Lon_DEM_Vis_Temp')))
                a6 = np.vstack((a5, ReadHDF5SDS(filename[6], 'Fog_Lat_Lon_DEM_Vis_Temp')))
                arr_fog_new = np.vstack((a6, ReadHDF5SDS(filename[7], 'Fog_Lat_Lon_DEM_Vis_Temp')))
            elif len(filename) == 1:
                arr_fog_new = ReadHDF5SDS(filename[0], 'Fog_Lat_Lon_DEM_Vis_Temp')
            # 获取非相同元素所在的行
            # 1.取出经纬度矩阵
            lon_lat = arr_fog_new[:, 0:2]
            # 2. 求出不同行所在的索引素组
            x111, index = np.unique(lon_lat, return_index=True, axis=0)
            # 3. 赋值
            daily_Fog = np.empty((len(index), 5))
            for j in range(len(index)):
                daily_Fog[j, :] = arr_fog_new[index[j], :]
            # 开始输出每日的文件

            curr_date = ii[0:6]
            outpath1 = os.path.join(outpath, curr_date)
            if not os.path.exists(outpath1):
                os.mkdir(outpath1)
            Fog_writer(outpath1, curr_date, daily_Fog, start)

            filename.clear()
    return 0
# 输出数据为矩阵hdf，方便以后读取
def Fog_writer(filename111,curr_data1, data_fog_arr,start1):
    # 获取输出的文件名

    name1 = curr_data1 + '.HDF'
    outfilefullpath = os.path.join(filename111, name1)

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
        savehdf.attrs['Dataset Name'] = 'Fog stations Product of Daily'
        savehdf.attrs['File Name'] = name1

        savehdf.attrs['Data Level'] = 'L0'
        savehdf.attrs['Version Of Software'] = 'V1.0.0'
        savehdf.attrs['Software Revision Date'] = '2022-04-15'

        savehdf.attrs['Data Creating Date'] = datetime.datetime.now().date().strftime("%Y-%m-%d")
        savehdf.attrs['Data Creating Time'] = datetime.datetime.now().time().strftime("%H:%M:%S")
        savehdf.attrs['Time Of Data Composed'] = time.time() - start1

        savehdf.attrs['Number Of Data Level'] = 2
        savehdf.attrs['Projection Type'] = 'GLL'

        savehdf.attrs['Product Creator'] = 'Ranyz'
        savehdf.attrs['Programmer'] = 'Ranyz'
        savehdf.attrs['Additional Annotation'] = 'Product Creator:Ranyz, Tel:(86)010-12345678,Email:ranyinze@163.com'

    print('......Writing Fog HDF file success!......')

    out_fullname = os.path.join(filename111, os.path.splitext(name1)[0]+'.png')
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


if __name__=="__main__":
    # 具体路径到每个月份
    start = time.time()
    year = '2014'
    month111 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    for jj in range(len(month111)):
        filepath = r'D:\future_study\FPI\HDF\YYYYMM'
        filepath = filepath.replace('YYYY',year)
        filepath = filepath.replace('MM',month111[jj])

        outpath = r'D:\future_study\FPI\DAILY'
        outmonth = filepath[-6:]
        print(outmonth)
        outpath = os.path.join(outpath,outmonth)
        if not os.path.exists(outpath):
            os.mkdir(outpath)
        return_code = GetDailyfog(filepath)

        filepath = r'D:\future_study\FPI\HDF\YYYYMM'
    end = time.time()
    print("cost time: ", end-start)

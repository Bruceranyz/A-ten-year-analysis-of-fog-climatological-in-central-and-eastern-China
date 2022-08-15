import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pyplot

# -*- coding:utf-8 -*-
import os, h5py
import numpy as np
import datetime,time
from sklearn.cluster import KMeans
from matplotlib import pyplot


class K_Means(object):
    # k是分组数；tolerance‘中心点误差’；max_iter是迭代次数
    def __init__(self, k=2, tolerance=0.0001, max_iter=300):
        self.k_ = k
        self.tolerance_ = tolerance
        self.max_iter_ = max_iter

    def fit(self, data):
        self.centers_ = {}
        for i in range(self.k_):
            self.centers_[i] = data[i]

        for i in range(self.max_iter_):
            self.clf_ = {}
            for i in range(self.k_):
                self.clf_[i] = []
            # print("质点:",self.centers_)
            for feature in data:
                # distances = [np.linalg.norm(feature-self.centers[center]) for center in self.centers]
                distances = []
                for center in self.centers_:
                    # 欧拉距离
                    # np.sqrt(np.sum((features-self.centers_[center])**2))
                    distances.append(np.linalg.norm(feature - self.centers_[center]))
                classification = distances.index(min(distances))
                self.clf_[classification].append(feature)

            # print("分组情况:",self.clf_)
            prev_centers = dict(self.centers_)
            for c in self.clf_:
                self.centers_[c] = np.average(self.clf_[c], axis=0)

            # '中心点'是否在误差范围
            optimized = True
            for center in self.centers_:
                org_centers = prev_centers[center]
                cur_centers = self.centers_[center]
                if np.sum((cur_centers - org_centers) / org_centers * 100.0) > self.tolerance_:
                    optimized = False
            if optimized:
                break

    def predict(self, p_data):
        distances = [np.linalg.norm(p_data - self.centers_[center]) for center in self.centers_]
        index = distances.index(min(distances))
        return index

# 读取hdf文件
def ReadHDF5SDS(filename, sds):
    if os.path.exists(filename):
        with h5py.File(filename, 'r') as f:
            data = f[sds][:]
    else:
        print("%s is not exists, Read HDF Data fileld!" % ('filename'))
    return data

if __name__ == '__main__':
    x1 = ReadHDF5SDS(r'D:\future_study\FPI\YEAR\2016\2016.HDF','Fog_Lat_Lon_DEM_Vis_Temp')
    x = np.zeros((x1.shape[0],int(4)))
    x11 = np.zeros((x1.shape[0],int(2)))
    x[:,0] = x1[:,0]
    x[:,1] = x1[:,1]
    x[:,2] = x1[:,6]
    x[:,3] = x1[:,2]

    x11[:,0] = x1[:,6]
    x11[:,1] = x1[:,2]

    #
    # k_means = K_Means(k=3)
    # k_means.fit(x)
    # print(k_means.centers_)
    # for center in k_means.centers_:
    #     pyplot.scatter(k_means.centers_[center][0], k_means.centers_[center][1], marker='*', s=150)
    #
    # for cat in k_means.clf_:
    #     for point in k_means.clf_[cat]:
    #         pyplot.scatter(point[0], point[1], c=('r' if cat == 0 else 'b'))
    #
    # predict = [[2, 1], [6, 9]]
    # for feature in predict:
    #     cat = k_means.predict(predict)
    #     pyplot.scatter(feature[0], feature[1], c=('r' if cat == 0 else 'b'), marker='x')
    #
    # pyplot.show()

    # 把上面数据点分为两组（非监督学习）
    clf = KMeans(n_clusters=3)
    clf.fit(x)  # 分组

    centers = clf.cluster_centers_  # 两组数据点的中心点
    labels = clf.labels_  # 每个数据点所属分组
    print(centers)
    print(labels)

    for i in range(len(labels)):
        if labels[i] == 0:
            pyplot.scatter(x[i][0], x[i][1], c='r')
        elif labels[i] == 1:
            pyplot.scatter(x[i][0], x[i][1], c='g')
        elif labels[i] == 3:
            pyplot.scatter(x[i][0], x[i][1], c='y')
        elif labels[i] == 4:
            pyplot.scatter(x[i][0], x[i][1], c='black')
        elif labels[i] == 5:
            pyplot.scatter(x[i][0], x[i][1], c='c')
        else:
            pyplot.scatter(x[i][0], x[i][1], c='b')
        # pyplot.scatter(x[i][0], x[i][1], c=('r' if labels[i] == 0 else 'b'))
    # pyplot.scatter(centers[:, 0], centers[:, 1], marker='*', s=100)
    plt.show()

    # # 预测
    # predict = [[2, 1], [6, 9]]
    # label = clf.predict(predict)
    # for i in range(len(label)):
    #     pyplot.scatter(predict[i][0], predict[i][1], c=('r' if label[i] == 0 else 'b'), marker='x')
    #
    # pyplot.show()


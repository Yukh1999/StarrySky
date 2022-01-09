from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.impute import SimpleImputer
import numpy as np


def normalization():
    """
    将特征数据进行归一化处理
    """

    # 原始特征数据：随便给一个矩阵
    ori_vec = [
        [90, 80, 50, 30],
        [80, 200, 60, 50],
        [150, 60, 33, 59]
    ]

    print('原始数据')
    print(ori_vec)

    # 实例化一个缩放工具类
    mm = MinMaxScaler(feature_range=(0, 1))  # feature_range 默认是 (0,1)，表示要将原始数据映射的目标区间

    # 进行数据转化
    output = mm.fit_transform(ori_vec)

    # 输出数据
    print('归一化数据')
    print(output)


def standardization():
    """
    标准化处理
    """

    # 原始特征数据：随便给一个矩阵
    ori_vec = [
        [90, 80, 50, 30],
        [80, 200, 60, 50],
        [150, 60, 33, 59],
        [600, 1, 52, 43]
    ]

    print('原始数据')
    print(ori_vec)

    # 实例化一个标准化工具类
    std = StandardScaler()  # feature_range 默认是 (0,1)，表示要将原始数据映射的目标区间

    # 进行数据转化
    output = std.fit_transform(ori_vec)

    # 输出数据
    print('标准化数据')
    print(output)


def miss_value():
    """
    缺失值处理
    """

    # 原始数据
    ori_data = [
        [5, 7, 12, 19],
        [6, np.nan, 9, 3],
        [np.nan, 12, 13, 15],
        [1, 3, 11, 6],
        [2, 4, 6, np.nan]
    ]

    # 实例化一个缺失值填补类
    im = SimpleImputer(missing_values=np.nan, strategy='mean')

    # 缺失值处理
    output = im.fit_transform(ori_data)

    # 输出结果
    # 原始数据
    print('原始数据')
    print(ori_data)

    # 填补后的数据
    print('缺失值填补后数据')
    print(output)


if __name__ == '__main__':
    # 调用归一化示例
    normalization()

    # 调用标准化示例
    print('-' * 100)
    standardization()

    # 调用缺失值填补示例
    print('-' * 100)
    miss_value()

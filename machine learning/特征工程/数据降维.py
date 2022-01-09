from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import PCA


# 特征选择
def var_select():
    """
    方差特征选择：删除低于方差阈值的特征
    """

    # 原始数据
    ori_data = [
        [5, 48, 32, 99],
        [5, 1, 15, 33],
        [5, 3, 2, 10],
        [5, 15, 15, 33]
    ]

    # 实例化一个方差过滤器
    var_thr = VarianceThreshold(threshold=0)

    # 进行特征选择
    output = var_thr.fit_transform(ori_data)

    # 输出结果
    print('原始数据')
    print(ori_data)

    print('特征选择后的数据')
    print(output)


# 主成分分析
def pca_demo():
    """
    主成分分析进行数据降维
    """

    # 原始数据
    ori_data = [
        [5, 48, 32, 99],
        [5, 1, 15, 33],
        [5, 3, 2, 10],
        [5, 15, 15, 33]
    ]

    # 实例化一个主成分分析工具
    pca = PCA(n_components=0.92)

    # 进行主成分分析
    output = pca.fit_transform(ori_data)

    # 输出结果
    print('原始数据')
    print(ori_data)

    print('主成分分析后降维的数据')
    print(output)


if __name__ == '__main__':
    # 运行方差特征选择示例
    var_select()

    # 运行主成分分析示例
    print('-' * 100)
    pca_demo()

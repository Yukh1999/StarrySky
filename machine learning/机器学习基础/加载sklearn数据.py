from sklearn.datasets import load_iris, fetch_20newsgroups, load_boston
from sklearn.model_selection import train_test_split

"""
获取数据集练习
1. load_xxx 都是本地数据集
2. fetch_xxx 都是远程获取的数据集
"""


def print_info():
    """
    输出数据集信息
    """
    # 加载数据集
    li = load_iris()

    # 打印数据
    # 特征值
    print('特征值')
    print(li.data)

    print('-' * 100)
    # 目标值
    print('目标值')
    print(li.target)

    print('-' * 100)
    # 数据集说明
    # print(li.DESCR)

    print('-' * 100)
    # 特征名称
    print('feature names: ', li.feature_names)
    # 目标类别名称
    print('target names: ', li.target_names)


def data_split():
    """
    训练集与测试集数据划分
    """
    # 加载数据
    li = load_iris()

    # 数据划分
    # 返回值为 train_data, train_target, test_data, test_target
    # 输入第一项为特征数据，第二项为目标值
    train_data, train_target, test_data, test_target = train_test_split(li.data, li.target, test_size=0.25)

    # 打印数据
    print('训练特征数据: \n', train_data)
    print('训练目标值: \n', train_target)
    print('测试特征数据: \n', test_data)
    print('测试目标值: \n', test_target)


def news_data():
    """
    获取远程数据: 20组新闻
    """
    # 获取数据集
    news = fetch_20newsgroups(data_home=r'D:\MLDataSet\20newsgroups', subset='all')

    # 打印数据
    print('特征数据: ', news.data)
    print('目标值: ', news.target)


def boston():
    """
    获取回归类型的数据: boston
    目标值连续
    """
    # 获取数据集
    lb = load_boston()

    # 打印数据
    print('特征数据: ', lb.data)
    print('目标值: ', lb.target)


if __name__ == '__main__':
    # 打印数据集的信息
    # print_info()

    # 数据划分
    # data_split()

    # 远程数据: 20组新闻
    # news_data()

    # 回归型数据: boston
    boston()

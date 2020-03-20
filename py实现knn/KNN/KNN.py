import numpy as np
from collections import Counter
from utils.model_selection import train_test_split
from sklearn import datasets
from sklearn.preprocessing import StandardScaler


class KNNClassifier(object):
    """模拟KNN分类器"""
    def __init__(self, k):
        assert k >= 1
        self.k = k
        self.x_train = None
        self.y_train = None

    def fit(self, x_train, y_train):
        self.x_train = x_train
        self.y_train = y_train

    def _predict(self, x):
        """给定单个待预测数据x，返回x的预测结果值"""
        distances = []
        for i in range(len(self.x_train)):
            distance = np.linalg.norm(x-self.x_train[i], 2)
            distances.append((distance, self.y_train[i]))
        distances.sort()
        neightbors = distances[:self.k]
        target = [i[-1] for i in neightbors]
        return Counter(target).most_common()[0][0]

    def predict(self, X_predict):
        """给定待预测数据集X_predict，返回表示X_predict的结果向量"""
        return [self._predict(i) for i in X_predict]

    def score(self, x_test, y_test):
        """根据测试数据集 X_test 和 y_test 确定当前模型的准确度"""
        s = 0
        right = 0
        for i in range(len(x_test)):
            s += 1
            if self._predict(x_test[i]) == y_test[i]:
                right += 1
        return right/s

    def __repr__(self):
        return "KNN(k = %d)" % self.k


if __name__ == "__main__":
    iris = datasets.load_iris()  # 导入数据
    x = iris.data  # 将特征值和目标值分别赋给x，y
    y = iris.target

    # 将数据分为训练集和测试集
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    # 对训练集和测试集中的特征值数据进行标准化
    std = StandardScaler()
    x_train = std.fit_transform(x_train)
    x_test = std.transform(x_test)

    # 使用knn分类器
    knn = KNNClassifier(4)
    knn.fit(x_train, y_train)

    # 输入测试集
    predict = knn.predict(x_test)

    # 准确率
    accuracy = knn.score(x_test, y_test)

    print('训练结果：', predict, '\n', '正确答案：', y_test, '\n', '准确率：', accuracy)


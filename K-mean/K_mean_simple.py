import numpy as np
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans

class Kmean_simple():
    """一个简单的K_mean模型"""
    def __init__(self, k=2, max_iterations=500):
        self.k = k
        self.max_iterations = max_iterations

    def _init_centers(self, X):
        """创建第一批中心点"""
        n_sample, n_featrue = X.shape[0], X.shape[1]
        centers = np.zeros((self.k, n_featrue))
        for i in range(self.k):
            center = X[np.random.randint(n_sample)]
            centers[i] = center
        return centers

    def _create_complexs(self, X, centres):
        """创建各个类的集合体"""
        complexs = [[] for _ in range(self.k)]
        for i_index, i_sample in enumerate(X):
            init_distance = float('inf')
            for j_index, j_center in enumerate(centres):
                distance = np.linalg.norm(i_sample - j_center)
                if distance < init_distance:
                    init_distance = distance
                    sample_type = j_index
            complexs[sample_type].append(i_index)
        return complexs

    def _recenters(self, X, complexs):
        """重新修改中心点"""
        n_featrue = X.shape[1]
        centers = np.zeros((self.k, n_featrue))
        for type_index, type_value in enumerate(complexs):
            new_center = np.mean(X[type_value], axis=0)
            centers[type_index] = new_center
        return centers

    def _get_results(self, X, complexs):
        """得出最后的结果"""
        result_predict = np.zeros((X.shape[0], ))
        for type_index, type_value in enumerate(complexs):
            for sample_index in type_value:
                result_predict[sample_index] = type_index
        return result_predict

    def predict(self, X):
        centres = self._init_centers(X)
        time = 0
        while time < self.max_iterations:
            time += 1
            complexs = self._create_complexs(X, centres)
            pre_centers = centres
            centres = self._recenters(X, complexs)
            if np.linalg.norm(centres-pre_centers) == 0:
                return self._get_results(X, complexs)

if __name__ == "__main__":
    iris = load_iris()
    X = iris['data'][:, (2, 3)]
    y = iris['target']
    KMean = Kmean_simple(k=3)
    Kmean2 = KMeans(n_clusters=3)
    Kmean2.fit(X)
    result = KMean.predict(X)  # 看一下sklearn里面封装好的聚类结果
    result2 = Kmean2.predict(X)
    print(result)
    print(result2)
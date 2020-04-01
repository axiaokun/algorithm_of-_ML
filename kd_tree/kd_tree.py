import numpy as np


class Node:
    def __init__(self, value):
        self.value = value  # 该节点数据
        self.axis = None  # 该节点划分维度
        self.right = None  # 右子树
        self.left = None  # 左子树


def create_tree(values, axis, shape_1):
    """
    递归构造kd树
    :param values: 传入数据，类型array矩阵
    :param axis:   划分维度，类型int
    :param shape_1: 特征数，类型int
    :return:根节点，类型Node object
    """
    if values.size == 0:  # 如果已经没有数据传进，说明已经划分到叶节点了，返回None
        return None
    data_axis = values[:, axis % shape_1]  # 取出划分维度上的数据
    sort_axis = np.sort(data_axis)  # 对划分维度上的数据进行排序
    median_data = sort_axis[sort_axis.__len__() // 2]  # 取出中位数
    left_data = values[values[:, axis % shape_1] < median_data]  # 左子树数据
    right_data = values[values[:, axis % shape_1] > median_data]  # 右子树数据
    node = Node(values[values[:, axis % shape_1] == median_data])  # 该节点
    node.axis = axis % shape_1  # 保存当前划分维度，后面搜索的时候要用到
    node.left = create_tree(left_data, axis + 1, shape_1)  # 递归
    node.right = create_tree(right_data, axis + 1, shape_1)
    return node


def search(root_point, check_point):
    """
    搜索最近邻
    :param root_point: 根节点，类型Node object
    :param check_point: 目标点，类型array矩阵
    :return:
    """
    p_tail = root_point
    stack = []  # 保存路径上的点
    while p_tail is not None:  # 这个while循环是找到最初的那个最近点
        stack.append(p_tail)
        if check_point[:, p_tail.axis] < p_tail.value[:, p_tail.axis]:
            p_tail = p_tail.left
        else:
            p_tail = p_tail.right
    min_distance = np.linalg.norm(check_point - stack[-1].value)
    min_point = stack[-1]
    while len(stack) != 0:
        pop_point = stack.pop()
        distance = np.linalg.norm(check_point - pop_point.value)
        if distance < min_distance:
            min_distance = distance
            min_point = pop_point
        # 下面是一个判断是否回溯的过程，激动死我了，终于想明白怎么弄了
        # 当你判断出父节点的另一个子树中有可能存在更近的点时，一定要重新按照上面那个递归的方法一直递归到底
        # 然后继续寻找，找到就更新最近点和最近距离，找不到更近的点就会一直回溯到栈为空时停止
        if np.linalg.norm(check_point[:, pop_point.axis]-pop_point.value[:, pop_point.axis], ord=1) < min_distance:
            if check_point[:, pop_point.axis]-pop_point.value[:, pop_point.axis] > 0 and pop_point.left is not None:
                p_tail = pop_point.left
                while p_tail is not None:
                    stack.append(p_tail)
                    if check_point[:, p_tail.axis] < p_tail.value[:, p_tail.axis]:
                        p_tail = p_tail.left
                    else:
                        p_tail = p_tail.right
            if check_point[:, pop_point.axis] - pop_point.value[:, pop_point.axis] < 0 and pop_point.right is not None:
                p_tail = pop_point.right
                while p_tail is not None:
                    stack.append(p_tail)
                    if check_point[:, p_tail.axis] < p_tail.value[:, p_tail.axis]:
                        p_tail = p_tail.left
                    else:
                        p_tail = p_tail.right
    return min_distance, min_point


def traver(node):
    if node is None:
        return
    print(node.value)
    traver(node.left)
    traver(node.right)


if __name__ == '__main__':
    data = np.array([[1, 1], [2, 4], [5, 1], [7, 1], [7, 5], [3, 7], [1, 7]])
    root = create_tree(data, 1, data.shape[1])
    # traver(root)
    check_data = np.array([7, 3.5]).reshape((1, 2))
    min_distance, min_point = search(root, check_data)
    print(min_point.value)

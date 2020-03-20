# 线性规划
对于只有一个特征的样本数据，且数据呈线性分布，那么我们可以用一元线性方程$f(x) = ax + b$进行拟合，将其扩展到多元的情况，拟合方程变为：$f(x) = a_1 x_1 + a_2 x_2 + .....a_n x_n + b$。这里特征权重$a_1, a_2.....a_n 以及  偏置项 b$ 是我们通过拟合数据要求出的参数，使用方法为最小二乘法。

**最小二乘法**

对于方程预测值和实际值之间的差距我们称为残差$|f(x_i) - y_i|$由于这个式子并不是处处可导，我们使用其平方$|f(x_i) - y_i|^2$,于是总残差为：
$$D = \sum_{i = 1}^n (y_i - f(x_i))^2$$
通过使残差平方和最小来求出参数。

**向量化**

对于偏置项以及特征权值，我们可以将偏置项作为一个特征值，且特征值为1，作为特征数据集的第一个特征，同时将偏置项的值加入到特征权值中。于是$X = [x_0, x_1, x_2, .... x_n], \theta = [a_0(也就是原来的b), a_1, a_2, .... a_n]^T$于是原来的式子就是$a_1 x_1 + a_2 x_2 + .....a_n x_n + b = X\theta$

<img src = "X_b.jpg">

**注意**这里的传进来的y也要改变一下形状，原来为(len(y), ),矩阵运算时会出错，应该改为(len(y), 1)

改写一下残差平方和，写成矩阵表达式（这里在前面添加一个1/2，方便后序计算）：
$$D = \frac{1}{2}(X\theta - y)^T(X\theta - y)$$
将其展开后就得到下面这个式子(这里自变量变为$\theta$,因为数据是先给定的，我们要通过训练这些数据得到一个较好的参数$\theta$):

$$D(\theta) = \frac{1}{2}(\theta^TX^TX\theta-\theta^TX^Ty - y^TX\theta - y^Ty)$$

接下来我们要用到几个矩阵求导的法则：

$$\frac{dAB}{dB} = A^T$$
$$\frac{dX^TAX}{dX} = 2AX$$
$$\frac{dX^TB}{dX} = B$$

接下来就只要将这些运用到上面得到的矩阵表达式的求导中就可以得到最后的式子：

$$\frac{\partial D(\theta)}{\partial \theta} = X^TX\theta - X^Ty$$

由于函数为一个凸函数，所以令这个导数趋于零，就可以取得令残差平方和最小的参数向量。
$$\theta = (X^TX)^{-1}X^Ty$$

```
self.fit_theta = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)
```
使用np.linalg.inv求逆和.dot()求矩阵相乘。

# 梯度下降——BGD
对于线性模型成本函数：
$$MSE(X, h_\theta) = \frac{1}{m}\sum_{i = 1}^m(X^{(i)} \theta - y^{(i)})^2$$

求偏导得出梯度：
$$\frac{\partial}{\partial \theta_j}MSE = \frac{2}{m}\sum_{i = 1}^m (X^{(i)} \theta - y^{(i)})x_j^{(i)}$$

注意这里的$x_j^{(i)}$为对应取偏导参数$\theta_j$对应的第$j$列上的第$i$个特征值。
例如我们对$\theta_0$求偏导的话，首先$\sum_{i=1}^m (X^{(i)} \theta - y^{(i)}) = X\theta - y = [X^{(1)}\theta - y, X^{(2)} - y, ... , X^{(m)} - y]^T$,然后与$\theta_0$对应特征$X_0$这一列相乘也就是每一个实例的第一个特征值组成的列向量$[X_0^{(0)}, X_0^{(1)}, ...X_0^{(m)}]^T$

于是我们又可以将对某一个$\theta_j$求偏导写成：
$$\frac{2}{m}X_j^T(X\theta - y)$$
这里将第j列的全部特征组成向量进行转置，结果就可以与上面的式子一样。

那么当使用整批数据进行计算时,将$X_j^T$写为$X^T$,此时$X^T$第一行就是原来的第一列且按照原来的顺序排列，同理第二行为原来的第二列，以此类推。
$$\frac{2}{m}X^T(X\theta - y)$$
<img src = "BGD梯度.jpg">

# SGD
成本函数还是一样的。不过这里是随机取实例，使用单个实例计算梯度：
$$\frac{\partial}{\partial \theta_j}MSE = \frac{2}{m}\sum_{i = 1}^m (X^{(i)} \theta - y^{(i)})x_j^{(i)}$$

BGD使用整体全部实例，而随机梯度下降只使用了随机挑选的一个实例，于是当我们算出$\sum_{i=1}^m (X^{(i)} \theta - y^{(i)})$后并不是与每一个实例$\theta_j$对应的特征值相乘，而是只与选出来的实例$\theta_j$对应的特征值相乘。所以最后的式子也不用除以m，而是：
$$X^{(i)^T}(X^{(i)}\theta - y^{(i)})$$
<img src = "SGD梯度.jpg">

也就是图中这一步。

# MBGD 
MBGD介于SGD和BGD这两之间，采用部分的实例计算梯度。借鉴随机梯度下降，这里先随机选择一个实例，接下来利用这个实例更新参数的过程跟随机梯度下降一样。然后接着下一个实例直到达到批次数量后这一次循环才结束。
```
for _ in range(self.batch_size): # 执行一次批次的循环
    i = np.random.randint(sample) # 随机选标签
    X_i = X_b[i: i + 1]
    y_i = y[i: i + 1]
    gradients = 2 * X_i.T.dot(X_i.dot(theta) - y_i)
    theta = theta - self.eta * gradients
```
这里的batch_size为每批次的实例个数， sample为总实例个数。其实对于BGD也可以使用这种方法，改成遍历所有实例数据。

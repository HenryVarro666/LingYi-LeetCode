---
title: "1515. 服务中心的最佳位置"
aliases: ["yiduobo的每日leetcode 1515.服务中心的最佳位置"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/421193407"
zhihu_id: "421193407"
zhihu_title: "yiduobo的每日leetcode 1515.服务中心的最佳位置"
question_id: "1515"
question: "服务中心的最佳位置"
problem_url: "https://leetcode.cn/problems/best-position-for-a-service-centre/"
created: "2021-10-13T23:24:40+08:00"
updated: "2021-10-13T23:24:40+08:00"
upvotes: 1
comments: 0
---

# 1515. 服务中心的最佳位置

> **[yiduobo的每日leetcode 1515.服务中心的最佳位置](https://zhuanlan.zhihu.com/p/421193407) · 知乎 · 2021-10-13 · 赞同 1**
> 力扣：[1515. 服务中心的最佳位置](https://leetcode.cn/problems/best-position-for-a-service-centre/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1515.服务中心的最佳位置

[力扣](https://leetcode-cn.com/problems/best-position-for-a-service-centre/)

在leetcode这类居然还能碰到凸优化问题。

首先，对于服务中心的位置(x, y)，其最终代价为

f(x, y) \= sqrt((x - x[0])^2 + (y - y[0])^2) + sqrt((x - x[1])^2 + (y - y[1])^2) + ... + sqrt((x - x[n - 1])^2 + (y - y[n - 1])^2)

对于判凸而言，经典的做法是通过求二阶偏导得到黑塞矩阵，然后判断黑塞矩阵是否为半正定矩阵。这里得到的黑塞矩阵的主子式都是非负的，也就是说这是一个凸函数。具体的求导这里就不展开了，主要还是知乎这里编辑数学符号确实蛮麻烦的。。

知道f是一个凸函数之后，其局部极值就是全局最优值，那么可以通过经典的凸优化方法来逼近这个极值，例如sgd这类算法。另一个思路就是通过牛顿法、二阶牛顿法来毕竟。我在这里采用的三分法来逼近，即对于凸函数上的区间(l, r)，三分这个区间，选出两个三分点，分别为

m1 \= l + (r - l) / 3

m2 \= l + (r - l) / 3 \* 2

对于m1和m2分别求值，若m1更接近最优值，那么将r移动到m2，否则将l移动到m1。

对于本体而言，f值越小就意味着与最优值越接近，而由于这里有x和y两个变量，因此需要分别进行三分。首先三分x，然后对于得到的mx1和mx2，再三分y，得到此时mx1以及mx2对应的最优的y，然后在确定此时mx1和mx2的优劣性。

最后附上python代码：

```python
class Solution(object):
    def getMinDistSum(self, positions):
        """
        :type positions: List[List[int]]
        :rtype: float
        """

        lx, rx = 0.0, 100.0
        while rx - lx > 0.000001:
            mx1 = lx + (rx - lx) / 3
            mx2 = lx + (rx - lx) / 3 * 2
            dis1 = self.get_dis(mx1, positions)
            dis2 = self.get_dis(mx2, positions)
            if dis1 < dis2:
                rx = mx2
            else:
                lx = mx1
        
        return self.get_dis(lx, positions)
    
    def get_dis(self, xc, positions):
        ly, ry = 0.0, 100.0
        while ry - ly > 0.000001:
            my1 = ly + (ry - ly) / 3
            my2 = ly + (ry - ly) / 3 * 2
            dis1 = dis2 = 0.0
            for x, y in positions:
                dis1 += ((x - xc) ** 2 + (my1 - y) ** 2) ** 0.5
                dis2 += ((x - xc) ** 2 + (my2 - y) ** 2) ** 0.5
            
            if dis1 < dis2:
                ry = my2
            else:
                ly = my1
        
        res = 0.0
        for x, y in positions:
            res += ((x - xc) ** 2 + (ly - y) ** 2) ** 0.5

        return res
```

---
title: "478. 在圆内随机生成点"
aliases: ["yiduobo的每日leetcode 478.在圆内随机生成点"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/243337041"
zhihu_id: "243337041"
zhihu_title: "yiduobo的每日leetcode 478.在圆内随机生成点"
question_id: "478"
question: "在圆内随机生成点"
problem_url: "https://leetcode.cn/problems/generate-random-point-in-a-circle/"
created: "2020-09-14T21:53:25+08:00"
updated: "2020-09-14T21:53:25+08:00"
upvotes: 0
comments: 0
---

# 478. 在圆内随机生成点

> **[yiduobo的每日leetcode 478.在圆内随机生成点](https://zhuanlan.zhihu.com/p/243337041) · 知乎 · 2020-09-14 · 赞同 0**
> 力扣：[478. 在圆内随机生成点](https://leetcode.cn/problems/generate-random-point-in-a-circle/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

478.在圆内随机生成点<https://leetcode-cn.com/problems/generate-random-point-in-a-circle/>

拿到题目的第一想法依然是用拒绝采样法来做，即在-r到r之间随机生成x和y，若(x, y)落在圆内，就将其根据圆心坐标进行平移然后返回即可，否则就重新生成x和y。

不过在这里，如果不用欧式坐标而是用极坐标来看这个问题，就会有不一样的思路。极坐标需要知道的是半径r以及夹角θ。在这里，θ的取值是等概率的，因此可以通过0到1之间的随机值乘上π来得到θ。而对于r，则相对复杂一些。不妨设落在半径等于r，即最外面的圆环上的概率为p，那么对于0到r之间的r'，落在半径为r'的圆环上的概率则应该是两个圆环的周长之比，即p / p' \= 2πr / 2πr'，那么就有p' \= pr' / r。

由于所有的这些概率之和应该为1，那么就可以得到积分式子 $\int_{0}^{r}p'dr' = 1$ ，最后解出来就是p \= 2/r，那么就有p' \= 2r' / r^2。有了p'，就可以得到累积分布函数F(p') \= r'^2/r^2，于是就有r' \= r \* sqrt(F(p'))。

得到了θ和r'之后，将其转化回欧式坐标，然后根据圆心坐标进行平移即可。

最后附上python代码：

```python
import math
import random

class Solution(object):

    def __init__(self, radius, x_center, y_center):
        """
        :type radius: float
        :type x_center: float
        :type y_center: float
        """
        self.radius = radius
        self.x_center = x_center
        self.y_center = y_center

    def randPoint(self):
        """
        :rtype: List[float]
        """
        r = self.radius * sqrt(random.random())
        theta = 2 * math.pi * random.random()
        return [r * math.cos(theta) + self.x_center, r * math.sin(theta) + self.y_center]

# Your Solution object will be instantiated and called as such:
# obj = Solution(radius, x_center, y_center)
# param_1 = obj.randPoint()
```

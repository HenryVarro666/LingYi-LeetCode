---
title: "LCP 37. 最小矩形面积"
aliases: ["yiduobo的每日leetcode LCP37.最小矩形面积"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/575337490"
zhihu_id: "575337490"
zhihu_title: "yiduobo的每日leetcode LCP37.最小矩形面积"
question_id: "LCP 37"
question: "最小矩形面积"
problem_url: "https://leetcode.cn/problems/zui-xiao-ju-xing-mian-ji/"
created: "2022-10-20T04:59:30+08:00"
updated: "2022-10-20T04:59:30+08:00"
upvotes: 1
comments: 0
---

# LCP 37. 最小矩形面积

> **[yiduobo的每日leetcode LCP37.最小矩形面积](https://zhuanlan.zhihu.com/p/575337490) · 知乎 · 2022-10-20 · 赞同 1**
> 力扣：[LCP 37. 最小矩形面积](https://leetcode.cn/problems/zui-xiao-ju-xing-mian-ji/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP37.最小矩形面积

[力扣](https://leetcode.cn/problems/zui-xiao-ju-xing-mian-ji/)

对于本题，由于矩形平行于坐标轴，那么为了使得矩形的面积尽量小，实际上就是需要找到所有交点中最左、最右、最上、最下的点，然后构造一个刚好可以覆盖这四个点的矩形。换言之，就是需要求出所有交点中最大和最小的横坐标以及纵坐标是什么。

题目的数据规模给到了10000，因此最直观的额两两枚举直线计算交点的暴力算法很可能会超时，需要想办法优化。对于这类几何问题，通常是因为存在某种空间结构，所以可以使用贪心法来进行优化，在这里也尝试这往这个路子上去。

在不知道怎么处理的时候，不妨在纸上画一画。简单起见，就先假设有三条直线中相交于一点b，即三条直线

y \= k1 \* x+ b

y \= k2 \* x+ b

y \= k3 \* x + b

在这里不妨设k1 \< k2 \< k3

接下来，尝试对这三条直线做一些上下平移操作，相当于对应的b产生了变化，并观察直线交点的变化。可以发现，横坐标最大和最小的点要么是k1和k2的交点，要么是k2和k3的交点。那么在这里可以大胆猜测，横坐标的最大值和最小值是否必然出现在k值相邻的直线中。

接下来需要想办法进行证明。为了不失一般性，在这里重新给出三条直线的方程，分别为

y \= k1 \* x + b1

y \= k2 \* x + b2

y \= k3 \* x + b3

两两联立这三个方程，就可以得到三条直线的三个交点的坐标，在这里只考虑横坐标。

x12 \= (b1 - b2) / (k2 - k1)

x13 \= (b1 - b3) / (k3 - k1)

x23 \= (b2 - b3) / (k3 - k2)

令a \= b1 - b2，b \= k2 - k1，c \= b2 - b3，d \= k3 - k2，那么

x12 \= a / b

x23 \= c / d

x13 \= (a + c) / (b + d)

同时隐藏条件是b \= k2 - k1 > 0，c \= k3 - k2 > 0

接下来分情况讨论a / b与c / d的大小：

1、若a / b > c / d，即ad > bc，那么

x12 - x13 \= (a(b + d) - b(a + c)) / b(b + d) \= (ad - bc) / b(b + d) > 0，从而有x12 > x13

x23 - x13 \= (c(b + d) - d(a + c)) / d(b + d) \= (bc - ad) / d(b + d) \< 0，从而有x23 \< x13

2、若a / b \= c / d，即ad \= bc，那么

x12 - x13 \= 0，从而有x12 \= x13

x23 - x13 \= 0，从而有x23 \= x13

3、若a / b \< c / d，即ad \< bc，那么

x12 - x13 \= (ad - bc) / b(b + d) \< 0，从而有x12 \< x13

x23 - x13 \= (bc - ad) / d(b + d) > 0，从而有x23 > x13

综合上面三种情况可以发现，当k1 \< k2 \< k3时，三条直线交点x的最大值和最小值必然出现在相邻k值相邻直线的交点中。

上面只考虑了k值不相等的情况，而出现k相等，b不相等时，不妨设存在两条直线

y \= k \* x + b1

y \= k \* x + b2

其中b1 !\= b2

接下来求这两条直线与执行啊y \= kp \* x + bp的交点，那么就有

x1 \= (b1 - bp) / (kp - k)

x2 \= (b2 - bp) / (kp - k)

可以发现，这里x的大小关系完全取决于b1和b2的大小关系。换言之，对于k相等的直线，最大和最小的坐标只会在b最大或b最小的情况下出现，于是对于每种k只需要保留b最大和b最小的两条直线就行了。

综合上面得到的最大和最小x只会出现在k相邻的直线中，那么将所有直线按照k从小到大进行排序，然后枚举所有k相邻的直线，计算对应的最大和最小的x以及y就行了。

具体来说：

1、x \= (b[i] - b[i + 1]) / (k[i +1] - k[i])

由于这里的k[i + 1]一定大于k[i]，那么为了使得x尽量大，b[i]就应该取k \= k[i]时最大的b，而b[i + 1]则应该取k \= k[i + 1]时最小的b。反之，如果要使得x尽量小，那么b[i]就应该尽量小，b[i + 1]就应该尽量大。

2、y \= b[i] + k[i] \* (b[i] - b[i + 1]) / (k[i + 1] - k[i])

由于所有的k都是正数，因此y的最大值和最小值的趋势与x是完全一致的，同样是带入最大的b[i]以及最小的b[i + 1]得到最大的y，最小的b[i]以及最大的b[i + 1]得到最小的y

遍历完成后，计算得到了四个坐标，那么(max_x - min_x) \* (max_y - min_y)就是最终答案。

另外，观察题目给出的样例2，可以发现有特殊情况，即只存在一个交点时，答案为0。另外，如果所有直线全部平行，也就是只存在一种k值，那么答案也是0。

最后附上python代码：

```python
class Solution(object):
    def minRecSize(self, lines):
        """
        :type lines: List[List[int]]
        :rtype: float
        """

        if len(lines) <= 2:
            return 0.0
        
        k_set = set()
        max_b = {}
        min_b = {}
        for k, b in lines:
            if k not in k_set:
                k_set.add(k)
                max_b[k] = b
                min_b[k] = b
            else:
                max_b[k] = max(max_b[k], b)
                min_b[k] = min(min_b[k], b)

        if len(k_set) == 1:
            return 0.0

        left_x = right_x = top_y = botton_y = None
        sorted_k = sorted(list(k_set))
        for index in range(len(sorted_k) - 1):
            k1 = sorted_k[index]
            k2 = sorted_k[index + 1]
            if left_x is None or left_x > (min_b[k1] - max_b[k2]) * 1.0 / (k2 - k1):
                left_x = (min_b[k1] - max_b[k2]) * 1.0 / (k2 - k1)
            if right_x is None or right_x < (max_b[k1] - min_b[k2]) * 1.0 / (k2 - k1):
                right_x = (max_b[k1] - min_b[k2]) * 1.0 / (k2 - k1)
            if top_y is None or top_y < (max_b[k1] - min_b[k2]) * 1.0 / (k2 - k1) * k1 + max_b[k1]:
                top_y = (max_b[k1] - min_b[k2]) * 1.0 / (k2 - k1) * k1 + max_b[k1]
            if botton_y is None or botton_y > (min_b[k1] - max_b[k2]) * 1.0 / (k2 - k1) * k1 + min_b[k1]:
                botton_y = (min_b[k1] - max_b[k2]) * 1.0 / (k2 - k1) * k1 + min_b[k1]

        return (right_x - left_x) * (top_y - botton_y)
```

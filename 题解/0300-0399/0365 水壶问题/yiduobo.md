---
title: "365. 水壶问题"
aliases: ["yiduobo的每日leetcode 365.水壶问题"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/164878585"
zhihu_id: "164878585"
zhihu_title: "yiduobo的每日leetcode 365.水壶问题"
question_id: "365"
question: "水壶问题"
problem_url: "https://leetcode.cn/problems/water-and-jug-problem/"
created: "2020-07-28T21:55:06+08:00"
updated: "2020-07-28T21:55:06+08:00"
upvotes: 0
comments: 0
---

# 365. 水壶问题

> **[yiduobo的每日leetcode 365.水壶问题](https://zhuanlan.zhihu.com/p/164878585) · 知乎 · 2020-07-28 · 赞同 0**
> 力扣：[365. 水壶问题](https://leetcode.cn/problems/water-and-jug-problem/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

365.水壶问题<https://leetcode-cn.com/problems/water-and-jug-problem/>

经典的数学题。

1、对于x + y \< z的情况，必然是False。

2、当z等于0时，必然是True

3、对于x等于0的情况，必须要求y等于z。同样的，对于y等于0的情况，必须要求x等于z。

4、最后则是x和y都不为0的情况。

此时必然是形如ax + by的形式。不妨设x和y的最大公约数为k，设x \= pk，y \= qk，那么ax + by \= k(ap + bq)，其中p和q互质。

此时，若z不为k的倍数，那么必然是False。

若z为k的倍数，那么对于ap + bq，可以使用扩展欧几里得算法计算出ap + bq \= 1的解，于是此时可以通过凑够若干个k达成z。

那么对于这种情况，只需要判断x和y的最大公约数k是否能被z整除即可。

最后附上python代码：

```python
class Solution(object):
    def canMeasureWater(self, x, y, z):
        """
        :type x: int
        :type y: int
        :type z: int
        :rtype: bool
        """

        if x + y < z:
            return False

        if z == 0:
            return True

        if x == 0:
            if y == z:
                return True
            else:
                return False
        if y == 0:
            if x == z:
                return True
            else:
                return False
        
        if x < y:
            x, y = y, x
        while y != 0:
            tmp = x % y
            x = y
            y = tmp
        return z % x == 0
```

---
title: "970. 强整数"
aliases: ["yiduobo的每日leetcode 970.强整数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/362119690"
zhihu_id: "362119690"
zhihu_title: "yiduobo的每日leetcode 970.强整数"
question_id: "970"
question: "强整数"
problem_url: "https://leetcode.cn/problems/powerful-integers/"
created: "2021-04-03T19:17:04+08:00"
updated: "2021-04-03T19:17:04+08:00"
upvotes: 0
comments: 0
---

# 970. 强整数

> **[yiduobo的每日leetcode 970.强整数](https://zhuanlan.zhihu.com/p/362119690) · 知乎 · 2021-04-03 · 赞同 0**
> 力扣：[970. 强整数](https://leetcode.cn/problems/powerful-integers/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

970.强整数

[力扣](https://leetcode-cn.com/problems/powerful-integers/)

首先，我们可以计算出x和y的所有小于等于bound的幂次。当某个数等于1时，其幂次只有1，否则由于其指数增长，其幂次很快就能达到bound，因此总的数量是很少的。

得到所有幂次之后，两两枚举x和y的幂次，若二者之和小于等于bound就将其加入到哈希表中，哈希表中最后所有的key就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def powerfulIntegers(self, x, y, bound):
        """
        :type x: int
        :type y: int
        :type bound: int
        :rtype: List[int]
        """

        pow_x = [1]
        if x > 1:
            while pow_x[-1] * x <= bound:
                pow_x.append(pow_x[-1] * x)
        
        pow_y = [1]
        if y > 1:
            while pow_y[-1] * y <= bound:
                pow_y.append(pow_y[-1] * y)
        
        res_set = set()
        for px in pow_x:
            for py in pow_y:
                if px + py <= bound:
                    res_set.add(px + py)
        
        return list(res_set)
```

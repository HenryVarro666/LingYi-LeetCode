---
title: "1447. 最简分数"
aliases: ["yiduobo的每日leetcode 1447.最简分数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/411190042"
zhihu_id: "411190042"
zhihu_title: "yiduobo的每日leetcode 1447.最简分数"
question_id: "1447"
question: "最简分数"
problem_url: "https://leetcode.cn/problems/simplified-fractions/"
created: "2021-09-16T23:19:06+08:00"
updated: "2021-09-16T23:19:06+08:00"
upvotes: 0
comments: 0
---

# 1447. 最简分数

> **[yiduobo的每日leetcode 1447.最简分数](https://zhuanlan.zhihu.com/p/411190042) · 知乎 · 2021-09-16 · 赞同 0**
> 力扣：[1447. 最简分数](https://leetcode.cn/problems/simplified-fractions/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1447.最简分数

[力扣](https://leetcode-cn.com/problems/simplified-fractions/)

由于这里的n最大只有100，那么可以直接枚举分母和分子，然后对于每一组分母和分子，计算其最大公约数并进行约分即可。

最后附上python代码：

```python
class Solution(object):
    def simplifiedFractions(self, n):
        """
        :type n: int
        :rtype: List[str]
        """

        res = []
        for i in range(2, n + 1):
            for j in range(1, i):
                x = i
                y = j
                while y:
                    x, y = y, x % y

                if x == 1:
                   res.append(str(j) + '/' + str(i))
        
        return res
```

---
title: "1556. 千位分隔数"
aliases: ["yiduobo的每日leetcode 1556.千位分隔数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/426543818"
zhihu_id: "426543818"
zhihu_title: "yiduobo的每日leetcode 1556.千位分隔数"
question_id: "1556"
question: "千位分隔数"
problem_url: "https://leetcode.cn/problems/thousand-separator/"
created: "2021-10-27T23:16:57+08:00"
updated: "2021-10-27T23:16:57+08:00"
upvotes: 0
comments: 0
---

# 1556. 千位分隔数

> **[yiduobo的每日leetcode 1556.千位分隔数](https://zhuanlan.zhihu.com/p/426543818) · 知乎 · 2021-10-27 · 赞同 0**
> 力扣：[1556. 千位分隔数](https://leetcode.cn/problems/thousand-separator/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1556.千位分隔数

[力扣](https://leetcode-cn.com/problems/thousand-separator/)

比较基础的题目，不断将n模1000并除以1000直到n小于1000，并记录下每次模的结果。这样一来按逗号分割的各个部分的值就计算出来了，整理后输出即可。

最后附上python代码：

```python
class Solution(object):
    def thousandSeparator(self, n):
        """
        :type n: int
        :rtype: str
        """

        res = []
        while n >= 1000:
            res.append("%03d" % (n % 1000))
            n /= 1000

        res.append(str(n))
        return '.'.join(res[::-1])
```

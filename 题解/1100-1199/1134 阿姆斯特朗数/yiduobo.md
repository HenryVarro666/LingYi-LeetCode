---
title: "1134. 阿姆斯特朗数"
aliases: ["yiduobo的每日leetcode 1134.阿姆斯特朗数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/610557958"
zhihu_id: "610557958"
zhihu_title: "yiduobo的每日leetcode 1134.阿姆斯特朗数"
question_id: "1134"
question: "阿姆斯特朗数"
problem_url: "https://leetcode.cn/problems/armstrong-number/"
created: "2023-03-01T21:36:07+08:00"
updated: "2023-03-01T21:36:07+08:00"
upvotes: 0
comments: 0
---

# 1134. 阿姆斯特朗数

> **[yiduobo的每日leetcode 1134.阿姆斯特朗数](https://zhuanlan.zhihu.com/p/610557958) · 知乎 · 2023-03-01 · 赞同 0**
> 力扣：[1134. 阿姆斯特朗数](https://leetcode.cn/problems/armstrong-number/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1134.阿姆斯特朗数

[力扣](https://leetcode.cn/problems/armstrong-number/)

逐位分离n的每一位数字，并记录下数字的数位k。接下来遍历这些数字，按照题目给出的定义判断n是否为阿姆斯特朗数即可。

最后附上python代码：

```python
class Solution(object):
    def isArmstrong(self, n):
        """
        :type n: int
        :rtype: bool
        """

        num_list = []
        tmp = n
        while tmp:
            num_list.append(tmp % 10)
            tmp /= 10
        
        s = 0
        for digit in num_list:
            s += digit ** len(num_list)
        
        return s == n
```

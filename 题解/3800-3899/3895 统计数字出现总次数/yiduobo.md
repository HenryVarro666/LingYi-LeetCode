---
title: "3895. 统计数字出现总次数"
aliases: ["yiduobo的每日leetcode 3895.统计数字出现总次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2027506948241725208"
zhihu_id: "2027506948241725208"
zhihu_title: "yiduobo的每日leetcode 3895.统计数字出现总次数"
question_id: "3895"
question: "统计数字出现总次数"
problem_url: "https://leetcode.cn/problems/count-digit-appearances/"
difficulty: "Medium"
created: "2026-04-14T22:04:21+08:00"
updated: "2026-04-14T22:04:21+08:00"
upvotes: 1
comments: 2
---

# 3895. 统计数字出现总次数

> **[yiduobo的每日leetcode 3895.统计数字出现总次数](https://zhuanlan.zhihu.com/p/2027506948241725208) · 知乎 · 2026-04-14 · 赞同 1**
> 力扣：[3895. 统计数字出现总次数](https://leetcode.cn/problems/count-digit-appearances/) · Medium · 灵茶山艾府：[遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3895.统计数字出现总次数

<https://leetcode.cn/problems/count-digit-appearances/description/>

题目给出一个整数数组nums以及一个整数digit。

要求计算nums中所有元素的十进制表示中digit出现的总次数。

对nums进行一趟遍历，对于当前遍历到的元素v，通过模10除以10的方法分离出其中的数位，然后统计digit在其中出现的次数即可。

最后附上python代码：

```python
class Solution(object):
    def countDigitOccurrences(self, nums, digit):
        """
        :type nums: List[int]
        :type digit: int
        :rtype: int
        """
        
        res = 0
        for v in nums:
            while v:
                if v % 10 == digit:
                    res += 1
                v //= 10
        
        return res
```

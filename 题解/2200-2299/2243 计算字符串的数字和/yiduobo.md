---
title: "2243. 计算字符串的数字和"
aliases: ["yiduobo的每日leetcode 2243.计算字符串的数字和"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/545563671"
zhihu_id: "545563671"
zhihu_title: "yiduobo的每日leetcode 2243.计算字符串的数字和"
question_id: "2243"
question: "计算字符串的数字和"
problem_url: "https://leetcode.cn/problems/calculate-digit-sum-of-a-string/"
difficulty: "Easy"
created: "2022-07-24T18:11:47+08:00"
updated: "2022-07-24T18:11:47+08:00"
upvotes: 0
comments: 0
---

# 2243. 计算字符串的数字和

> **[yiduobo的每日leetcode 2243.计算字符串的数字和](https://zhuanlan.zhihu.com/p/545563671) · 知乎 · 2022-07-24 · 赞同 0**
> 力扣：[2243. 计算字符串的数字和](https://leetcode.cn/problems/calculate-digit-sum-of-a-string/) · Easy · 灵茶山艾府：[模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2243.计算字符串的数字和

[力扣](https://leetcode.cn/problems/calculate-digit-sum-of-a-string/)

没有什么好的思路，不过好在题目给出的字符串长度比较短，因此可以直接按照题目描述的操作进行模拟，不断重复拆分-求和-合并，直到字符串的长度小于等于k为止。

最后附上python代码：

```python
class Solution(object):
    def digitSum(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: str
        """

        num_list = [int(x) for x in list(s)]
        while len(num_list) > k:
            next_list = []
            for start in range(0, len(num_list), k):
                next_list.append(0)
                for index in range(start, min(start + k, len(num_list))):
                    next_list[-1] += num_list[index]
            
            next_s = ''.join([str(x) for x in next_list])
            num_list = [int(x) for x in list(next_s)]

        return ''.join([str(x) for x in num_list])
```

---
title: "1423. 可获得的最大点数"
aliases: ["yiduobo的每日leetcode 1423.可获得的最大点数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/一-定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/408404301"
zhihu_id: "408404301"
zhihu_title: "yiduobo的每日leetcode 1423.可获得的最大点数"
question_id: "1423"
question: "可获得的最大点数"
problem_url: "https://leetcode.cn/problems/maximum-points-you-can-obtain-from-cards/"
difficulty: "Medium"
rating: 1574
created: "2021-09-08T23:31:37+08:00"
updated: "2021-09-08T23:31:37+08:00"
upvotes: 1
comments: 0
---

# 1423. 可获得的最大点数

> **[yiduobo的每日leetcode 1423.可获得的最大点数](https://zhuanlan.zhihu.com/p/408404301) · 知乎 · 2021-09-08 · 赞同 1**
> 力扣：[1423. 可获得的最大点数](https://leetcode.cn/problems/maximum-points-you-can-obtain-from-cards/) · Medium · 灵茶山艾府：[两种方法：逆向思维/正向思维（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1423.可获得的最大点数

[力扣](https://leetcode-cn.com/problems/maximum-points-you-can-obtain-from-cards/)

按照题目的意思，如果每一步都只能从当前剩下数字的两端来取，那么最后拿到的答案必然是一个前缀与一个后缀。于是我们可以先预处理出前缀和，然后从后往前一趟扫描，在计算后缀的同时可以根据这个后缀长度确定对应的前缀长度，然后使用这个和来更新答案即可。

需要注意判断后缀长度为0的情况。

最后附上python代码：

```python
class Solution(object):
    def maxScore(self, cardPoints, k):
        """
        :type cardPoints: List[int]
        :type k: int
        :rtype: int
        """

        left = [0]
        for point in cardPoints[:k]:
            left.append(left[-1] + point)
        
        res = left[-1]
        right = 0
        for index in range(1, k + 1):
            right += cardPoints[-index]
            res = max(res, right + left[-index - 1])
        
        return res
```

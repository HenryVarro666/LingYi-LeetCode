---
title: "2264. 字符串中最大的3位相同数字"
aliases: ["yiduobo的每日leetcode 2264.字符串中最大的3位相同数字"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/enumeration", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/548784464"
zhihu_id: "548784464"
zhihu_title: "yiduobo的每日leetcode 2264.字符串中最大的3位相同数字"
question_id: "2264"
question: "字符串中最大的 3 位相同数字"
problem_url: "https://leetcode.cn/problems/largest-3-same-digit-number-in-string/"
difficulty: "Easy"
rating: 1309
created: "2022-08-01T23:49:37+08:00"
updated: "2022-08-01T23:49:37+08:00"
upvotes: 0
comments: 0
---

# 2264. 字符串中最大的3位相同数字

> **[yiduobo的每日leetcode 2264.字符串中最大的3位相同数字](https://zhuanlan.zhihu.com/p/548784464) · 知乎 · 2022-08-01 · 赞同 0**
> 力扣：[2264. 字符串中最大的 3 位相同数字](https://leetcode.cn/problems/largest-3-same-digit-number-in-string/) · Easy · 灵茶山艾府：[两种方法：十次遍历 / 一次遍历+优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2264.字符串中最大的3位相同数字

[力扣](https://leetcode.cn/problems/largest-3-same-digit-number-in-string/)

从字符串中下标2开始向后遍历，若当前字符与上一个及上上个字符相同，那么说明这三个字符能形成一个优质整数，使用这个值来更新答案就行了。

最后附上python代码：

```python
class Solution(object):
    def largestGoodInteger(self, num):
        """
        :type num: str
        :rtype: str
        """

        res = -1
        for index in range(2, len(num)):
            if num[index] == num[index - 1] == num[index - 2]:
                res = max(res, int(num[index]))
        
        if res == -1:
            return ''
        
        return str(res) * 3
```

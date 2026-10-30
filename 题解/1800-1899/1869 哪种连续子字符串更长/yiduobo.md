---
title: "1869. 哪种连续子字符串更长"
aliases: ["yiduobo的每日leetcode 1869.哪种连续子字符串更长"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/474441248"
zhihu_id: "474441248"
zhihu_title: "yiduobo的每日leetcode 1869.哪种连续子字符串更长"
question_id: "1869"
question: "哪种连续子字符串更长"
problem_url: "https://leetcode.cn/problems/longer-contiguous-segments-of-ones-than-zeros/"
difficulty: "Easy"
rating: 1205
created: "2022-03-02T01:08:41+08:00"
updated: "2022-03-02T01:08:41+08:00"
upvotes: 0
comments: 0
---

# 1869. 哪种连续子字符串更长

> **[yiduobo的每日leetcode 1869.哪种连续子字符串更长](https://zhuanlan.zhihu.com/p/474441248) · 知乎 · 2022-03-02 · 赞同 0**
> 力扣：[1869. 哪种连续子字符串更长](https://leetcode.cn/problems/longer-contiguous-segments-of-ones-than-zeros/) · Easy · 灵茶山艾府：[分组循环](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1869.哪种连续子字符串更长

[力扣](https://leetcode-cn.com/problems/longer-contiguous-segments-of-ones-than-zeros/)

比较基础的题目，直接从头开始向后一趟遍历，使用一个变量last记录当前连续子字符串的开端位置。对于当前字符，若其不等于前一个字符，说明上一段连续子字符串已经结束了，因此可以使用当前下标index与last，以及上一个字符是0还是1来更新最长连续0的长度或者最长连续1的长度，同时重置last为index。

遍历完成后，对比最长0和最长1的长度返回结果即可。

需要注意在遍历完成后，最后一个连续子字符串由于没有遇到不同的字符，因此其的长度是没有被计算过的，需要单独拿出来计算。

最后附上python代码：

```python
class Solution(object):
    def checkZeroOnes(self, s):
        """
        :type s: str
        :rtype: bool
        """

        last = 0
        max_zero = max_one = 0
        res = 0
        for index, char in enumerate(s):
            if index == 0:
                last = 0
            elif char != s[index - 1]:
                if char == '1':
                    max_zero = max(max_zero, index - last)
                else:
                    max_one = max(max_one, index - last)
                last = index
        
        if s[-1] == '1':
            max_one = max(max_one, len(s) - last)
        else:
            max_zero = max(max_zero, len(s) - last)
        
        return max_one > max_zero
```

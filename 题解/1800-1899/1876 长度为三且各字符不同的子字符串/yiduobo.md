---
title: "1876. 长度为三且各字符不同的子字符串"
aliases: ["yiduobo的每日leetcode 1876.长度为三且各字符不同的子字符串"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/475563927"
zhihu_id: "475563927"
zhihu_title: "yiduobo的每日leetcode 1876.长度为三且各字符不同的子字符串"
question_id: "1876"
question: "长度为三且各字符不同的子字符串"
problem_url: "https://leetcode.cn/problems/substrings-of-size-three-with-distinct-characters/"
difficulty: "Easy"
created: "2022-03-04T03:01:52+08:00"
updated: "2022-03-04T03:01:52+08:00"
upvotes: 0
comments: 0
---

# 1876. 长度为三且各字符不同的子字符串

> **[yiduobo的每日leetcode 1876.长度为三且各字符不同的子字符串](https://zhuanlan.zhihu.com/p/475563927) · 知乎 · 2022-03-04 · 赞同 0**
> 力扣：[1876. 长度为三且各字符不同的子字符串](https://leetcode.cn/problems/substrings-of-size-three-with-distinct-characters/) · Easy · 灵茶山艾府：[模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1876.长度为三且各字符不同的子字符串

[力扣](https://leetcode-cn.com/problems/substrings-of-size-three-with-distinct-characters/)

由于字符长度比较小，因此各种算法都是可以的。我在这里采用的是类似滑动窗口的做法，使用两个遍历分别保留窗口中的第一个字符和第二个字符。对于当前字符，若三个字符不相等，那么将答案加上1，接下来窗口向右移动，此时的原来的第二个字符就变成了新的第一个字符，而当前字符则变成了新的第二个字符。

最后附上python代码：

```python
class Solution(object):
    def countGoodSubstrings(self, s):
        """
        :type s: str
        :rtype: int
        """

        if len(s) < 3:
            return 0

        first = s[0]
        second = s[1]
        res = 0
        for now in s[2:]:
            if first != second and first != now and second != now:
                res += 1
            first, second = second, now
        
        return res
```

---
title: "3114. 替换字符可以得到的最晚时间"
aliases: ["yiduobo的每日leetcode 3114.替换字符可以得到的最晚时间"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/enumeration"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/701137736"
zhihu_id: "701137736"
zhihu_title: "yiduobo的每日leetcode 3114.替换字符可以得到的最晚时间"
question_id: "3114"
question: "替换字符可以得到的最晚时间"
problem_url: "https://leetcode.cn/problems/latest-time-you-can-obtain-after-replacing-characters/"
difficulty: "Easy"
created: "2024-06-01T23:19:09+08:00"
updated: "2024-06-01T23:19:09+08:00"
upvotes: 1
comments: 0
---

# 3114. 替换字符可以得到的最晚时间

> **[yiduobo的每日leetcode 3114.替换字符可以得到的最晚时间](https://zhuanlan.zhihu.com/p/701137736) · 知乎 · 2024-06-01 · 赞同 1**
> 力扣：[3114. 替换字符可以得到的最晚时间](https://leetcode.cn/problems/latest-time-you-can-obtain-after-replacing-characters/) · Easy · 灵茶山艾府：[两种方法：枚举/直接判断（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3114.替换字符可以得到的最晚时间

[. - 力扣（LeetCode）](https://leetcode.cn/problems/latest-time-you-can-obtain-after-replacing-characters/description/)

题目给出一个带问号的十二小时制的时间字符串，要求填充其中的问号使得时间最晚。

由于是十二小时制的，那么小时位上最多是11，分钟位则是59。

对于小时位，若高位和低位都是问号，则填充11；若仅有高位为问号，那么只有当低位上为0或者1时，高位上才能填充1，否则只能填充0；若仅有低位为问号，那么只有当高位为0时，低位上才能填充9，否则只能填充1。

分钟位则比较简单，高位上为问号则填5，低位上为问号则填9。

最后附上python代码：

```python
class Solution(object):
    def findLatestTime(self, s):
        """
        :type s: str
        :rtype: str
        """

        res = list(s)
        if res[0] == '?':
            if res[1] == '?':
                res[0] = '1'
                res[1] = '1'
            elif res[1] <= '1':
                res[0] = '1'
            else:
                res[0] = '0'
        
        elif res[1] == '?':
            if res[0] == '0':
                res[1] = '9'
            else:
                res[1] = '1'
        

        if res[3] == '?':
            res[3] = '5'
        if res[4] == '?':
            res[4] = '9'
        
        return ''.join(res)
```

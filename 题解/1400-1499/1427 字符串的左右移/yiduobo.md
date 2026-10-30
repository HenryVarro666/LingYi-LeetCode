---
title: "1427. 字符串的左右移"
aliases: ["yiduobo的每日leetcode 1427.字符串的左右移"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/616227848"
zhihu_id: "616227848"
zhihu_title: "yiduobo的每日leetcode 1427.字符串的左右移"
question_id: "1427"
question: "字符串的左右移"
problem_url: "https://leetcode.cn/problems/perform-string-shifts/"
created: "2023-03-22T23:10:48+08:00"
updated: "2023-03-22T23:10:48+08:00"
upvotes: 0
comments: 0
---

# 1427. 字符串的左右移

> **[yiduobo的每日leetcode 1427.字符串的左右移](https://zhuanlan.zhihu.com/p/616227848) · 知乎 · 2023-03-22 · 赞同 0**
> 力扣：[1427. 字符串的左右移](https://leetcode.cn/problems/perform-string-shifts/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1427.字符串的左右移

[力扣](https://leetcode.cn/problems/perform-string-shifts/)

可以发现，题目中向右移动i位实际上可以认为是向左移动了n - i位，因此可以将所有的移动操作都视为向左移动，然后将移动的位数累加起来，这个累加和对n取模就得到了最终向左移动的位数。

最后附上python代码：

```python
class Solution(object):
    def stringShift(self, s, shift):
        """
        :type s: str
        :type shift: List[List[int]]
        :rtype: str
        """

        n = len(s)
        cnt = 0
        for d, a in shift:
            if d == 0:
                cnt += a
            else:
                cnt += n - a
        
        cnt %= n
        return s[cnt:] + s[:cnt]
```

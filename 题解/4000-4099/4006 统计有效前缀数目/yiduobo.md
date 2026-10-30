---
title: "4006. 统计有效前缀数目"
aliases: ["yiduobo的每日leetcode 4006.统计有效前缀数目"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2068104469099947066"
zhihu_id: "2068104469099947066"
zhihu_title: "yiduobo的每日leetcode 4006.统计有效前缀数目"
question_id: "4006"
question: "统计有效前缀数目"
problem_url: "https://leetcode.cn/problems/count-valid-prefixes/"
difficulty: "Easy"
created: "2026-08-04T22:46:23+08:00"
updated: "2026-08-04T22:46:23+08:00"
upvotes: 1
comments: 0
---

# 4006. 统计有效前缀数目

> **[yiduobo的每日leetcode 4006.统计有效前缀数目](https://zhuanlan.zhihu.com/p/2068104469099947066) · 知乎 · 2026-08-04 · 赞同 1**
> 力扣：[4006. 统计有效前缀数目](https://leetcode.cn/problems/count-valid-prefixes/) · Easy · 灵茶山艾府：[O(n) 一次遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4006.统计有效前缀数目

<https://leetcode.cn/problems/count-valid-prefixes/description/>

题目给出一个二进制字符串s。

对于s中的某个前缀，若这个前缀可以重新排列成交替字符串，那么该前缀则被认为是有效的。

问s中有效前缀的数目。

一个01字符串可以被重新排列成交替字符串，那么其重新排列后要么是101010...的形式，要么是010101...的形式。对于前面这种情况，1的数量要么和0相等，要么比0的数量多1个。对于后面这种情况，0的数量要么和1相等，要么比1的数量多1个。

也就是说，对于一个前缀字符串，若其中0的数量与1的数量之差diff的绝对值不超过1，那么这个前缀就是有效的。于是可以一趟遍历，计算每种前缀中0和1数量之差，若这个差的绝对值不超过1，则更新答案。

最后附上python代码：

```python
class Solution(object):
    def countValidPrefixes(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        diff = 0
        res = 0
        for c in s:
            if c == '1':
                diff += 1
            else:
                diff -= 1
            
            if abs(diff) <= 1:
                res += 1
        
        return res
```

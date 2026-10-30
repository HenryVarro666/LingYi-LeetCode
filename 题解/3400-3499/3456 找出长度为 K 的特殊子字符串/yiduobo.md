---
title: "3456. 找出长度为K的特殊子字符串"
aliases: ["yiduobo的每日leetcode 3456.找出长度为K的特殊子字符串"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1894146703390642737"
zhihu_id: "1894146703390642737"
zhihu_title: "yiduobo的每日leetcode 3456.找出长度为K的特殊子字符串"
question_id: "3456"
question: "找出长度为 K 的特殊子字符串"
problem_url: "https://leetcode.cn/problems/find-special-substring-of-length-k/"
difficulty: "Easy"
rating: 1244
created: "2025-04-11T22:03:38+08:00"
updated: "2025-04-11T22:03:51+08:00"
upvotes: 0
comments: 0
---

# 3456. 找出长度为K的特殊子字符串

> **[yiduobo的每日leetcode 3456.找出长度为K的特殊子字符串](https://zhuanlan.zhihu.com/p/1894146703390642737) · 知乎 · 2025-04-11 · 赞同 0**
> 力扣：[3456. 找出长度为 K 的特殊子字符串](https://leetcode.cn/problems/find-special-substring-of-length-k/) · Easy · 灵茶山艾府：[一次遍历，简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3456.找出长度为K的子字符串

[3456. 找出长度为 K 的特殊子字符串 - 力扣（LeetCode）](https://leetcode.cn/problems/find-special-substring-of-length-k/description/)

题目给出一个字符串s以及一个整数k。要求判断是否存在一个长度为k的子串，这个子串中仅包含一种字符，同时这个子串中的字符不能与这个子串相邻的左侧或者右侧字符相同。

一趟遍历，使用两个指针将s中所有由相同的字符构成的子串分离出来。若某个子串长度恰好为k，那么答案为true，否则为false。

具体的分离方法为初始化起点p为0，然后让q从p + 1开始不断向后移动，直到q来到s末尾或者s[q]不等于s[p]为止。那么p到q - 1这一段，也就是s[p: q]中的字符都是相同的，此时需要检测这个子串的长度，也就是q减去p是否恰好等于k，若等于，则返回true，否则就将p迭代到q的位置，然后继续向后检测，直到p来到s的末尾。

最后附上python代码：

```python
class Solution(object):
    def hasSpecialSubstring(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: bool
        """
        
        p = 0
        while p < len(s):
            q = p + 1
            while q < len(s) and s[p] == s[q]:
                q += 1
            
            if q - p == k:
                return True
            
            p = q
        
        return False
```

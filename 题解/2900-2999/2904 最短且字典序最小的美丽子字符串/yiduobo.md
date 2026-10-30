---
title: "2904. 最短且字典序最小的美丽子字符串"
aliases: ["yiduobo的每日leetcode 2904.最短且字典序最小的美丽子字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/字符串", "题单/滑动窗口与双指针/二-不定长滑动窗口", "题单/字符串/八-后缀数组/后缀自动机"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/663895758"
zhihu_id: "663895758"
zhihu_title: "yiduobo的每日leetcode 2904.最短且字典序最小的美丽子字符串"
question_id: "2904"
question: "最短且字典序最小的美丽子字符串"
problem_url: "https://leetcode.cn/problems/shortest-and-lexicographically-smallest-beautiful-string/"
difficulty: "Medium"
created: "2023-10-29T00:01:07+08:00"
updated: "2023-10-29T00:01:07+08:00"
upvotes: 0
comments: 0
---

# 2904. 最短且字典序最小的美丽子字符串

> **[yiduobo的每日leetcode 2904.最短且字典序最小的美丽子字符串](https://zhuanlan.zhihu.com/p/663895758) · 知乎 · 2023-10-29 · 赞同 0**
> 力扣：[2904. 最短且字典序最小的美丽子字符串](https://leetcode.cn/problems/shortest-and-lexicographically-smallest-beautiful-string/) · Medium · 灵茶山艾府：[两种方法：枚举/滑动窗口（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2904.最短且字典序最小的美丽子字符串

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/shortest-and-lexicographically-smallest-beautiful-string/description/)

经典的变长滑动窗口问题。为了使得最终答案最小，那么答案字符串必然以1开头，再以1结尾，因此可以先将窗口左边界滑动到剩余字符串中最左侧1所在的位置，然后将右边界在上一轮的基础上滑动到下一个1，然后使用窗口内的子串更新答案。滑动的过程中，若剩余窗口中1的数量不足，那么就可以直接退出循环。

最后附上python代码：

```python
class Solution(object):
    def shortestBeautifulSubstring(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: str
        """

        res = ''
        p = 0
        q = 0
        cnt = 0
        while p < len(s):
            while p < len(s) and s[p] == '0':
                p += 1

            if p == len(s):
                break

            if q < p:
                q = p
            while q < len(s) and cnt < k:
                if s[q] == '1':
                    cnt += 1
                q += 1
            
            if cnt < k:
                break

            if len(res) == 0 or len(res) > q - p or (len(res) == q - p and res > s[p : q]):
                res = s[p: q]

            cnt -= 1
            p += 1
        
        return res
```

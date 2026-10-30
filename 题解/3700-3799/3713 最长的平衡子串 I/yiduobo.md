---
title: "3713. 最长的平衡子串I"
aliases: ["yiduobo的每日leetcode 3713.最长的平衡子串I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/enumeration", "leetcode/bao-li", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1961925501846267760"
zhihu_id: "1961925501846267760"
zhihu_title: "yiduobo的每日leetcode 3713.最长的平衡子串I"
question_id: "3713"
question: "最长的平衡子串 I"
problem_url: "https://leetcode.cn/problems/longest-balanced-substring-i/"
difficulty: "Medium"
created: "2025-10-15T22:59:30+08:00"
updated: "2025-10-15T22:59:31+08:00"
upvotes: 3
comments: 0
---

# 3713. 最长的平衡子串I

> **[yiduobo的每日leetcode 3713.最长的平衡子串I](https://zhuanlan.zhihu.com/p/1961925501846267760) · 知乎 · 2025-10-15 · 赞同 3**
> 力扣：[3713. 最长的平衡子串 I](https://leetcode.cn/problems/longest-balanced-substring-i/) · Medium · 灵茶山艾府：[两种方法：暴力枚举 / 枚举右维护左（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3713.最长的平衡子串I

[3713. 最长的平衡子串 I - 力扣（LeetCode）](https://leetcode.cn/problems/longest-balanced-substring-i/description/)

题目给出一个由小写英文字母组成的字符串s，s的长度不超过1000。

对于一个子串，若子串中所有不同子串出现的次数都相同，那么就称其为平衡子串。

要求找出s中最长平衡子串的长度。

题目的数据规模不大，因此可以枚举s中所有子串的起点和终点，然后检测当前子串中每种字符出现的次数是否都相同。若是，则可以使用子串的长度更新答案。

需要注意的是，在这里如果对于每个子串都进行一趟遍历来统计每种字符出现次数的话，时间复杂度就太高了。对于子串s[left: right + 1]中每种字符出现的次数，可以认为是在s[left: right]中每种字符出现次数的基础上，额外添加s[right]得到。

基于这一点，就可以遍历每种left，对于当前的left，让right从left出发向后遍历，使用一个哈希表freq记录当前子串中每种字符出现的次数，同时使用另一个哈希表freq_freq记录freq中每种次数出现的次数。对于当前的遍历到的right，先更新s\[right\]出现的次数freq\[s\[right\]\]，记为f，然后更新f出现的次数freq_freq\[f\]。需要注意，若此时的f大于1，就说明f是从f - 1变化而来的，此时应该将freq_freq\[f - 1\]减去1，若其变为0，则应该将f - 1从freq_freq中弹出。这样一来，freq_freq中记录的就是当前子串中每种字符出现次数的次数，若freq_freq中仅有一个元素，就说明当前子串中仅有一种次数，即每种字符出现的次数相同，此时就可以使用子串的长度更新答案了。

最后附上python代码：

```python
class Solution(object):
    def longestBalanced(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        n = len(s)
        res = 0
        for left in range(n):
            freq = {}
            freq_freq = {}
            for right in range(left, n):
                freq[s[right]] = freq.get(s[right], 0) + 1
                f = freq[s[right]]
                freq_freq[f] = freq_freq.get(f, 0) + 1
                if f > 1:
                    freq_freq[f - 1] -= 1
                    if freq_freq[f - 1] == 0:
                        freq_freq.pop(f - 1)
                
                if len(freq_freq) == 1:
                    res = max(res, right - left + 1)
        
        return res
```

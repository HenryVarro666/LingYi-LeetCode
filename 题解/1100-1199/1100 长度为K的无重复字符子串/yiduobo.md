---
title: "1100. 长度为K的无重复字符子串"
aliases: ["yiduobo的每日leetcode 1100.长度为K的无重复字符子串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/609406138"
zhihu_id: "609406138"
zhihu_title: "yiduobo的每日leetcode 1100.长度为K的无重复字符子串"
question_id: "1100"
question: "长度为K的无重复字符子串"
problem_url: "https://leetcode.cn/problems/find-k-length-substrings-with-no-repeated-characters/"
created: "2023-02-25T17:33:00+08:00"
updated: "2023-02-25T17:33:00+08:00"
upvotes: 1
comments: 0
---

# 1100. 长度为K的无重复字符子串

> **[yiduobo的每日leetcode 1100.长度为K的无重复字符子串](https://zhuanlan.zhihu.com/p/609406138) · 知乎 · 2023-02-25 · 赞同 1**
> 力扣：[1100. 长度为K的无重复字符子串](https://leetcode.cn/problems/find-k-length-substrings-with-no-repeated-characters/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1100.长度为K的无重复字符子串

[力扣](https://leetcode.cn/problems/find-k-length-substrings-with-no-repeated-characters/)

非常标准的滑动窗口问题。首先还是先考虑边界情况。若整个字符串的长度都小于k，那么答案必然为0，直接返回0即可。

反之，若字符串的长度大于等于k，那么就按照常规滑动窗口的方式进行处理。

使用一个哈希表记录窗口内各个字符出现的次数，然后使用字符串中的前k个字符初始化哈希表。若此时哈希表中的key恰好是k个，说明当前窗口中有k个字符，且每个字符恰好出现了一次，因此需要初始化答案为1，否则初始化答案为0。

接下来从字符串的第k + 1个字符，也就是下标k开始向后遍历。对于当前遍历到的下标index，将s[index]在哈希表中的计数加上1，同时将窗口左侧被移除的字符，也就是s[index - k]在哈希表中的计数减去1。需要注意的是，若此时这个左侧字符在哈希表中的计数为0，那么就将其从哈希表中移除。

在窗口移动后，若哈希表中记录的字符数恰好为k，那么说明每种字符都恰好出现了一次，也就是说此时对应的窗口是一个合法的子串，因此需要将答案加上1。

最后附上python代码：

```python
class Solution(object):
    def numKLenSubstrNoRepeats(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """

        n = len(s)
        if n < k:
            return 0
        
        cnt = {}
        for char in s[:k]:
            cnt[char] = cnt.get(char, 0) + 1
        
        if len(cnt) == k:
            res = 1
        else:
            res = 0
        
        for index, char in enumerate(s[k:]):
            cnt[char] = cnt.get(char, 0) + 1
            cnt[s[index]] -= 1
            if cnt[s[index]] == 0:
                cnt.pop(s[index])
            
            if len(cnt) == k:
                res += 1
        
        return res
```

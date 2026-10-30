---
title: "3692. 众数频率字符"
aliases: ["yiduobo的每日leetcode 3692.众数频率字符"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1956110548740596249"
zhihu_id: "1956110548740596249"
zhihu_title: "yiduobo的每日leetcode 3692.众数频率字符"
question_id: "3692"
question: "众数频率字符"
problem_url: "https://leetcode.cn/problems/majority-frequency-characters/"
difficulty: "Easy"
created: "2025-09-30T22:45:02+08:00"
updated: "2025-09-30T22:45:03+08:00"
upvotes: 1
comments: 0
---

# 3692. 众数频率字符

> **[yiduobo的每日leetcode 3692.众数频率字符](https://zhuanlan.zhihu.com/p/1956110548740596249) · 知乎 · 2025-09-30 · 赞同 1**
> 力扣：[3692. 众数频率字符](https://leetcode.cn/problems/majority-frequency-characters/) · Easy · 灵茶山艾府：[按照字母出现次数分组（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3692.众数频率字符

[3692. 众数频率字符 - 力扣（LeetCode）](https://leetcode.cn/problems/majority-frequency-characters/description/)

题目给出一个由小写英文字母组成的字符串s，对于一个值k，频率组指的是s中恰好出现k次的字符结合。

众数频率组是包含不同字符数量最多的频率组。

现在要求返回一个字符串，其中包含众数频率组中的所有字符。若两个频率组的大小并列最大，则选择其频率k较大的那个组。

题目描述看上去很绕，实际上就是要先计算出字符串中每种字符出现的次数，接下来计算出这些次数出现的次数，然后取其中次数的次数最大的那一组。若由多个次数的次数最大，则取对应次数最大的那一组。

具体实现上，先使用一个哈希表freq记录每种字符出现的次数，接下来对于freq中记录的每种次数，使用另一个哈希表freq_group记录每种次数出现的次数，然后再一趟遍历，取出其中次数的次数最大、且次数也最大的那一组，并记录其对应的次数ma_f。最后，再遍历freq，将其中次数恰好等于ma_f的字符加入到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def majorityFrequencyGroup(self, s):
        """
        :type s: str
        :rtype: str
        """
        
        freq = {}
        for c in s:
            freq[c] = freq.get(c, 0) + 1
        
        freq_group = {}
        for f in freq.values():
            freq_group[f] = freq_group.get(f, 0) + 1
        
        ma = 0
        ma_f = None
        for f in freq_group:
            if freq_group[f] > ma or (freq_group[f] == ma and f > ma_f):
                ma = freq_group[f]
                ma_f = f
        
        res = []
        for c in freq:
            if freq[c] == ma_f:
                res.append(c)
        
        return ''.join(res)
```

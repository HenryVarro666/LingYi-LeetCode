---
title: "3839. 前缀连接组的数目"
aliases: ["yiduobo的每日leetcode 3839.前缀连接组的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2010128224479360158"
zhihu_id: "2010128224479360158"
zhihu_title: "yiduobo的每日leetcode 3839.前缀连接组的数目"
question_id: "3839"
question: "前缀连接组的数目"
problem_url: "https://leetcode.cn/problems/number-of-prefix-connected-groups/"
difficulty: "Medium"
created: "2026-02-26T21:56:37+08:00"
updated: "2026-02-26T21:56:38+08:00"
upvotes: 1
comments: 0
---

# 3839. 前缀连接组的数目

> **[yiduobo的每日leetcode 3839.前缀连接组的数目](https://zhuanlan.zhihu.com/p/2010128224479360158) · 知乎 · 2026-02-26 · 赞同 1**
> 力扣：[3839. 前缀连接组的数目](https://leetcode.cn/problems/number-of-prefix-connected-groups/) · Medium · 灵茶山艾府：[阅读理解题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3839.前缀连接组的数目

<https://leetcode.cn/problems/number-of-prefix-connected-groups/description/>

题目给出一个字符串数组words以及一个整数k。

若两个位于不同下标的单词a和b满足a[0..k - 1] \=\= b[0..k - 1]，那么就称它们是前缀连接的。

一个连接组是指一组单词，其中每对单词都是前缀连接的。若两个单词是前缀连接的，那么它们就必须被分到同一组中。需要注意，长度小于k的单词不能加入任何组，应该被忽略。

要求计算words中形成包含至少两个单词的连接组数目。

题目中的前缀连接实际上就是长度为k的前缀相同，同时题目需要计算的是连接组的数目，不需要记录原始单词，于是可以一趟遍历，将每个单词转化为其前k个字符形成的前缀。若某个单词的长度不足k，则直接跳过。接下来对于这些长度为k的前缀，使用哈希表统计每种前缀出现的次数，而最终答案就是哈希表中值大于1的元素数目，对应的就是包含单词数目至少两个的连接组的数目。

最后附上python代码：

```python
class Solution(object):
    def prefixConnected(self, words, k):
        """
        :type words: List[str]
        :type k: int
        :rtype: int
        """
        
        freq = {}
        for w in words:
            if len(w) < k:
                continue
            prefix = w[:k]
            freq[prefix] = freq.get(prefix, 0) + 1
        
        res = 0
        for p in freq:
            if freq[p] > 1:
                res += 1
        
        return res
```

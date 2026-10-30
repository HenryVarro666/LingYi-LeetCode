---
title: "3805. 统计凯撒加密对数目"
aliases: ["yiduobo的每日leetcode 3805.统计凯撒加密对数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1993703276894507533"
zhihu_id: "1993703276894507533"
zhihu_title: "yiduobo的每日leetcode 3805.统计凯撒加密对数目"
question_id: "3805"
question: "统计凯撒加密对数目"
problem_url: "https://leetcode.cn/problems/count-caesar-cipher-pairs/"
difficulty: "Medium"
rating: 1624
created: "2026-01-13T23:00:33+08:00"
updated: "2026-01-13T23:00:36+08:00"
upvotes: 0
comments: 0
---

# 3805. 统计凯撒加密对数目

> **[yiduobo的每日leetcode 3805.统计凯撒加密对数目](https://zhuanlan.zhihu.com/p/1993703276894507533) · 知乎 · 2026-01-13 · 赞同 0**
> 力扣：[3805. 统计凯撒加密对数目](https://leetcode.cn/problems/count-caesar-cipher-pairs/) · Medium · 灵茶山艾府：[枚举右，维护左 + 优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3805.统计凯撒加密对数目

[3805. 统计凯撒加密对数目 - 力扣（LeetCode）](https://leetcode.cn/problems/count-caesar-cipher-pairs/description/)

题目给出一个由n个字符串组成的数组words，每个字符串的长度均为m，且仅包含小写英文字母。

对于两个字符串s和t，若可以通过执行以下操作任意次(包括零次)，使得二者变得相等，则称这两个字符串是相似的。每次操作中，需要将某个字符串中的每个字符都替换成字母表中的下一个字符，'z'的下一个字符为'a'。

现在要求计算words中满足i \< j且words[i]与words[j]相似的下标对数目。

由于题目中的操作是将某个字符串中的所有字符同时替换成下一个字符，因此无论如何轮转，字符串中的每个字符与首字符的距离都是不变的，因此可以将每个字符串都转化为其中所有字符到首字符的距离的数组diff。对于两个字符串，若这两个字符串对应的diff相同，就说明这两个字符串可以通过题目中的操作进行转换。

这样一来，就只需要对words进行一趟遍历，通过哈希表记录当前遍历过的字符串中每种diff数组出现的次数。对于当前遍历到的字符串w，先计算其距离数组diff，然后通过哈希表查找diff出现的次数并更新答案，然后将哈希表中diff出现的次数加上1即可。

最后附上python代码：

```python
class Solution(object):
    def countPairs(self, words):
        """
        :type words: List[str]
        :rtype: int
        """
        
        cnt = {}
        res = 0
        for w in words:
            diff = tuple([(ord(c) - ord(w[0])) % 26 for c in w[1:]])
            v = cnt.get(diff, 0)
            res += v
            cnt[diff] = v + 1
        
        return res
```

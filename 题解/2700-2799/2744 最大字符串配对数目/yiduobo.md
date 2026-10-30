---
title: "2744. 最大字符串配对数目"
aliases: ["yiduobo的每日leetcode 2744.最大字符串配对数目"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/array", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/653628878"
zhihu_id: "653628878"
zhihu_title: "yiduobo的每日leetcode 2744.最大字符串配对数目"
question_id: "2744"
question: "最大字符串配对数目"
problem_url: "https://leetcode.cn/problems/find-maximum-number-of-string-pairs/"
difficulty: "Easy"
created: "2023-09-01T01:17:26+08:00"
updated: "2023-09-01T01:17:26+08:00"
upvotes: 0
comments: 0
---

# 2744. 最大字符串配对数目

> **[yiduobo的每日leetcode 2744.最大字符串配对数目](https://zhuanlan.zhihu.com/p/653628878) · 知乎 · 2023-09-01 · 赞同 0**
> 力扣：[2744. 最大字符串配对数目](https://leetcode.cn/problems/find-maximum-number-of-string-pairs/) · Easy · 灵茶山艾府：[O(n) 一次遍历（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2744.最大字符串配对数目

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/find-maximum-number-of-string-pairs/)

由于题目的数据规模非常小，因此可以直接二重循环暴力枚举所有当前还未使用过的字符串组合。若某个组合符合条件，那么就将这两个字符串标记为使用过。枚举结束后，标记的字符串数量除以2即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def maximumNumberOfStringPairs(self, words):
        """
        :type words: List[str]
        :rtype: int
        """

        n = len(words)
        vis = set()
        for i in range(n - 1):
            if i not in vis:
                for j in range(i + 1, n):
                    if j not in vis and words[i][0] == words[j][1] and words[i][1] == words[j][0]:
                        vis.add(i)
                        vis.add(j)
        
        return len(vis) / 2
```

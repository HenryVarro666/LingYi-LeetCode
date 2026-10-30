---
title: "1061. 按字典序排列最小的等效字符串"
aliases: ["yiduobo的每日leetcode 1061.按字典序排列最小的等效字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/union-find", "题单/常用数据结构", "题单/常用数据结构/七-并查集"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/607660506"
zhihu_id: "607660506"
zhihu_title: "yiduobo的每日leetcode 1061.按字典序排列最小的等效字符串"
question_id: "1061"
question: "按字典序排列最小的等效字符串"
problem_url: "https://leetcode.cn/problems/lexicographically-smallest-equivalent-string/"
difficulty: "Medium"
created: "2023-02-19T19:23:26+08:00"
updated: "2023-02-19T19:23:26+08:00"
upvotes: 0
comments: 0
---

# 1061. 按字典序排列最小的等效字符串

> **[yiduobo的每日leetcode 1061.按字典序排列最小的等效字符串](https://zhuanlan.zhihu.com/p/607660506) · 知乎 · 2023-02-19 · 赞同 0**
> 力扣：[1061. 按字典序排列最小的等效字符串](https://leetcode.cn/problems/lexicographically-smallest-equivalent-string/) · Medium · 灵茶山艾府：[并查集（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1061.按字典序排列最小的等效字符串

[力扣](https://leetcode.cn/problems/lexicographically-smallest-equivalent-string/)

如果将单个字母视为图中的点，那么字母间的等价关系就可以视为无向图中的边，在同一个连通分量间的字符则可以互相替换。接下来就只需遍历每一对等价关系，通过并查集来维护字符间的连通性。

注意到题目要求最终答案的字典序最小，那么在并查集合并时就可以将字典序较大的合并到字典序较小的，这样一来每个字符只需通过并查集的find操作就可以找到其可以替换的字典序最小的字符了。

最后附上python代码：

```python
class Solution(object):
    def smallestEquivalentString(self, s1, s2, baseStr):
        """
        :type s1: str
        :type s2: str
        :type baseStr: str
        :rtype: str
        """

        fa = range(26)

        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        for char1, char2 in zip(s1, s2):
            x = ord(char1) - 97
            y = ord(char2) - 97

            fa_x = find(x)
            fa_y = find(y)
            if fa_x != fa_y:
                if fa_x < fa_y:
                    fa[fa_y] = fa_x
                else:
                    fa[fa_x] = fa_y

        return ''.join([chr(find(ord(char) - 97) + 97) for char in baseStr])
```

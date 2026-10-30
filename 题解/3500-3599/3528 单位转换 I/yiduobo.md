---
title: "3528. 单位转换I"
aliases: ["yiduobo的每日leetcode 3528.单位转换I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/tree", "leetcode/depth-first-search", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1904685929379111619"
zhihu_id: "1904685929379111619"
zhihu_title: "yiduobo的每日leetcode 3528.单位转换I"
question_id: "3528"
question: "单位转换 I"
problem_url: "https://leetcode.cn/problems/unit-conversion-i/"
difficulty: "Medium"
rating: 1580
created: "2025-05-12T22:59:58+08:00"
updated: "2025-05-12T22:59:58+08:00"
upvotes: 0
comments: 0
---

# 3528. 单位转换I

> **[yiduobo的每日leetcode 3528.单位转换I](https://zhuanlan.zhihu.com/p/1904685929379111619) · 知乎 · 2025-05-12 · 赞同 0**
> 力扣：[3528. 单位转换 I](https://leetcode.cn/problems/unit-conversion-i/) · Medium · 灵茶山艾府：[自顶向下 DFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3528.单位转换I

[3528. 单位转换 I - 力扣（LeetCode）](https://leetcode.cn/problems/unit-conversion-i/description/)

题目给出一个整数n，表示有n种单位，编号为0到n - 1。另外给出一个二维整数数组conversions，其长度为n - 1，其中conversions\[index\] \= \[source\[index\], target\[index\], factor\[index\]\]，表示一个source类型的单位等于factor\[index\]个target类型的单位。

现在要求返回一个长度为n的数组，其中下标index的元素表示一个0类型的单位等于多少个index类型的单位。

题目保证单位0可以通过唯一的转换路径转换为任何其他单位。

题目相当于给出一颗树，同时题目又保证了从0开始可以转换到其他任意单位，于是可以认为0是这颗树的树根，只需从0开始做bfs，计算0到其他所有节点的距离就行了，这里的距离指的是路径上factor的累乘。

最后附上python代码：

```python
class Solution(object):
    def baseUnitConversions(self, conversions):
        """
        :type conversions: List[List[int]]
        :rtype: List[int]
        """
        
        n = len(conversions) + 1
        g = [[] for _ in range(n)]
        for x, y, w in conversions:
            g[x].append((y, w))
            g[y].append((x, w))
        
        res = [None] * n
        res[0] = 1
        mod = 10 ** 9 + 7
        q = deque()
        q.append(0)
        while q:
            now = q.popleft()
            for nxt, w in g[now]:
                if res[nxt] is None:
                    res[nxt] = res[now] * w % mod
                    q.append(nxt)
        
        return res
```

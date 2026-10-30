---
title: "2307. 检查方程中的矛盾之处"
aliases: ["yiduobo的每日leetcode 2307.检查方程中的矛盾之处"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/629368738"
zhihu_id: "629368738"
zhihu_title: "yiduobo的每日leetcode 2307.检查方程中的矛盾之处"
question_id: "2307"
question: "检查方程中的矛盾之处"
problem_url: "https://leetcode.cn/problems/check-for-contradictions-in-equations/"
created: "2023-05-15T02:27:19+08:00"
updated: "2023-05-15T02:27:19+08:00"
upvotes: 0
comments: 0
---

# 2307. 检查方程中的矛盾之处

> **[yiduobo的每日leetcode 2307.检查方程中的矛盾之处](https://zhuanlan.zhihu.com/p/629368738) · 知乎 · 2023-05-15 · 赞同 0**
> 力扣：[2307. 检查方程中的矛盾之处](https://leetcode.cn/problems/check-for-contradictions-in-equations/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2307.检查方程中的矛盾之处

[力扣](https://leetcode.cn/problems/check-for-contradictions-in-equations/)

经典的带权并查集问题。除了常规并查集维护每个节点的父节点fa之外，还需要维护使用另一个数组weight维护当前节点与父节点的放缩关系。简单来说，就是weight\[x\] \* val\[x\] \= val\[fa\[x\]\]。有了weight之后，对于并查集中的find和union操作，就需要对weight进行对应的处理。

对于find操作，若fa\[x\]不等于x，那么就递归求解fa\[x\]，同时在这个过程中也会更新weight\[fa\[x\]\]，接下来将weight\[x\]更新为weight\[x\] \* weight\[fa\[x\]\]，再将fa\[x\]更新为fa\[x\]的祖先。

对于union操作，题目给出的式子是

val[a] \= val[b] \* v

再配合上

val\[a\] \= val\[fa\[a\]\] \* weight\[a\]

val\[b\] \= val\[fa\[b\]\] \* weight\[b\]

而此时需要求解weight\[fa\[b\]\]，将其val\[fa\[b\]\]与val\[fa\[a\]\]建立关联，也就是式子

val\[fa\[b\]\] \= val\[fa\[a\]\] \* weight\[fa\[b\]\]中的weight\[fa\[b\]\]

于是有

weight\[fa\[b\]\] \= val\[fa\[b\]\] / val\[fa\[a\]\]

而通过val[b]的式子除以val[a]的式子，就有

val\[fa\[b\]\] / val\[fa\[a\]\] \= val\[b\] \* weight\[a\] / (val\[a\] \* weight\[b\])

再带入val[b] / val[a] \= 1 / v，于是有

weight\[fa\[b\]\] \= val\[fa\[b\]\] / val\[fa\[a\]\] \= weight\[a\] / weight\[b\] / v

得到了weight的更新方法后，就只需按照常规并查集的处理方法。

对于题目给出的val\[a\] \= val\[b\] \* v，首先执行find(a)与find(b)操作，接下来若fa\[a\]等于fa\[b\]，那么val\[a\] / val\[b\]就等于weight\[a\] / weight\[b\]，此时只需检测这个值是否等于v。反之，若fa\[a\]不等于fa\[b\]，那么就应该执行union操作，更新weight\[fa\[b\]\]为weight\[a\] / weight\[b\] / v。

最后附上python代码：

```python
class Solution(object):
    def checkContradictions(self, equations, values):
        """
        :type equations: List[List[str]]
        :type values: List[float]
        :rtype: bool
        """

        fa = {}
        weight = {}
        eps = 10 ** -5

        def find(x):
            if x not in fa:
                fa[x] = x
                weight[x] = 1.0
            elif fa[x] != x:
                tmp = find(fa[x])
                weight[x] *= weight[fa[x]]
                fa[x] = tmp
                
            
            return fa[x]

        mapping = {}
        cnt = 0
        for (a, b), v in zip(equations, values):
            if a not in mapping:
                mapping[a] = cnt
                cnt += 1
            
            if b not in mapping:
                mapping[b] = cnt
                cnt += 1
            
            a = mapping[a]
            b = mapping[b]

            fa_a = find(a)
            fa_b = find(b)

            

            if fa_a == fa_b:
                if abs(weight[a] - weight[b] * v) > eps:
                    return True
            else:
                fa[fa_b] = fa_a
                weight[fa_b] = weight[a] / weight[b] / v

        return False
```

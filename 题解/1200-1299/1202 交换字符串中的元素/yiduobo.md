---
title: "1202. 交换字符串中的元素"
aliases: ["yiduobo的每日leetcode 1202.交换字符串中的元素"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/381685618"
zhihu_id: "381685618"
zhihu_title: "yiduobo的每日leetcode 1202.交换字符串中的元素"
question_id: "1202"
question: "交换字符串中的元素"
problem_url: "https://leetcode.cn/problems/smallest-string-with-swaps/"
created: "2021-06-17T23:54:18+08:00"
updated: "2021-06-17T23:54:18+08:00"
upvotes: 0
comments: 0
---

# 1202. 交换字符串中的元素

> **[yiduobo的每日leetcode 1202.交换字符串中的元素](https://zhuanlan.zhihu.com/p/381685618) · 知乎 · 2021-06-17 · 赞同 0**
> 力扣：[1202. 交换字符串中的元素](https://leetcode.cn/problems/smallest-string-with-swaps/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1202.交换字符串中的元素

[力扣](https://leetcode-cn.com/problems/smallest-string-with-swaps/)

如果我们将每个下标看成图中的一个点，而一组pair看成图中的一条边的话，那么我们最终可以得到一个无向图，而图中连通的部分其对应的字符值可以任意进行交换。

为了使得最终结果的字典序最小，那么对于每个连通的部分我们都应该将其按字典序从小到大进行排序，于是现在的做法就是先根据pair构造无向图，并对图进行染色，将位于同一连通分量的节点染成同一种颜色，并将节点对应的字符添加到其颜色对应的list当中。染色完毕后，将每种颜色的字符list分别进行排序，然后将其按节点对应的下标填充到答案中即可。

最后附上pythond代码：

```python
class Solution(object):
    def smallestStringWithSwaps(self, s, pairs):
        """
        :type s: str
        :type pairs: List[List[int]]
        :rtype: str
        """

        n = len(s)
        g = {x:set() for x in range(n)}
        for x, y in pairs:
            g[x].add(y)
            g[y].add(x)
        
        color = [None] * n
        char_list = []
        now_color = 0
        for index in range(n):
            if color[index] is None:
                char_list.append([])
                self.dfs(index, color, g, now_color, char_list, s)
                now_color += 1
        
        for index in range(now_color):
            char_list[index] = sorted(char_list[index])
        res = []
        pos_list = [0] * now_color
        for index in range(n):
            res.append(char_list[color[index]][pos_list[color[index]]])
            pos_list[color[index]] += 1

        return ''.join(res)

    def dfs(self, now, color, g, now_color, char_list, s):
        color[now] = now_color
        char_list[-1].append(s[now])
        for next in g[now]:
            if color[next] is None:
                self.dfs(next, color, g, now_color, char_list, s)
```

---
title: "1722. 执行交换操作后的最小汉明距离"
aliases: ["yiduobo的每日leetcode 1722.执行交换操作后的最小汉明距离"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/depth-first-search", "leetcode/graph", "leetcode/recursion", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/七-并查集", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/451441301"
zhihu_id: "451441301"
zhihu_title: "yiduobo的每日leetcode 1722.执行交换操作后的最小汉明距离"
question_id: "1722"
question: "执行交换操作后的最小汉明距离"
problem_url: "https://leetcode.cn/problems/minimize-hamming-distance-after-swap-operations/"
difficulty: "Medium"
rating: 1892
created: "2021-12-29T23:26:54+08:00"
updated: "2021-12-29T23:26:54+08:00"
upvotes: 0
comments: 0
---

# 1722. 执行交换操作后的最小汉明距离

> **[yiduobo的每日leetcode 1722.执行交换操作后的最小汉明距离](https://zhuanlan.zhihu.com/p/451441301) · 知乎 · 2021-12-29 · 赞同 0**
> 力扣：[1722. 执行交换操作后的最小汉明距离](https://leetcode.cn/problems/minimize-hamming-distance-after-swap-operations/) · Medium · 灵茶山艾府：[建图 + DFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1722.执行交换后的最小汉明距离

[力扣](https://leetcode-cn.com/problems/minimize-hamming-distance-after-swap-operations/)

由于可以执行任意次数的交换，那么对于一组互相之间可以交换的位置而言，就可以按意愿任意排布这些位置上的数字。换言之，只需统计source中这些位置上每个数字出现的数量，然后与target中对应的位置进行对比，不同字符出现的次数就是这些位置交换后的最小汉明距离。

接下来的问题就是如何找出这些可以互换的位置。如果将每个位置视为图中的一个点，可以交换的\[a\[i\], b\[i\]\]视为图中的一条边，那么问题就变成了找出图中所有的连通分量。对于这个问题可以使用并查集高效解决。

于是此时的做法就变成了通过并查集找出所有可以互换的位置，然后分别统计source中每一组可互换位置中数字出现的次数，并与target中对应位置上出现的数字进行比较，将不同数字的个数累加到答案中。

最后附上python代码：

```python
class Solution(object):
    def minimumHammingDistance(self, source, target, allowedSwaps):
        """
        :type source: List[int]
        :type target: List[int]
        :type allowedSwaps: List[List[int]]
        :rtype: int
        """

        n = len(source)
        f = range(n)
        for x, y in allowedSwaps:
            fa_x = self.find(x, f)
            fa_y = self.find(y, f)
            if fa_x != fa_y:
                if fa_x < fa_y:
                    f[fa_y] = fa_x
                else:
                    f[fa_x] = fa_y
        
        part_dict = {}
        for index in range(n):
            fa = self.find(index, f)
            if fa not in part_dict:
                part_dict[fa] = {}
            part_dict[fa][source[index]] = part_dict[fa].get(source[index], 0) + 1

        res = 0
        print target
        for index in range(n):
            fa = self.find(index, f)
            if part_dict[fa].get(target[index], 0) > 0:
                part_dict[fa][target[index]] -= 1
            else:
                res += 1
        
        return res
        
    def find(self, x, f):
        if f[x] != x:
            f[x] = self.find(f[x], f)
        return f[x]
```

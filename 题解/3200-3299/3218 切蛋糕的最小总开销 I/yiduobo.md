---
title: "3218. 切蛋糕的最小总开销I & 3219. 切蛋糕的最小总开销II"
aliases: ["yiduobo的每日leetcode 3218.切蛋糕的最小总开销I && 3219.切蛋糕的最小总开销II", "3218. 切蛋糕的最小总开销I", "3219. 切蛋糕的最小总开销II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/graph", "leetcode/minimum-spanning-tree", "题单/动态规划", "题单/动态规划/七-其他线性-DP", "leetcode/hard", "题单/图论算法", "题单/图论算法/四-最小生成树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/719415310"
zhihu_id: "719415310"
zhihu_title: "yiduobo的每日leetcode 3218.切蛋糕的最小总开销I && 3219.切蛋糕的最小总开销II"
question_id: ["3218", "3219"]
question: ["切蛋糕的最小总开销 I", "切蛋糕的最小总开销 II"]
problem_url: ["https://leetcode.cn/problems/minimum-cost-for-cutting-cake-i/", "https://leetcode.cn/problems/minimum-cost-for-cutting-cake-ii/"]
difficulty: ["Medium", "Hard"]
created: "2024-09-10T23:39:04+08:00"
updated: "2024-09-10T23:39:04+08:00"
upvotes: 2
comments: 1
---

# 3218. 切蛋糕的最小总开销I & 3219. 切蛋糕的最小总开销II

> **[yiduobo的每日leetcode 3218.切蛋糕的最小总开销I && 3219.切蛋糕的最小总开销II](https://zhuanlan.zhihu.com/p/719415310) · 知乎 · 2024-09-10 · 赞同 2**
> 力扣：[3218. 切蛋糕的最小总开销 I](https://leetcode.cn/problems/minimum-cost-for-cutting-cake-i/) · Medium · 灵茶山艾府：[【图解】逆向思维+最小生成树（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)
> 力扣：[3219. 切蛋糕的最小总开销 II](https://leetcode.cn/problems/minimum-cost-for-cutting-cake-ii/) · Hard · 灵茶山艾府：[【图解】逆向思维+最小生成树（Python/Java/C++/C/Go/JS/Rust）](../3219%20切蛋糕的最小总开销%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3218.切蛋糕的最小总开销I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-cost-for-cutting-cake-i/description/)

3219.切蛋糕的最小总开销II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-cost-for-cutting-cake-ii/description/)

题目给出一块大小为m \* n的蛋糕，要求将其切割成1 \* 1的小块，另外给出一个大小为m - 1的数组horizontalCut以及一个大小为n - 1的数组verticalCut，分别表示在对应的水平线和垂直线切开蛋糕的代价，问切分的最小代价是多少。

两题的题设一样，第二题的数据规模比较大。

随着切割的进行，被切分出来的蛋糕块就越多，这也就意味着越晚对某条线进行切割，需要切割的次数就越多。由于所有的切割都至少需要执行一次，因此对于同一方向上的切割，就应该先完成代价较大的切割。另一方面，对于不同方向上的切割，不妨设切割的代价分别为x和y，需要切割次数分别为h和v，那么两种切割顺序对应的代价就分别是x \* h + y \* (v + 1)以及x \* (h + 1) + y \* v，可以发现，这两种代价的大小关系只与x和y的大小有关，因此对于不同方向上的切割，同样应该先完成代价较大的切割。

根据上面的结论，只需将horizontalCut以及verticalCut都按照从大到小的顺序进行排序，然后使用类似二路归并的方法进行遍历，计算切割的总代价即可。

最后附上python代码：

```python
class Solution(object):
    def minimumCost(self, m, n, horizontalCut, verticalCut):
        """
        :type m: int
        :type n: int
        :type horizontalCut: List[int]
        :type verticalCut: List[int]
        :rtype: int
        """

        horizontalCut.sort(reverse=True)
        verticalCut.sort(reverse=True)
        i = j = 0
        res = 0
        while i < m - 1 and j < n - 1:
            if horizontalCut[i] > verticalCut[j]:
                res += (j + 1) * horizontalCut[i]
                i += 1
            else:
                res += (i + 1) * verticalCut[j]
                j += 1
        
        while i < m - 1:
            res += n * horizontalCut[i]
            i += 1
        
        while j < n - 1:
            res += m * verticalCut[j]
            j += 1
        
        return res
```

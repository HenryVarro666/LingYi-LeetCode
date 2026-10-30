---
title: "3378. 统计最小公倍数图中的连通块数目"
aliases: ["yiduobo的每日leetcode 3378.统计最小公倍数图中的连通块数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/union-find", "leetcode/graph", "leetcode/math", "leetcode/number-theory", "题单/常用数据结构", "题单/常用数据结构/七-并查集"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/29042111086"
zhihu_id: "29042111086"
zhihu_title: "yiduobo的每日leetcode 3378.统计最小公倍数图中的连通块数目"
question_id: "3378"
question: "统计最小公倍数图中的连通块数目"
problem_url: "https://leetcode.cn/problems/count-connected-components-in-lcm-graph/"
difficulty: "Hard"
rating: 2532
created: "2025-03-09T23:03:12+08:00"
updated: "2025-03-09T23:03:12+08:00"
upvotes: 1
comments: 0
---

# 3378. 统计最小公倍数图中的连通块数目

> **[yiduobo的每日leetcode 3378.统计最小公倍数图中的连通块数目](https://zhuanlan.zhihu.com/p/29042111086) · 知乎 · 2025-03-09 · 赞同 1**
> 力扣：[3378. 统计最小公倍数图中的连通块数目](https://leetcode.cn/problems/count-connected-components-in-lcm-graph/) · Hard · 灵茶山艾府：[枚举 GCD + 并查集（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3378.统计最小公倍数图中的连通块数目

[3378. 统计最小公倍数图中的连通块数目 - 力扣（LeetCode）](https://leetcode.cn/problems/count-connected-components-in-lcm-graph/description/)

题目给出一个长度为n的整数数组nums以及一个正整数threshold，表示有一张n个节点的图，图中节点i对应的值为nums[i]。若两个节点i和j的值满足lcm(nums[i], nums[j]) \<\= threshold，那么这两个节点间就有一条无向边相连，其中lcm(a, b)指的是a和b的最小公倍数。问这张图中的连通块数量是多少。

题目中nums的长度可以达到10^5，其中元素大小可达10^9，且各不相同。threshold的大小则可达2 \* 10^5。

由于nums的规模比较大，因此两两枚举检测是否有边是不行的，只能从数值方面入手想办法。注意到两个数a和b的最小公倍数lcm(a, b)必然是大于等于a和b的，因此若某个数nums[i]大于threshold，那么其与任意其他数的lcm也必然大于threshold，也就是说nums[i]在图中必然不会与其他节点相连。于是可以先对nums进行一趟遍历，将其中大于threshold的元素滤出去，同时根据这些元素的数量更新答案。

接下来对于小于等于threshold的元素，则可以利用类似筛法的处理方法，先使用一个数组divisor记录每个数有哪些约数。具体来说，对于每个nums中的每个元素v，可以从v开始，以v为步长向上枚举到threshold。对于当前枚举到的x，v必然是x的约数，此时需要v加入到divisor[x]中。

得到divisor后，再从1到threshold枚举所有的倍数v，那么对于divisor[v]中的所有元素两两之间的元素对，v都是这些元素对的公倍数。更进一步的，这些元素对两两之间的最小公倍数必然小于等于v，也就小于等于threshold，因此这些元素对之间就存在一条边。对于这些元素对，使用并查集来维护连通性，当出现合并操作时，将连通块的数量减去一即可。

最后附上python代码：

```python
class Solution(object):
    def countComponents(self, nums, threshold):
        """
        :type nums: List[int]
        :type threshold: int
        :rtype: int
        """
        
        divisor = [[] for _ in range(threshold + 1)]
        fa = {}

        res = len(nums)
        nums.sort()
        for v in nums:
            if v > threshold:
                break
            fa[v] = v
            for x in range(v, threshold + 1, v):
                divisor[x].append(v)

        def find(fa, x):
            if fa[x] != x:
                fa[x] = find(fa, fa[x])
            return fa[x]

        for v in range(1, threshold + 1):
            if len(divisor[v]) < 2:
                continue
            x = divisor[v][0]
            fa_x = find(fa, x)
            for y in divisor[v][1:]:
                fa_y = find(fa, y)
                if fa_x != fa_y:
                    fa[fa_y] = fa_x
                    res -= 1

        return res
```

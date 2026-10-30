---
title: "LCP 05. 发LeetCoin"
aliases: ["yiduobo的每日leetcode LCP05.发LeetCoin"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/570472925"
zhihu_id: "570472925"
zhihu_title: "yiduobo的每日leetcode LCP05.发LeetCoin"
question_id: "LCP 05"
question: "发LeetCoin"
problem_url: "https://leetcode.cn/problems/coin-bonus/"
created: "2022-10-04T04:44:44+08:00"
updated: "2022-10-04T04:44:44+08:00"
upvotes: 0
comments: 0
---

# LCP 05. 发LeetCoin

> **[yiduobo的每日leetcode LCP05.发LeetCoin](https://zhuanlan.zhihu.com/p/570472925) · 知乎 · 2022-10-04 · 赞同 0**
> 力扣：[LCP 05. 发LeetCoin](https://leetcode.cn/problems/coin-bonus/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP05.发LeetCoin

[力扣](https://leetcode.cn/problems/coin-bonus/)

不得不承认，leetcode杯的题目中还是有比较有水平的题目的，比如本题。

题目给出了一棵树，要求实现下面三种操作：

1、将树中某个节点的值加上coin

2、将以某个节点为根节点的子树中的所有节点值都加上coin

3、计算以某个节点为根节点的子树中，所有节点值之和

对于本题，完全按照题目要求更新节点值显然是不现实的。由于只有操作3是查询操作，因此可以在适配操作3的前提下设法简化前两个操作。比较容易想到的方法是对于操作2，转化为子树中节点的数量乘以增量，而操作1保持不变。这样一来，就可以在O(1)的时间内完成操作1和操作2。但是这个做法无法处理操作3。每一次询问，相当于都要从询问的节点开始遍历这棵子树。反过来，如果现在操作1和操作2就更新好所有子树的值，同样需要从当前节点开始向上遍历到根节点，复杂度还是很高。

如果不考虑变换树的重心重新选根的话，就需要另想办法了。当然，树分治相关的内容我认为不会出现在这里，因此就没有细想是否可行了。

接下来考虑其他做法。本题的最难处理的是操作2，主要难点在于虽然是整颗子树，但是并没有什么操作可以一次性修改整颗子树的值，常规的批量操作通常出现在一维或者二维的数组中。受到这个启发，就想到使用dfs序来将树结构转化为线性结构。

关于dfs相关的内容可以参考之前的1993题

[yiduobo：yiduobo的每日leetcode 1993.树上的操作](https://zhuanlan.zhihu.com/p/500177848)

对于本题，由于接下来需要在dfs序上做一些操作，那么方便起见就只保留首次访问某个节点的时间戳，但仍需记录子树dfs序中的最后的下标。得到dfs序后，树就转化成了线性表，而对于子树的操作就变成了区间操作。于是现在问题就变成了：

1、给定某个下标，将该下标对应的值加上coin

2、给定某个区间，将区间内的所有数加上coin

3、给定某个区间，求区间内所有数之和

上述操作涉及到区间的修改和查询，王道做法自然是线段树，但是涉及区间修改的线段树实现起来比较麻烦，所以我在这里采用的是树状数组的进阶版。另外，为了方便树状数组相关的操作，下面所有数组的下标都是从1开始。

首先，操作1可以看作给定某个下标x，将区间[x, x]内的所有数加上coin，这样一来就与操作2对齐了。于是现在就是两种操作：修改区间值，求区间和。

对于修改区间值得操作，常见的做法是使用差分数组。即使用一个数组delta，其中delta[i]表示后缀[i, n]这个区间中的数都加上delta[i]，那么对于区间[x, y]加上coin这个操作，就可以拆分成delta[x]加上coin，以及delta[y + 1]减去coin。另一方面，通过差分数组求解数组的特定结果则需要计算差分数组的前缀和。令value表示修改后区间的最终值，那么就有value[x] \= delta[1] + delta[2] + ... + delta[x]。这是一个前缀和问题，可以交给树状数组去做。

然而现在的问题是求解区间value[x: y + 1]的和，但是使用树状数组只能求出value上单个位置的值，需要进一步优化。对于区间和问题，通常是转化为前缀和问题求解，在这里也是一样，改为想办法求出value[1: y + 1]以及value[1: x]的和。在这里不妨拆分其中一个来看看。

s \= sum(value[1: x]) \= value[1] + value[2] + ... + value[x - 1]

将value[i]再拆开，就有

s \= delta[1] + (delta[1] + delta[2]) + ... + (delta[1] + delta[2] + ... + delta[x - 1])

我们现在可以通过树状数组求解最后一项suf[x - 1] \= (delta[1] + delta[2] + ... + delta[x - 1])，那么就有

s \= suf[x - 1] \* (x - 1) - 0 \* delta[1] - 1 \* delta[2] - ... - (x - 2) \* delta[x - 1]

可以发现，所有delta项的系数都是很规整的，那么在这里就可以使用另一个树状数组来维护(i - 1) \* delta[i]的前缀和，与维护delta的树状数组同步更新，这样一来就可以通过两次树状数组的计算求解value的前缀和了。

到了这里，总算是得到了一种可行的做法：

1、首先从根节点开始向下dfs，得到dfs序

2、设f和g分别为维护常规delta和带系数delta的树状数组，接下来遍历每种操作，对于每种操作，记node为操作的节点，start和end分别为node在dfs序中的位置以及管辖区间的右边界。记coin为操作的金额(如有)，那么：

2-1）对于操作1：

使用coin更新f，起始下标为start；使用coin \* (start - 1)更新g，起始下标与f相同

使用-coin更新f，起始下标为start + 1；使用-coin \* start更新g，起始下标与f相同

2-2）对于操作2：

使用coin更新f，起始下标为start；使用coin \* (start - 1)更新g，起始下标与f相同

使用-coin更新f，起始下标为end + 1；使用-coin \* end更新g，起始下标与f相同

2-3）对于操作3：

题目要求的是value[start : end + 1]的和，那么就是求value[1 : end + 1]的和减去value[1 : start]的和，这两个前缀和的求法则可以使用上面所说的，使用f求得的前缀和再乘以下标，减去g求得的前缀和来得到

最后附上python代码：

```python
class Solution(object):
    def bonus(self, n, leadership, operations):
        """
        :type n: int
        :type leadership: List[List[int]]
        :type operations: List[List[int]]
        :rtype: List[int]
        """

        mod = 10 ** 9 + 7
        fa = {}
        childs = {}

        for x, y in leadership:
            if x not in childs:
                childs[x] = []
            childs[x].append(y)
            fa[y] = x
        
        root = 0
        for node in range(1, n + 1):
            if node not in fa:
                root = node
                break

        def dfs(now, order, start_pos, end_pos):
            order.append(now)
            start_pos[now] = len(order)
            if now in childs:
                for next in childs[now]:
                    dfs(next, order, start_pos, end_pos)
            end_pos[now] = len(order)

        def add(arr, now, delta):
            if delta >= mod:
                delta %= mod
            elif delta < 0:
                delta = -((-delta) % mod) + mod
            while now <= n:
                arr[now] += delta
                if arr[now] >= mod:
                    arr[now] -= mod
                now += now & -now
        
        def get(arr, now):
            res = 0
            while now > 0:
                res += arr[now]
                if res >= mod:
                    res -= mod
                elif res < 0:
                    res += mod
                now -= now & -now
            return res
        
        order = []
        start_pos = [0] * (n + 1)
        end_pos = [0] * (n + 1)

        dfs(root, order, start_pos, end_pos)

        f = [0] * (n + 1)
        g = [0] * (n + 1)
        res = []

        for op in operations:
            if op[0] == 1:
                node = op[1]
                coin = op[2]
                add(f, start_pos[node], coin)
                add(g, start_pos[node], (start_pos[node] - 1) * coin)
                add(f, start_pos[node] + 1, -coin)
                add(g, start_pos[node] + 1, -start_pos[node] * coin)
            elif op[0] == 2:
                node = op[1]
                coin = op[2]
                add(f, start_pos[node], coin)
                add(g, start_pos[node], (start_pos[node] - 1) * coin)
                add(f, end_pos[node] + 1, -coin)
                add(g, end_pos[node] + 1, -end_pos[node] * coin)
            else:
                node = op[1]
                prefix_sum_f = get(f, end_pos[node]) * end_pos[node] % mod
                prefix_sum_f -= get(f, start_pos[node] - 1) * (start_pos[node] - 1) % mod
                if prefix_sum_f < 0:
                    prefix_sum_f += mod
                
                prefix_sum_g = get(g, end_pos[node]) - get(g, start_pos[node] - 1)
                if prefix_sum_g < 0:
                    prefix_sum_g += mod

                res.append(prefix_sum_f - prefix_sum_g)
                if res[-1] < 0:
                    res[-1] += mod

        return res
```

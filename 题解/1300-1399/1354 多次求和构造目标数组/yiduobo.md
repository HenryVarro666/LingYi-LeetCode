---
title: "1354. 多次求和构造目标数组"
aliases: ["yiduobo的每日leetcode 1354.多次求和构造目标数组"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/五-堆-优先队列", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/398460420"
zhihu_id: "398460420"
zhihu_title: "yiduobo的每日leetcode 1354.多次求和构造目标数组"
question_id: "1354"
question: "多次求和构造目标数组"
problem_url: "https://leetcode.cn/problems/construct-target-array-with-multiple-sums/"
difficulty: "Hard"
rating: 2015
created: "2021-08-10T23:15:48+08:00"
updated: "2021-08-10T23:15:48+08:00"
upvotes: 1
comments: 0
---

# 1354. 多次求和构造目标数组

> **[yiduobo的每日leetcode 1354.多次求和构造目标数组](https://zhuanlan.zhihu.com/p/398460420) · 知乎 · 2021-08-10 · 赞同 1**
> 力扣：[1354. 多次求和构造目标数组](https://leetcode.cn/problems/construct-target-array-with-multiple-sums/) · Hard · 灵茶山艾府：[逆向思维（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1354.多次求和构造目标数组

[力扣](https://leetcode-cn.com/problems/construct-target-array-with-multiple-sums/)

由于数组的初始值都是1，也就是说数组中的所有数必然都是正数，那么在一次求和执行后，这里的和s必然大于数组中的其他数。根据这一点，我们可以从target开始倒推。

对于当前的数组f，我们先找出其中最大的数，不妨设为f[k]。另外，设f是通过g构造得来的，那么就有

g[0] + g[1] + ... + g[n - 1] \= f[k]

另外，除了f[k]之外，其他的数都不变，那么就有

g[0] \= f[0]

g[1] \= f[1]

...

g[k - 1] \= f[k - 1]

g[k + 1] \= f[k + 1]

...

g[n - 1] \= f[n - 1]

我们将其带入到上面求和的式子，就有

f[0] + f[1] + ... + f[k - 1] + g[k] + f[k + 1] + ... + f[n - 1] \= f[k]

于是此时我们可以计算得到g[k]，从而得到整个数组g。

重复这个过程，若某一时刻g[k]小于等于0，那么说明无法构造得到target，此时应该返回false。若最终倒推会了全1，那么就返回true。

对于上面求解的过程，直接执行的复杂度是很高的，存在几处可以优化的地方。

1、由于每次我们都是要找出数组中的最大值，而每一轮仅有一个数产生了变化，那么我们可以使用一个堆来维护当前数组中的最大值。

2、对于求和等式的计算，无需每次都计算加法。由于只有一个数产生了变化，那么我们可以每一轮都维护当前数组的和s，然后都某个数产生变化时，我们通过这个变化来更新s即可。

3、对于g[k]的求解，若此时的f[k]远大于其他数的和，那么需要执行多次减法，此时可以通过直接求f[k]对于其他数的和的余数来进行加速。

最后附上python代码，其中ma是每一轮的最大值，s是每一轮的和，而rest就是每一轮剩下其他数的和：

```python
class Solution(object):
    def isPossible(self, target):
        """
        :type target: List[int]
        :rtype: bool
        """

        if len(target) == 1:
            return target[0] == 1

        heap = [-x for x in target]
        s = sum(target)
        n = len(target)
        heapq.heapify(heap)
        
        while s != n:
            ma = -heapq.heappop(heap)
            rest = s - ma
            if ma <= rest:
                return False

            if ma % rest == 0:
                tmp = rest
            else:
                tmp = ma % rest

            s = rest + tmp
            heapq.heappush(heap, - tmp)

        return True
```

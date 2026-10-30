---
title: "4029. 电梯请求IV"
aliases: ["yiduobo的每日leetcode 4029.电梯请求IV"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2077203987573559992"
zhihu_id: "2077203987573559992"
zhihu_title: "yiduobo的每日leetcode 4029.电梯请求IV"
question_id: "4029"
question: "电梯请求 IV"
problem_url: "https://leetcode.cn/problems/elevator-requests-iv/"
difficulty: "Hard"
created: "2026-08-30T01:43:48+08:00"
updated: "2026-08-30T01:43:48+08:00"
upvotes: 1
comments: 0
---

# 4029. 电梯请求IV

> **[yiduobo的每日leetcode 4029.电梯请求IV](https://zhuanlan.zhihu.com/p/2077203987573559992) · 知乎 · 2026-08-30 · 赞同 1**
> 力扣：[4029. 电梯请求 IV](https://leetcode.cn/problems/elevator-requests-iv/) · Hard · 灵茶山艾府：[O(m^2) 区间 DP（Python/Java/C++/Go）](灵茶山艾府.md)

因为家里有事，加上正好碰到了难题，索性鸽了一阵子。题解恢复更新，依然是每天两题，争取不卡题吧。

4029.电梯请求IV

<https://leetcode.cn/problems/elevator-requests-iv/description/>

题目给出一个整数n，表示一栋建筑的楼层数，楼层编号从0到n - 1。

同时给出一个整数start，表示电梯的起始层数，以及一个二维整数数组requests，其中requests\[index\] \= \[arrival\[index\], floor\[index\]\]，表示在时间arrival\[index\]发出一个前往楼层floor\[index\]的请求。requests的长度不超过500。

在时间0，电梯在楼层start。

每一秒，电梯可以向上移动一层、向下移动一层，或者停留在当前楼层。

一个请求只能在其到达时间后之后被处理。从请求到达时起，只要电梯在任意时刻位于该请求对应的楼层，那么该请求将被立即处理。

问处理所有请求所需的最短时间。

之前4027题的加强版。

[yiduobo的每日leetcode 4027.电梯请求III](https://zhuanlan.zhihu.com/p/2073916695496888651)

本题的数据规模来到了500，因此之前的状态压缩动态规划不再适用，必须另想办法。

基于本题的数据规模，最终做法无外乎是贪心或者区间动态规划，无论是哪一种，都需要先分析下电梯最终的行进路线。

首先可以明确的是，电梯必然是来回来回地走折线，这一点是没有任何疑问的。

接下来对这条折线进行分析，可以发现有趣的结论，那就是除了首次移动之外，其他的折线必然被包含在上一轮的折线之内。以a \< b \< c \< d的四个楼层举例，最开始，电梯处于a。

在这里不妨考察不满足以上条件的行进路线，即a -> c -> b -> d。其中，从c折返回到b的唯一原因，只能是b对应的请求到达时间比c要晚，所以不能在第一次路过的时候就完成b对应的请求。

上面这条路径所需的时间，可以拆分为a->c->b这一段所需的时间，以及b->d所需的时间。对于前面这一段，其耗时必然大于等于从a直接走到b，然后等着b对应的请求到来的时间，因此在这里完全可以采用a->b，然后在b处等待直到请求到来，再继续向d行进。基于最开始的分析，b对应的请求到达时间一定比c要晚，因此等到请求b完成后，再前往d的过程中顺便就把c给完成了。这也就印证了上面的结论，即折线是越折越往内的。

另一方面， 首次行动也必然到达所有请求的某个端点，因为无论如何行动，两个端点都是要走到的，那么在走到两个端点之前的所有行动，都可以按照上面描述的方法通过等待来将折线摊平，得到的结果是更优的。

基于上面这个折线越来越内缩的结果，就很容易想到一种动态规划的做法了：

将所有请求先按照楼层去重，留下到达时间最晚的那个，接下来按楼层数从小到大进行排序。

接下来，令f[start][end]表示接下来的折线还需要经过start到end，且start处的请求已经被满足时的最小总耗时，而g[start][end]则表示end处的请求已经被满足时的最小总耗时，那么在这里就可以先计算从start到最底层以及最高层的请求对应的楼层所需的时间以及这两个请求到达的时间，来初始化f[0][m - 1]以及g[0][m - 1]，其中的m为请求的总数。

接下来，从m到2枚举上一轮折线的长度length，并枚举起点start，然后通过start + length - 1计算出终点end，就可以通过f[start][end]以及g[start][end]来更新后续的状态了。

对于f[start][end]：

- 其可以从start走到start + 1，并完成start + 1处的请求，此时的耗时就是start + 1处请求的到达时间，以及f[start][end]加上从start走到start + 1所需时间之和，这二者中的较大值。使用这个值更新f[start + 1][end]
- 也可以直接从start走到end，并完成end处的请求，此时的耗时就是end处请求的到达时间，以及f[start][end]加上从start走到end所需的时间之和，这二者中的较大值。使用这个值更新g[start + 1][end]

而对于g[start][end]，则与f对称：

- 可以从end走到end - 1，更新g[start][end - 1]
- 也可以直接走到start，更新f[start][end - 1]

可以发现，以上对于f和g的更新，本质上就是在上面不断画折线的过程。全部计算完成后，则只需枚举最终的楼层x，取所有f[x][x]和g[x][x]中的最小值作为最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def elevatorRequests(self, n, start, requests):
        """
        :type n: int
        :type start: int
        :type requests: List[int]
        :rtype: int
        """
        
        last = {}
        for t, x in requests:
            last[x] = max(t, last.get(x, 0))
        
        if start in last and last[start] == 0:
            last.pop(start)
        
        if not last:
            return 0

        r = sorted(last.items())
        m = len(r)

        f = [[None] * m for _ in range(m)]
        g = [[None] * m for _ in range(m)]
        f[0][m - 1] = max(r[0][1], abs(start - r[0][0]))
        g[0][m - 1] = max(r[-1][1], abs(start - r[-1][0]))

        for length in range(m, 1, -1):
            for start in range(m):
                end = start + length - 1
                if end >= m:
                    break
                
                if f[start][end]:
                    f_from_left = max(r[start + 1][1], f[start][end] + r[start + 1][0] - r[start][0])
                    if f[start + 1][end] is None or f[start + 1][end] > f_from_left:
                        f[start + 1][end] = f_from_left

                    g_from_left = max(r[end][1], f[start][end] + r[end][0] - r[start][0])
                    if g[start + 1][end] is None or g[start + 1][end] > g_from_left:
                        g[start + 1][end] = g_from_left
                
                if g[start][end]:
                    f_from_right = max(r[start][1], g[start][end] + r[end][0] - r[start][0])
                    if f[start][end - 1] is None or f[start][end - 1] > f_from_right:
                        f[start][end - 1] = f_from_right
                
                    g_from_right = max(r[end - 1][1], g[start][end] + r[end][0] - r[end - 1][0])
                    if g[start][end - 1] is None or g[start][end - 1] > g_from_right:
                        g[start][end - 1] = g_from_right

        res = None
        for x in range(m):
            if f[x][x] is not None and (res is None or res > f[x][x]):
                res = f[x][x]
            if g[x][x] is not None and (res is None or res > g[x][x]):
                res = g[x][x]
        return res
```

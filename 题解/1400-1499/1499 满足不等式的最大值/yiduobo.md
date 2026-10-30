---
title: "1499. 满足不等式的最大值"
aliases: ["yiduobo的每日leetcode 1499.满足不等式的最大值"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/monotonic-queue", "题单/常用数据结构", "题单/常用数据结构/四-队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/416798268"
zhihu_id: "416798268"
zhihu_title: "yiduobo的每日leetcode 1499.满足不等式的最大值"
question_id: "1499"
question: "满足不等式的最大值"
problem_url: "https://leetcode.cn/problems/max-value-of-equation/"
difficulty: "Hard"
rating: 2456
created: "2021-10-07T17:58:16+08:00"
updated: "2021-10-07T17:58:16+08:00"
upvotes: 0
comments: 0
---

# 1499. 满足不等式的最大值

> **[yiduobo的每日leetcode 1499.满足不等式的最大值](https://zhuanlan.zhihu.com/p/416798268) · 知乎 · 2021-10-07 · 赞同 0**
> 力扣：[1499. 满足不等式的最大值](https://leetcode.cn/problems/max-value-of-equation/) · Hard · 灵茶山艾府：[O(n) 单调队列，附题单！（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1499.满足不等式的最大值

[力扣](https://leetcode-cn.com/problems/max-value-of-equation/)

题目一面说已经按x排好了序，一面又要求有关与|x[i] - x[j]|的项，而这里的i还写明了是小于j的，那么必然有x[i] \<\= x[j]，因此这里绝对值打开就是x[j] - x[i]。

于是，最终的得分公式就是x[j] + y[j] + y[i] - x[i]。

一个自然的想法就是将右边界j给固定下来，那么x[j] + y[j]的值就固定下来了。为了使得整个式子最大，那么就需要使得y[i] - x[i]最大。除此之外，这里的x[i]还有一个额外条件就是x[j] - x[i] \<\= k。由于这里的x已经排好了序，那么这里候选的i实际上也是从j往前看的一端连续区间。那么问题到这里就转化成了经典的单调双端队列问题。

简单来说就是对于两个位置p和q，若满足p \< q且y[p] - x[p] \<\= y[q] - x[q]，那么此时对于后续的所有q右侧所有的位置j而言，都不可能选择p作为其配对的位置i了，因此在这里可以维护一个单调递减的数据结构，用来储存可能被后续的j选择作为配对i的值。另外，由于x这里还有一个距离k的限制，因此这个数据结构的最左侧还需要可以清除掉越界的数据，综合起来，这里就应该选择单调双端队列来进行处理。

那么现在的做法就是维护一个双端队列q，接下来遍历每一组now_x和now_y：

1、首先，若队列不为空，且队列头部的head_x满足now_x - head_x > k，那么说明队列头部已经越界，后续不可能再用上，因此需要将队列头移出。重复该过程直到队列为空或者队列头部在k的限制范围之内

2、接下来，若队列不为空，那么对于now_x以及now_y，能达成最优解的配对必然就是队列头部的head_x和head_y。此时应该使用now_x + now_y + head_y - head_x来更新答案

3、接下来，使用now_x和now_y来更新队列的尾部。若此时队列尾部满足now_y - now_x >\= tail_y - tail_x，那么就应该将队尾弹出。重复该过程直到队列为空或者队尾满足now_y - now_x \< tail_y - tail_x

4、最后，将now_x和now_y加入到队列中，供后续位置使用

最后附上python代码：

```python
class Solution(object):
    def findMaxValueOfEquation(self, points, k):
        """
        :type points: List[List[int]]
        :type k: int
        :rtype: int
        """

        q = []
        l = r = 0
        res = None

        for x, y in points:
            while l < r and x - q[l][0] > k:
                l += 1
            
            if l < r and (res is None or res < x + y + q[l][1] - q[l][0]):
                res = x + y + q[l][1] - q[l][0]
            
            while r > l and y - x >= q[-1][1] - q[-1][0]:
                q.pop()
                r -= 1
            
            q.append([x, y])
            r += 1

        return res
```

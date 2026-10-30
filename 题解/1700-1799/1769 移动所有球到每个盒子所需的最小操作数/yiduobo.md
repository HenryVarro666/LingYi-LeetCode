---
title: "1769. 移动所有球到每个盒子所需的最小操作数"
aliases: ["yiduobo的每日leetcode 1769.移动所有球到每个盒子所需的最小操作数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/460969826"
zhihu_id: "460969826"
zhihu_title: "yiduobo的每日leetcode 1769.移动所有球到每个盒子所需的最小操作数"
question_id: "1769"
question: "移动所有球到每个盒子所需的最小操作数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-operations-to-move-all-balls-to-each-box/"
created: "2022-01-23T15:51:23+08:00"
updated: "2022-01-23T15:51:24+08:00"
upvotes: 0
comments: 0
---

# 1769. 移动所有球到每个盒子所需的最小操作数

> **[yiduobo的每日leetcode 1769.移动所有球到每个盒子所需的最小操作数](https://zhuanlan.zhihu.com/p/460969826) · 知乎 · 2022-01-23 · 赞同 0**
> 力扣：[1769. 移动所有球到每个盒子所需的最小操作数](https://leetcode.cn/problems/minimum-number-of-operations-to-move-all-balls-to-each-box/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1769.移动所有球到每个盒子所需的最小操作数

[力扣](https://leetcode-cn.com/problems/minimum-number-of-operations-to-move-all-balls-to-each-box/)

由于题目的数据规模并不大，那么直接枚举每个盒子然后模拟也是可以的，不过这里还存在更好的做法。

注意到题目要求只能在相邻的盒子中移动，那么对于p这个盒子而言，其左侧所有小球都必须经过p - 1这个盒子才能到达p，而右侧所有小球则必须经过p + 1这个盒子才能到达p。左右两边是镜像操作，因此在这里只讨论如何计算左侧的操作数。

根据上面必须经过p - 1才能到达p这个结论，那么一个自然的想法就是计算p这个位置的代价时想办法用上p - 1的代价。不妨将p左侧小球移动到p的过程分两步走。首先将这些小球全部移动到p - 1这个位置，然后将这些球连同原来就在p - 1这个位置上的球移动到p。令f[p]表示将p左侧所有小球移动到p的最小操作数，那么这里第一步操作的代价就是f[p - 1]，而第二步操作的代价则为cnt[p - 1]，这里的cnt[p - 1]表示0到p - 1之间所有小球的个数。那么就有f[p] \= f[p - 1] + cnt[p - 1]。而对于cnt而言，若p这个位置上有小球，那么就有cnt[p] \= cnt[p - 1] + 1，否则就是cnt[p] \= cnt[p - 1]。

这样一来，就能利用上面递推的方法在O(n)的时间内求出f。类似的，令g[p]表示将p右侧所有小球移动到p的最小操作数，那么可以使用相同的方法从右到左在O(n)的时间内计算出g。得到f和g之后，f[p] + g[p]就是将所有小球移动到p的最小操作数了。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, boxes):
        """
        :type boxes: str
        :rtype: List[int]
        """

        n = len(boxes)

        f = [0]
        if boxes[0] == '1':
            cnt = 1
        else:
            cnt = 0
        for index in range(1, n):
            f.append(f[-1] + cnt)
            if boxes[index] == '1':
                cnt += 1
        
        g = [0]
        if boxes[-1] == '1':
            cnt = 1
        else:
            cnt = 0
        for index in range(n - 2, -1, -1):
            g.append(g[-1] + cnt)
            if boxes[index] == '1':
                cnt += 1
        g.reverse()
        
        return [f[index] + g[index] for index in range(n)]
```

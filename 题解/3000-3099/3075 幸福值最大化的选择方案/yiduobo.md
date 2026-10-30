---
title: "3075. 幸福值最大化的选择方案"
aliases: ["yiduobo的每日leetcode 3075.幸福值最大化的选择方案"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/697758101"
zhihu_id: "697758101"
zhihu_title: "yiduobo的每日leetcode 3075.幸福值最大化的选择方案"
question_id: "3075"
question: "幸福值最大化的选择方案"
problem_url: "https://leetcode.cn/problems/maximize-happiness-of-selected-children/"
difficulty: "Medium"
rating: 1326
created: "2024-05-14T21:23:28+08:00"
updated: "2024-05-14T21:24:20+08:00"
upvotes: 0
comments: 0
---

# 3075. 幸福值最大化的选择方案

> **[yiduobo的每日leetcode 3075.幸福值最大化的选择方案](https://zhuanlan.zhihu.com/p/697758101) · 知乎 · 2024-05-14 · 赞同 0**
> 力扣：[3075. 幸福值最大化的选择方案](https://leetcode.cn/problems/maximize-happiness-of-selected-children/) · Medium · 灵茶山艾府：[排序 + 贪心（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3075.幸福值最大化的选择方案

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-happiness-of-selected-children/description/)

题目要求最终的幸福值之和最大，那么常规的思路就是优先选择幸福值大的，但是在这里还有衰减的存在，需要考虑衰减对结果的影响。

首先可以明确的是，最终选择的必然是初始幸福值最大的k个，理由是如果其中存在前k大之外的，就可以用初始幸福值前k大中落选的，来替换掉这个前k大之外的。由于二者经过的衰减是相同的，因此最终的幸福值之和必然是更优的。

接下来，则需要确定这前k大的幸福值应该按什么顺序选取。不妨设选取的下标顺序为p[0]，p[1]，...，p[k - 1]，那么最终的幸福值之和就是

max(happiness\[p\[0\]\] - 0, 0) + max(happiness\[p\[1\]\] - 1, 0) + ... + max(happiness\[p\[k - 1\]\] - (k - 1), 0)

观察这个式子可以发现，若happiness[index]大于等于index，那么就相当于付出了index的代价，但是当happiness[index]小于index时，实际上付出的代价只有happiness[index]，是小于index的。为了使得这个式子的值最大，由于happiness前k大的和是固定的，那么就应该想办法让付出的代价值之和最小，于是一个自然的想法就是让happiness较小的值去应对较大的代价，即使用happiness第k大的去对应k - 1，happiness第k - 1大的去对应k - 2，...，happiness最大的去对应0。

下面给出简单的证明。

不妨设happiness中第k大的值为x，接下来只讨论x \< k - 1情况，因为当x >\= k - 1时，无论怎么排布付出的代价都不变，无需讨论。

若最终对应k - 1的不是x，那么不妨设对应k - 1的为y，在这里就有隐藏条件y > x。另外，不妨设x此时对应的是t，同样有隐藏条件t \< k - 1，此时就可以分几种情况进行讨论：

1、若y \<\= k - 1，x \< t：

此时二者的代价和为x + y。

若交换x和y，又可以分为两种情况。若y > t，那么交换后的代价和为x + t \< x + y，是更优的选择；若y \<\= t，交换后的代价和依然是x + y。

2、若y > k - 1，x \< t:

此时二者的代价和为k - 1 + x。

若交换x和y，由于y > k - 1 > t，因此交换后的代价和为t + x \< k - 1 + x，是更优的选择。

3、若y \<\= k - 1，x > t：

此时二者的代价和为y + t。

若交换x和y，由于y > x > t，因此交换后的代价和为x + t \< y + t，是更优的选择。

4、若y > k - 1, x > t:

此时二者的代价和为k - 1 + t

若交换x和y，由于y > x > t，因此交换后的代价和为x + t \< k - 1 + t，是更优的选择。

综合上面几种情况就可以发现，让x对应到k - 1一定是最优的选择。更进一步的，可以使用相同的方法证明应该让第k - 1大的对应到k - 2，依次类推。这样一来就证明了从大到小进行选取是最优的，因此只需将happiness从大到小排序后选取前k个就行了。

最后附上python代码：

```python
class Solution(object):
    def maximumHappinessSum(self, happiness, k):
        """
        :type happiness: List[int]
        :type k: int
        :rtype: int
        """

        return sum([max(v - index, 0) for index, v in enumerate(sorted(happiness, reverse=True)[:k])])
```

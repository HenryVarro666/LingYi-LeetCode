---
title: "2916. 子数组不同元素数目的平方和II"
aliases: ["yiduobo的每日leetcode 2916.子数组不同元素数目的平方和II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/segment-tree", "leetcode/dynamic-programming", "题单/常用数据结构", "题单/动态规划", "题单/常用数据结构/八-树状数组和线段树", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/664807254"
zhihu_id: "664807254"
zhihu_title: "yiduobo的每日leetcode 2916.子数组不同元素数目的平方和II"
question_id: "2916"
question: "子数组不同元素数目的平方和 II"
problem_url: "https://leetcode.cn/problems/subarrays-distinct-element-sum-of-squares-ii/"
difficulty: "Hard"
rating: 2816
created: "2023-11-03T04:35:49+08:00"
updated: "2023-11-03T04:35:49+08:00"
upvotes: 0
comments: 0
---

# 2916. 子数组不同元素数目的平方和II

> **[yiduobo的每日leetcode 2916.子数组不同元素数目的平方和II](https://zhuanlan.zhihu.com/p/664807254) · 知乎 · 2023-11-03 · 赞同 0**
> 力扣：[2916. 子数组不同元素数目的平方和 II](https://leetcode.cn/problems/subarrays-distinct-element-sum-of-squares-ii/) · Hard · 灵茶山艾府：[一步步提示你思考本题！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2916.子数组不同元素数目的平方和II

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/subarrays-distinct-element-sum-of-squares-ii/)

之前2913题的升级版，题设没有变化但是数据规模大了很多，这也就意味着只能使用O(n)或者O(nlogn)的算法。

由于题目需要针对子数组进行计算，那么本题只能是枚举子数组的一侧，然后通过之前的计算结果以及当前新加入到的数来得到当前的结果才有可能满足时间复杂度的要求。对于本题，我选择的是枚举子数组的右边界，因为这样的话就可以在正序遍历中利用上一轮的计算结果，比较顺手。如果枚举左边界的话，就需要倒序遍历了。

对于当前枚举到的右边界index，不妨设对于index - 1，子数组nums[0: index]中不同元素的数目为v[0]，nums[1: index]中不同元素的数目为v[1]，以此类推，最终得到的是一个v数组v[0]到v[index - 1]，那么以index - 1为右边界的所有子数组的不同元素数目平方和就是square_s \= v[0]^2 + v[1]^2 + ... + v[index - 1]^2。

接下来的任务就是：

1、如何在新加入nums[index]之后更新v数组

2、如何在更新v数组之后得到最新的square_s

如果能解决以上两点的话，将每一步的square_s累加起来就能得到最终答案。

---

首先来看任务1，如何使用nums[index]更新数组v。

不妨设nums[index]最后一次出现在index左侧的位置为pre，那么对于所有左边界在0到pre之间，右边界为index的子数组而言，其中由于已经出现过了nums[index]，因此在加入了nums[index]之后不同元素的数量依然会保持不变，即v[0]到v[pre]的值将保持不变；反之，对于所有左边界在pre + 1到index之间，右边界为index的子数组而言，由于nums[index]是首次出现，因此这些子数组中不同元素的数目多出了1，换言之，在这里需要将v的pre + 1到index这个区间都加上1。

这是一个非常经典的区间加法操作，但是暂时还不好确定使用什么数据结构来执行。如果后续需要动态查询，那么就需要使用线段树；如果不需要，则可以通过差分数组记录，最后一趟遍历离线计算。

---

接下来对于任务2，观察上一轮的square_s和本轮的差别。

square_s[index - 1] \= v[0]^2 + v[1]^2 + ... + v[index - 1]^2 + v[index]^2

最后这一项v[index]必然为0，在这里添加进来只是为了方便对比计算

square_s[index] \= (v[0]^2 + v[1]^2 + ... + v[pre]^2) + ((v[pre + 1] + 1)^2 + ... (v[index - 1] + v)^2 + (v[index] + 1) ^2)

新的平方和可以分为两个部分，分别是0到pre这个部分，与上一轮的计算方式保持一致；以及pre + 1到index这个部分，由于其对应的v值增加了1，因此在计算平方和时需要考虑这个新来的1。

直接用square_s[index] - square_s[index - 1]，就可以约掉所有的平方项，而剩下的是从pre + 1开始的一次项以及若干个1，具体来说，为

square_s[index] - square_s[index - 1] \= (2 \* v[pre + 1] + 1) + (2 \* v[pre + 2] + 1) + ... + (2 \* v[index] + 1)

整理后就是

square_s[index] - square_s[index - 1] \= 2 \* (v[pre + 1] + v[pre + 2] + ... + v[index]) + index - pre + 1

可以发现，其中2 \* (v[pre + 1] + v[pre + 2] + ... + v[index])这一段是数组v在上一轮的区间和，同时恰好也是任务1中需要修改的这一段，那么在这里就需要采用线段树来完成这个求和以及更新。

---

综合以上的分析就得到了一种做法：

一趟遍历枚举右边界index，同时在过程中使用线段树f维护v数组，使用square_s记录当前右边界对应的所有子数组的平方和，使用哈希表pre记录每个数最后一次出现的位置。接下来对于nums[index]：

1、首先得到需要计算区间和以及更新区间v数值的区间左右边界left和right。其中right就是index，而对于left的计算，若nums\[index\]存在于pre中，那么left就是pre\[nums\[index\]\] + 1，否则就为0

2、通过线段树得到v[left]到v[right]的区间和s

3、通过线段树更新v[left]到v[right]的值，为每个位置都加上1。由于是区间修改，因此在这里需要采用懒更新

4、将最新的square_s更新为square_s + s \* 2 + right - left + 1，然后累加到答案中

5、将pre\[nums\[index\]\]更新为index

这样一来，就可以在O(nlogn)的时间内解决这个问题了。

最后附上python代码：

```python
class Solution(object):
    def sumCounts(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        f = [0] * (n * 4)
        g = [0] * (n * 4)
        pre = {}
        mod = 10 ** 9 + 7

        def add(f, g, now, left, right, i, j, v):
            f[now] += v * (j - i + 1)
            f[now] %= mod
            if left == i and right == j:
                g[now] += v
                return

            mid = (left + right) / 2
            if j <= mid:
                add(f, g, now + now + 1, left, mid, i, j, v)
            elif i > mid:
                add(f, g, now + now + 2, mid + 1, right, i, j, v)
            else:
                add(f, g, now + now + 1, left, mid, i, mid, v)
                add(f, g, now + now + 2, mid + 1, right, mid + 1, j, v)

        def get(f, now, left, right, i, j):
            if left == i and right == j:
                return f[now]

            mid = (left + right) / 2

            if g[now] > 0:
                add(f, g, now + now + 1, left, mid, left, mid, g[now])
                add(f, g, now + now + 2, mid + 1, right, mid + 1, right, g[now])
                g[now] = 0

            if j <= mid:
                return get(f, now + now + 1, left, mid, i, j)
            elif i > mid:
                return get(f, now + now + 2, mid + 1, right, i, j)
            else:
                return get(f, now + now + 1, left, mid, i, mid) + get(f, now + now + 2, mid + 1, right, mid + 1, j)

        square_s = 0
        res = 0
        for index, v in enumerate(nums):
            left, right = pre.get(v, -1) + 1, index

            s = get(f, 0, 0, n - 1, left, right)
            add(f, g, 0, 0, n - 1, left, right, 1)
            square_s += s * 2 + right - left + 1
            square_s %= mod
            res += square_s
            res %= mod

            pre[v] = index
        
        return res
```

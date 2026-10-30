---
title: "3719. 最长平衡子数组I & 3721. 最长平衡子数组II"
aliases: ["yiduobo的每日leetcode 3719.最长平衡子数组I && 3721.最长平衡子数组II", "3719. 最长平衡子数组I", "3721. 最长平衡子数组II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/segment-tree", "leetcode/hash-table", "leetcode/prefix-sum", "leetcode/hard", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1963357666714813491"
zhihu_id: "1963357666714813491"
zhihu_title: "yiduobo的每日leetcode 3719.最长平衡子数组I && 3721.最长平衡子数组II"
question_id: ["3719", "3721"]
question: ["最长平衡子数组 I", "最长平衡子数组 II"]
problem_url: ["https://leetcode.cn/problems/longest-balanced-subarray-i/", "https://leetcode.cn/problems/longest-balanced-subarray-ii/"]
difficulty: ["Medium", "Hard"]
rating: 2724
created: "2025-10-20T21:27:13+08:00"
updated: "2025-10-20T21:27:17+08:00"
upvotes: 3
comments: 0
---

# 3719. 最长平衡子数组I & 3721. 最长平衡子数组II

> **[yiduobo的每日leetcode 3719.最长平衡子数组I && 3721.最长平衡子数组II](https://zhuanlan.zhihu.com/p/1963357666714813491) · 知乎 · 2025-10-20 · 赞同 3**
> 力扣：[3719. 最长平衡子数组 I](https://leetcode.cn/problems/longest-balanced-subarray-i/) · Medium · 灵茶山艾府：[非暴力做法（Python/Java/C++/Go）](../3719%20最长平衡子数组%20I/灵茶山艾府.md)
> 力扣：[3721. 最长平衡子数组 II](https://leetcode.cn/problems/longest-balanced-subarray-ii/) · Hard · 灵茶山艾府：[两种方法维护前缀和：Lazy 线段树 / 分块（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3719.最长平衡子数组I

[3719. 最长平衡子数组 I - 力扣（LeetCode）](https://leetcode.cn/problems/longest-balanced-subarray-i/description/)

3721.最长平衡子数组II

[3721. 最长平衡子数组 II - 力扣（LeetCode）](https://leetcode.cn/problems/longest-balanced-subarray-ii/description/)

题目给出一个整数数组nums。

若一个子数组中不同偶数的数量与不同奇数的数量相等，就称该子数组为平衡的。

要求返回nums中最长平衡子数组的长度。

两题的题设一致，第二题的数据规模较大，nums的长度以及其中元素的大小都可达10^5。

如果不考虑不同偶数以及不同奇数这个要求的话，就变成了之前遇到过的经典问题。只需要将所有的奇数都视为-1，将偶数都视为1，问题就变成了找出最长的和为零的子数组。对于这个问题，只需要将区间和问题转化为前缀和问题，配合哈希表一趟遍历就行了。

回到本题。如果想继续沿用上面的思路，就需要想办法出现重复元素的问题。

如果还是采用类似的一趟遍历计算前缀和的方式，那么对于当前遍历到的位置的前缀和s是很好计算的，只需要判断当前元素在之前是否出现过，如果没有，就根据奇偶性正常更新s，否则s不变。

而对于被减掉的那个前缀和而言，就比较麻烦了。不妨设当前元素上一次出现的位置为p，那么当被减掉的前缀和的结束位置小于等于p时，当前子数组内当前元素至少出现了两次，也就是说当前元素不应该计数。反之，若结束位置大于p时，当前元素在子数组内是独一无二的，应该被计数。可以发现，对于后面这种情况计算会出现问题，因为在计算s的时候因为当前元素不是独一无二的，因此当前元素是没有被计入s的，需要想办法进行修正。

在这里直接对s进行修正不是好的处理方案，因为一开始并不知道被减掉的前缀和的结束位置，也就是说并不清楚哪些在计算s时没有被计算的元素应该重新被计数。基于这一点，则可以反过来思考，修正之前储存的前缀和。具体来说，对于当前元素v，若其是首次出现，那么所有包含其的前缀都应该将其计算进去，反之，若其上次出现的位置为p，由于v在s中没有被计数，那么此时只能让作为被减数的一方，也就是从p开始的所有前缀和都反向计数当前元素一次。

更形式化的说法就是，对于首次出现的元素v，将终点在[index, n]之间的前缀和都加上v对应的值，其中v为偶数时加上1，v为奇数时加上-1。反之，若v不是首次出现，那么就将终点在[p, index - 1]之间的前缀和都减去v对应的值，其中v为偶数时减去1，v为奇数时减去-1。

修正完成后，只需要找出最小的等于s的前缀和的下标q，使用index - q更新答案即可。

到了这里，问题就转化为了给出一个一开始全为0的数组，在每次操作中，可能：

1、将某个区间中的所有元素加上1或者减去1

2、查询特定值s在数组中第一次出现的下标

对于前面这个操作，利用线段树可以很方便的解决。

对于后面这个操作，由于题目中所有的区间修正操作，对于同一个左边界只会执行最多一次加法操作以及一次减法操作，因此最终的数组相邻元素之差不会超过1。基于这一点，就可以将查询问题转化为判定问题，只需记录区间中的最大值和最小值，若s在最大值和最小值之间，那么区间中必然存在s。区间最值同样可以通过线段树很方便的解决。

在具体实现上，线段树中的区间修改只需要记录而不需要下放。

不妨设这区间被修改的值、最大值、最小值分别为f、ma、mi，那么在更新时，可以先递归修改左右子区间，然后通过子区间的ma + f以及mi + f来更新当前区间的ma以及mi。

在查询时，则只需判断查询的v减去左半子区间的f是否落在左半子区间的ma与mi之间，若是，则将v减去左半子区间的f，然后在左半子区间中递归查询v，反之则将v减去右半子区间的f，然后在右边子区间中递归查询v。

最后附上python代码：

```python
class Solution(object):
    def longestBalanced(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        n = len(nums)
        ma = [0] * ((n + 1) * 4)
        mi = [0] * ((n + 1) * 4)
        f = [0] * ((n + 1) * 4)
        pre = {}
        res = 0

        def update(now, left, right, start, end, delta):
            if left == start and right == end:
                f[now] += delta
                return
            
            mid = (left + right) // 2
            if end <= mid:
                update(now + now + 1, left, mid, start, end, delta)
            elif start > mid:
                update(now + now + 2, mid + 1, right, start, end, delta)
            else:
                update(now + now + 1, left, mid, start, mid, delta)
                update(now + now + 2, mid + 1, right, mid + 1, end, delta)

            ma[now] = max(ma[now + now + 1] + f[now + now + 1], ma[now + now + 2] + f[now + now + 2])
            mi[now] = min(mi[now + now + 1] + f[now + now + 1], mi[now + now + 2] + f[now + now + 2])
        
        def get(now, left, right, v):
            if left == right:
                if mi[now] <= v <= ma[now]:
                    return left
                return None
            
            mid = (left + right) // 2
            if mi[now + now + 1] <= v - f[now + now + 1] <= ma[now + now + 1]:
                return get(now + now + 1, left, mid, v - f[now + now + 1])
            else:
                return get(now + now + 2, mid + 1, right, v - f[now + now + 2])

        s = 0
        for index, v in enumerate(nums):
            if v % 2 == 0:
                delta = 1
            else:
                delta = -1

            if v not in pre:
                update(0, 0, n, index + 1, n, delta)
                s += delta
            else:
                update(0, 0, n, pre[v], index, -delta)

            pre[v] = index + 1
            p = get(0, 0, n, s)
            if p is not None:
                res = max(res, index + 1 - p)
        
        return res
```

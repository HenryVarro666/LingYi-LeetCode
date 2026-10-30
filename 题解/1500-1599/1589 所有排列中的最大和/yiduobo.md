---
title: "1589. 所有排列中的最大和"
aliases: ["yiduobo的每日leetcode 1589.所有排列中的最大和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/431418392"
zhihu_id: "431418392"
zhihu_title: "yiduobo的每日leetcode 1589.所有排列中的最大和"
question_id: "1589"
question: "所有排列中的最大和"
problem_url: "https://leetcode.cn/problems/maximum-sum-obtained-of-any-permutation/"
created: "2021-11-09T23:53:02+08:00"
updated: "2021-11-09T23:53:02+08:00"
upvotes: 1
comments: 0
---

# 1589. 所有排列中的最大和

> **[yiduobo的每日leetcode 1589.所有排列中的最大和](https://zhuanlan.zhihu.com/p/431418392) · 知乎 · 2021-11-09 · 赞同 1**
> 力扣：[1589. 所有排列中的最大和](https://leetcode.cn/problems/maximum-sum-obtained-of-any-permutation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1589.所有排列中的最大和

[力扣](https://leetcode-cn.com/problems/maximum-sum-obtained-of-any-permutation/)

题目中的每个request实际上是求一个区间的和，那么如果将这些区间和展开，就可以得到0到n - 1这n个位置每个位置被计算的次数。为了使得最终结果最大，显然就应该将较大的数放在使用次数较多的位置上。

根据上面的结论，现在题目就被分成了两个部分，即如何求出每个位置被计算的次数，以及如何分配最终的数字。

首先考虑统计计算的次数。按常规动态区间的做法，使用各种logn的数据结构都是可以的，不过注意到这里是一个静态的区间和问题，同时每次修改的值都是1，那么在这里使用差分数组就可以完成求解。具体来说就是从0到n - 1一趟扫描，对于当前位置index，使用一个变量now统计当前正在生效的区间数目。若index是某个区间的起点，那么将now加上1，若index是某个区间终点的后一位，那么将now减去1。最终now的值就是覆盖index这个位置的区间数目了。为了让这个计算过程更加高效，可以将区间按起点从小到大进行排序，那么随着index的增大，利用区间起点的单调性则可以在均摊O(1)的时间复杂度内找出所有起点为index的区间，而对于当前正在生效区间的终点，则可以使用一个数组记录下这些结束位置，当index到达这些位置时再进行相应的更新。

得到每个位置被计算的次数之后，只需要将原数组从大到小进行排序，然后将大的数填充到次数较多的位置上，并计算总和即可。

最后附上python代码：

```python
class Solution(object):
    def maxSumRangeQuery(self, nums, requests):
        """
        :type nums: List[int]
        :type requests: List[List[int]]
        :rtype: int
        """

        n = len(nums)
        end_pos = [0] * n
        requests = sorted(requests, key=lambda d:d[0])
        now = 0
        p = 0
        cnt_dict = {}
        for index in range(n):
            now -= end_pos[index]
            while p < len(requests) and requests[p][0] == index:
                now += 1
                if requests[p][1] < n - 1:
                    end_pos[requests[p][1] + 1] += 1
                p += 1
            
            if now > 0:
                cnt_dict[now] = cnt_dict.get(now, 0) + 1
        
        nums = sorted(nums, reverse=True)
        offset = 0
        res = 0
        mod = 10 ** 9 + 7
        for cnt in sorted(cnt_dict.keys(), reverse=True):
            for index in range(cnt_dict[cnt]):
                res += nums[offset + index] * cnt
                res %= mod
            offset += cnt_dict[cnt]
        
        return res
```

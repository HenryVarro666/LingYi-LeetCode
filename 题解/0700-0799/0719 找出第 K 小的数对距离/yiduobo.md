---
title: "719. 找出第k小的距离对"
aliases: ["yiduobo的每日leetcode 719.找出第k小的距离对"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/two-pointers", "leetcode/binary-search", "leetcode/sorting", "题单/二分算法", "题单/二分算法/二-二分答案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/331765163"
zhihu_id: "331765163"
zhihu_title: "yiduobo的每日leetcode 719.找出第k小的距离对"
question_id: "719"
question: "找出第 K 小的数对距离"
problem_url: "https://leetcode.cn/problems/find-k-th-smallest-pair-distance/"
difficulty: "Hard"
created: "2020-12-05T17:51:17+08:00"
updated: "2020-12-05T17:51:17+08:00"
upvotes: 0
comments: 0
---

# 719. 找出第k小的距离对

> **[yiduobo的每日leetcode 719.找出第k小的距离对](https://zhuanlan.zhihu.com/p/331765163) · 知乎 · 2020-12-05 · 赞同 0**
> 力扣：[719. 找出第 K 小的数对距离](https://leetcode.cn/problems/find-k-th-smallest-pair-distance/) · Hard · 灵茶山艾府：[第 k 小/大问题的通用转化方法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

719.找出第k小的距离对

[力扣](https://leetcode-cn.com/problems/find-k-th-smallest-pair-distance/)

最简单的做法自然是一组组来算，时间复杂度为O(n^2)。注意到这里每个数的范围都在0到1000000之间，因此这个距离的上界最多为1000000，而下界为0，因此我们可以二分答案，对于当前二分到的mid，检查所有距离对中有多少个小于等于mid，这一步在对nums排序后，可以在O(n)的时间复杂度完成，因此最终的时间复杂度就是排序的时间加上二分检测的时间，为O(nlogn + nlog(max_diff))。

其中检测距离对中有多少个小于等于mid的做法，简单来说就是先对nums进行排序，然后对于每个nums[index]，先找到最小的p，满足nums[p] - nums[index] > mid，此时以nums[index]作为较小数的距离在mid之内的数对就有p - index - 1组。

接下来对于nums[index + 1]，由于nums[index + 1] >\= nums[index]，因此对于nums[index + 2]到nums[p - 1]，这些数与nums[index]差小于等于mid，那么与nums[index +1]的差必然也小于等于mid，因此接下来就可以直接从p开始往后移动，直到nums[p] - nums[index + 1] > mid。

由于index和p都只会遍历一次，因此检测这个操作的时间复杂度就是O(n)。

最后附上python代码：

```python
class Solution(object):
    def smallestDistancePair(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        nums = sorted(nums)
        n = len(nums)

        l = 0
        r = nums[-1] - nums[0]
        while l < r:
            mid = (l + r) >> 1
            p = 1
            cnt = 0
            for index in range(n - 1):
                while p < n and nums[p] - nums[index] <= mid:
                    p += 1
                
                if p == index + 1:
                    p += 1
                else:
                    cnt += p - index - 1

            if cnt >= k:
                r = mid
            else:
                l = mid + 1

        return l
```

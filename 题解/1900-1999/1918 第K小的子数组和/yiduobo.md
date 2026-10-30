---
title: "1918. 第K小的子数组和"
aliases: ["yiduobo的每日leetcode 1918.第K小的子数组和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/623300256"
zhihu_id: "623300256"
zhihu_title: "yiduobo的每日leetcode 1918.第K小的子数组和"
question_id: "1918"
question: "第K小的子数组和"
problem_url: "https://leetcode.cn/problems/kth-smallest-subarray-sum/"
created: "2023-04-20T01:24:28+08:00"
updated: "2023-04-20T01:24:28+08:00"
upvotes: 0
comments: 0
---

# 1918. 第K小的子数组和

> **[yiduobo的每日leetcode 1918.第K小的子数组和](https://zhuanlan.zhihu.com/p/623300256) · 知乎 · 2023-04-20 · 赞同 0**
> 力扣：[1918. 第K小的子数组和](https://leetcode.cn/problems/kth-smallest-subarray-sum/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1918.第K小的子数组和

[力扣](https://leetcode.cn/problems/kth-smallest-subarray-sum/)

对于一个长度为n的数组，其中子数组的总数是O(n^2)级别的，那么直接暴力枚举显然是不行的。

另一种思路则是通过二分来寻找这个子数组和。对于当前二分到的数组和mid，计算所有子数组中有多少个子数组之和小于等于mid，然后通过这个数目与k的大小对比来调整二分的上下界。

现在的问题就变成了给出一个数mid，判断有多少个子数组之和小于等于mid。

注意到数组中的数都是正数，那么对于给定的位置index，就可以通过一趟遍历找出最大的满足子数组和不超过mid的边界bound，也就是说所有左边界为index，右边界在index到bound中的子数组都是符合条件的，一共有bound - index + 1个。

另一方面，对于位置index + 1，其对应的右边界必然大于等于bound，那么index + 1对应的新的bound就可以在index对应的bound的基础上得到，这样一来，就可以利用滑动窗口，在一趟遍历的时间内找出所有index对应的bound，从而计算出满足数组和小于等于mid的子数组数量cnt，然后通过cnt与k的大小来调整二分的上下界。

最后附上python代码：

```python
class Solution(object):
    def kthSmallestSubarraySum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        left = min(nums)
        right = sum(nums)
        n = len(nums)

        while left < right:
            mid = (left + right) / 2
            bound = 0
            now = 0
            while bound < n and now + nums[bound] <= mid:
                now += nums[bound]
                bound += 1

            cnt = bound
            for index, v in enumerate(nums):
                now -= v
                if bound < index:
                    bound = index
                while bound < n and now + nums[bound] <= mid:
                    now += nums[bound]
                    bound += 1
                cnt += bound - index - 1

            if cnt < k:
                left = mid + 1
            else:
                right = mid
        
        return left
```

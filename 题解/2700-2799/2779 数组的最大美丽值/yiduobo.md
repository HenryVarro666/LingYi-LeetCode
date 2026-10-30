---
title: "2779. 数组的最大美丽值"
aliases: ["yiduobo的每日leetcode 2779.数组的最大美丽值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sorting", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/655915897"
zhihu_id: "655915897"
zhihu_title: "yiduobo的每日leetcode 2779.数组的最大美丽值"
question_id: "2779"
question: "数组的最大美丽值"
problem_url: "https://leetcode.cn/problems/maximum-beauty-of-an-array-after-applying-operation/"
difficulty: "Medium"
rating: 1638
created: "2023-09-13T04:13:45+08:00"
updated: "2023-09-13T04:13:45+08:00"
upvotes: 0
comments: 0
---

# 2779. 数组的最大美丽值

> **[yiduobo的每日leetcode 2779.数组的最大美丽值](https://zhuanlan.zhihu.com/p/655915897) · 知乎 · 2023-09-13 · 赞同 0**
> 力扣：[2779. 数组的最大美丽值](https://leetcode.cn/problems/maximum-beauty-of-an-array-after-applying-operation/) · Medium · 灵茶山艾府：[转化成滑动窗口问题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2779.数组的最大美丽值

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/maximum-beauty-of-an-array-after-applying-operation/)

注意到题目中的数组元素大小以及k的大小与数组长度n是同一个量级的，那么就意味着完全可以直接暴力枚举数组得到最大美丽值时对应的最长子序列中的那个数值。值得一提的是，这个数值必然在数组最小值和数组最大值之间，因为对于超出边界的数，要得到它们的代价显然是更高的，因此可以形成的子序列长度必然就更短。

对于一个目标数值target，只有数值在target - k到target + k之间的数才能变成target，也就是说此时可以形成的子序列的最大长度就是数组中值在target - k到target + k之间的数的个数。对于这个问题，则可以通过类似桶排的方法，使用一个计数数组cnt记录数组中每个数出现的次数，接下来再一趟遍历，将cnt由计数数组转化为前缀和数组，这样一来就target - k到target + k之间的数的个数就是cnt[target + k] - cnt[target - k - 1]。

另外需要注意的是，这里的target - k和target + k都可能越界，因此在计算时需要处理边界情况。

最后附上python代码：

```python
class Solution(object):
    def maximumBeauty(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        ma = max(nums)

        cnt = [0] * (ma + 1)
        for v in nums:
            cnt[v] += 1
        for v in range(1, ma + 1):
            cnt[v] += cnt[v - 1]
        
        res = 0
        for target in range(ma + 1):
            left = max(0, target - k)
            right = min(ma, target + k)
            
            if left > 0:
                res = max(res, cnt[right] - cnt[left - 1])
            else:
                res = max(res, cnt[right])
        
        return res
```

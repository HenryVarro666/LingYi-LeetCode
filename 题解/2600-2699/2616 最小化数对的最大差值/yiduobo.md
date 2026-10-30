---
title: "2616. 最小化数对的最大差值"
aliases: ["yiduobo的每日leetcode 2616.最小化数对的最大差值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/binary-search", "leetcode/sorting", "题单/二分算法", "题单/二分算法/二-二分答案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/646174672"
zhihu_id: "646174672"
zhihu_title: "yiduobo的每日leetcode 2616.最小化数对的最大差值"
question_id: "2616"
question: "最小化数对的最大差值"
problem_url: "https://leetcode.cn/problems/minimize-the-maximum-difference-of-pairs/"
difficulty: "Medium"
rating: 2155
created: "2023-07-27T02:40:11+08:00"
updated: "2023-07-27T02:40:11+08:00"
upvotes: 0
comments: 0
---

# 2616. 最小化数对的最大差值

> **[yiduobo的每日leetcode 2616.最小化数对的最大差值](https://zhuanlan.zhihu.com/p/646174672) · 知乎 · 2023-07-27 · 赞同 0**
> 力扣：[2616. 最小化数对的最大差值](https://leetcode.cn/problems/minimize-the-maximum-difference-of-pairs/) · Medium · 灵茶山艾府：[二分答案 + 贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2616.最小化数对的最大差值

[力扣](https://leetcode.cn/problems/minimize-the-maximum-difference-of-pairs/)

数对间的最大差值越大，就越容易构造出足够的数对，也就是说在这里可以使用二分答案来求解。

对于当前二分到的最大差值mid，接下来要尝试构造出至少p对差值小于等于mid的数对。

不妨考虑当前剩余数中的最小值。对于这个最小值，第一种方案自然是直接放弃掉，而第二种方案则应该选择当前剩余数中次小值与其配对。在这里选择次小值的原因是由于后续配对的数会越来越大，因此在这里选择次小值就可以将更大的数留给后续的数进行配对，同时最小值与次小值配对的成功率也最高。

到了这里，可以发现这又是类似打家劫舍的动态规划问题。

将数组从小到大排序，令f[i]表示前i个数可以形成的合法配对数量，初始状态下就有f[0] \= f[1] \= 0。接下来对于i >\= 1，首先可以初始化f[i + 1] \= f[i]，表示放弃掉nums[i]，而如果要选择使用nums[i]的话，就需要满足nums[i] - nums[i - 1] \<\= mid，此时就有f[i + 1] \= max(f[i + 1], f[i - 1] + 1)。

若最终的f[n]大于等于p，说明可以找出足够的配对，此时更新二分的上界为mid，否则更新二分的下界为mid + 1即可。

最后附上python代码：

```python
class Solution(object):
    def minimizeMax(self, nums, p):
        """
        :type nums: List[int]
        :type p: int
        :rtype: int
        """

        nums.sort()
        left = 0
        right = nums[-1] - nums[0]
        while left < right:
            mid = (left + right) >> 1
            f = [0, 0]
            for index in range(1, len(nums)):
                f.append(f[-1])
                if nums[index] - nums[index - 1] <= mid:
                    f[-1] = max(f[-1], f[-3] + 1)

            if f[-1] >= p:
                right = mid
            else:
                left = mid + 1
        
        return left
```

---
title: "4067. 数对和受限的最长子数组"
aliases: ["yiduobo的每日leetcode 4067.数对和受限的最长子数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sliding-window"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2089025950491080339"
zhihu_id: "2089025950491080339"
zhihu_title: "yiduobo的每日leetcode 4067.数对和受限的最长子数组"
question_id: "4067"
question: "数对和受限的最长子数组"
problem_url: "https://leetcode.cn/problems/longest-subarray-with-restricted-pair-sums/"
difficulty: "Medium"
created: "2026-10-01T17:15:42+08:00"
updated: "2026-10-01T17:15:42+08:00"
upvotes: 2
comments: 0
---

# 4067. 数对和受限的最长子数组

> **[yiduobo的每日leetcode 4067.数对和受限的最长子数组](https://zhuanlan.zhihu.com/p/2089025950491080339) · 知乎 · 2026-10-01 · 赞同 2**
> 力扣：[4067. 数对和受限的最长子数组](https://leetcode.cn/problems/longest-subarray-with-restricted-pair-sums/) · Medium · 灵茶山艾府：[滑动窗口：维护两数之和与两数之差的个数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4067.数对和受限的最长子数组

<https://leetcode.cn/problems/longest-subarray-with-restricted-pair-sums/description/>

题目给出一个整数数组nums，其长度不超过1000。

对于一个从l到r的子数组，若其中不存在三个互不相同的下标i、j和k，满足l \<\= i, j, k \<\= r且nums[i] + nums[j] \= nums[k]，那么就称这个子数组为有效子数组。

问有效子数组的最大长度。

对于两个左边界相同的子数组，右边界越靠后，其有效的可能性就越低，因此在这里可以利用滑动窗口计算对于每个左边界找出最大的合法右边界。

对于右边界的检测，需要考察新加入的元素是否会使得窗口内出现nums[i] + nums[j] \= nums[k]的情况。由于nums[i]和nums[j]是等价的，那么在这里只需要考察新元素是否可能成为nums[i]或者nums[k]。更具体的，就是当前窗口中是否有两个元素之和恰好等于新元素，或者两个元素之差恰好等于新元素。

因此，在这里可以维护两个哈希表s和d，分别记录窗口中每种数对和以及数对差出现的次数。那么对于新元素，只要其没有出现在s和d中，就可以将其加入窗口，同时记得使用这个新元素与其他元素的和与差来更新s和d。

同样的，当窗口左边界向后移动时，也需要将窗口中其他元素与左边界形成的和与差从哈希表中减去。

窗口移动时，维护哈希表的复杂度为O(n)，因此总的时间复杂度为O(n^2)，对于本题的数据规模是没有问题的。

最后附上python代码：

```python
class Solution(object):
    def maxSubarray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        s = {}
        d = {}

        p = 0
        res = 0
        for index, v in enumerate(nums):
            while p < len(nums) and nums[p] not in s and nums[p] not in d:
                for x in nums[index: p]:
                    s[x + nums[p]] = s.get(x + nums[p], 0) + 1
                    diff = abs(x - nums[p])
                    if diff != 0:
                        d[diff] = d.get(diff, 0) + 1

                p += 1
            
            res = max(res, p - index)

            if index < p:
                for x in nums[index + 1: p]:
                    s[x + v] -= 1
                    if s[x + v] == 0:
                        s.pop(x + v)
                    diff = abs(x - v)
                    if diff != 0:
                        d[diff] -= 1
                        if d[diff] == 0:
                            d.pop(diff)
        
        return res
```

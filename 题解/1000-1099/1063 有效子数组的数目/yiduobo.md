---
title: "1063. 有效子数组的数目"
aliases: ["yiduobo的每日leetcode 1063.有效子数组的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/monotonic-stack", "题单/单调栈", "题单/单调栈/一-单调栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/608032615"
zhihu_id: "608032615"
zhihu_title: "yiduobo的每日leetcode 1063.有效子数组的数目"
question_id: "1063"
question: "有效子数组的数目"
problem_url: "https://leetcode.cn/problems/number-of-valid-subarrays/"
difficulty: "Hard"
created: "2023-02-20T23:38:20+08:00"
updated: "2023-02-20T23:38:20+08:00"
upvotes: 0
comments: 0
---

# 1063. 有效子数组的数目

> **[yiduobo的每日leetcode 1063.有效子数组的数目](https://zhuanlan.zhihu.com/p/608032615) · 知乎 · 2023-02-20 · 赞同 0**
> 力扣：[1063. 有效子数组的数目](https://leetcode.cn/problems/number-of-valid-subarrays/) · Hard · 灵茶山艾府：[Go 单调栈](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1063.有效子数组的数目

[力扣](https://leetcode.cn/problems/number-of-valid-subarrays/)

题目的数据规模较大，因此不能直接使用O(n^2)的暴力算法，必须想办法进行优化。

对于左边界为left的子数组而言，不妨设p是left右侧最小的，且满足nums[p] > nums[left]的下标，那么当子数组的右边界right满足left \<\= right \< p时，子数组[left, right]都是有效子数组，而对于所有满足right \<\= p的子数组而言，则都不是有效子数组。换言之，左边界为left的有效子数组一共有p - 1 - left + 1 \= p - left个。另外需要注意的是，对于left若不存在符合条件的p，那么说明left右侧所有的元素都大于等于nums[left]，此时可以形成的有效子数组数目就是n - 1 - left + 1 \= n - left。

到了这里，问题就转化成了找出数组中下一个更小值的位置。这个问题可以直接参考之前496题的处理方法，使用单调栈来求解。需要注意符号的变换。

[yiduobo：yiduobo的每日leetcode 496.下一个更大元素I](https://zhuanlan.zhihu.com/p/257283167)

一趟遍历，求解出数组中所有下一个更小元素的下标，然后再一趟遍历，求解最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def validSubarrays(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        stack = []
        pos = [n] * n
        for index, num in enumerate(nums):
            while stack and num < nums[stack[-1]]:
                pos[stack[-1]] = index
                stack.pop()
            
            stack.append(index)
        
        res = 0
        for index, p in enumerate(pos):
            res += p - index
        
        return res
```

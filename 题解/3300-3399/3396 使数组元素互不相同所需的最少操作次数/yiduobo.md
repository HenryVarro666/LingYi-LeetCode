---
title: "3396. 使数组元素互不相同所需的最少操作次数"
aliases: ["yiduobo的每日leetcode 3396.使数组元素互不相同所需的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/bian-li", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/30646099328"
zhihu_id: "30646099328"
zhihu_title: "yiduobo的每日leetcode 3396.使数组元素互不相同所需的最少操作次数"
question_id: "3396"
question: "使数组元素互不相同所需的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-operations-to-make-elements-in-array-distinct/"
difficulty: "Easy"
rating: 3779
created: "2025-03-16T22:14:18+08:00"
updated: "2025-03-16T22:14:30+08:00"
upvotes: 1
comments: 0
---

# 3396. 使数组元素互不相同所需的最少操作次数

> **[yiduobo的每日leetcode 3396.使数组元素互不相同所需的最少操作次数](https://zhuanlan.zhihu.com/p/30646099328) · 知乎 · 2025-03-16 · 赞同 1**
> 力扣：[3396. 使数组元素互不相同所需的最少操作次数](https://leetcode.cn/problems/minimum-number-of-operations-to-make-elements-in-array-distinct/) · Easy · 灵茶山艾府：[O(n) 一次遍历，简洁写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3396.使数组元素互不相同所需的最少操作数

[3396. 使数组元素互不相同所需的最少操作次数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-number-of-operations-to-make-elements-in-array-distinct/description/)

题目给出一个整数数组nums，接下来可以对nums执行若干次操作。每次操作，会将nums开头的3个元素移除，若nums中元素的数目不足3个，则移除所有元素。问至少需要多少次操作才能使得nums中的元素互不相同。

对nums进行一趟遍历，使用哈希表cnt记录每种元素出现的次数，另外使用一个变量same记录nums中重复元素的数目。对于当前遍历到的元素v，若cnt[v]从1变成了2，说明v是重复的，此时应该将same加上1。

遍历完成后，再按照题目描述模拟，从下标0开始3个一个遍历nums，使用当前遍历到的元素值v修正cnt。若某一个时刻cnt[v]从2变成了1，说明v不再重复，此时应该将same减去1。重复此过程直到same等于0，执行的轮次即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minimumOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        cnt = {}
        same = 0
        for v in nums:
            cnt[v] = cnt.get(v, 0) + 1
            if cnt[v] == 2:
                same += 1
        
        res = 0
        p = 0
        while same > 0:
            res += 1
            for index in range(p, min(p + 3, len(nums))):
                v = nums[index]
                cnt[v] -= 1
                if cnt[v] == 1:
                    same -= 1
            p += 3
        
        return res
```

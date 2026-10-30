---
title: "3779. 得到互不相同元素的最少操作次数"
aliases: ["yiduobo的每日leetcode 3779.得到互不相同元素的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1986208485537517647"
zhihu_id: "1986208485537517647"
zhihu_title: "yiduobo的每日leetcode 3779.得到互不相同元素的最少操作次数"
question_id: "3779"
question: "得到互不相同元素的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-operations-to-have-distinct-elements/"
difficulty: "Medium"
rating: 1444
created: "2025-12-21T23:03:26+08:00"
updated: "2025-12-21T23:03:40+08:00"
upvotes: 2
comments: 0
---

# 3779. 得到互不相同元素的最少操作次数

> **[yiduobo的每日leetcode 3779.得到互不相同元素的最少操作次数](https://zhuanlan.zhihu.com/p/1986208485537517647) · 知乎 · 2025-12-21 · 赞同 2**
> 力扣：[3779. 得到互不相同元素的最少操作次数](https://leetcode.cn/problems/minimum-number-of-operations-to-have-distinct-elements/) · Medium · 灵茶山艾府：[O(n) 一次遍历，简洁写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3779.得到互不相同元素的最少操作次数

[3779. 得到互不相同元素的最少操作次数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-number-of-operations-to-have-distinct-elements/description/)

题目给出一个整数数组nums。

在每次操作中，需要移除当前数组中的前三个元素，若剩余元素不足三个，则移除所有剩余元素。

重复此操作直到数组为空，或者其中不包含任何重复元素为止。

要求返回执行操作的次数。

由于操作停止的条件是数组为空或者其中不包含任意重复元素，而空数组自然是不包含重复元素的，因此可以统一理解成，将最后一个重复元素从数组中移除后，操作就停止了。

于是只需计算每个元素倒数第二次出现的位置中的最大值p，那么这个p就是上面说的最后一个重复元素的下标。在具体实现上，可以从后往前进行一趟遍历，使用哈希表记录出现过的元素。对于当前元素nums[index]，如果已经出现过，那么当前的index就是要找的p。

若不存在这样的p，说明数组一开始就是互不相同的，此时答案为0，否则就需要执行操作，移除掉数组中nums[0]到nums[p]这一共p + 1个元素，需要的操作次数就是(p + 1 - 1) // 3 + 1，即p // 3 + 1。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        vis = set()
        p = -1
        for index in range(len(nums) - 1, -1, -1):
            if nums[index] in vis:
                p = index
                break
            else:
                vis.add(nums[index])
        
        if p == -1:
            return 0
        
        return p // 3 + 1
```

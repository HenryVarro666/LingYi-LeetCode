---
title: "3810. 变成目标数组的最少操作次数"
aliases: ["yiduobo的每日leetcode 3810.变成目标数组的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1996366885109929971"
zhihu_id: "1996366885109929971"
zhihu_title: "yiduobo的每日leetcode 3810.变成目标数组的最少操作次数"
question_id: "3810"
question: "变成目标数组的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-reach-target-array/"
difficulty: "Medium"
rating: 1492
created: "2026-01-18T23:54:03+08:00"
updated: "2026-01-18T23:54:04+08:00"
upvotes: 0
comments: 0
---

# 3810. 变成目标数组的最少操作次数

> **[yiduobo的每日leetcode 3810.变成目标数组的最少操作次数](https://zhuanlan.zhihu.com/p/1996366885109929971) · 知乎 · 2026-01-18 · 赞同 0**
> 力扣：[3810. 变成目标数组的最少操作次数](https://leetcode.cn/problems/minimum-operations-to-reach-target-array/) · Medium · 灵茶山艾府：[脑筋急转弯（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3810.变成目标数组的最少操作次数

[3810. 变成目标数组的最少操作次数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-operations-to-reach-target-array/)

题目给出两个长度为n的整数数组nums和target，现在要求执行一下操作若干次（可以为零次），使得nums变成target。

每次操作中：

- 选择一个整数x
- 找出nums中所有的极大连续段，满足其中的所有元素都等于x，且无法再向两侧扩展
- 对于每个这样的段[left, right]，同时进行更新，使得:
   - nums[left] \= target[left], nums[left + 1] \= target[left + 1], ..., nums[right] \= target[right]

问最少需要执行多少次操作。

题目中关于操作的描述比较绕，实际上可以理解成每次操作，都选择一个整数x，然后将nums中所有等于x的都变为与对应的target相等。另一方面，这次操作可以将nums中所有等于x的元素都调整到等于target的状态，因此只需一趟遍历，对于当前的nums[index]，若其不等于target[index]，就将其加入到集合中，最终集合的大小就是需要执行操作的次数。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums, target):
        """
        :type nums: List[int]
        :type target: List[int]
        :rtype: int
        """
        
        m = set()
        for x, y in zip(nums, target):
            if x != y:
                m.add(x)
        
        return len(m)
```

---
title: "3523. 非递减数组的最大长度"
aliases: ["yiduobo的每日leetcode 3523.非递减数组的最大长度"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/八-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1902568467594449413"
zhihu_id: "1902568467594449413"
zhihu_title: "yiduobo的每日leetcode 3523.非递减数组的最大长度"
question_id: "3523"
question: "非递减数组的最大长度"
problem_url: "https://leetcode.cn/problems/make-array-non-decreasing/"
difficulty: "Medium"
rating: 1435
created: "2025-05-10T19:49:14+08:00"
updated: "2025-05-10T19:49:14+08:00"
upvotes: 2
comments: 0
---

# 3523. 非递减数组的最大长度

> **[yiduobo的每日leetcode 3523.非递减数组的最大长度](https://zhuanlan.zhihu.com/p/1902568467594449413) · 知乎 · 2025-05-10 · 赞同 2**
> 力扣：[3523. 非递减数组的最大长度](https://leetcode.cn/problems/make-array-non-decreasing/) · Medium · 灵茶山艾府：[贪心及其证明（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3523.非递减数组的最大长度

[3523. 非递减数组的最大长度 - 力扣（LeetCode）](https://leetcode.cn/problems/make-array-non-decreasing/description/)

题目给出一个整数数组nums，接下来每次操作，可以将nums中的某个子数组替换为这个子数组中的最大值。问使得nums变为非递减时nums的最大长度是多少。

题目要求nums变为非递减，那么就可以一趟遍历，逐对检测每组相邻的元素。对于nums中的某个元素v，若v小于其前一个元素，在这里就必须通过操作将v消除掉。在这里不能消除掉v的前一个元素，因为前面的部分是非递减的。无论v是与前一个元素进行操作，或是与后续的元素进行操作，v自身都必然会被消除掉，因此在这里无需关心具体的操作方式，只需将最终答案的长度减去1就行了。

另外需要注意的是，当某个元素v被消除后，其下一个元素的上一个元素应该是v的上一个元素，因此在这里还需要使用一个变量last记录剩余数组中的最后一个元素值。当v被消除时，last不变，当v不需要被消除时，就需要将last更新为v。

最后附上python代码：

```python
class Solution(object):
    def maximumPossibleSize(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        ma = nums[0]
        res = len(nums)
        for v in nums[1:]:
            if v < ma:
                res -= 1
            else:
                ma = v
        
        return res
```

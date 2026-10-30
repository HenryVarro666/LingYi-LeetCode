---
title: "3644. 排序排列"
aliases: ["yiduobo的每日leetcode 3644.排序排列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/brainteaser", "题单/位运算", "题单/贪心算法", "题单/位运算/八-思维题", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1948042633583768707"
zhihu_id: "1948042633583768707"
zhihu_title: "yiduobo的每日leetcode 3644.排序排列"
question_id: "3644"
question: "排序排列"
problem_url: "https://leetcode.cn/problems/maximum-k-to-sort-a-permutation/"
difficulty: "Medium"
rating: 1775
created: "2025-09-07T16:11:42+08:00"
updated: "2025-09-07T16:11:47+08:00"
upvotes: 0
comments: 0
---

# 3644. 排序排列

> **[yiduobo的每日leetcode 3644.排序排列](https://zhuanlan.zhihu.com/p/1948042633583768707) · 知乎 · 2025-09-07 · 赞同 0**
> 力扣：[3644. 排序排列](https://leetcode.cn/problems/maximum-k-to-sort-a-permutation/) · Medium · 灵茶山艾府：[构造 + 严谨证明（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3644.排序排列

<https://leetcode.cn/problems/maximum-k-to-sort-a-permutation/>

题目给出一个长度为n的整数数组nums，其中nums是0到n - 1的一个排列。现在可以在满足nums[i] AND nums[j] \= k的情况下交换nums[i]和nums[j]，其中AND表示按位与运算，k为一个非负整数。要求找出可以使得数组变为递增的最大的k，若nums已经有序，则返回0。

首先可以明确的一点是，对于一个处在正确位置上的元素而言，原则上是不应该动它的，因为本题中交换的规则只与元素值有关，与下标无关。当然，也有一个例外，就是这个元素就是答案k，需要用到这个元素作为中转。

基于这一点，就可以只考虑所有不在正确位置上的元素应该如何处理。由于本题中交换的规则是按位与的结果等于k，也就是说这些需要交换的元素的二进制位中必须包含k。更进一步的，这些不在正确位置上的元素的按位与结果就是答案的上限。

另一方面，由于按位与的结果是越来越小的，因此这些元素的按位与的结果也必然在0到n - 1之间，选择这个按位与的结果元素作为最终的k必然可以完成所有的交换。也就是说，这些元素的按位与即为最终答案。

另外，如果所有元素都在正确的位置上，应该直接返回0。

最后附上python代码：

```python
class Solution(object):
    def sortPermutation(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        res = None

        for index, v in enumerate(nums):
            if index != v:
                if res is None:
                    res = v
                else:
                    res &= v
        
        if res is None:
            return 0
        return res
```

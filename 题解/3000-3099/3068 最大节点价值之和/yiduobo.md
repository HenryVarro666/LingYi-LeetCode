---
title: "3068. 最大节点价值之和"
aliases: ["yiduobo的每日leetcode 3068.最大节点价值之和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/brainteaser", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/六-状态机-DP", "题单/动态规划/十二-树形-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/697272535"
zhihu_id: "697272535"
zhihu_title: "yiduobo的每日leetcode 3068.最大节点价值之和"
question_id: "3068"
question: "最大节点价值之和"
problem_url: "https://leetcode.cn/problems/find-the-maximum-sum-of-node-values/"
difficulty: "Hard"
rating: 2268
created: "2024-05-12T05:07:16+08:00"
updated: "2024-05-12T05:07:16+08:00"
upvotes: 1
comments: 0
---

# 3068. 最大节点价值之和

> **[yiduobo的每日leetcode 3068.最大节点价值之和](https://zhuanlan.zhihu.com/p/697272535) · 知乎 · 2024-05-12 · 赞同 1**
> 力扣：[3068. 最大节点价值之和](https://leetcode.cn/problems/find-the-maximum-sum-of-node-values/) · Hard · 灵茶山艾府：[脑筋急转弯，状态机 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3068.最大节点价值之和

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-maximum-sum-of-node-values/description/)

题目给出一棵树，要求对树中的边进行若干次操作，每次操作可以任选一条边，将边连接的两个节点值分别异或上k，问执行操作后树中节点值之和的最大值。

首先考虑选边然后异或这个操作。如果选择了两条边u - v以及v - w，各执行一次操作的结果就是u、w各执行了一次异或操作，而v执行了两次相当于没有执行。更进一步的，对于树中从p开始到q结束的某条路径，如果将路径上的边都执行一次操作，那么路径上的节点除p和q之外，其他节点都执行了两次异或操作相当于没有执行，而p和q则执行了一次。

换言之，本题中树的形态无关紧要，可以视为给出一个数组，每一轮从中选出两个数执行异或k的操作，要求执行操作之后数组和最大。

由于对同一个数执行多次异或操作是没有意义的，因此在这里只需要考虑对于每个数是否应该执行异或操作。于是可以一趟遍历，计算出每个数异或k之后与原数之差，记为数组diff，那么最优解就应该在原数组和的基础上加上diff数组中的所有正数项，相当于对这些正数项执行异或操作。

不过需要注意的是，本题中必须成对地执行异或操作，因此当diff中的正数项的个数为奇数时，就需要考虑是否有必要混进来一个非正数项，此时就应该对比最小的正数项与最大的非负数项之和是否大于0，若不满足则没必要执行最后这次操作。

根据上面的结论，就得到了一种算法：

1、首先一趟遍历，计算出异或后的值与原数值之差的数组diff，并更新最终结果res为原数组之和

2、接下来遍历diff数组，将其中的正数项累加到答案中，并统计其中正数项的数目pos_cnt，同时记录其中最小的正数项mi_pos以及最大的非正数项ma_non_pos

3、遍历完成后，若pos_cnt为奇数，那么就需要考虑最后这次异或操作是否需要执行。此时若ma_non_pos存在，同时mi_pos与ma_non_pos为正数，那么就表示应该执行最后这次异或操作。由于mi_pos在步骤2中已经累加到答案中了，因此在这里只需将ma_non_pos也累加到答案中即可；反之，若ma_non_pos不存在，即diff中全部位正数，即就没有数与mi_pos组队，又或者ma_non_pos与mi_pos之和为负数，即最后这次异或操作的收益为负，那么就不应该执行，此时应该将mi_pos从答案中减去。

最后附上python代码：

```python
class Solution(object):
    def maximumValueSum(self, nums, k, edges):
        """
        :type nums: List[int]
        :type k: int
        :type edges: List[List[int]]
        :rtype: int
        """

        diff = [(x ^ k) - x for x in nums]
        res = sum(nums)
        mi_pos = None
        pos_cnt = 0
        ma_non_pos = None

        for v in diff:
            if v > 0:
                if mi_pos is None or mi_pos > v:
                    mi_pos = v
                res += v
                pos_cnt += 1
            else:
                if ma_non_pos is None or ma_non_pos < v:
                    ma_non_pos = v
        
        if pos_cnt % 2 == 1:
            if ma_non_pos is not None and mi_pos + ma_non_pos > 0:
                res += ma_non_pos
            else:
                res -= mi_pos
        
        return res
```

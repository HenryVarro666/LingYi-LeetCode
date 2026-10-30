---
title: "3781. 二进制交换后的最大分数"
aliases: ["yiduobo的每日leetcode 3781.二进制交换后的最大分数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1986217114030322756"
zhihu_id: "1986217114030322756"
zhihu_title: "yiduobo的每日leetcode 3781.二进制交换后的最大分数"
question_id: "3781"
question: "二进制交换后的最大分数"
problem_url: "https://leetcode.cn/problems/maximum-score-after-binary-swaps/"
difficulty: "Medium"
rating: 1823
created: "2025-12-22T21:52:19+08:00"
updated: "2025-12-22T21:52:25+08:00"
upvotes: 1
comments: 0
---

# 3781. 二进制交换后的最大分数

> **[yiduobo的每日leetcode 3781.二进制交换后的最大分数](https://zhuanlan.zhihu.com/p/1986217114030322756) · 知乎 · 2025-12-22 · 赞同 1**
> 力扣：[3781. 二进制交换后的最大分数](https://leetcode.cn/problems/maximum-score-after-binary-swaps/) · Medium · 灵茶山艾府：[两种方法：从左到右 / 从右到左（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3781.二进制交换后的最大分数

[3781. 二进制交换后的最大分数 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-score-after-binary-swaps/description/)

题目给出一个长度为n的整数数组nums以及一个相同长度的二进制字符串s。

在一开始，总的得分为0。对于每个s[index]为'1'的下标index，都会为分数共享nums[index]。

现在可以执行任意次操作，每次操作中，需要从0到n - 2之间选择一个下标index，满足s[index]为'0'且s[index + 1]为'1'，然后交换这两个字符。

问最终可以得到的最大得分是多少。

对于题目中的操作，要求0在左边1在右边，而操作可以执行任意次，那么就意味着对于每个'1'，其可以与左侧任意一个'0'进行交换。为了使得最终得分最大，那么对于每个'1'，其最佳的交换位置就是左侧所有的'0'中，对应元素最大的那一个。

于是只需一趟遍历，使用一个大顶堆来维护当前对应的s为0的所有元素。对于当前遍历到的nums[index]，若s[index]为'0'，那么就将nums[index]加入到堆中；若s[index]为'1'，那么则需要将nums[index]加入到堆中后，再从堆中弹出堆顶元素并加入到答案中，相当于将这个'1'通过操作移动到了这个对应元素对应的位置上。

最后附上python代码：

```python
class Solution(object):
    def maximumScore(self, nums, s):
        """
        :type nums: List[int]
        :type s: str
        :rtype: int
        """
        
        heap = []
        res = 0
        for v, g in zip(nums, s):
            heapq.heappush(heap, -v)
            if g == '1':
                res -= heapq.heappop(heap)
        return res
```

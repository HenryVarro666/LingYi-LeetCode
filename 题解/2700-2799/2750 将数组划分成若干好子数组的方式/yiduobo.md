---
title: "2750. 将数组划分成若干好子数组的方式"
aliases: ["yiduobo的每日leetcode 2750.将数组划分成若干好子数组的方式"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/数学算法", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/654101995"
zhihu_id: "654101995"
zhihu_title: "yiduobo的每日leetcode 2750.将数组划分成若干好子数组的方式"
question_id: "2750"
question: "将数组划分成若干好子数组的方式"
problem_url: "https://leetcode.cn/problems/ways-to-split-array-into-good-subarrays/"
difficulty: "Medium"
rating: 1598
created: "2023-09-04T01:43:39+08:00"
updated: "2023-09-04T01:43:39+08:00"
upvotes: 0
comments: 0
---

# 2750. 将数组划分成若干好子数组的方式

> **[yiduobo的每日leetcode 2750.将数组划分成若干好子数组的方式](https://zhuanlan.zhihu.com/p/654101995) · 知乎 · 2023-09-04 · 赞同 0**
> 力扣：[2750. 将数组划分成若干好子数组的方式](https://leetcode.cn/problems/ways-to-split-array-into-good-subarrays/) · Medium · 灵茶山艾府：[乘法原理（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2750.将数组划分成若干好子数组的方式

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/ways-to-split-array-into-good-subarrays/)

首先考虑特殊情况。若数组中全都是0，那么必然不存在合法的划分方式，此时直接返回0。

接下来是一般情况。可以发现，数组中的前导0必然只能被划分到数组的首个1所在的子数组，而后缀0则只能被划分到数组中最后那个1所在的子数组，而在两个1之间的连续0，则可以将前半段划分到左侧的子数组，将后半段划分到右侧的子数组。更具体的，对于两个1之间的一段长度为k的0，一共有左0右k、左1右k - 1、...、左k右0这一共k + 1中划分方案，根据乘法原理，此时就可以将k + 1累乘到答案中。

于是可以初始化答案为1，然后从数组左侧开始向右侧遍历，先找到首个1的位置p，然后从p开始，找到下一个1的位置q，此时p到q之间就有q - p - 1个1，将q - p累乘到答案中，然后将p更新为q，再重复上述过程直到当前p的右侧不存在1为止。

最后附上python代码：

```python
class Solution(object):
    def numberOfGoodSubarraySplits(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        mod = 10 ** 9 + 7
        p = 0
        while p < len(nums) and nums[p] == 0:
            p += 1
        
        if p == len(nums):
            return 0
        
        res = 1
        while p < len(nums):
            q = p + 1
            while q < len(nums) and nums[q] == 0:
                q += 1
            
            if q == len(nums):
                break
                
            res = res * (q - p) % mod
            p = q
        
        return res
```

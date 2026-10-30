---
title: "532. 数组中的k-diff数对"
aliases: ["yiduobo的每日leetcode 532.数组中的k-diff数对"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/261169570"
zhihu_id: "261169570"
zhihu_title: "yiduobo的每日leetcode 532.数组中的k-diff数对"
question_id: "532"
question: "数组中的k-diff数对"
problem_url: "https://leetcode.cn/problems/k-diff-pairs-in-an-array/"
created: "2020-10-05T23:22:51+08:00"
updated: "2020-10-05T23:22:51+08:00"
upvotes: 0
comments: 0
---

# 532. 数组中的k-diff数对

> **[yiduobo的每日leetcode 532.数组中的k-diff数对](https://zhuanlan.zhihu.com/p/261169570) · 知乎 · 2020-10-05 · 赞同 0**
> 力扣：[532. 数组中的k-diff数对](https://leetcode.cn/problems/k-diff-pairs-in-an-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

532.数组中的k-diff数对<https://leetcode-cn.com/problems/k-diff-pairs-in-an-array/>

哈希表的题目，使用一个集合num_set记录之前出现过的数，那么对于当前数now，若num_set中存在now - k，那么now - k和now是一组合法的k-diff数对。同样的，若num_set中存在now + k，那么now + k和now也是一组合法的k-diff数对。

接下里需要考虑的问题是如何去重。我的做法是对于一个k-diff数对，我们将其中较小的那个数保存在集合res中，那么对于重复的k-diff数对，其较小的那个数也必然相同，此时的res就起到了去重的作用。

于是具体做法为遍历每个数now：

1、若num_set中有now - k，那么将now - k加入到res中

2、若num_set中有now + k，那么此时较小的那个数为now，于是将now加入到res中

3、将now加入到num_set中

处理完成后，res的长度即为最终答案。

最后附上python代码：

```
class Solution(object):
    def findPairs(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        res = set()
        num_set = set()

        for num in nums:
            if num - k in num_set:
                res.add(num - k)
            if num + k in num_set:
                res.add(num)
            num_set.add(num)

        return len(res)
```

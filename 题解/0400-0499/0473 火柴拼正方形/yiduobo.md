---
title: "473. 火柴拼正方形"
aliases: ["yiduobo的每日leetcode 473.火柴拼正方形"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/235648886"
zhihu_id: "235648886"
zhihu_title: "yiduobo的每日leetcode 473.火柴拼正方形"
question_id: "473"
question: "火柴拼正方形"
problem_url: "https://leetcode.cn/problems/matchsticks-to-square/"
created: "2020-09-11T23:46:40+08:00"
updated: "2020-09-11T23:46:40+08:00"
upvotes: 1
comments: 0
---

# 473. 火柴拼正方形

> **[yiduobo的每日leetcode 473.火柴拼正方形](https://zhuanlan.zhihu.com/p/235648886) · 知乎 · 2020-09-11 · 赞同 1**
> 力扣：[473. 火柴拼正方形](https://leetcode.cn/problems/matchsticks-to-square/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

473.火柴拼正方形<https://leetcode-cn.com/problems/matchsticks-to-square/>

注意到题目保证火柴的数目小于等于15，那么可以使用之前464题类似的做法，使用状态压缩动态规划来做（传送门在这里[yiduobo：yiduobo的每日leetcode 464.我能赢吗](https://zhuanlan.zhihu.com/p/226019524)）。

首先，将所有火柴的长度相加得到长度之和sum，那么若sum不是4的倍数，那么必然无法拼成正方形，否则可以计算出正方形的边长target_len \= sum / 4。

我在这里使用的是记忆化搜索的写法。与464题一样，也是对火柴是否使用过进行状态编码。那么对于f[i]，依然是枚举所有火柴的下标index，然后通过i & (1\<\< index) 来判断当前是否已经拿了这根火柴。获取到目前拿了哪些火柴之后，可以将这些火柴的长度相加，然后对target_len取模，就可以得到当前正在拼的这条边目前拼好的长度l。接下来枚举没有使用过的火柴，若其长度加上l小于等于target_len，那么就尝试选择这根火柴，更新状态同时尝试选择下一根火柴即可。

最后附上python代码：

```python
class Solution(object):
    def makesquare(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        if not nums:
            return False

        sum_len = sum(nums)
        if sum_len % 4 != 0:
            return False

        f = [None] * (1 << len(nums))

        return self.dfs(0, nums, sum_len / 4, f)

    def dfs(self, now_stat, nums, target_len, f):
        if f[now_stat] is not None:
            return f[now_stat]
        if now_stat + 1 == 1 << len(nums):
            f[now_stat] = True
            return f[now_stat]
        
        sum_now = 0
        unused_set = set()
        for index, num in enumerate(nums):
            if now_stat & (1 << index):
                sum_now += num
            else:
                unused_set.add(index)

        for index in unused_set:
            if nums[index] + sum_now % target_len <= target_len:
                if self.dfs(now_stat + (1 << index), nums, target_len, f):
                    f[now_stat] = True
                    return True

        f[now_stat] = False
        return False
```

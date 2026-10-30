---
title: "2364. 统计坏数对的数目"
aliases: ["yiduobo的每日leetcode 2364.统计坏数对的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/562739375"
zhihu_id: "562739375"
zhihu_title: "yiduobo的每日leetcode 2364.统计坏数对的数目"
question_id: "2364"
question: "统计坏数对的数目"
problem_url: "https://leetcode.cn/problems/count-number-of-bad-pairs/"
difficulty: "Medium"
rating: 1622
created: "2022-09-09T02:09:30+08:00"
updated: "2022-09-09T02:09:30+08:00"
upvotes: 0
comments: 0
---

# 2364. 统计坏数对的数目

> **[yiduobo的每日leetcode 2364.统计坏数对的数目](https://zhuanlan.zhihu.com/p/562739375) · 知乎 · 2022-09-09 · 赞同 0**
> 力扣：[2364. 统计坏数对的数目](https://leetcode.cn/problems/count-number-of-bad-pairs/) · Medium · 灵茶山艾府：[式子变形 + 枚举右维护左（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2364.统计坏数对的数目

[力扣](https://leetcode.cn/problems/count-number-of-bad-pairs/)

对于一个长度为n的数组，一共有n \* (n - 1) / 2组不同的数对，那么在这里就可以先将问题从统计坏数对变为统计好数对，然后使用这个总数减去好数对得到题目要求的坏数对。这样做的理由是一般来说，统计相等比统计不等还是容易点。

接下来的问题就是如何高效统计好数对的数目。由于数组规模不小，在这里肯定不能两两枚举，那么一般的做法就是枚举其中一个数，然后计算满足条件的另一个数有多少个。在这里不妨枚举nums[i]，那么接下来就需要找到数组中满足j - i \= nums[j] - nums[i]的j的数目。由于i和nums[i]已经确定，那么实际上要找的就是满足nums[j] - j \= nums[i] - i的j的数目。式子的左侧只与j有关，那么很自然想到使用哈希表来统计每种nums[j] - j出现的次数。于是就有了一种做法：

从左向右一趟遍历，对于当前遍历到的nums[index]，首先使用哈希表中nums[index] - index对应的权重来更好数对的数目，接下来还需要将哈希表中nums[index] - index对应的权重加1。全部遍历完成后，使用n \* (n - 1) / 2减去好数对的总数目即可。

最后附上python代码：

```python
class Solution(object):
    def countBadPairs(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        cnt_dict = {}
        res = len(nums) * (len(nums) - 1) / 2
        for index, num in enumerate(nums):
            res -= cnt_dict.get(num - index, 0)
            cnt_dict[num - index] = cnt_dict.get(num - index, 0) + 1
        
        return res
```

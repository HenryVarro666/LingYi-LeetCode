---
title: "594. 最长和谐子序列"
aliases: ["yiduobo的每日leetcode 594.最长和谐子序列"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/268208779"
zhihu_id: "268208779"
zhihu_title: "yiduobo的每日leetcode 594.最长和谐子序列"
question_id: "594"
question: "最长和谐子序列"
problem_url: "https://leetcode.cn/problems/longest-harmonious-subsequence/"
difficulty: "Easy"
created: "2020-10-23T22:41:18+08:00"
updated: "2020-10-23T22:41:18+08:00"
upvotes: 0
comments: 0
---

# 594. 最长和谐子序列

> **[yiduobo的每日leetcode 594.最长和谐子序列](https://zhuanlan.zhihu.com/p/268208779) · 知乎 · 2020-10-23 · 赞同 0**
> 力扣：[594. 最长和谐子序列](https://leetcode.cn/problems/longest-harmonious-subsequence/) · Easy · 灵茶山艾府：[O(n) 做法，哈希表统计元素出现次数（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

594.最长和谐子序列<https://leetcode-cn.com/problems/longest-harmonious-subsequence/>

比较基础的题目。统计每个数字出现的次数，然后遍历每个数字x，计算x和x - 1出现的总次数，选择总次数最大的x即可。

最后附上python代码：

```python
class Solution(object):
    def findLHS(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        count_dict = {}
        for num in nums:
            count_dict[num] = count_dict.get(num, 0) + 1
        res = 0
        for num in count_dict:
            if num - 1 in count_dict:
                res = max(res, count_dict[num] + count_dict[num - 1])
        return res
```

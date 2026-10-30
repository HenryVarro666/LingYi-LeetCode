---
title: "2442. 反转之后不同整数的数目"
aliases: ["yiduobo的每日leetcode 2442.反转之后不同整数的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/584447915"
zhihu_id: "584447915"
zhihu_title: "yiduobo的每日leetcode 2442.反转之后不同整数的数目"
question_id: "2442"
question: "反转之后不同整数的数目"
problem_url: "https://leetcode.cn/problems/count-number-of-distinct-integers-after-reverse-operations/"
difficulty: "Medium"
created: "2022-11-18T00:09:52+08:00"
updated: "2022-11-18T00:09:52+08:00"
upvotes: 0
comments: 0
---

# 2442. 反转之后不同整数的数目

> **[yiduobo的每日leetcode 2442.反转之后不同整数的数目](https://zhuanlan.zhihu.com/p/584447915) · 知乎 · 2022-11-18 · 赞同 0**
> 力扣：[2442. 反转之后不同整数的数目](https://leetcode.cn/problems/count-number-of-distinct-integers-after-reverse-operations/) · Medium · 灵茶山艾府：[一次遍历](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2442.反转之后不同整数的数目

[力扣](https://leetcode.cn/problems/count-number-of-distinct-integers-after-reverse-operations/)

首先将所有整数都加入到哈希表中，然后一趟遍历，逐位分离当前遍历到的数，反转并组装起来之后同样也加入到哈希表中。处理完成后，哈希表中数的数目就是最终答案了。

最后附上python代码：

```python
class Solution(object):
    def countDistinctIntegers(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        num_set = set(nums)

        for num in nums:
            now = num
            digit_list = []
            while now:
                digit_list.append(now % 10)
                now /= 10
            
            now = 0
            for digit in digit_list:
                now = now * 10 + digit
            
            num_set.add(now)

        return len(num_set)
```

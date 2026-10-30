---
title: "2150. 找出数组中的所有孤独数字"
aliases: ["yiduobo的每日leetcode 2150.找出数组中的所有孤独数字"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/530618301"
zhihu_id: "530618301"
zhihu_title: "yiduobo的每日leetcode 2150.找出数组中的所有孤独数字"
question_id: "2150"
question: "找出数组中的所有孤独数字"
problem_url: "https://leetcode.cn/problems/find-all-lonely-numbers-in-the-array/"
difficulty: "Medium"
created: "2022-06-18T16:13:08+08:00"
updated: "2022-06-18T16:13:08+08:00"
upvotes: 0
comments: 0
---

# 2150. 找出数组中的所有孤独数字

> **[yiduobo的每日leetcode 2150.找出数组中的所有孤独数字](https://zhuanlan.zhihu.com/p/530618301) · 知乎 · 2022-06-18 · 赞同 0**
> 力扣：[2150. 找出数组中的所有孤独数字](https://leetcode.cn/problems/find-all-lonely-numbers-in-the-array/) · Medium · 灵茶山艾府：[哈希表模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2150.找出数组中的所有孤独数字

<https://leetcode.cn/problems/find-all-lonely-numbers-in-the-array/>

使用哈希表统计数组中每个数字出现的次数，接下来遍历哈希表中的所有数，对于当前遍历到的数num，若num在哈希表中恰好出现一次，且num - 1和num + 1都没有出现在哈希表中，那么就将num加入到答案中。

最后附上python代码：

```python
class Solution(object):
    def findLonely(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        num_dict = {}
        for num in nums:
            num_dict[num] = num_dict.get(num, 0) + 1
        
        res = []
        for num in num_dict:
            if num_dict.get(num - 1, 0) == 0 and num_dict.get(num + 1, 0) == 0 and num_dict[num] == 1:
                res.append(num)
        
        return res
```

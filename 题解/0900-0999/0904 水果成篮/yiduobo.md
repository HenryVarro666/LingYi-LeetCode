---
title: "904. 水果成篮"
aliases: ["yiduobo的每日leetcode 904.水果成篮"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/353862560"
zhihu_id: "353862560"
zhihu_title: "yiduobo的每日leetcode 904.水果成篮"
question_id: "904"
question: "水果成篮"
problem_url: "https://leetcode.cn/problems/fruit-into-baskets/"
difficulty: "Medium"
rating: 1516
created: "2021-03-01T22:17:23+08:00"
updated: "2021-03-01T22:17:23+08:00"
upvotes: 1
comments: 0
---

# 904. 水果成篮

> **[yiduobo的每日leetcode 904.水果成篮](https://zhuanlan.zhihu.com/p/353862560) · 知乎 · 2021-03-01 · 赞同 1**
> 力扣：[904. 水果成篮](https://leetcode.cn/problems/fruit-into-baskets/) · Medium · 灵茶山艾府：[滑动窗口+哈希表（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

904.水果成篮

[力扣](https://leetcode-cn.com/problems/fruit-into-baskets/)

题目要求从数组中找出一个最长连续的子序列，且这个子序列中只包含最多两种不同的数字。对于这类问题，很自然想到使用滑动窗口来解决。使用一个dict来维护当前窗口中每种数字出现的个数，然后从头到尾一趟扫描，每次将当前数字加入到滑动窗口当中。若此时dict中不同数字个数超过2个，那么就将滑动窗口的左边界向右移动，同时将对应的数字从dict中弹出，直到dict中不同数字的个数小于等于2。在每次调整完左边界的位置之后，计算其大小并更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def totalFruit(self, tree):
        """
        :type tree: List[int]
        :rtype: int
        """

        num_dict = {}
        res = 0
        l = 0
        for index, num in enumerate(tree):
            num_dict[num] = num_dict.get(num, 0) + 1
            while len(num_dict) > 2:
                num_dict[tree[l]] -= 1
                if num_dict[tree[l]] == 0:
                    num_dict.pop(tree[l])
                l += 1
            
            res = max(res, index - l + 1)
        
        return res
```

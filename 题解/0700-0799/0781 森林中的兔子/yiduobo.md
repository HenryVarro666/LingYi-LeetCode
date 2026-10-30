---
title: "781. 森林中的兔子"
aliases: ["yiduobo的每日leetcode 781.森林中的兔子"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/hash-table", "题单/贪心算法", "题单/贪心算法/八-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/340503118"
zhihu_id: "340503118"
zhihu_title: "yiduobo的每日leetcode 781.森林中的兔子"
question_id: "781"
question: "森林中的兔子"
problem_url: "https://leetcode.cn/problems/rabbits-in-forest/"
difficulty: "Medium"
rating: 1453
created: "2020-12-29T23:20:44+08:00"
updated: "2020-12-29T23:20:44+08:00"
upvotes: 0
comments: 0
---

# 781. 森林中的兔子

> **[yiduobo的每日leetcode 781.森林中的兔子](https://zhuanlan.zhihu.com/p/340503118) · 知乎 · 2020-12-29 · 赞同 0**
> 力扣：[781. 森林中的兔子](https://leetcode.cn/problems/rabbits-in-forest/) · Medium · 灵茶山艾府：[逻辑推理题（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

781.森林中的兔子

[力扣](https://leetcode-cn.com/problems/rabbits-in-forest/)

设answer中等于k的兔子一共有p只，那么要是最终的答案尽可能小，我们就必须尽可能让每只兔子描述的都是出现在answer中的兔子，因此我们可以按每k + 1只兔子进行分组，组内的兔子颜色一致。那么对于这p只兔子，至少需要t \= p / (k + 1)种颜色，这里的t需要向上取整。得到组数t之后，每个组当中有k + 1只兔子，因此这里需要在答案中累加上t \* (k + 1)。

最后附上python代码：

```python
class Solution(object):
    def numRabbits(self, answers):
        """
        :type answers: List[int]
        :rtype: int
        """

        count_dict = {}
        for num in answers:
            count_dict[num] = count_dict.get(num, 0) + 1
        
        res = 0
        for num, cnt in count_dict.items():
            res += cnt / (num + 1) * (num + 1)
            if cnt % (num + 1) != 0:
                res += num + 1
        return res
```

---
title: "1181. 前后拼接"
aliases: ["yiduobo的每日leetcode 1181.前后拼接"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/612141508"
zhihu_id: "612141508"
zhihu_title: "yiduobo的每日leetcode 1181.前后拼接"
question_id: "1181"
question: "前后拼接"
problem_url: "https://leetcode.cn/problems/before-and-after-puzzle/"
created: "2023-03-07T21:32:06+08:00"
updated: "2023-03-07T21:32:06+08:00"
upvotes: 0
comments: 0
---

# 1181. 前后拼接

> **[yiduobo的每日leetcode 1181.前后拼接](https://zhuanlan.zhihu.com/p/612141508) · 知乎 · 2023-03-07 · 赞同 0**
> 力扣：[1181. 前后拼接](https://leetcode.cn/problems/before-and-after-puzzle/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1181.前后拼接

[力扣](https://leetcode.cn/problems/before-and-after-puzzle/)

没有什么特别好的思路，不过好在数据规模不大，因此可以直接两两枚举字符串，使用集合储存拼接后的结果，最终集合的大小就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def beforeAndAfterPuzzles(self, phrases):
        """
        :type phrases: List[str]
        :rtype: List[str]
        """

        n = len(phrases)
        parts_list = [s.split(' ') for s in phrases]
        res = set()
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                
                if parts_list[i][-1] != parts_list[j][0]:
                    continue
                
                res.add(' '.join(parts_list[i] + parts_list[j][1:]))
        
        return sorted(list(res))
```

---
title: "LCS 02. 完成一半题目"
aliases: ["yiduobo的每日leetcode LCS02.完成一半题目"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/581010996"
zhihu_id: "581010996"
zhihu_title: "yiduobo的每日leetcode LCS02.完成一半题目"
question_id: "LCS 02"
question: "完成一半题目"
problem_url: "https://leetcode.cn/problems/WqXACV/"
difficulty: "Easy"
created: "2022-11-07T01:08:59+08:00"
updated: "2022-11-07T01:08:59+08:00"
upvotes: 0
comments: 0
---

# LCS 02. 完成一半题目

> **[yiduobo的每日leetcode LCS02.完成一半题目](https://zhuanlan.zhihu.com/p/581010996) · 知乎 · 2022-11-07 · 赞同 0**
> 力扣：[LCS 02. 完成一半题目](https://leetcode.cn/problems/WqXACV/) · Easy · 灵茶山艾府：[贪心](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

LCS02.完成一半题目

[力扣](https://leetcode.cn/problems/WqXACV/)

为了最终选择的知识点最少，那么就应该优先选择对应题目数量最多的知识点。于是可以先统计每种知识点对应的题目数量，从大到小排序后一趟遍历，找到最小的k，满足前k种知识点对应的题目数量之和大于等于n，这个k就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def halfQuestions(self, questions):
        """
        :type questions: List[int]
        :rtype: int
        """

        n = len(questions) / 2

        cnt_dict = {}
        for q in questions:
            cnt_dict[q] = cnt_dict.get(q, 0) + 1
        
        now = 0
        res = 0
        for cnt in sorted(cnt_dict.values(), reverse=True):
            now += cnt
            res += 1
            if now >= n:
                break
        
        return res
```

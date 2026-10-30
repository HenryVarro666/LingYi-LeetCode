---
title: "1086. 前五科的均分"
aliases: ["yiduobo的每日leetcode 1086.前五科的均分"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/608950267"
zhihu_id: "608950267"
zhihu_title: "yiduobo的每日leetcode 1086.前五科的均分"
question_id: "1086"
question: "前五科的均分"
problem_url: "https://leetcode.cn/problems/high-five/"
created: "2023-02-23T22:54:32+08:00"
updated: "2023-02-23T22:54:32+08:00"
upvotes: 0
comments: 0
---

# 1086. 前五科的均分

> **[yiduobo的每日leetcode 1086.前五科的均分](https://zhuanlan.zhihu.com/p/608950267) · 知乎 · 2023-02-23 · 赞同 0**
> 力扣：[1086. 前五科的均分](https://leetcode.cn/problems/high-five/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1086.前五科的均分

[力扣](https://leetcode.cn/problems/high-five/)

一趟遍历，以学生的id作为key，使用哈希表将每个学生前5高的分数分别储存起来。遍历完成后，对于每个学生计算其前5高的分数的平均值，排序后即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def highFive(self, items):
        """
        :type items: List[List[int]]
        :rtype: List[List[int]]
        """

        score_dict = {}
        for id, score in items:
            if id not in score_dict:
                score_dict[id] = [0] * 5
            
            p = 5
            for index in range(5):
                if score_dict[id][index] < score:
                    p = index
                    break
            
            for index in range(4, p, -1):
                score_dict[id][index] = score_dict[id][index - 1]
            
            if p < 5:
                score_dict[id][p] = score
        
        result = []
        for id in score_dict:
            result.append([id, sum(score_dict[id]) / 5])
        
        return sorted(result)
```

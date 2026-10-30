---
title: "2512. 奖励最顶尖的K名学生"
aliases: ["yiduobo的每日leetcode 2512.奖励最顶尖的K名学生"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/634316931"
zhihu_id: "634316931"
zhihu_title: "yiduobo的每日leetcode 2512.奖励最顶尖的K名学生"
question_id: "2512"
question: "奖励最顶尖的 K 名学生"
problem_url: "https://leetcode.cn/problems/reward-top-k-students/"
difficulty: "Medium"
created: "2023-06-05T16:16:11+08:00"
updated: "2023-06-05T16:16:11+08:00"
upvotes: 0
comments: 0
---

# 2512. 奖励最顶尖的K名学生

> **[yiduobo的每日leetcode 2512.奖励最顶尖的K名学生](https://zhuanlan.zhihu.com/p/634316931) · 知乎 · 2023-06-05 · 赞同 0**
> 力扣：[2512. 奖励最顶尖的 K 名学生](https://leetcode.cn/problems/reward-top-k-students/) · Medium · 灵茶山艾府：[模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2512.奖励最顶尖的K名学生

[力扣](https://leetcode.cn/problems/reward-top-k-students/)

很常规的模拟题，题目的数据规模也不大，直接按照题目描述按部就班地计算就行了。

具体来说，首先将正向词表和负向词表分别加入到两个集合中，接下来遍历每个学生，对于当前学生的评语，遍历其中的单词，根据之前的正负向集合来计算这名学生的得分。计算完所有学生的得分后，按照得分为第一优先级倒叙，id为第二优先级顺序进行一趟排序，然后取排序结果的top k的id返回即可。

对于这个top k问题，则还可以使用一个大小为k的堆，或者通过快速选择算法找出排名第k的学生来进行优化，不过我在这里偷懒，就直接使用的排序。

最后附上python代码：

```python
class Solution(object):
    def topStudents(self, positive_feedback, negative_feedback, report, student_id, k):
        """
        :type positive_feedback: List[str]
        :type negative_feedback: List[str]
        :type report: List[str]
        :type student_id: List[int]
        :type k: int
        :rtype: List[int]
        """

        pos_set = set(positive_feedback)
        neg_set = set(negative_feedback)

        score_list = []
        for r, id in zip(report, student_id):
            score = 0
            for word in r.split(' '):
                if word in pos_set:
                    score += 3
                elif word in neg_set:
                    score -= 1
            score_list.append([score, id])

        score_list.sort(key=lambda d:(-d[0], d[1]))
        return [info[1] for info in score_list[:k]]
```

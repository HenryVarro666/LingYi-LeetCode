---
title: "2358. 分组的最大数量"
aliases: ["yiduobo的每日leetcode 2358.分组的最大数量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/brainteaser", "leetcode/math", "leetcode/sorting", "leetcode/simulation", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/561982201"
zhihu_id: "561982201"
zhihu_title: "yiduobo的每日leetcode 2358.分组的最大数量"
question_id: "2358"
question: "分组的最大数量"
problem_url: "https://leetcode.cn/problems/maximum-number-of-groups-entering-a-competition/"
difficulty: "Medium"
rating: 1503
created: "2022-09-06T23:53:31+08:00"
updated: "2022-09-06T23:53:31+08:00"
upvotes: 0
comments: 0
---

# 2358. 分组的最大数量

> **[yiduobo的每日leetcode 2358.分组的最大数量](https://zhuanlan.zhihu.com/p/561982201) · 知乎 · 2022-09-06 · 赞同 0**
> 力扣：[2358. 分组的最大数量](https://leetcode.cn/problems/maximum-number-of-groups-entering-a-competition/) · Medium · 灵茶山艾府：[两种做法：排序 + 贪心模拟 / 脑筋急转弯](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2358.分组的最大数量

[力扣](https://leetcode.cn/problems/maximum-number-of-groups-entering-a-competition/)

题目要求对学生进行分组，要求每一组的人数比前一组多，同时每一组的总分也比前一组的多，问最多可以分多少组。为了尽可能多地分组，在分组人数上的最优做法就是按1、2、3、...，这种形式类推上去，在这个前提下，需要满足每一组的总分都比前一组要高。由于可以任意分组，这个要求也很容易达成，只需要按分数从低到高依次分到对应的组里就行了。由于后一组任意学生的分数大于等于前一组任意学生的分数，同时后一组还要多出一个人，那么后一组的总分就必然高于前一组。

可以发现，在这里其实根本就不需要关心最终是怎么分的，只需要找出最大的分数组k就行了。设最终分了k组，那么这k组人至少有(1 + k) \* k / 2个，只需要这个值小于等于总人数就行了，于是可以从1开始向上枚举最终答案，通过这个式子判断当前答案是否能形成有效的分组即可。

最后附上python代码：

```python
class Solution(object):
    def maximumGroups(self, grades):
        """
        :type grades: List[int]
        :rtype: int
        """
        
        res = 1
        while res * (res + 1) / 2 <= len(grades):
            res += 1
        
        return res - 1
```

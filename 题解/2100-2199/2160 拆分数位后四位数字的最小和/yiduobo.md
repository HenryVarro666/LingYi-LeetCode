---
title: "2160. 拆分数位后四位数字的最小和"
aliases: ["yiduobo的每日leetcode 2160.拆分数位后四位数字的最小和"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/string", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/532023978"
zhihu_id: "532023978"
zhihu_title: "yiduobo的每日leetcode 2160.拆分数位后四位数字的最小和"
question_id: "2160"
question: "拆分数位后四位数字的最小和"
problem_url: "https://leetcode.cn/problems/minimum-sum-of-four-digit-number-after-splitting-digits/"
difficulty: "Easy"
rating: 1314
created: "2022-06-22T00:07:09+08:00"
updated: "2022-06-22T00:07:09+08:00"
upvotes: 0
comments: 0
---

# 2160. 拆分数位后四位数字的最小和

> **[yiduobo的每日leetcode 2160.拆分数位后四位数字的最小和](https://zhuanlan.zhihu.com/p/532023978) · 知乎 · 2022-06-22 · 赞同 0**
> 力扣：[2160. 拆分数位后四位数字的最小和](https://leetcode.cn/problems/minimum-sum-of-four-digit-number-after-splitting-digits/) · Easy · 灵茶山艾府：[ 贪心 + 排序](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2160.拆分数位后四位数字的最小和

[力扣](https://leetcode.cn/problems/minimum-sum-of-four-digit-number-after-splitting-digits/)

比较基础的题目。为了使得和最小，显然应该构造出两个两位数，同时将数字中较小的两个放在十位上。将数字分离出来并排序后得到num_list，答案就是num_list[0] \* 10 + num_list[1] \* 10 + num_list[2] + num_list[3]。

最后附上python代码：

```python
class Solution(object):
    def minimumSum(self, num):
        """
        :type num: int
        :rtype: int
        """

        num_list = sorted([num / 1000, num / 100 % 10, num / 10 % 10, num % 10])
        return num_list[0] * 10 + num_list[1] * 10 + num_list[2] + num_list[3]
```

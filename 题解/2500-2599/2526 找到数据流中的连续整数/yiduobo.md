---
title: "2526. 找到数据流中的连续整数"
aliases: ["yiduobo的每日leetcode 2526.找到数据流中的连续整数"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/636326122"
zhihu_id: "636326122"
zhihu_title: "yiduobo的每日leetcode 2526.找到数据流中的连续整数"
question_id: "2526"
question: "找到数据流中的连续整数"
problem_url: "https://leetcode.cn/problems/find-consecutive-integers-from-a-data-stream/"
difficulty: "Medium"
created: "2023-06-11T21:59:26+08:00"
updated: "2023-06-11T21:59:26+08:00"
upvotes: 0
comments: 0
---

# 2526. 找到数据流中的连续整数

> **[yiduobo的每日leetcode 2526.找到数据流中的连续整数](https://zhuanlan.zhihu.com/p/636326122) · 知乎 · 2023-06-11 · 赞同 0**
> 力扣：[2526. 找到数据流中的连续整数](https://leetcode.cn/problems/find-consecutive-integers-from-a-data-stream/) · Medium · 灵茶山艾府：[模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2526.找到数据流中的连续整数

[力扣](https://leetcode.cn/problems/find-consecutive-integers-from-a-data-stream/)

使用一个变量cnt记录当前最后连续出现的value的次数，对于每次consec操作，若添加的num等于value，那么就将cnt加上1，否则将cnt重置为0，这样一来每次conces操作就只需要判断cnt是否大于等于k了。

最后附上python代码：

```python
class DataStream(object):

    def __init__(self, value, k):
        """
        :type value: int
        :type k: int
        """
        self.cnt = 0
        self.k = k
        self.value = value

    def consec(self, num):
        """
        :type num: int
        :rtype: bool
        """

        if num != self.value:
            self.cnt = 0
        else:
            self.cnt += 1
        
        return self.cnt >= self.k

# Your DataStream object will be instantiated and called as such:
# obj = DataStream(value, k)
# param_1 = obj.consec(num)
```

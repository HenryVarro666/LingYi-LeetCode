---
title: "LCP 01. 猜数字"
aliases: ["yiduobo的每日leetcode LCP01.猜数字"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/569971967"
zhihu_id: "569971967"
zhihu_title: "yiduobo的每日leetcode LCP01.猜数字"
question_id: "LCP 01"
question: "猜数字"
problem_url: "https://leetcode.cn/problems/guess-numbers/"
created: "2022-10-01T17:23:49+08:00"
updated: "2022-10-01T17:23:49+08:00"
upvotes: 0
comments: 0
---

# LCP 01. 猜数字

> **[yiduobo的每日leetcode LCP01.猜数字](https://zhuanlan.zhihu.com/p/569971967) · 知乎 · 2022-10-01 · 赞同 0**
> 力扣：[LCP 01. 猜数字](https://leetcode.cn/problems/guess-numbers/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP01.猜数字

[力扣](https://leetcode.cn/problems/guess-numbers/)

leetcode的常规题库要等更新，所以计划先把LCP给写了。

比较基础的题目，一趟遍历，统计两个数组中值相同的下标数即可。

最后附上python代码：

```python
class Solution(object):
    def game(self, guess, answer):
        """
        :type guess: List[int]
        :type answer: List[int]
        :rtype: int
        """

        res = 0
        for index in range(3):
            if guess[index] == answer[index]:
                res += 1
        
        return res
```

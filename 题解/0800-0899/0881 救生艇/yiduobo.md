---
title: "881. 救生艇"
aliases: ["yiduobo的每日leetcode 881.救生艇"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/351096279"
zhihu_id: "351096279"
zhihu_title: "yiduobo的每日leetcode 881.救生艇"
question_id: "881"
question: "救生艇"
problem_url: "https://leetcode.cn/problems/boats-to-save-people/"
created: "2021-02-17T18:25:46+08:00"
updated: "2021-02-17T18:25:46+08:00"
upvotes: 0
comments: 0
---

# 881. 救生艇

> **[yiduobo的每日leetcode 881.救生艇](https://zhuanlan.zhihu.com/p/351096279) · 知乎 · 2021-02-17 · 赞同 0**
> 力扣：[881. 救生艇](https://leetcode.cn/problems/boats-to-save-people/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

881.救生艇

[力扣](https://leetcode-cn.com/problems/boats-to-save-people/)

注意到一艘船最多只能坐两个人，因此如果我们考虑当前最重的人，那么若其与当前最轻的人体重之和超过了limit，最重的人就只能单独坐一艘船，否则就应当安排其与最轻的人坐一艘船。于是可以先对所有人按体重进行排序，然后使用两个指针l和r指向当前最轻和最重的人。

当l小于r时：

1、若l等于r，说明此时就剩最后一个人，因此需要再安排一艘船，然后返回答案

2、若people[l] + people[r] \<\= limit，说明可以将最轻的人和最终的人安排在同一艘船上，因此此时有l+\=1，r-\=1

3、其他情况下，需要单独为r安排一艘船，于是此时有r-\=1

最后附上python代码：

```python
class Solution(object):
    def numRescueBoats(self, people, limit):
        """
        :type people: List[int]
        :type limit: int
        :rtype: int
        """

        l = 0
        r = len(people) - 1
        people = sorted(people)
        res = 0
        while l <= r:
            if l == r:
                return res + 1
            if people[l] + people[r] <= limit:
                l += 1
                r -= 1
                res += 1
            else:
                r -= 1
                res += 1
        
        return res
```

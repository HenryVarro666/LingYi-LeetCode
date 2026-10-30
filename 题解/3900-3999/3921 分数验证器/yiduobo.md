---
title: "3921. 分数验证器"
aliases: ["yiduobo的每日leetcode 3921.分数验证器"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2037307357034762480"
zhihu_id: "2037307357034762480"
zhihu_title: "yiduobo的每日leetcode 3921.分数验证器"
question_id: "3921"
question: "分数验证器"
problem_url: "https://leetcode.cn/problems/score-validator/"
difficulty: "Easy"
created: "2026-05-11T23:09:23+08:00"
updated: "2026-05-11T23:09:24+08:00"
upvotes: 3
comments: 0
---

# 3921. 分数验证器

> **[yiduobo的每日leetcode 3921.分数验证器](https://zhuanlan.zhihu.com/p/2037307357034762480) · 知乎 · 2026-05-11 · 赞同 3**
> 力扣：[3921. 分数验证器](https://leetcode.cn/problems/score-validator/) · Easy · 灵茶山艾府：[模拟（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3921.分数验证器

<https://leetcode.cn/problems/score-validator/description/>

题目给出一个字符串数组events。

最开始，总得分score和计数器counter都为0，events中的每个元素为一下之一：

- '0'、'1'、'2'、'3'、'4'、'6'：将该值累加到score中
- 'W'：计数器加1
- 'WD'、'NB'：总得分加1

现在要求从左到右处理events，直到events中所有元素处理完毕，或者counter变为10。

要求返回一个长度为2的整数数组[score, counter]。

按照题目要求对events进行一趟遍历，根据具体的元素更新score或者counter即可。注意counter变为10时应该退出遍历的循环。

最后附上python代码：

```python
class Solution(object):
    def scoreValidator(self, events):
        """
        :type events: List[str]
        :rtype: List[int]
        """
        
        score = 0
        counter = 0
        for e in events:
            if e == 'W':
                counter += 1
                if counter == 10:
                    break
            elif e == 'WD' or e == 'NB':
                score += 1
            else:
                score += int(e)
        
        return [score, counter]
```

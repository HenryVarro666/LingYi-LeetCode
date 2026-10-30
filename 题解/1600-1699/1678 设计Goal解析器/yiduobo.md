---
title: "1678. 设计Goal解析器"
aliases: ["yiduobo的每日leetcode 1678.设计Goal解析器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/444449243"
zhihu_id: "444449243"
zhihu_title: "yiduobo的每日leetcode 1678.设计Goal解析器"
question_id: "1678"
question: "设计Goal解析器"
problem_url: "https://leetcode.cn/problems/goal-parser-interpretation/"
created: "2021-12-12T20:47:19+08:00"
updated: "2021-12-12T20:47:19+08:00"
upvotes: 1
comments: 0
---

# 1678. 设计Goal解析器

> **[yiduobo的每日leetcode 1678.设计Goal解析器](https://zhuanlan.zhihu.com/p/444449243) · 知乎 · 2021-12-12 · 赞同 1**
> 力扣：[1678. 设计Goal解析器](https://leetcode.cn/problems/goal-parser-interpretation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1678.设计Goal解析器

[力扣](https://leetcode-cn.com/problems/goal-parser-interpretation/)

比较基础的题目，从头开始向后一趟扫描：

1、若当前字符为G，那么将G加入到答案中，然后考虑下一个字符

2、若不满足情况1，那么此时当前字符必然为左括号。若下一个字符为右括号，那么将o加入到答案中，然后跳过下一个字符，直接考虑往后数的第二个字符

3、若不满足情况1和情况2，那么此时将al加入到答案中，然后跳过后面3个字符，直接考虑往后数第四个字符

扫描完成后，整理答案输出即可

最后附上python代码：

```python
class Solution(object):
    def interpret(self, command):
        """
        :type command: str
        :rtype: str
        """

        res = []
        now = 0
        n = len(command)
        while now < n:
            char = command[now]
            if char == 'G':
                res.append('G')
                now += 1
            elif command[now + 1] == ')':
                res.append('o')
                now += 2
            else:
                res.append('al')
                now += 4
        
        return ''.join(res)
```

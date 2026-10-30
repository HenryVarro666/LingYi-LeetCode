---
title: "433. 最小基因变化"
aliases: ["yiduobo的每日leetcode 433.最小基因变化"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/198196723"
zhihu_id: "198196723"
zhihu_title: "yiduobo的每日leetcode 433.最小基因变化"
question_id: "433"
question: "最小基因变化"
problem_url: "https://leetcode.cn/problems/minimum-genetic-mutation/"
created: "2020-08-25T23:32:16+08:00"
updated: "2020-08-25T23:32:16+08:00"
upvotes: 0
comments: 0
---

# 433. 最小基因变化

> **[yiduobo的每日leetcode 433.最小基因变化](https://zhuanlan.zhihu.com/p/198196723) · 知乎 · 2020-08-25 · 赞同 0**
> 力扣：[433. 最小基因变化](https://leetcode.cn/problems/minimum-genetic-mutation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

433.最小基因变化<https://leetcode-cn.com/problems/minimum-genetic-mutation/>

如果将bank中的所有基因看成点，那么对于基因x，若替换其中某个字符后能变成基因y，那么就认为在x到y之间存在一条边。我们从start开始进行bfs，抵达end的轮次即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minMutation(self, start, end, bank):
        """
        :type start: str
        :type end: str
        :type bank: List[str]
        :rtype: int
        """

        gen_bank = set(bank)
        if end not in gen_bank:
            return -1

        q = [start]
        l = 0
        r = 1
        res = 0
        while l < r:
            res += 1
            new_r = r
            for now in q[l:r]:
                for index, char in enumerate(now):
                    for replace_char in ['A', 'C', 'G', 'T']:
                        if replace_char != char:
                            tmp = now[:index] + replace_char + now[index + 1:]
                            if tmp == end:
                                return res
                            if tmp in gen_bank:
                                q.append(tmp)
                                new_r += 1
                                gen_bank.remove(tmp)
            l = r
            r = new_r

        return -1
```

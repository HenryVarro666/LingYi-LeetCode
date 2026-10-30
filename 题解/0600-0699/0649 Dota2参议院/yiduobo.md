---
title: "649. Dota2参议院"
aliases: ["yiduobo的每日leetcode 649.Dota2参议院"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/276578921"
zhihu_id: "276578921"
zhihu_title: "yiduobo的每日leetcode 649.Dota2参议院"
question_id: "649"
question: "Dota2参议院"
problem_url: "https://leetcode.cn/problems/dota2-senate/"
created: "2020-11-06T23:29:19+08:00"
updated: "2020-11-06T23:29:19+08:00"
upvotes: 0
comments: 0
---

# 649. Dota2参议院

> **[yiduobo的每日leetcode 649.Dota2参议院](https://zhuanlan.zhihu.com/p/276578921) · 知乎 · 2020-11-06 · 赞同 0**
> 力扣：[649. Dota2参议院](https://leetcode.cn/problems/dota2-senate/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

649.Dota2参议院

[力扣](https://leetcode-cn.com/problems/dota2-senate/)

题目中的禁止规则存在一个先后顺序，因此在进行投票ban人时，应当优先杀伤对手马上要投票的生力军，而对于已经投过票的对手可以留在后面再ban。

例如RDDRDR这种情况，第一个R禁掉了第一个D，那么第二个D就应当禁掉第二个R，这样第三个D也能有出手的机会从而取胜。若第二个D禁掉第一个R，那么第二个R就可以出手禁掉第三个D，此时D方就输了。

有了上面这个思路，我们就可以不断模拟双方投票的过程。在投票的过程中，我们需要使用变量记录此时的ban人情况。对于当前遍历到的人，若其阵营接下来要ban的人数不为0，那么此人就应该被ban掉，同时该阵营接下来要ban的人数减1，否则此人就会反过来ban掉对方阵营中的1人，即对方阵营接下来要ban的人数加1。重复这个过程直到某个阵营没有人了为止。

每一轮投票中，都应该有不少于一半的人被投出去，因此轮次应该是log级别的。不过注意到实际上每轮需要处理的人都是折半的，因此时间复杂度应该是O(n)。

最后附上python代码：

```python
class Solution(object):
    def predictPartyVictory(self, senate):
        """
        :type senate: str
        :rtype: str
        """

        q = []
        r = d = 0
        del_r = del_d = 0
        for char in senate:
            q.append(char)
            if char == 'R':
                r += 1
            else:
                d += 1
        
        while r > 0 and d > 0:
            tot = r + d
            r = d = 0
            for index in range(tot):
                if q[index] == 'R':
                    if del_r > 0:
                        del_r -= 1
                    else:
                        q[r + d] = q[index]
                        r += 1
                        del_d += 1
                else:
                    if del_d > 0:
                        del_d -= 1
                    else:
                        q[r + d] = q[index]
                        d += 1
                        del_r += 1

        if r > 0:
            return 'Radiant'
        else:
            return 'Dire'
```

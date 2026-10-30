---
title: "292. Nim游戏"
aliases: ["yiduobo的每日leetcode 292.Nim游戏"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/156842688"
zhihu_id: "156842688"
zhihu_title: "yiduobo的每日leetcode 292.Nim游戏"
question_id: "292"
question: "Nim游戏"
problem_url: "https://leetcode.cn/problems/nim-game/"
created: "2020-07-05T17:06:04+08:00"
updated: "2020-07-05T17:06:04+08:00"
upvotes: 0
comments: 0
---

# 292. Nim游戏

> **[yiduobo的每日leetcode 292.Nim游戏](https://zhuanlan.zhihu.com/p/156842688) · 知乎 · 2020-07-05 · 赞同 0**
> 力扣：[292. Nim游戏](https://leetcode.cn/problems/nim-game/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

292.Nim游戏<https://leetcode-cn.com/problems/nim-game/>

Nim游戏有各式各样的变种，往大了扯就是SG函数以及博弈论之类的东西了，不过这里是最简单的一种形式，处理方法也比较简单：注意到每次只能拿1-3颗石头，那么后手总是能根据先手拿的石头数量将这一轮的总数补充到4。

如果n是4的倍数，那么后手根据先手拿的数量每轮补充到4即可，此时后手必胜。

如果n不是4的倍数，先手可以拿n%4颗石头，其实剩下的石头是4的倍数，且可以视为先后手互换了，于是此时先手必胜。

代码也很简单，就一行:

```python
class Solution(object):
    def canWinNim(self, n):
        """
        :type n: int
        :rtype: bool
        """

        return n % 4 != 0
```

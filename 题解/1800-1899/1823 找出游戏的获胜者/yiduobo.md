---
title: "1823. 找出游戏的获胜者"
aliases: ["yiduobo的每日leetcode 1823.找出游戏的获胜者"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/466700168"
zhihu_id: "466700168"
zhihu_title: "yiduobo的每日leetcode 1823.找出游戏的获胜者"
question_id: "1823"
question: "找出游戏的获胜者"
problem_url: "https://leetcode.cn/problems/find-the-winner-of-the-circular-game/"
created: "2022-02-12T21:22:30+08:00"
updated: "2022-02-12T21:22:30+08:00"
upvotes: 1
comments: 0
---

# 1823. 找出游戏的获胜者

> **[yiduobo的每日leetcode 1823.找出游戏的获胜者](https://zhuanlan.zhihu.com/p/466700168) · 知乎 · 2022-02-12 · 赞同 1**
> 力扣：[1823. 找出游戏的获胜者](https://leetcode.cn/problems/find-the-winner-of-the-circular-game/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1823.找出游戏的获胜者

[力扣](https://leetcode-cn.com/problems/find-the-winner-of-the-circular-game/)

经典的约瑟夫环问题，常规做法为模拟或者动态规划。在这里数据规模比较小，两种做法都行得通。

我在这里使用的是动态规划。其思路也很容想到，就是在n个人在执行一轮之后变成n - 1个人，对于这n - 1个人而言，其在n - 1个人这一轮的编号要如何与在n个人这一轮的编号建立起映射。

简单模拟一下可以发现，对于n个人的情况，第m \= k % n个人被淘汰出局，还剩下n - 1个人。对于这n - 1个人而言，新的1号对应的是原来n个人中的m % n + 1这个人，新的2号对应的是，(m + 1) % n + 1，依次类推。

令f[n]表示n个人时最终幸存者的编号，那么在执行一轮之后，就有新的f[n - 1]号对应的是原来n个人中(f[n - 1] + m - 1) % n + 1，即

f[n] \= (f[n - 1] + m - 1) % n + 1

注意到这里的m \= k % n，那么可以去掉重复的模k，就有f[n] \= (f[n - 1] + k - 1) % n + 1

显然f[1] \= 1，那么可以通过上面式子递推计算出f[n]了。

在这里有一个小优化是只要不出现到达数组末尾被迫重新开始，即f[n - 1] + k - 1小于n，那么就可以认为f[n] \= f[n - 1] + k。多次执行这个递推式相当于连续加k，那么一个自然的想法就是对于当前的f[next]，计算出最近的next，满足f[next - 1] + k - 1大于等于next，那么在now到next之间的这一段就可以直接用乘以k带过了。具体实现起来边界的处理有点麻烦，我在这里偷懒就没有实现了。

最后附上python代码：

```python
class Solution(object):
    def findTheWinner(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: int
        """

        res = 1
        for index in range(2, n + 1):
            res = (res + k - 1) % index + 1
        return res
```

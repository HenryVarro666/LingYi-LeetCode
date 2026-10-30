---
title: "517. 超级洗衣机"
aliases: ["yiduobo的每日leetcode 517.超级洗衣机"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/260514853"
zhihu_id: "260514853"
zhihu_title: "yiduobo的每日leetcode 517.超级洗衣机"
question_id: "517"
question: "超级洗衣机"
problem_url: "https://leetcode.cn/problems/super-washing-machines/"
created: "2020-09-29T21:54:17+08:00"
updated: "2020-09-29T21:54:17+08:00"
upvotes: 0
comments: 0
---

# 517. 超级洗衣机

> **[yiduobo的每日leetcode 517.超级洗衣机](https://zhuanlan.zhihu.com/p/260514853) · 知乎 · 2020-09-29 · 赞同 0**
> 力扣：[517. 超级洗衣机](https://leetcode.cn/problems/super-washing-machines/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

517.超级洗衣机<https://leetcode-cn.com/problems/super-washing-machines/>

很有意思的题目。首先，我们可以求出衣服的总数，从而得到每台洗衣机最终应该有的衣服数量，设其为avg。对于一台洗衣机而言：

1、若当前衣服数量k等于avg：

此时这台洗衣机可能从左侧或者右侧接收到m件衣服，然后再将这m件衣服给到另一侧。给出这些衣服需要的次数为m，而从上游给当前洗衣机这m件衣服的次数同样是m，因此可以略过当前这台洗衣机不予考虑。

2、若当前衣服数量k小于avg，此时可以分为若干种情况：

1)从一侧或两侧接收avg - m件衣服：这种情况当前洗衣机任何操作，可以直接略过

2)从一侧接收p件衣服，然后给另一方q件衣服，自己留下avg：这种情况下，

p + k - avg \= q，那么就有p -q \= avg - k > 0，即这台洗衣机给出衣服需要操作的次数必然小于其上游给到当前洗衣机所需的操作次数，因此也可以不予考虑。

综合上面两种情况，即当前洗衣机中现有衣服数量k小于等于目标数量avg时，都可以不予考虑。这里有一个隐藏条件就是，若当前衣服数量k小于要给出的衣服数量m，那么期间是可能存在一段时间是需要等待上游衣服过来的。但是相对的，等待的时间越长，说明上游中的0越多，从而使得上游最大的分发者需要的操作次数越多，即当前洗衣机的等待时间加上操作时间依然不会超过上游最大分发者的操作时间。

接下来就只需要考虑当前衣服数量k大于avg时的操作了：

3、若当前衣服数量k大于avg：

显然，此时这台洗衣机至少需要操作rest \= k - avg次，将多余的衣服分发出去。简单起见我们先考虑一侧的情况，即设当前洗衣机左侧的所有洗衣机最终能有多少件衣服给到当前洗衣机。这里的left_rest可以为负数，表示左侧没得衣服给过来，反而需要当前洗衣机给衣服过去，那么这里就继续分情况讨论：

1)若left_rest大于等于0，说明有left_rest件衣服给过来，再加上这台洗衣机本身需要给出的rest件衣服，即这台洗衣机需要left_rest + rest次操作，需要用这个数来更新答案。

2)若left_rest小于0，且left_rest + rest >\= 0，说明这台洗衣机需要分发left_rest件衣服给左边，分发rest - left_rest件衣服给右边，那么这台洗衣机就需要rest次操作，同样需要用这个数来更新答案。

3)若left_rest小于0，且left_rest + rest \< 0，说明这台洗衣机需要从右侧接受一些衣服，然后再给左侧left_rest件衣服，那么就需要left_rest次操作。这里同样可能出现等待的情况，但是跟上面说的一样，越长的等待说明右侧的0越多，即右侧的上游分发者的操作也越多，因此这里不考虑等待的时间也不会影响到最终的答案。于是这里直接用-left_rest来更新答案。

最后，需要根据rest来更新left_rest。

最后附上python代码：

```python
class Solution(object):
    def findMinMoves(self, machines):
        """
        :type machines: List[int]
        :rtype: int
        """

        n = len(machines)
        tot = sum(machines)

        if tot % n != 0:
            return -1

        tot /= n
        left_rest = 0
        res = 0
        for now in machines:
            if now == tot:
                continue
            elif now < tot:
                left_rest += now - tot
            else:
                now_rest = now - tot
                if left_rest < 0:
                    if now_rest + left_rest >= 0:
                        res = max(now_rest, res)
                    else:
                        res = max(-left_rest, res)
                else:
                    res = max(left_rest + now_rest, res)
                left_rest += now_rest

        return res
```

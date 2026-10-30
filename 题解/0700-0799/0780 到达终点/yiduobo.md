---
title: "780. 到达终点"
aliases: ["yiduobo的每日leetcode 780.到达终点"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/340500701"
zhihu_id: "340500701"
zhihu_title: "yiduobo的每日leetcode 780.到达终点"
question_id: "780"
question: "到达终点"
problem_url: "https://leetcode.cn/problems/reaching-points/"
created: "2020-12-29T23:13:23+08:00"
updated: "2020-12-29T23:13:23+08:00"
upvotes: 1
comments: 0
---

# 780. 到达终点

> **[yiduobo的每日leetcode 780.到达终点](https://zhuanlan.zhihu.com/p/340500701) · 知乎 · 2020-12-29 · 赞同 1**
> 力扣：[780. 到达终点](https://leetcode.cn/problems/reaching-points/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

780.到达终点

[力扣](https://leetcode-cn.com/problems/reaching-points/)

首先，如果直接从(sx, sy)开始往外扩展然后检测能否到达(tx, ty)，理论上的复杂度太高，可能到达10^9，于是我们只能想办法从(tx, ty)开始倒推。

在其之前，我们先来确定几种特殊情况：

1、sx等于tx，且sy等于ty：

此时答案显然为true

2、不满足条件1，且tx等于ty：

由于sx和sy都大于0，那么每一轮变换中，sx或sy都必然小于sx + sy，因此若tx等于ty，那么答案必然是false

3、不满足条件1和2，且tx小于sx，或ty小于sy：

同上，由于sx和sy都大于0，那么每轮变换只能越来越大，因此答案必然为false

接下来，我们考虑一般的情况。方便起见，我们认定sx是sx和sy中较小的，tx是tx和ty中较小的。若不满足可以交换sx和sy或tx和ty，因为根据变换的规则二者是等价的。

对于tx和ty，其上一轮的结果必然是tx和ty - tx，接下来我们则需要根据tx以及ty - tx的大小判断上上轮的情况。换言之，这里可以看做ty对tx取模，即(tx, ty)这种状态必然是从(ty % tx, tx)变换得来的。

进一步的，我们如果继续对(ty % tx, tx)进行溯源，实际上就是对(tx, ty)执行类似辗转相除法的操作，而这个操作的停止条件则是某次执行完毕后较小的数tx小于等于sx。因为当tx小于sx时，是必然无解的。

当辗转相除停止时，若tx小于sx，则返回false，否则此时tx此时必然等于sx，那么相当于要从(sx, sy)得到当前的(tx, ty)。由于有sx等于tx，那么此时只需要ty大于等于sy，且二者的差值是sx的倍数即可。若不满足这个条件，则答案依然是false。

以样例中的(1, 1), (3, 5)来说明：

1、(3, 5)必然是从(5 % 3 \= 2, 3)得来的

2、(2, 3)必然是从(3 % 2 \= 1, 2)得来的

3、此时已经有tx \= sx \= 1，且ty - sy \= 2 - 1 \= 1，是sx的倍数，说明可以从(sx, sy)得到当前的(tx, ty)，然后进一步得到最终的(tx, ty)

最后附上python代码：

```python
class Solution(object):
    def reachingPoints(self, sx, sy, tx, ty):
        """
        :type sx: int
        :type sy: int
        :type tx: int
        :type ty: int
        :rtype: bool
        """

        if sx == tx and sy == ty:
            return True
        if tx == ty:
            return False

        if tx < sx:
            return False
        if ty < sy:
            return False

        if tx > ty:
            tx, ty = ty, tx
        if sx > sy:
            sx, sy = sy, sx

        if sx == 0:
            sx, sy = sy, sy
        while tx > sx:
            tx, ty = ty % tx, tx   

        return tx == sx and ty >=sy and (ty - sy) % sx == 0
```

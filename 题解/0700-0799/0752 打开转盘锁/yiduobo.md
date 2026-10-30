---
title: "752. 打开转盘锁"
aliases: ["yiduobo的每日leetcode 752.打开转盘锁"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/337970384"
zhihu_id: "337970384"
zhihu_title: "yiduobo的每日leetcode 752.打开转盘锁"
question_id: "752"
question: "打开转盘锁"
problem_url: "https://leetcode.cn/problems/open-the-lock/"
created: "2020-12-18T20:47:14+08:00"
updated: "2020-12-18T20:47:14+08:00"
upvotes: 0
comments: 0
---

# 752. 打开转盘锁

> **[yiduobo的每日leetcode 752.打开转盘锁](https://zhuanlan.zhihu.com/p/337970384) · 知乎 · 2020-12-18 · 赞同 0**
> 力扣：[752. 打开转盘锁](https://leetcode.cn/problems/open-the-lock/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

752.打开转盘锁

[力扣](https://leetcode-cn.com/problems/open-the-lock/)

还是bfs的题目。我们的目标就是从0000开始进行bfs，每次可以选择其中的一位进行旋转。若新得到的数字没有被使用过，且不是死亡数字，那么就将其加入到bfs队列中。转到目标数字时，当前bfs的轮次就是最终答案。若bfs结束，那么说明无法转到目标数字，此时返回-1。

最后附上python代码：

```python
class Solution(object):
    def openLock(self, deadends, target):
        """
        :type deadends: List[str]
        :type target: str
        :rtype: int
        """

        if target == '0000':
            return 0
        

        used = [False] * 10000
        for num in deadends:
            used[int(num)] = True
        
        if used[0]:
            return -1

        q = [0]
        l = 0
        r = 1
        step = 0
        while l < r:
            step += 1
            for now in q[l:r]:
                base = 1
                for index in range(4):
                    mod = now / base % 10
                    if mod == 0:
                        prev = now + base * 9
                    else:
                        prev = now - base
                    if prev == int(target):
                        return step
                    if not used[prev]:
                        used[prev] = True
                        q.append(prev)

                    if mod == 9:
                        next = now - base * 9
                    else:
                        next = now + base
                    if next == int(target):
                        return step
                    if not used[next]:
                        used[next] = True
                        q.append(next)

                    base *= 10
            
            l = r
            r = len(q)
        
        return -1
```

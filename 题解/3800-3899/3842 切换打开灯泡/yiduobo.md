---
title: "3842. 切换打开灯泡"
aliases: ["yiduobo的每日leetcode 3842.切换打开灯泡"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2010151113563849360"
zhihu_id: "2010151113563849360"
zhihu_title: "yiduobo的每日leetcode 3842.切换打开灯泡"
question_id: "3842"
question: "切换打开灯泡"
problem_url: "https://leetcode.cn/problems/toggle-light-bulbs/"
difficulty: "Easy"
created: "2026-02-28T03:01:19+08:00"
updated: "2026-02-28T03:01:20+08:00"
upvotes: 1
comments: 0
---

# 3842. 切换打开灯泡

> **[yiduobo的每日leetcode 3842.切换打开灯泡](https://zhuanlan.zhihu.com/p/2010151113563849360) · 知乎 · 2026-02-28 · 赞同 1**
> 力扣：[3842. 切换打开灯泡](https://leetcode.cn/problems/toggle-light-bulbs/) · Easy · 灵茶山艾府：[和 100 无关的做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3842.切换打开灯泡

<https://leetcode.cn/problems/toggle-light-bulbs/description/>

题目给出一个整数数组bulbs，其中每个元素的取值范围都在1到100之间。

现在有100个电灯泡，按照1到100编号。初始情况下，所有灯泡都是关闭状态。

对于bulbs中的每个元素bulbs[index]，若bulbs[index]目前是关闭的，那么就将其打开，反之则将其关闭。

现在要求按照bulbs操作灯泡，按升序返回最终打开的灯泡编号。

初始化一个布尔数组flag，其中flag[index]表示index的开关状态。flag初始值都为false，表示所有灯泡都是关闭的。

接下来遍历bulbs，对于当前遍历到的bulbs\[index\]，将flag\[bulbs\[index\]\]取反，表示对bulbs\[index\]这个灯泡进行操作。

遍历完成后，再从1到100遍历，对于当前的index，若flag[index]为true，则将其加入到答案数组即可。

最后附上python代码：

```python
class Solution(object):
    def toggleLightBulbs(self, bulbs):
        """
        :type bulbs: List[int]
        :rtype: List[int]
        """
        
        flag = [False] * 101
        for b in bulbs:
            flag[b] = not flag[b]
        
        res = []
        for index in range(1, 101):
            if flag[index]:
                res.append(index)
        
        return res
```

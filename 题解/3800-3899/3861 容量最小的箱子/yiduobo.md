---
title: "3861. 容量最小的箱子"
aliases: ["yiduobo的每日leetcode 3861.容量最小的箱子"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2014134459117609954"
zhihu_id: "2014134459117609954"
zhihu_title: "yiduobo的每日leetcode 3861.容量最小的箱子"
question_id: "3861"
question: "容量最小的箱子"
problem_url: "https://leetcode.cn/problems/minimum-capacity-box/"
difficulty: "Easy"
created: "2026-03-11T02:01:34+08:00"
updated: "2026-03-11T02:01:34+08:00"
upvotes: 1
comments: 0
---

# 3861. 容量最小的箱子

> **[yiduobo的每日leetcode 3861.容量最小的箱子](https://zhuanlan.zhihu.com/p/2014134459117609954) · 知乎 · 2026-03-11 · 赞同 1**
> 力扣：[3861. 容量最小的箱子](https://leetcode.cn/problems/minimum-capacity-box/) · Easy · 灵茶山艾府：[遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3861.容量最小的箱子

<https://leetcode.cn/problems/minimum-capacity-box/description/>

题目给出一个整数数组capacity，其中capacity[index]表示第index个箱子的容量。另外给出一个整数itemSize，表示一个物品的大小。

若第index个箱子对应的capacity[index] >\= itemSize，那么该箱子就可以存放该物品。

要求返回可以存放该物品的容量最小的箱子下标，若存在多个这样的箱子，返回下标最小的那一个。若没有可用的箱子，则返回-1。

首先初始化答案为-1，然后对capacity进行一趟遍历，若当前的capacity[index]大于等于itemSize，且目前的答案为-1，或者目前答案对应的箱子容量大于当前的capacity[index]，就将答案更新为index即可。

最后附上python代码：

```python
class Solution(object):
    def minimumIndex(self, capacity, itemSize):
        """
        :type capacity: List[int]
        :type itemSize: int
        :rtype: int
        """
        
        res = -1
        for index, c in enumerate(capacity):
            if c >= itemSize and (res == -1 or capacity[res] > c):
                res = index
        
        return res
```

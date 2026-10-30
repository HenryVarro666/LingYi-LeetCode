---
title: "3237. Alt和Tab模拟"
aliases: ["yiduobo的每日leetcode 3237.Alt和Tab模拟"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/720580380"
zhihu_id: "720580380"
zhihu_title: "yiduobo的每日leetcode 3237.Alt和Tab模拟"
question_id: "3237"
question: "Alt和Tab模拟"
problem_url: "https://leetcode.cn/problems/alt-and-tab-simulation/"
created: "2024-09-17T23:31:28+08:00"
updated: "2024-09-17T23:31:28+08:00"
upvotes: 1
comments: 0
---

# 3237. Alt和Tab模拟

> **[yiduobo的每日leetcode 3237.Alt和Tab模拟](https://zhuanlan.zhihu.com/p/720580380) · 知乎 · 2024-09-17 · 赞同 1**
> 力扣：[3237. Alt和Tab模拟](https://leetcode.cn/problems/alt-and-tab-simulation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3237.Alt和Tab模拟

[. - 力扣（LeetCode）](https://leetcode.cn/problems/alt-and-tab-simulation/)

有n个编号为1到n的窗口，现在要模拟使用alt + tab在窗口间导航。

给出两个数组windows以及queries，其中windows保存的是窗口的初始顺序，第一个元素在最前面，最后一个元素在最后面，而queries表示的则是按顺序将queries[i]表示的窗口切换到最前面。问windows数组最终的状态。

对于windows中的窗口，有一部分是被queries切换过的，另一部分没有切换过的则会保持原来的顺序，同时这些窗口一定在被切换过的窗口后面。而对于queries中的窗口，最后一次切换越靠后的，在windows中的位置就越靠前。

于是可以从后往前倒序遍历queries，若当前窗口是首次被切换，则将其加入到答案中。注意这里指的是倒序的首次切换，也就是正常顺序的最后一次切换。

接下来再从前往后遍历windows，若当前窗口没有被切换过，则将其加入到答案中。

最后附上python代码：

```python
class Solution(object):
    def simulationResult(self, windows, queries):
        """
        :type windows: List[int]
        :type queries: List[int]
        :rtype: List[int]
        """

        vis = set()
        res = []
        for q in queries[::-1]:
            if q not in vis:
                res.append(q)
                vis.add(q)
        
        for v in windows:
            if v not in vis:
                res.append(v)
                vis.add(v)

        return res
```

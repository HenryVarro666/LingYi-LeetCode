---
title: "582. 杀掉进程"
aliases: ["yiduobo的每日leetcode 582.杀掉进程"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/601538753"
zhihu_id: "601538753"
zhihu_title: "yiduobo的每日leetcode 582.杀掉进程"
question_id: "582"
question: "杀掉进程"
problem_url: "https://leetcode.cn/problems/kill-process/"
created: "2023-01-28T23:22:09+08:00"
updated: "2023-01-28T23:22:09+08:00"
upvotes: 0
comments: 0
---

# 582. 杀掉进程

> **[yiduobo的每日leetcode 582.杀掉进程](https://zhuanlan.zhihu.com/p/601538753) · 知乎 · 2023-01-28 · 赞同 0**
> 力扣：[582. 杀掉进程](https://leetcode.cn/problems/kill-process/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

582.杀掉进程

[力扣](https://leetcode.cn/problems/kill-process/)

根据题目给出的父子关系建立有向图，然后从kill节点开始向下进行bfs，遍历到的所有进程都是会连带被杀掉的进程，而bfs的队列q就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def killProcess(self, pid, ppid, kill):
        """
        :type pid: List[int]
        :type ppid: List[int]
        :type kill: int
        :rtype: List[int]
        """

        childs = {}
        for x, y in zip(pid, ppid):
            if y not in childs:
                childs[y] = []
            childs[y].append(x)

        q = [kill]
        head, tail = 0, 1
        while head < tail:
            now = q[head]
            head += 1
            for next in childs.get(now, []):
                q.append(next)
                tail += 1
        
        return q
```

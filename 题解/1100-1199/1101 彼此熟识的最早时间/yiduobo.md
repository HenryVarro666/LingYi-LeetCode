---
title: "1101. 彼此熟识的最早时间"
aliases: ["yiduobo的每日leetcode 1101.彼此熟识的最早时间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/609407647"
zhihu_id: "609407647"
zhihu_title: "yiduobo的每日leetcode 1101.彼此熟识的最早时间"
question_id: "1101"
question: "彼此熟识的最早时间"
problem_url: "https://leetcode.cn/problems/the-earliest-moment-when-everyone-become-friends/"
created: "2023-02-25T17:39:54+08:00"
updated: "2023-02-25T17:39:54+08:00"
upvotes: 0
comments: 0
---

# 1101. 彼此熟识的最早时间

> **[yiduobo的每日leetcode 1101.彼此熟识的最早时间](https://zhuanlan.zhihu.com/p/609407647) · 知乎 · 2023-02-25 · 赞同 0**
> 力扣：[1101. 彼此熟识的最早时间](https://leetcode.cn/problems/the-earliest-moment-when-everyone-become-friends/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1101.彼此熟识的最早时间

[力扣](https://leetcode.cn/problems/the-earliest-moment-when-everyone-become-friends/)

对于这类连通性判定的问题，并查集是一个不错的选择。另外为了方便判断当前是否所有人都熟识，在维护常规并查集使用的父亲节点数组fa之外，还需要维护当前连通块中节点数量的数组weight。

将所有log按时间戳从小到大进行排序，然后一趟遍历。对于当前遍历到的新关系(x, y)，若x在并查集中的祖先与y在并查集中的祖先不同，那么就将二者合并，同时更新fa以及weight。若合并后的weight等于n，就说明此时所有人都在一个连通块里，返回当前的时间戳即可。

若遍历完后依然没有出现某个节点的weight等于n，那么返回-1。

最后附上python代码：

```python
class Solution(object):
    def earliestAcq(self, logs, n):
        """
        :type logs: List[List[int]]
        :type n: int
        :rtype: int
        """

        fa = range(n)
        weight = [1] * n

        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        for t, x, y in sorted(logs):
            fa_x = find(x)
            fa_y = find(y)

            if fa_x != fa_y:
                if weight[fa_x] < weight[fa_y]:
                    fa[fa_x] = fa_y
                    weight[fa_y] += weight[fa_x]
                    if weight[fa_y] == n:
                        return t
                else:
                    fa[fa_y] = fa_x
                    weight[fa_x] += weight[fa_y]
                    if weight[fa_x] == n:
                        return t
        
        return -1
```

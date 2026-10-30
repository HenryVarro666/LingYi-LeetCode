---
title: "1257. 最小公共区域"
aliases: ["yiduobo的每日leetcode 1257.最小公共区域"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/614876139"
zhihu_id: "614876139"
zhihu_title: "yiduobo的每日leetcode 1257.最小公共区域"
question_id: "1257"
question: "最小公共区域"
problem_url: "https://leetcode.cn/problems/smallest-common-region/"
created: "2023-03-17T19:35:00+08:00"
updated: "2023-03-17T19:35:00+08:00"
upvotes: 0
comments: 0
---

# 1257. 最小公共区域

> **[yiduobo的每日leetcode 1257.最小公共区域](https://zhuanlan.zhihu.com/p/614876139) · 知乎 · 2023-03-17 · 赞同 0**
> 力扣：[1257. 最小公共区域](https://leetcode.cn/problems/smallest-common-region/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1257.最小公共区域

[力扣](https://leetcode.cn/problems/smallest-common-region/)

题目可以认为是给出了一棵树，求树中两个节点的最近公共祖先。

对于单次求解的问题，可以先从一个节点开始向上一路走到根节点，同时使用哈希表记录路径上的节点。接下来再从另一个节点开始向上往根节点走，路径上最先出现在哈希表中的节点即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def findSmallestRegion(self, regions, region1, region2):
        """
        :type regions: List[List[str]]
        :type region1: str
        :type region2: str
        :rtype: str
        """

        fa = {}
        for r in regions:
            for p in r[1:]:
                fa[p] = r[0]
        
        vis = set([region1])
        now = region1
        while now in fa:
            now = fa[now]
            vis.add(now)
        
        now = region2
        while now not in vis:
            now = fa[now]
        
        return now
```

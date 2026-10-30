---
title: "1719. 重构一棵树的方案数"
aliases: ["yiduobo的每日leetcode 1719.重构一棵树的方案数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/451003558"
zhihu_id: "451003558"
zhihu_title: "yiduobo的每日leetcode 1719.重构一棵树的方案数"
question_id: "1719"
question: "重构一棵树的方案数"
problem_url: "https://leetcode.cn/problems/number-of-ways-to-reconstruct-a-tree/"
created: "2021-12-29T00:27:49+08:00"
updated: "2021-12-29T00:27:49+08:00"
upvotes: 0
comments: 0
---

# 1719. 重构一棵树的方案数

> **[yiduobo的每日leetcode 1719.重构一棵树的方案数](https://zhuanlan.zhihu.com/p/451003558) · 知乎 · 2021-12-29 · 赞同 0**
> 力扣：[1719. 重构一棵树的方案数](https://leetcode.cn/problems/number-of-ways-to-reconstruct-a-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1719.重构一棵树的方案数

[力扣](https://leetcode-cn.com/problems/number-of-ways-to-reconstruct-a-tree/)

很有难度的题目，在这里我也是摸索着想到了一种可行的做法，但是可能有更优的做法，而且也全凭经验直觉，并没有形成可靠的方法论。

首先可以明确的是，树的根节点必然与其他所有节点都有联系。如果记cnt[x]为与x有联系的节点数目，那么根节点root对应的cnt就必然是n - 1，这里的n为节点的总数。

那么可以先统计出每个节点的cnt：

1、若里面没有任何节点满足cnt等于n - 1，说明无法构造出合法的树，直接返回0

2、反过来，如果存在多个节点的cnt都等于n - 1，那么就可以让这些点形成一条链，且链中点的相对位置可以任意交换，也就是说对于剩下的节点而言，如果能成功构造出树，那么最终答案就是2。为了方便后续的计算，可以从中任意选择一个节点作为代表

3、最一般的情况，只有一个节点的cnt等于n - 1，那么这个节点就是整棵树的根节点

对于情况2和3，现在已经找出了树的根节点，接下来还需要考察剩下的节点。在这里有一个隐藏的条件就是如果两个有关系的节点x和y，cnt[x] > cnt[y]，那么只有当x是y的祖先时才可能得到合法的树。那么一个自然的想法就是将剩下的节点按cnt从大到小进行排序然后依次处理，这样就相当于自顶向下在构造这棵树了。

对于当前节点而言，需要确定该节点与树中已有节点的关系，如果按树中已有节点的cnt从小到大一次与当前节点进行对比的话，那么只要确定了该节点的父亲，就算是确定了这个节点的最终位置。

对于当前到的已有节点p以及当前处理的节点now而言：

1、若now和p有关系，那么有两种情况。要么p是now的祖先，要么p和now是等价节点。这里的等价节点指的是p的关系列表与now的关系列表完全一致。此时可以所有与now有关系，且没有被处理过的节点x。若x与p没有关系，那么与上面描述的两种关系都有矛盾，说明无法构成树，此时直接返回0。

若不存在这样的p，那么此时可以对比cnt[p]与cnt[now]的大小，若一样大，说明二者是等价节点，也就是说剩下的节点如果可以构造出树，那么答案就是2，此时无需再对now进行记录，因为p就是now这些节点的代表；若不一样大，说明p是now的祖先，此时可以简单认为now就是p的父亲节点。此时还需要将now也记录到已有节点当中

2、若now和p没有关系，那么此时需要检测now和p是否都与另一个节点存在关系。因为此时可以确定根节点root与now和p都有关系。当然，也可能存在部分上级节点也是now和p共同的祖先，但是可以确定的是，now和p分属两棵不同的子树。若此时存在某个还未处理过的x，满足now和p都与x存在关系，那么此时树中就出现了一个环，是不合法的，此时直接返回0

按上面的方法依次处理每个节点，完了根据树是否合法，以及是否有等价节点来决定答案。

最后附上python代码：

```python
class Solution(object):
    def checkWays(self, pairs):
        """
        :type pairs: List[List[int]]
        :rtype: int
        """

        g = {}
        cnt_dict = {}
        for x, y in pairs:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)
            cnt_dict[x] = cnt_dict.get(x, 0) + 1
            cnt_dict[y] = cnt_dict.get(y, 0) + 1
        
        cnt_list = sorted(cnt_dict.items(), key=lambda d:-d[1])
        n = len(cnt_list)
        if cnt_list[0][1] != n - 1:
            return 0

        rest = set([x[0] for x in cnt_list])
        index = 0
        while index < n and cnt_list[index][1] == n - 1:
            rest.remove(cnt_list[index][0])
            index += 1
        
        if index > 1:
            res = 2
        else:
            res = 1
        
        q = [cnt_list[0][0]]

        while index < n:
            now, cnt = cnt_list[index]
            for p in q[::-1]:
                if now in g[p]:
                    for x in g[now]:
                        if x in rest and x not in g[p]:
                            return 0
                    if cnt_dict[p] == cnt:
                        res = 2
                    else:
                        q.append(now)
                    rest.remove(now)
                    break
                else:
                    for x in g[now]:
                        if x in rest and x in g[p]:
                            return 0
            
            index += 1
        
        return res
```

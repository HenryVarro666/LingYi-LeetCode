---
title: "1203. 项目管理"
aliases: ["yiduobo的每日leetcode 1203.项目管理"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/382015547"
zhihu_id: "382015547"
zhihu_title: "yiduobo的每日leetcode 1203.项目管理"
question_id: "1203"
question: "项目管理"
problem_url: "https://leetcode.cn/problems/sort-items-by-groups-respecting-dependencies/"
created: "2021-06-18T23:36:57+08:00"
updated: "2021-06-18T23:36:57+08:00"
upvotes: 0
comments: 0
---

# 1203. 项目管理

> **[yiduobo的每日leetcode 1203.项目管理](https://zhuanlan.zhihu.com/p/382015547) · 知乎 · 2021-06-18 · 赞同 0**
> 力扣：[1203. 项目管理](https://leetcode.cn/problems/sort-items-by-groups-respecting-dependencies/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1203.项目管理

[力扣](https://leetcode-cn.com/problems/sort-items-by-groups-respecting-dependencies/)

首先，为了方便起见，我们可以先给所有没有组别的任务安排上一个组，例如样例中第0、1、7个任务，我们可以分别将其安排在第2、3、4组，这样一来题目描述就更加统一简洁。

如果抛开组内任务必须连续这个要求来看的话，题目就是很常见的拓扑排序的问题。为了使得组内任务必须连续，那么在开始某一组的任务之前，需要将组内所有任务的前置任务中属于其他组的这些前置任务完成，而这也可以反映到组与组之间的拓扑关系上。也就是说对于任务a和任务b，如果a要在b之后完成，那么说明group[a]中的任务必须要等到group[b]中的任务完成之后才能进行。

那么一个可行的做法是对于每个组单独维护拓扑排序的队列，然后对于当前没有前置要求的组先进行拓扑排序，对于当前任务而言：

1、需要将当前任务加入到答案中

2、需要更新单个任务的入度信息，并将入度为0的任务加入到其对应的组的队列中

3、还需要一并更新组的入度信息，并将入度为0的组加入到组的拓扑排序队列当中

若某一组的拓扑排序完成后其执行的任务数小于该组的总任务数，那么说明该组中有任务无法完成，应当返回空。另外，若最终执行拓扑排序的组的数量小于总的组的数量，那么也应当返回空。

最后附上python代码：

```python
class Solution(object):
    def sortItems(self, n, m, group, beforeItems):
        """
        :type n: int
        :type m: int
        :type group: List[int]
        :type beforeItems: List[List[int]]
        :rtype: List[int]
        """

        item_cnt = [0] * m
        for index in range(n):
            if group[index] == -1:
                group[index] = m
                item_cnt.append(1)
                m += 1
            else:
                item_cnt[group[index]] += 1
        
        g = {x:set() for x in range(n)}
        ind_item = [0] * n
        ind_group = [0] * m
        

        for index in range(n):
            for before in beforeItems[index]:
                ind_item[index] += 1
                g[before].add(index)

                if group[before] != group[index]:
                    ind_group[group[index]] += 1

        group_q = []
        item_q = [[] for _ in range(m)]
        

        for index in range(n):
            if ind_item[index] == 0:
                item_q[group[index]].append(index)

        for index in range(m):
            if ind_group[index] == 0:
                group_q.append(index)
        
        res = []
        group_l = 0
        group_r = len(group_q)
        while group_l < group_r:
            now_group = group_q[group_l]
            group_l += 1
            item_l = 0
            while item_l < len(item_q[now_group]):
                now_item = item_q[now_group][item_l]
                item_l += 1
                res.append(now_item)
                for next_item in g[now_item]:
                    ind_item[next_item] -= 1
                    if ind_item[next_item] == 0:
                        item_q[group[next_item]].append(next_item)
                    
                    if group[next_item] != now_group:
                        ind_group[group[next_item]] -= 1
                        if ind_group[group[next_item]] == 0:
                            group_q.append(group[next_item])
                            group_r += 1

            if len(item_q[now_group]) != item_cnt[now_group]:
                return []
        
        if group_r != m:
            return []

        return res
```

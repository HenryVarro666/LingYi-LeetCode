---
title: "2115. 从给定原材料中找到所有可以做出的菜"
aliases: ["yiduobo的每日leetcode 2115.从给定原材料中找到所有可以做出的菜"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/graph", "leetcode/topological-sort", "leetcode/queue", "leetcode/hash-table", "leetcode/you-xiang-tu", "题单/图论算法", "题单/图论算法/二-拓扑排序"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/524065136"
zhihu_id: "524065136"
zhihu_title: "yiduobo的每日leetcode 2115.从给定原材料中找到所有可以做出的菜"
question_id: "2115"
question: "从给定原材料中找到所有可以做出的菜"
problem_url: "https://leetcode.cn/problems/find-all-possible-recipes-from-given-supplies/"
difficulty: "Medium"
rating: 1679
created: "2022-06-04T00:09:27+08:00"
updated: "2022-06-04T00:09:27+08:00"
upvotes: 0
comments: 0
---

# 2115. 从给定原材料中找到所有可以做出的菜

> **[yiduobo的每日leetcode 2115.从给定原材料中找到所有可以做出的菜](https://zhuanlan.zhihu.com/p/524065136) · 知乎 · 2022-06-04 · 赞同 0**
> 力扣：[2115. 从给定原材料中找到所有可以做出的菜](https://leetcode.cn/problems/find-all-possible-recipes-from-given-supplies/) · Medium · 灵茶山艾府：[简洁写法：哈希表+拓扑排序](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2115.从给定原材料中找到所有可以做出的菜

[力扣](https://leetcode.cn/problems/find-all-possible-recipes-from-given-supplies/)

非常标准的拓扑排序问题。将所有的菜和原材料都视为图中的点，若某道菜依赖某种材料，那么就从这种材料连一条有向边到这道菜。接下来执行拓扑排序，拓扑排序的初始对列为所有的材料，而最终答案就是拓扑排序能够遍历到的菜谱。

具体实现上，为了避免字符串比较的复杂度，我在这里先建立到字符串到节点编号的映射，之后的建图和拓扑排序都是基于节点编号进行的，最后再将编号还原成菜名。

最后附上python代码：

```python
class Solution(object):
    def findAllRecipes(self, recipes, ingredients, supplies):
        """
        :type recipes: List[str]
        :type ingredients: List[List[str]]
        :type supplies: List[str]
        :rtype: List[str]
        """

        mapping_dict = {}

        n = len(recipes)
        for index in range(n):
            mapping_dict[recipes[index]] = index
        
        g = {}
        cnt = n
        ind = []
        for index in range(n):
            ind.append(len(ingredients[index]))
            for info in ingredients[index]:
                if info not in mapping_dict:
                    mapping_dict[info] = cnt
                    cnt += 1
                
                num = mapping_dict[info]
                if num not in g:
                    g[num] = set()
                g[num].add(index)

        q = []
        used = set()
        for info in supplies:
            if info not in mapping_dict:
                mapping_dict[info] = cnt
                cnt += 1
            
            num = mapping_dict[info]
            q.append(num)
            used.add(num)
        
        l = 0
        r = len(q)
        while l < r:
            now = q[l]
            l += 1
            for next in g.get(now, set()):
                ind[next] -= 1
                if ind[next] == 0:
                    q.append(next)
                    used.add(next)
                    r += 1
        
        res = []
        for index in range(n):
            if index in used:
                res.append(recipes[index])
        
        return res
```

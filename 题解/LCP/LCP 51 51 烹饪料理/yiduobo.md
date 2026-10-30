---
title: "LCP 51. 烹饪料理"
aliases: ["yiduobo的每日leetcode LCP51.烹饪料理"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/577668370"
zhihu_id: "577668370"
zhihu_title: "yiduobo的每日leetcode LCP51.烹饪料理"
question_id: "LCP 51"
question: "烹饪料理"
created: "2022-10-27T03:08:44+08:00"
updated: "2022-10-27T03:08:44+08:00"
upvotes: 1
comments: 0
---

# LCP 51. 烹饪料理

> **[yiduobo的每日leetcode LCP51.烹饪料理](https://zhuanlan.zhihu.com/p/577668370) · 知乎 · 2022-10-27 · 赞同 1**
> 力扣：LCP 51. 烹饪料理

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP51.烹饪料理

[力扣](https://leetcode.cn/problems/UEcfPD/)

题目的数据规模非常小，那么就可以直接暴力搜索出所有可能的料理组合，选择其中满足饱腹感且美味度最大的组合作为答案即可。

最后附上python代码：

```python
class Solution(object):
    def perfectMenu(self, materials, cookbooks, attribute, limit):
        """
        :type materials: List[int]
        :type cookbooks: List[List[int]]
        :type attribute: List[List[int]]
        :type limit: int
        :rtype: int
        """

        global res
        res = -1
        n = len(cookbooks)

        def dfs(level, materials, now_limit, now_v):
            global res
            if level == n:
                if now_limit >= limit:
                    res = max(res, now_v)
            
                return

            dfs(level + 1, materials, now_limit, now_v)

            flag = True
            for index in range(len(materials)):
                if materials[index] < cookbooks[level][index]:
                    flag = False
                    break
            
            if flag:
                for index in range(len(materials)):
                    materials[index] -= cookbooks[level][index]

                dfs(level + 1, materials, now_limit + attribute[level][1], now_v + attribute[level][0])

                for index in range(len(materials)):
                    materials[index] += cookbooks[level][index]

        dfs(0, materials, 0, 0)
        return res
```

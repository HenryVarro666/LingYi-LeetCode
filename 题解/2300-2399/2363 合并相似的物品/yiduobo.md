---
title: "2363. 合并相似的物品"
aliases: ["yiduobo的每日leetcode 2363.合并相似的物品"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/562739145"
zhihu_id: "562739145"
zhihu_title: "yiduobo的每日leetcode 2363.合并相似的物品"
question_id: "2363"
question: "合并相似的物品"
problem_url: "https://leetcode.cn/problems/merge-similar-items/"
difficulty: "Easy"
created: "2022-09-09T01:57:58+08:00"
updated: "2022-09-09T01:57:58+08:00"
upvotes: 0
comments: 0
---

# 2363. 合并相似的物品

> **[yiduobo的每日leetcode 2363.合并相似的物品](https://zhuanlan.zhihu.com/p/562739145) · 知乎 · 2022-09-09 · 赞同 0**
> 力扣：[2363. 合并相似的物品](https://leetcode.cn/problems/merge-similar-items/) · Easy · 灵茶山艾府：[语法题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2363.合并相似的物品

[力扣](https://leetcode.cn/problems/merge-similar-items/)

使用哈希表统计每种重量下的总价值，然后从1到1000枚举所有可能的重量。若当前重量在哈希表中出现过，那么就将其和对应的价值加入到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def mergeSimilarItems(self, items1, items2):
        """
        :type items1: List[List[int]]
        :type items2: List[List[int]]
        :rtype: List[List[int]]
        """

        d = {}
        for w, v in items1:
            d[w] = d.get(w, 0) + v
        
        for w, v in items2:
            d[w] = d.get(w, 0) + v
        
        res = []
        for w in range(1, 1001):
            if w in d:
                res.append([w, d[w]])
        
        return res
```

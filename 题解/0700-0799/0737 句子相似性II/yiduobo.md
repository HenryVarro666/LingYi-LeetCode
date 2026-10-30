---
title: "737. 句子相似性II"
aliases: ["yiduobo的每日leetcode 737.句子相似性II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/605311977"
zhihu_id: "605311977"
zhihu_title: "yiduobo的每日leetcode 737.句子相似性II"
question_id: "737"
question: "句子相似性II"
problem_url: "https://leetcode.cn/problems/sentence-similarity-ii/"
created: "2023-02-10T23:33:46+08:00"
updated: "2023-02-10T23:33:46+08:00"
upvotes: 0
comments: 0
---

# 737. 句子相似性II

> **[yiduobo的每日leetcode 737.句子相似性II](https://zhuanlan.zhihu.com/p/605311977) · 知乎 · 2023-02-10 · 赞同 0**
> 力扣：[737. 句子相似性II](https://leetcode.cn/problems/sentence-similarity-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

737.句子相似性II

[力扣](https://leetcode.cn/problems/sentence-similarity-ii/)

上一题的加强版本。本题中相似性是可以传递的，那么如果将单词视为无向图中的点，相似关系视为无向图中的边，那么同一个连通块中的单词都是相似的。对于这个问题，则可以使用并查集来维护单词间的连通关系，从而高效地进行相似性的判断。

具体判断方式与上一题类似，无非就是将相似性判断的方式从哈希表变成了并查集。字符串转id的做法也同样可以运用起来。

最后附上python代码：

```python
class Solution(object):
    def areSentencesSimilarTwo(self, sentence1, sentence2, similarPairs):
        """
        :type sentence1: List[str]
        :type sentence2: List[str]
        :type similarPairs: List[List[str]]
        :rtype: bool
        """

        if len(sentence1) != len(sentence2):
            return False

        words_mapping = {}
        fa = {}
        id = 0

        def find(now):
            if fa[now] != now:
                fa[now] = find(fa[now])
            return fa[now]

        for x, y in similarPairs:
            if x not in words_mapping:
                words_mapping[x] = id
                fa[id] = id
                id += 1
            if y not in words_mapping:
                words_mapping[y] = id
                fa[id] = id
                id += 1

            x_id, y_id = words_mapping[x], words_mapping[y]

            x_fa = find(x_id)
            y_fa = find(y_id)
            if x_fa != y_fa:
                fa[x_fa] = y_fa

        for x, y in zip(sentence1, sentence2):
            if x == y:
                continue
            
            x_id, y_id = words_mapping.get(x, -1), words_mapping.get(y, -1)
            if x_id == -1 or y_id == -1:
                return False

            x_fa = find(x_id)
            y_fa = find(y_id)
            if x_fa != y_fa:
                return False
        
        return True
```

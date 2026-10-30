---
title: "243. 最短单词距离"
aliases: ["yiduobo的每日leetcode 243.最短单词距离"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/591642565"
zhihu_id: "591642565"
zhihu_title: "yiduobo的每日leetcode 243.最短单词距离"
question_id: "243"
question: "最短单词距离"
problem_url: "https://leetcode.cn/problems/shortest-word-distance/"
created: "2022-12-14T03:55:44+08:00"
updated: "2022-12-14T03:55:44+08:00"
upvotes: 0
comments: 0
---

# 243. 最短单词距离

> **[yiduobo的每日leetcode 243.最短单词距离](https://zhuanlan.zhihu.com/p/591642565) · 知乎 · 2022-12-14 · 赞同 0**
> 力扣：[243. 最短单词距离](https://leetcode.cn/problems/shortest-word-distance/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

243.最短单词距离

[力扣](https://leetcode.cn/problems/shortest-word-distance/)

题目给出一个单词数组以及其中的两个单词，要求找出这两个单词在数组中出现位置距离的最小值是多少。很明显，最终答案必然是由一前一后两个单词计算得到的，那么对于出现在后面的这个单词而言，需要知道的就是另一个单词在当前位置之前最后一次出现的位置，于是可以使用两个遍历p1和p2分别记录word1和word2最后一次出现的位置，然后一趟遍历，若当前位置上的单词属于要找的两个单词之一，那么就使用当前位置与另一个单词对应的p值更新最终答案，然后使用当前位置更新当前单词对应的p值，然后继续向后遍历。

最后附上python代码：

```python
class Solution(object):
    def shortestDistance(self, wordsDict, word1, word2):
        """
        :type wordsDict: List[str]
        :type word1: str
        :type word2: str
        :rtype: int
        """

        pos1 = pos2 = None
        res = len(wordsDict)
        for index, word in enumerate(wordsDict):
            if word == word1:
                pos1 = index
                if pos2 is not None:
                    res = min(res, pos1 - pos2)
            elif word == word2:
                pos2 = index
                if pos1 is not None:
                    res = min(res, pos2 - pos1)
        
        return res
```

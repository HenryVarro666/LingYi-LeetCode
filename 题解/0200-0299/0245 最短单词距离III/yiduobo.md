---
title: "245. 最短单词距离III"
aliases: ["yiduobo的每日leetcode 245.最短单词距离III"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/591896540"
zhihu_id: "591896540"
zhihu_title: "yiduobo的每日leetcode 245.最短单词距离III"
question_id: "245"
question: "最短单词距离III"
problem_url: "https://leetcode.cn/problems/shortest-word-distance-iii/"
created: "2022-12-14T23:40:01+08:00"
updated: "2022-12-14T23:40:01+08:00"
upvotes: 0
comments: 0
---

# 245. 最短单词距离III

> **[yiduobo的每日leetcode 245.最短单词距离III](https://zhuanlan.zhihu.com/p/591896540) · 知乎 · 2022-12-14 · 赞同 0**
> 力扣：[245. 最短单词距离III](https://leetcode.cn/problems/shortest-word-distance-iii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

245.最短单词距离III

[力扣](https://leetcode.cn/problems/shortest-word-distance-iii/)

之前243题的进阶版，额外添加了一种word1和word2相同的情况，那么在这里就可以在之前243题算法的基础上做一些特殊处理来应付这种情况就行了。对于相同的情况，可以在一开始先设置一个same_flag来表示两个单词是否相同，在接下来的遍历过程中，若出现词典中的单词等于word1，且same_flag为真的情况，就是用当前位置和word1上次出现的位置之差来更新答案即可，而对于其他情况，则保持243题的做法不变。

最后附上python代码：

```python
class Solution(object):
    def shortestWordDistance(self, wordsDict, word1, word2):
        """
        :type wordsDict: List[str]
        :type word1: str
        :type word2: str
        :rtype: int
        """

        pos1 = pos2 = None
        if word1 == word2:
            same_flag = True
        else:
            same_flag = False

        res = len(wordsDict)
        for index, word in enumerate(wordsDict):
            if word == word1:
                if same_flag:
                    if pos1 is not None:
                        res = min(res, index - pos1)
                    pos1 = index
                else:
                    pos1 = index
                    if pos2 is not None:
                        res = min(res, pos1 - pos2)
            elif word == word2:
                pos2 = index
                if pos1 is not None:
                    res = min(res, pos2 - pos1)
        
        return res
```

---
title: "748. 最短补全词"
aliases: ["yiduobo的每日leetcode 748.最短补全词"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/337736925"
zhihu_id: "337736925"
zhihu_title: "yiduobo的每日leetcode 748.最短补全词"
question_id: "748"
question: "最短补全词"
problem_url: "https://leetcode.cn/problems/shortest-completing-word/"
created: "2020-12-17T23:17:12+08:00"
updated: "2020-12-17T23:17:12+08:00"
upvotes: 0
comments: 0
---

# 748. 最短补全词

> **[yiduobo的每日leetcode 748.最短补全词](https://zhuanlan.zhihu.com/p/337736925) · 知乎 · 2020-12-17 · 赞同 0**
> 力扣：[748. 最短补全词](https://leetcode.cn/problems/shortest-completing-word/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

748.最短补全词

[力扣](https://leetcode-cn.com/problems/shortest-completing-word/)

统计牌照中每个字符出现的次数，然后遍历每个单词，统计单词中每个字符出现的次数。若满足条件，且当前单词的长度比答案的长度要短，那么就更新答案。

一个小优化是将长度的判断提前，若当前单词的长度大于等于答案的长度，那么就直接跳过该单词。

最后附上python代码：

```python
class Solution(object):
    def shortestCompletingWord(self, licensePlate, words):
        """
        :type licensePlate: str
        :type words: List[str]
        :rtype: str
        """

        target_dict = {}
        for char in licensePlate:
            if char >= 'a' and char <= 'z':
                target_dict[char] = target_dict.get(char, 0) + 1
            elif char >= 'A' and char <= 'Z':
                char = chr(ord(char) + 32)
                target_dict[char] = target_dict.get(char, 0) + 1
        
        res = None
        for word in words:
            if res is not None and len(word) >= len(res):
                continue

            word_dict = {}
            for char in word:
                word_dict[char] = word_dict.get(char, 0) + 1
            
            flag = True
            for char in target_dict:
                if word_dict.get(char, 0) < target_dict[char]:
                    flag = False
                    break
            
            if flag:
                res = word

        return res
```

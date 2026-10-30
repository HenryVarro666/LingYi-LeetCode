---
title: "2085. 统计出现过一次的公共字符串"
aliases: ["yiduobo的每日leetcode 2085.统计出现过一次的公共字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/518152136"
zhihu_id: "518152136"
zhihu_title: "yiduobo的每日leetcode 2085.统计出现过一次的公共字符串"
question_id: "2085"
question: "统计出现过一次的公共字符串"
problem_url: "https://leetcode.cn/problems/count-common-words-with-one-occurrence/"
created: "2022-05-22T12:02:39+08:00"
updated: "2022-05-22T12:02:39+08:00"
upvotes: 0
comments: 0
---

# 2085. 统计出现过一次的公共字符串

> **[yiduobo的每日leetcode 2085.统计出现过一次的公共字符串](https://zhuanlan.zhihu.com/p/518152136) · 知乎 · 2022-05-22 · 赞同 0**
> 力扣：[2085. 统计出现过一次的公共字符串](https://leetcode.cn/problems/count-common-words-with-one-occurrence/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2085.统计出现过一次的公共字符串

[力扣](https://leetcode.cn/problems/count-common-words-with-one-occurrence/)

使用哈希表统计words1和words2中每个字符串出现的次数，然后统计在word1和word2中都出现了一次的字符串的数目即可。

最后附上python代码：

```python
class Solution(object):
    def countWords(self, words1, words2):
        """
        :type words1: List[str]
        :type words2: List[str]
        :rtype: int
        """

        cnt1 = {}
        cnt2 = {}
        for word in words1:
            cnt1[word] = cnt1.get(word, 0) + 1
        for word in words2:
            cnt2[word] = cnt2.get(word, 0) + 1
        
        res = 0
        for word, cnt in cnt1.items():
            if cnt == 1 and cnt2.get(word, 0) == 1:
                res += 1
        
        return res
```

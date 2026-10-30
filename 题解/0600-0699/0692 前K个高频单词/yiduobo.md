---
title: "692. 前K个高频单词"
aliases: ["yiduobo的每日leetcode 692.前K个高频单词"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/310504273"
zhihu_id: "310504273"
zhihu_title: "yiduobo的每日leetcode 692.前K个高频单词"
question_id: "692"
question: "前K个高频单词"
problem_url: "https://leetcode.cn/problems/top-k-frequent-words/"
created: "2020-11-24T22:46:51+08:00"
updated: "2020-11-24T22:46:51+08:00"
upvotes: 0
comments: 0
---

# 692. 前K个高频单词

> **[yiduobo的每日leetcode 692.前K个高频单词](https://zhuanlan.zhihu.com/p/310504273) · 知乎 · 2020-11-24 · 赞同 0**
> 力扣：[692. 前K个高频单词](https://leetcode.cn/problems/top-k-frequent-words/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

692.前K个高频单词

[力扣](https://leetcode-cn.com/problems/top-k-frequent-words/)

题目要求O(nlogk)的时间复杂度以及O(n)的空间复杂度，看到这里的logk自然就想到了维护一个大小为k的堆。建堆的时间复杂度位O(n)，每次弹出元素的时间复杂度为O(logk)，一共需要弹出k次，因此最终的时间复杂度为O(n + klogk)。

最后附上python代码：

```python
import heapq
class Solution(object):
    def topKFrequent(self, words, k):
        """
        :type words: List[str]
        :type k: int
        :rtype: List[str]
        """

        word_dict = {}
        for word in words:
            word_dict[word] = word_dict.get(word, 0) + 1
        
        heap = [[-freq, word] for word, freq in word_dict.items()]
        heapq.heapify(heap)
        
        return [heapq.heappop(heap)[1] for index in range(k)]
```

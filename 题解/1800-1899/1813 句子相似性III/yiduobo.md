---
title: "1813. 句子相似性III"
aliases: ["yiduobo的每日leetcode 1813.句子相似性III"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/465120699"
zhihu_id: "465120699"
zhihu_title: "yiduobo的每日leetcode 1813.句子相似性III"
question_id: "1813"
question: "句子相似性III"
problem_url: "https://leetcode.cn/problems/sentence-similarity-iii/"
created: "2022-02-08T23:06:17+08:00"
updated: "2022-02-08T23:06:17+08:00"
upvotes: 0
comments: 0
---

# 1813. 句子相似性III

> **[yiduobo的每日leetcode 1813.句子相似性III](https://zhuanlan.zhihu.com/p/465120699) · 知乎 · 2022-02-08 · 赞同 0**
> 力扣：[1813. 句子相似性III](https://leetcode.cn/problems/sentence-similarity-iii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1813.句子相似性III

[力扣](https://leetcode-cn.com/problems/sentence-similarity-iii/)

题目中的相似性定义为在短句中插入一个句子后能否让其变得与长句一样，换言之，就是问能否用长句的某个前缀拼上某个后缀得到短句。于是可以先从前向后一趟扫描，记录前缀匹配的长度，然后再从后向前一趟扫描，记录后缀匹配的长度。若这两个长度之和大于等于短句的长度，那么说明句子相似。

最后附上python代码：

```python
class Solution(object):
    def areSentencesSimilar(self, sentence1, sentence2):
        """
        :type sentence1: str
        :type sentence2: str
        :rtype: bool
        """

        word_list1 = sentence1.split(' ')
        word_list2 = sentence2.split(' ')
        if len(word_list1) < len(word_list2):
            origin, target = word_list2, word_list1
        else:
            origin, target = word_list1, word_list2
        
        m = len(target)
        left = m
        for index in range(m):
            if origin[index] != target[index]:
                left = index
                break
        
        if left == m:
            return True

        n = len(origin)
        for index in range(m - 1, left - 1, -1):
            if origin[n - m + index] != target[index]:
                return False

        return True
```

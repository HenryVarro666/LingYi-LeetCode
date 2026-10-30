---
title: "1078. Bigram分词"
aliases: ["yiduobo的每日leetcode 1078.Bigram分词"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/372797920"
zhihu_id: "372797920"
zhihu_title: "yiduobo的每日leetcode 1078.Bigram分词"
question_id: "1078"
question: "Bigram分词"
problem_url: "https://leetcode.cn/problems/occurrences-after-bigram/"
created: "2021-05-16T22:13:50+08:00"
updated: "2021-05-16T22:13:50+08:00"
upvotes: 0
comments: 0
---

# 1078. Bigram分词

> **[yiduobo的每日leetcode 1078.Bigram分词](https://zhuanlan.zhihu.com/p/372797920) · 知乎 · 2021-05-16 · 赞同 0**
> 力扣：[1078. Bigram分词](https://leetcode.cn/problems/occurrences-after-bigram/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1078.Bigram分词

[力扣](https://leetcode-cn.com/problems/occurrences-after-bigram/)

先将text按逗号分割成list，然后一趟扫描，对于当前的index，若list[index]等于first，且list[index + 1]等于second，那么就将list[index + 2]加入到答案当中。

另外，本题如果是ngram分词的话，则可以利用类似kmp的做法来处理，即将每个单词看做一个字母的话，就是字符串匹配问题了。

最后附上python代码：

```python
class Solution(object):
    def findOcurrences(self, text, first, second):
        """
        :type text: str
        :type first: str
        :type second: str
        :rtype: List[str]
        """

        word_list = text.split(' ')
        res = []
        for index in range(len(word_list) - 2):
            if word_list[index] == first and word_list[index + 1] == second:
                res.append(word_list[index + 2])
        
        return res
```

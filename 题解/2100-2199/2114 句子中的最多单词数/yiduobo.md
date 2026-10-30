---
title: "2114. 句子中的最多单词数"
aliases: ["yiduobo的每日leetcode 2114.句子中的最多单词数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/524064537"
zhihu_id: "524064537"
zhihu_title: "yiduobo的每日leetcode 2114.句子中的最多单词数"
question_id: "2114"
question: "句子中的最多单词数"
problem_url: "https://leetcode.cn/problems/maximum-number-of-words-found-in-sentences/"
difficulty: "Easy"
created: "2022-06-04T00:05:30+08:00"
updated: "2022-06-04T00:05:30+08:00"
upvotes: 0
comments: 0
---

# 2114. 句子中的最多单词数

> **[yiduobo的每日leetcode 2114.句子中的最多单词数](https://zhuanlan.zhihu.com/p/524064537) · 知乎 · 2022-06-04 · 赞同 0**
> 力扣：[2114. 句子中的最多单词数](https://leetcode.cn/problems/maximum-number-of-words-found-in-sentences/) · Easy · 灵茶山艾府：[统计空格个数 +1 即为单词个数](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2114.句子中的最多单词数

[力扣](https://leetcode.cn/problems/maximum-number-of-words-found-in-sentences/)

由于句子中没有多余的空格，那么可以将问题转化为统计每个句子中空格的数目。若某个句子中空格的数目为cnt，那么句子中单词的数目就是cnt + 1。一趟遍历统计，取其中的最大值作为答案即可。

最后附上python代码：

```python
class Solution(object):
    def mostWordsFound(self, sentences):
        """
        :type sentences: List[str]
        :rtype: int
        """

        res = 0
        for sentence in sentences:
            cnt = 1
            for char in sentence:
                if char == ' ':
                    cnt += 1
            res = max(res, cnt)

        return res
```

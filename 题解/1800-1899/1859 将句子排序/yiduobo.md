---
title: "1859. 将句子排序"
aliases: ["yiduobo的每日leetcode 1859.将句子排序"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/472626969"
zhihu_id: "472626969"
zhihu_title: "yiduobo的每日leetcode 1859.将句子排序"
question_id: "1859"
question: "将句子排序"
problem_url: "https://leetcode.cn/problems/sorting-the-sentence/"
difficulty: "Easy"
created: "2022-02-25T23:06:24+08:00"
updated: "2022-02-25T23:06:25+08:00"
upvotes: 0
comments: 0
---

# 1859. 将句子排序

> **[yiduobo的每日leetcode 1859.将句子排序](https://zhuanlan.zhihu.com/p/472626969) · 知乎 · 2022-02-25 · 赞同 0**
> 力扣：[1859. 将句子排序](https://leetcode.cn/problems/sorting-the-sentence/) · Easy · 灵茶山艾府：[简洁写法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1859.将句子排序

[力扣](https://leetcode-cn.com/problems/sorting-the-sentence/)

先按照空格将句子中的单词分离出来，由于最多只有9个单词，因此每个单词仅有最后一位表示其在句子中的下标。根据这一位将单词对号入座放置到答案数组中，然后用空格按顺序将答案数组中的单词连接起来并返回即可。

最后附上python代码：

```python
class Solution(object):
    def sortSentence(self, s):
        """
        :type s: str
        :rtype: str
        """

        words = s.split(' ')
        res = [''] * len(words)
        for word in words:
            res[int(word[-1]) - 1] = word[:-1]
        
        return ' '.join(res)
```

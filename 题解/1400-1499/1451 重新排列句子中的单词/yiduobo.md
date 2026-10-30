---
title: "1451. 重新排列句子中的单词"
aliases: ["yiduobo的每日leetcode 1451.重新排列句子中的单词"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/411897585"
zhihu_id: "411897585"
zhihu_title: "yiduobo的每日leetcode 1451.重新排列句子中的单词"
question_id: "1451"
question: "重新排列句子中的单词"
problem_url: "https://leetcode.cn/problems/rearrange-words-in-a-sentence/"
difficulty: "Medium"
created: "2021-09-18T22:49:52+08:00"
updated: "2021-09-18T22:49:52+08:00"
upvotes: 0
comments: 0
---

# 1451. 重新排列句子中的单词

> **[yiduobo的每日leetcode 1451.重新排列句子中的单词](https://zhuanlan.zhihu.com/p/411897585) · 知乎 · 2021-09-18 · 赞同 0**
> 力扣：[1451. 重新排列句子中的单词](https://leetcode.cn/problems/rearrange-words-in-a-sentence/) · Medium · 灵茶山艾府：[Golang 稳定排序 - 5行代码](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1451.重新排列句子中的单词

[力扣](https://leetcode-cn.com/problems/rearrange-words-in-a-sentence/)

比较基础的题目。

首先按空格分离出各个单词，并将第0个单词的首字母从大写改为小写。

接下来将各个单词以长度为第一关键字，原始位置为第二关键字进行排序。

最后将各个单词拼起来，并将最终答案的首字母从小写改为大写。

最后附上python代码：

```python
class Solution(object):
    def arrangeWords(self, text):
        """
        :type text: str
        :rtype: str
        """

        words = text.split(' ')
        words[0] = chr(ord(words[0][0]) + 32) + words[0][1:]

        sorted_index = sorted(range(len(words)), key=lambda d:(len(words[d]), d))
        res = ' '.join([words[index] for index in sorted_index])
        return chr(ord(res[0]) - 32) + res[1:]
```

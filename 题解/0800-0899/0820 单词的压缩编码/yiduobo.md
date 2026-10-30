---
title: "820. 单词的压缩编码"
aliases: ["yiduobo的每日leetcode 820.单词的压缩编码"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/343857949"
zhihu_id: "343857949"
zhihu_title: "yiduobo的每日leetcode 820.单词的压缩编码"
question_id: "820"
question: "单词的压缩编码"
problem_url: "https://leetcode.cn/problems/short-encoding-of-words/"
created: "2021-01-17T19:10:25+08:00"
updated: "2021-01-17T19:10:25+08:00"
upvotes: 0
comments: 0
---

# 820. 单词的压缩编码

> **[yiduobo的每日leetcode 820.单词的压缩编码](https://zhuanlan.zhihu.com/p/343857949) · 知乎 · 2021-01-17 · 赞同 0**
> 力扣：[820. 单词的压缩编码](https://leetcode.cn/problems/short-encoding-of-words/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

820.单词的压缩编码

[力扣](https://leetcode-cn.com/problems/short-encoding-of-words/)

对于两个单词，若其中一个是另一个的后缀，那么就可以只保留较长的那个单词，否则两个都需要保留。关于判断后缀，则可以使用将单词倒转，将其转化为前缀匹配来做。前缀匹配则可以使用trie树或者哈希表。

我在这里采用的是哈希表。由于只可能是较短的单词成为较长单词的后缀，因此可以将单词按长度从长到短进行排序，然后逐个遍历。对于当前的单词，若该单词在哈希表中，那么就跳过，否则将答案加上当前单词长度加一，然后从末尾往前遍历单词中的每个字符，将单词的所有后缀加入到哈希表中。

最后附上python代码：

```python
class Solution(object):
    def minimumLengthEncoding(self, words):
        """
        :type words: List[str]
        :rtype: int
        """

        words = sorted(words, key=lambda d:len(d), reverse=True)
        suffix_set = set()
        res = 0
        for word in words:
            if word not in suffix_set:
                res += len(word) + 1
                tmp = ''
                for char in word[::-1]:
                    tmp = char + tmp
                    suffix_set.add(tmp)
        
        return res
```

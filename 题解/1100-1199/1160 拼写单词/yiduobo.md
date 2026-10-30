---
title: "1160. 拼写单词"
aliases: ["yiduobo的每日leetcode 1160.拼写单词"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/378435640"
zhihu_id: "378435640"
zhihu_title: "yiduobo的每日leetcode 1160.拼写单词"
question_id: "1160"
question: "拼写单词"
problem_url: "https://leetcode.cn/problems/find-words-that-can-be-formed-by-characters/"
created: "2021-06-07T00:15:14+08:00"
updated: "2021-06-07T00:15:14+08:00"
upvotes: 0
comments: 0
---

# 1160. 拼写单词

> **[yiduobo的每日leetcode 1160.拼写单词](https://zhuanlan.zhihu.com/p/378435640) · 知乎 · 2021-06-07 · 赞同 0**
> 力扣：[1160. 拼写单词](https://leetcode.cn/problems/find-words-that-can-be-formed-by-characters/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1160.拼写单词

[力扣](https://leetcode-cn.com/problems/find-words-that-can-be-formed-by-characters/)

分别统计出每个单词以及chars中每个字母出现的次数，然后一趟遍历，若当前的单词中所有字母出现的次数都小于等于chars中对应字母出现的次数，那么说明掌握了当前的单词，将其长度累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def countCharacters(self, words, chars):
        """
        :type words: List[str]
        :type chars: str
        :rtype: int
        """

        char_dict = {}
        for char in chars:
            char_dict[char] = char_dict.get(char, 0) + 1
        
        res = 0
        for word in words:
            tmp_dict = {}
            for char in word:
                tmp_dict[char] = tmp_dict.get(char, 0) + 1
            flag = True
            for char in tmp_dict:
                if tmp_dict[char] > char_dict.get(char, 0):
                    flag = False
                    break
            
            if flag:
                res += len(word)
        
        return res
```

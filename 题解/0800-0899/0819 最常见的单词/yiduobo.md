---
title: "819. 最常见的单词"
aliases: ["yiduobo的每日leetcode 819.最常见的单词"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/343840997"
zhihu_id: "343840997"
zhihu_title: "yiduobo的每日leetcode 819.最常见的单词"
question_id: "819"
question: "最常见的单词"
problem_url: "https://leetcode.cn/problems/most-common-word/"
created: "2021-01-16T19:19:03+08:00"
updated: "2021-01-16T19:19:03+08:00"
upvotes: 0
comments: 0
---

# 819. 最常见的单词

> **[yiduobo的每日leetcode 819.最常见的单词](https://zhuanlan.zhihu.com/p/343840997) · 知乎 · 2021-01-16 · 赞同 0**
> 力扣：[819. 最常见的单词](https://leetcode.cn/problems/most-common-word/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

819.最常见的单词

[力扣](https://leetcode-cn.com/problems/most-common-word/)

比较基础的题目，将每个单词转换成小写，若其未出现在banned中那么就统计出现次数，选择出现最多的单词即可。

最后附上python代码：

```python
class Solution(object):
    def mostCommonWord(self, paragraph, banned):
        """
        :type paragraph: str
        :type banned: List[str]
        :rtype: str
        """

        ban_set = set(banned)
        count_dict = {}
        now = ''
        max_cnt = 0
        max_word = None
        for char in paragraph + ' ':
            if char >= 'a' and char <= 'z':
                now += char
            elif char >= 'A' and char <= 'Z':
                now += chr(ord(char) + 32)
            else:
                if now != '' and now not in banned:
                    count_dict[now] = count_dict.get(now, 0) + 1
                    if count_dict[now] > max_cnt:
                        max_cnt = count_dict[now]
                        max_word = now
                now = ''

        return max_word
```

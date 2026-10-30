---
title: "320. 列举单词的全部缩写"
aliases: ["yiduobo的每日leetcode 320.列举单词的全部缩写"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/596116862"
zhihu_id: "596116862"
zhihu_title: "yiduobo的每日leetcode 320.列举单词的全部缩写"
question_id: "320"
question: "列举单词的全部缩写"
problem_url: "https://leetcode.cn/problems/generalized-abbreviation/"
created: "2023-01-03T01:27:02+08:00"
updated: "2023-01-03T01:27:02+08:00"
upvotes: 0
comments: 0
---

# 320. 列举单词的全部缩写

> **[yiduobo的每日leetcode 320.列举单词的全部缩写](https://zhuanlan.zhihu.com/p/596116862) · 知乎 · 2023-01-03 · 赞同 0**
> 力扣：[320. 列举单词的全部缩写](https://leetcode.cn/problems/generalized-abbreviation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

320.列举单词的全部缩写

[力扣](https://leetcode.cn/problems/generalized-abbreviation/)

题目的数据规模非常小，因此可以直接使用暴力dfs。对于当前这一轮dfs，不妨设是第level轮，当前构造的字符串now，以及正在被转化为数字缩写的字符数目len。对于当前字符s[level]，有两种处理方法：

1、将其转化为缩写，那么接下来就应该向后计算dfs(level + 1, now, len + 1)

2、保持该字符不变。若此时的len大于0，那么就应该先将之前转化为缩写的len个字符加入到now中，也就是在now中加入str(len)。接下来将s[level]加入到now中，然后继续向后计算dfs(level + 1, now, 0)

当level等于n时，则说明找到了一种合法的缩写方式，此时需要将now加入到答案数组中。需要注意的是，若此时len大于0，那么还需要在now的末尾加上str(len)。

最后附上python代码：

```python
class Solution(object):
    def generateAbbreviations(self, word):
        """
        :type word: str
        :rtype: List[str]
        """

        res = []
        n = len(word)

        def dfs(level, now, len):
            if level == n:
                if len > 0:
                    tmp = str(len)
                else:
                    tmp = ''
                res.append(''.join(now) + tmp)
            
                return

            dfs(level + 1, now, len + 1)
            
            if len > 0:
                now.append(str(len))
                now.append(word[level])
                dfs(level + 1, now, 0)
                now.pop()
                now.pop()
            else:
                now.append(word[level])
                dfs(level + 1, now, 0)
                now.pop()
        
        dfs(0, [], 0)

        return res
```

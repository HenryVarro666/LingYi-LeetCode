---
title: "3838. 带权单词映射"
aliases: ["yiduobo的每日leetcode 3838.带权单词映射"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2010126556358546880"
zhihu_id: "2010126556358546880"
zhihu_title: "yiduobo的每日leetcode 3838.带权单词映射"
question_id: "3838"
question: "带权单词映射"
problem_url: "https://leetcode.cn/problems/weighted-word-mapping/"
difficulty: "Easy"
created: "2026-02-25T23:04:39+08:00"
updated: "2026-02-25T23:04:43+08:00"
upvotes: 0
comments: 0
---

# 3838. 带权单词映射

> **[yiduobo的每日leetcode 3838.带权单词映射](https://zhuanlan.zhihu.com/p/2010126556358546880) · 知乎 · 2026-02-25 · 赞同 0**
> 力扣：[3838. 带权单词映射](https://leetcode.cn/problems/weighted-word-mapping/) · Easy · 灵茶山艾府：[按题意模拟（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3838.带权单词映射

<https://leetcode.cn/problems/weighted-word-mapping/description/>

题目给出一个字符串数组words，其中每个字符串表示一个由小写英文字母组成的单词。

另外给出一个长度为26的整数数组weights，其中weights[index]表示第index个小写英文字母的权重。单词的权重定义为其中所有字符的权重之和。

对于每个单词，现在要求将其权重对26取模，然后按照字母倒序映射到小写英文字母，也就是0->'z'，1->'y'，..., 25->'a'。

返回words中每个单词经过上述操作后得到的字符连接而成的字符串。

按照题目要求遍历所有单词，对于当前遍历到的单词w，先遍历其中每个字符c，通过c的ascii码减去字母'a'的ascii码，来定位到c在weights中的下标，然后将其对应的权重累加到w的总权值s中。计算完成后，将s对26取模，接下来令r \= 25 - s，理由是s的倒序映射，就相当于r的正序映射。最后，将r加上字母'a'的ascii码，就得到了w结果操作后得到字符的ascii码，将其转换为字符添加到答案末尾即可。

最后附上python代码：

```python
class Solution(object):
    def mapWordWeights(self, words, weights):
        """
        :type words: List[str]
        :type weights: List[int]
        :rtype: str
        """
        
        res = []
        for w in words:
            s = 0
            for c in w:
                s += weights[ord(c) - 97]
            s %= 26

            r = 25 - s
            res.append(chr(r + 97))
        
        return ''.join(res)
```

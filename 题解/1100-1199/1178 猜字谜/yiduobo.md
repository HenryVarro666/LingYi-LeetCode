---
title: "1178. 猜字谜"
aliases: ["yiduobo的每日leetcode 1178.猜字谜"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/380051616"
zhihu_id: "380051616"
zhihu_title: "yiduobo的每日leetcode 1178.猜字谜"
question_id: "1178"
question: "猜字谜"
problem_url: "https://leetcode.cn/problems/number-of-valid-words-for-each-puzzle/"
created: "2021-06-11T23:43:10+08:00"
updated: "2021-06-11T23:43:10+08:00"
upvotes: 0
comments: 0
---

# 1178. 猜字谜

> **[yiduobo的每日leetcode 1178.猜字谜](https://zhuanlan.zhihu.com/p/380051616) · 知乎 · 2021-06-11 · 赞同 0**
> 力扣：[1178. 猜字谜](https://leetcode.cn/problems/number-of-valid-words-for-each-puzzle/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1178.猜字谜

[力扣](https://leetcode-cn.com/problems/number-of-valid-words-for-each-puzzle/)

由于题目保证word和puzzle中都是小写字符，那么我们可以对每个word和puzzle进行二进制编码，具体来说就是先将a到z对应到0到25，然后对于当前字符串s，我们构造一个长度为26的二进制串，其中第k为表示s中是否具有k对应的小写字母。

值得注意的是，由于题目保证了puzzle的长度为7，而word的每一个字母都要能在puzzle中找到时word才可能成为其谜底，因此对于具有超过7个不同字符的word我们都可以直接忽略。换言之，这里的所有word和puzzle都可以编码成最多只有7个1的，长度为26位的二进制串。

完成对word的编码后，我们可以使用一个dict储存每种编码出现的次数，然后接下来开始枚举puzzle。

对于一个puzzle而言，其答案候选集中的字符串必须以puzzle[0]开头，因此其二进制表示中必然有1 \<\< (ord(puzzle[0]) - 97)这一项。而对于后续的puzzle[1:]中的所有字符，则都是可有可无的，那么我们需要遍历puzzle[1:]，对于当前处理的字符，若不将其加入答案候选集，那么答案候选集保持不变；若将其加入，则需要将答案候选集中的所有编码都与当前字符的编码进行按位或。由于是可有可无的，那么我们只需将后面这种情况新得到的答案候选集合并到老的答案候选集中即可。

由于puzzle[1:]只有6个字符，因此实际上最多只有32种不同的情况。

得到答案候选集之后，我们只需要看看其中有多少个编码出现在word编码的dict中即可。

最后附上python代码：

```python
class Solution(object):
    def findNumOfValidWords(self, words, puzzles):
        """
        :type words: List[str]
        :type puzzles: List[str]
        :rtype: List[int]
        """

        word_dict = {}
        for word in words:
            cnt = 0
            num = 0
            for char in word:
                p = 1 << (ord(char) - 97)
                if num & p:
                    continue
                cnt += 1
                num |= p
                if cnt > 7:
                    break
            
            if cnt <= 7:
                word_dict[num] = word_dict.get(num, 0) + 1

        res = []
        for puzzle in puzzles:
            candidate = set([1 << (ord(puzzle[0]) - 97)])
            for char in puzzle[1:]:
                candidate.update([x | (1 << ord(char) - 97) for x in candidate])
            res.append(sum([word_dict.get(x, 0) for x in candidate]))

        return res
```

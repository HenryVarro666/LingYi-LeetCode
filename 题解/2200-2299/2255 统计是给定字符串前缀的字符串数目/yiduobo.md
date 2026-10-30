---
title: "2255. 统计是给定字符串前缀的字符串数目"
aliases: ["yiduobo的每日leetcode 2255.统计是给定字符串前缀的字符串数目"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/547395172"
zhihu_id: "547395172"
zhihu_title: "yiduobo的每日leetcode 2255.统计是给定字符串前缀的字符串数目"
question_id: "2255"
question: "统计是给定字符串前缀的字符串数目"
problem_url: "https://leetcode.cn/problems/count-prefixes-of-a-given-string/"
difficulty: "Easy"
created: "2022-07-28T23:48:18+08:00"
updated: "2022-07-28T23:48:18+08:00"
upvotes: 0
comments: 0
---

# 2255. 统计是给定字符串前缀的字符串数目

> **[yiduobo的每日leetcode 2255.统计是给定字符串前缀的字符串数目](https://zhuanlan.zhihu.com/p/547395172) · 知乎 · 2022-07-28 · 赞同 0**
> 力扣：[2255. 统计是给定字符串前缀的字符串数目](https://leetcode.cn/problems/count-prefixes-of-a-given-string/) · Easy · 灵茶山艾府：[库函数写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2255.统计是给定字符串前缀的字符串数目

[力扣](https://leetcode.cn/problems/count-prefixes-of-a-given-string/)

由于题目中字符串的长度很短，同时words中单词的数量也很少，因此可以使用朴素算法，遍历words中的每个单词然后判断其是否为s的前缀。

除此之外，前缀匹配相关的问题也可以尝试使用trie树来解决。对于本题，可以先遍历words中的单词，并将这些单词加入到trie树中，同时在每个单词结尾的节点做好标记。接下来依照s在trie树中行走，统计路径上有标记的节点数目，即为最终答案。

最后附上python代码，我使用的是朴素算法：

```python
class Solution(object):
    def countPrefixes(self, words, s):
        """
        :type words: List[str]
        :type s: str
        :rtype: int
        """

        res = 0
        for word in words:
            if len(word) > len(s):
                continue

            flag = True
            for index, char in enumerate(word):
                if char != s[index]:
                    flag = False
                    break
            
            if flag:
                res += 1
        
        return res
```

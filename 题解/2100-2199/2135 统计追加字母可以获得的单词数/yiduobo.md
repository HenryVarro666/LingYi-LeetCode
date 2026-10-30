---
title: "2135. 统计追加字母可以获得的单词数"
aliases: ["yiduobo的每日leetcode 2135.统计追加字母可以获得的单词数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/hash-table", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/527752412"
zhihu_id: "527752412"
zhihu_title: "yiduobo的每日leetcode 2135.统计追加字母可以获得的单词数"
question_id: "2135"
question: "统计追加字母可以获得的单词数"
problem_url: "https://leetcode.cn/problems/count-words-obtained-after-adding-a-letter/"
difficulty: "Medium"
created: "2022-06-12T16:13:42+08:00"
updated: "2022-06-12T16:13:42+08:00"
upvotes: 0
comments: 0
---

# 2135. 统计追加字母可以获得的单词数

> **[yiduobo的每日leetcode 2135.统计追加字母可以获得的单词数](https://zhuanlan.zhihu.com/p/527752412) · 知乎 · 2022-06-12 · 赞同 0**
> 力扣：[2135. 统计追加字母可以获得的单词数](https://leetcode.cn/problems/count-words-obtained-after-adding-a-letter/) · Medium · 灵茶山艾府：[逆向思维 + 位运算 + 哈希表](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2135.统计追加字母可以获得的单词数

[力扣](https://leetcode.cn/problems/count-words-obtained-after-adding-a-letter/)

题目中的重排操作可以任意排列单词中的字母，且每个字母只出现一次，那么对于targetWords中的某个单词而言，只要其包含的字母集比startWords中某个单词包含的字母集恰好多出一个字母，就可以从startWords中的这个单词完成转换。

由于题目中每个单词都由小写字母组成，那么就可以使用26位的二进制数表示当前单词中包含了哪些字母，于是现在就得到了一种做法：

1、遍历startWords中的每个单词，计算其二进制表示，并用一个集合num_set将这些数收集起来

2、遍历targetWords中的每个单词，对于当前单词，同样先计算出其二进制表示，记为now。

接下来遍历当前单词中的每个字母，并判断在now中去除这个字母对应的二进制值之后，对应的结果是否出现在num_set中。若是，说明当前单词可以被转换得到，此时应该将答案加上1，然后考察下一个单词。若尝试去除所有字母后的结果都没有出现在num_set，那么说明当前单词无法被转换得到。

最后附上python代码：

```python
class Solution(object):
    def wordCount(self, startWords, targetWords):
        """
        :type startWords: List[str]
        :type targetWords: List[str]
        :rtype: int
        """

        num_set = set()
        for word in startWords:
            now = 0
            for char in word:
                now += (1 << (ord(char) - 97))
            num_set.add(now)
        
        res = 0
        for word in targetWords:
            now = 0
            for char in word:
                now += (1 << (ord(char) - 97))
            for char in word:
                if (now ^ (1 << (ord(char) - 97))) in num_set:
                    res += 1
                    break
        
        return res
```

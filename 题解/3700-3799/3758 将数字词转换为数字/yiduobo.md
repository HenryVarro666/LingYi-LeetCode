---
title: "3758. 将数字词转换为数字"
aliases: ["yiduobo的每日leetcode 3758.将数字词转换为数字"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/字符串", "题单/字符串/七-AC-自动机"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1976796937123563167"
zhihu_id: "1976796937123563167"
zhihu_title: "yiduobo的每日leetcode 3758.将数字词转换为数字"
question_id: "3758"
question: "将数字词转换为数字"
problem_url: "https://leetcode.cn/problems/convert-number-words-to-digits/"
difficulty: "Medium"
created: "2025-11-27T00:06:38+08:00"
updated: "2025-11-27T00:06:41+08:00"
upvotes: 2
comments: 0
---

# 3758. 将数字词转换为数字

> **[yiduobo的每日leetcode 3758.将数字词转换为数字](https://zhuanlan.zhihu.com/p/1976796937123563167) · 知乎 · 2025-11-27 · 赞同 2**
> 力扣：[3758. 将数字词转换为数字](https://leetcode.cn/problems/convert-number-words-to-digits/) · Medium · 灵茶山艾府：[暴力枚举](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3758.将数字词转换为数字

[3758. 将数字词转换为数字 - 力扣（LeetCode）](https://leetcode.cn/problems/convert-number-words-to-digits/description/)

题目给出一个由小写英文字母组成的字符串s，s中可能包含数字0到9的有效连续英文单词，且s中不包含空格。

现在要求按顺序提取s中每个有效的数字词，并将其转换为数字，生成一个数字字符串。

更具体的说，就是要求从左往右解析s，对于每个位置，若当前位置有一个有效的数字词，则将其对应的数字添加到答案中，同时将位置向后移动该单词的长度；反之，则跳过恰好一个字符然后继续解析。

一对多的字符串匹配，通常可以使用trie图来处理，不过本题中这些多的长度都很短，最长的3、7、8对应的three、seven、eight长度也仅为5，另一方面也没有多少值得复用的前缀，因此在这里直接暴力匹配就行了。

建立一个字符串到数字的哈希表nums，接下来使用一个变量p从s的头部开始向后移动。对于当前的p，遍历nums中的所有单词w，若从p开始往后数len(w)个字符没有超出s的边界，且从s[p]开始的len(w)个字符刚好构成了w，那么就将w对应的数字添加到答案中，然后将p移动到p + len(w)并开始下一轮的检测。若没有找到可用的w，则将p向后移动一位然后开始下一轮的检测。重复此过程直到p来到s的末尾为止。

最后附上python代码：

```python
class Solution(object):
    def convertNumber(self, s):
        """
        :type s: str
        :rtype: str
        """
        
        nums = {"one": "1",
                "two": "2",
                "three": "3",
                "four": "4",
                "five": "5",
                "six": "6",
                "seven": "7",
                "eight": "8",
                "nine": "9",
                "zero": "0"
        }

        res = []
        p = 0
        while p < len(s):
            for w, v in nums.items():
                if p + len(w) <= len(s) and s[p: p + len(w)] == w:
                    res.append(v)
                    p += len(w) - 1
                    break

            p += 1
        
        return ''.join(res)
```

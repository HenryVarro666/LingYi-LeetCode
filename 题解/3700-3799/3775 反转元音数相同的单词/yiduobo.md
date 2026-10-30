---
title: "3775. 反转元音数相同的单词"
aliases: ["yiduobo的每日leetcode 3775.反转元音数相同的单词"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/simulation", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1984013864736686119"
zhihu_id: "1984013864736686119"
zhihu_title: "yiduobo的每日leetcode 3775.反转元音数相同的单词"
question_id: "3775"
question: "反转元音数相同的单词"
problem_url: "https://leetcode.cn/problems/reverse-words-with-same-vowel-count/"
difficulty: "Medium"
rating: 1392
created: "2025-12-15T21:39:49+08:00"
updated: "2025-12-15T21:39:49+08:00"
upvotes: 2
comments: 0
---

# 3775. 反转元音数相同的单词

> **[yiduobo的每日leetcode 3775.反转元音数相同的单词](https://zhuanlan.zhihu.com/p/1984013864736686119) · 知乎 · 2025-12-15 · 赞同 2**
> 力扣：[3775. 反转元音数相同的单词](https://leetcode.cn/problems/reverse-words-with-same-vowel-count/) · Medium · 灵茶山艾府：[库函数写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3775.反转元音数相同的单词

[3775. 反转元音数相同的单词 - 力扣（LeetCode）](https://leetcode.cn/problems/reverse-words-with-same-vowel-count/description/)

题目给出一个字符串s，由小写英文单词组成，且每个单词之间由一个空格隔开。

现在要求先计算其中第一个单词中元音字母的数量，然后对于后续的每个单词，若该单词的元音字母数量与第一个单词相同，则将其反转，否则保持不变。

要求返回处理后的结果字符串。

直接按照题目要求模拟计算即可。先对字符串进行split操作，分离出各个单词。接下来遍历第一个单词，统计其中元音字母的数量v。得到v之后，再逐个遍历后续所有的单词，并统计每个单词中元音字母的数量。若其等于v，则将其反转后加入答案中，否则将其直接加入答案中。

最后附上python代码：

```python
class Solution(object):
    def reverseWords(self, s):
        """
        :type s: str
        :rtype: str
        """
        
        words = s.split()
        res = [words[0]]

        vowel = set(['a', 'e', 'i', 'o', 'u'])

        def count(w):
            v = 0
            for c in w:
                if c in vowel:
                    v += 1
            return v

        cnt = count(words[0])

        for w in words[1:]:
            if count(w) == cnt:
                res.append(w[::-1])
            else:
                res.append(w)
        
        return ' '.join(res)
```

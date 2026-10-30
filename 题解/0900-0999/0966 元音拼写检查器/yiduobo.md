---
title: "966. 元音拼写检查器"
aliases: ["yiduobo的每日leetcode 966.元音拼写检查器"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/361721769"
zhihu_id: "361721769"
zhihu_title: "yiduobo的每日leetcode 966.元音拼写检查器"
question_id: "966"
question: "元音拼写检查器"
problem_url: "https://leetcode.cn/problems/vowel-spellchecker/"
difficulty: "Medium"
created: "2021-04-01T22:59:46+08:00"
updated: "2021-04-01T22:59:46+08:00"
upvotes: 0
comments: 0
---

# 966. 元音拼写检查器

> **[yiduobo的每日leetcode 966.元音拼写检查器](https://zhuanlan.zhihu.com/p/361721769) · 知乎 · 2021-04-01 · 赞同 0**
> 力扣：[966. 元音拼写检查器](https://leetcode.cn/problems/vowel-spellchecker/) · Medium · 灵茶山艾府：[三个哈希表（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

966.元音拼写检查器

[力扣](https://leetcode-cn.com/problems/vowel-spellchecker/)

按照题目要求，匹配的优先级有三级，分别是原始单词，大小写匹配的单词、元音替换且大小写匹配的单词。

首先，对于原始单词，直接使用word_dict来记录wordlist并判断即可。

接下来，对于大小写匹配的单词，我们可以从wordlist头部开始往后遍历，对于当前处理到的单词word，我们可以将word中的所有字符变为小写然后使用low_case_dict记录下来。在判断时，若某个单词不在原始单词的word_dict中，且将其转化为全小写字符之后可以在low_case_dict中找到，那么说明该单词能通过大小写匹配上low_case_dict中对应的单词。

最后，对于元音替换且大小写匹配的单词，注意到这里单词的长度不超过7，那么我可以先找出word中元音出现的位置，然后使用二进制编码进行状态压缩得到元音字母位置的状态表示state，同时收集剩下的辅音字母形成rest_word，那么这样一个二元组(state, rest_word)就可以表示一类可以通过元音替换且大小写匹配的单词。同样使用一个spell_dict记录下来。

预处理完成后，遍历queries中的所有单词：

1、首先在word_dict中寻找当前单词

2、接下来将当前单词所有字符变为小写，然后在low_case_dict中寻找小写后的单词

3、最后将当前单词所有元音字母的位置通过二进制计算出对应的状态并收集剩下的辅音字母，然后在spell_dict中寻找二元组

最后附上python代码：

```python
class Solution(object):
    def spellchecker(self, wordlist, queries):
        """
        :type wordlist: List[str]
        :type queries: List[str]
        :rtype: List[str]
        """

        word_dict = {}
        for index, word in enumerate(wordlist):
            word_dict[word] = index
        
        low_case_dict = {}
        for index, word in enumerate(wordlist):
            low_case_word = ''.join([x if ord(x) >= 97 else chr(ord(x) + 32) for x in word])
            if low_case_word not in low_case_dict:
                low_case_dict[low_case_word] = index
        
        spell_dict = {}
        for index, word in enumerate(wordlist):
            rest_word = ''
            spell_state = 0
            for p, char in enumerate(word):
                if ord(char) < 97:
                    char = chr(ord(char) + 32)

                if char in ('a', 'e', 'i', 'o', 'u'):
                    spell_state += (1 << p)
                else:
                    rest_word += char
            
            if (rest_word, spell_state) not in spell_dict:
                spell_dict[(rest_word, spell_state)] = index
        
        res = []
        for word in queries:
            if word in word_dict:
                res.append(wordlist[word_dict[word]])
            else:
                low_case_word = ''.join([x if ord(x) >= 97 else chr(ord(x) + 32) for x in word])
                if low_case_word in low_case_dict:
                    res.append(wordlist[low_case_dict[low_case_word]])
                else:
                    rest_word = ''
                    spell_state = 0
                    for p, char in enumerate(word):
                        if ord(char) < 97:
                            char = chr(ord(char) + 32)

                        if char in ('a', 'e', 'i', 'o', 'u'):
                            spell_state += (1 << p)
                        else:
                            rest_word += char
                    
                    if (rest_word, spell_state) in spell_dict:
                        res.append(wordlist[spell_dict[(rest_word, spell_state)]])
                    else:
                        res.append('')
        
        return res
```

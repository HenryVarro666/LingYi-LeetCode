---
title: "527. 单词缩写"
aliases: ["yiduobo的每日leetcode 527.单词缩写"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/600544222"
zhihu_id: "600544222"
zhihu_title: "yiduobo的每日leetcode 527.单词缩写"
question_id: "527"
question: "单词缩写"
problem_url: "https://leetcode.cn/problems/word-abbreviation/"
created: "2023-01-23T00:40:28+08:00"
updated: "2023-01-23T00:40:28+08:00"
upvotes: 0
comments: 0
---

# 527. 单词缩写

> **[yiduobo的每日leetcode 527.单词缩写](https://zhuanlan.zhihu.com/p/600544222) · 知乎 · 2023-01-23 · 赞同 0**
> 力扣：[527. 单词缩写](https://leetcode.cn/problems/word-abbreviation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

527.单词缩写

[力扣](https://leetcode.cn/problems/word-abbreviation/)

首先，若每个单词都不进行缩写，那么必然不会出现冲突的情况，因此可以使用原始单词来初始化最终答案。

接下来考虑冲突是如何发生的。可以发现，只有长度相同，且首尾字符相同的单词才可能出现冲突，因此可以使用这三个元素做key，在一开始就使用哈希表将所有单词分组，接下来就只需要逐个组考虑组间的单词是否会出现冲突了。

对于一个单词，缩写后的形式是单词前缀 + 缩写字符长度 + 末尾字符。由于组内单词的长度和末尾字符必然相同，因此单词缩写唯一性的保证就是其缩写后的单词前缀是唯一的。对于这个问题，则可以利用trie树来解决。

对组内的单词进行一趟遍历，将其加入到trie树中，同时对于trie树中的每个节点，记录其在构建过程中被访问的次数，这个次数实际上就是组内具有以这个节点为末尾的前缀的单词数目。

trie树构建完成后，再对组内的单词进行一趟遍历，通过trie树找出其在组内只出现过一次的最短前缀，也就是以最浅的访问次数为1的节点为末尾的前缀，接下来就可以通过这个前缀以及长度得到最终的缩写结果并更新最终答案了。

最后附上python代码：

```python
class Solution(object):
    def wordsAbbreviation(self, words):
        """
        :type words: List[str]
        :rtype: List[str]
        """

        res = words[:]

        word_dict = {}
        for index in range(len(words)):
            word = words[index]
            key = (word[0], word[-1], len(word))
            if key not in word_dict:
                word_dict[key] = []
            word_dict[key].append(index)

        for group in word_dict.values():
            if len(group) == 1:
                word = words[group[0]]
                abbr = word[0] + str(len(word) - 2) + word[-1]
                if len(abbr) < len(word):
                    res[group[0]] = abbr
                continue
                
            root = [{}, 0]
            for index in group:
                word = words[index]
                now = root
                n = len(word)
                for p in range(1, n - 1):
                    char = word[p]
                    if char not in now[0]:
                        now[0][char] = [{}, 0]
                    now = now[0][char]
                    now[1] += 1
            
            for index in group:
                word = words[index]
                now = root
                n = len(word)
                abbr = None
                for p in range(1, n - 1):
                    char = word[p]
                    now = now[0][char]
                    if now[1] == 1:
                        abbr = word[:p + 1] + str(len(word) - p - 2) + word[-1]
                        break

                if abbr is not None and len(abbr) < len(word):
                    res[index] = abbr

        return res
```

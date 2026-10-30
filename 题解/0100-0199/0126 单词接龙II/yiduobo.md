---
title: "126. 单词接龙II & 127. 单词接龙"
aliases: ["yiduobo的每日leetcode 126.单词接龙II && 127.单词接龙", "126. 单词接龙II", "127. 单词接龙"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/140534196"
zhihu_id: "140534196"
zhihu_title: "yiduobo的每日leetcode 126.单词接龙II && 127.单词接龙"
question_id: ["126", "127"]
question: ["单词接龙II", "单词接龙"]
problem_url: ["https://leetcode.cn/problems/word-ladder-ii/", "https://leetcode.cn/problems/word-ladder/"]
created: "2020-05-13T22:29:25+08:00"
updated: "2020-05-13T22:29:25+08:00"
upvotes: 0
comments: 0
---

# 126. 单词接龙II & 127. 单词接龙

> **[yiduobo的每日leetcode 126.单词接龙II && 127.单词接龙](https://zhuanlan.zhihu.com/p/140534196) · 知乎 · 2020-05-13 · 赞同 0**
> 力扣：[126. 单词接龙II](https://leetcode.cn/problems/word-ladder-ii/)
> 力扣：[127. 单词接龙](https://leetcode.cn/problems/word-ladder/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

126.单词接龙II <https://leetcode-cn.com/problems/word-ladder-ii/>

127.单词接龙 <https://leetcode-cn.com/problems/word-ladder/>

字符串处理加上图论的题目。

127是寻找最短操作次数，126则是输出所有的最短操作。

首先，逐个枚举每个词，并得到其删去一个字符后剩下的部分，作为key保存起来。

例如hit与hot，

hit可以得到\_it，h_t与hi\_

hot可以得到\_ot，h_t与ho\_

可以发现二者都能形成h_t这个key，于是hit可以通过一次操作变成hot。

在整理好所有词能形成的key之后，将词作为点，在同一个key中的词之间两两连上边，这样图就构造好了。

对于127题，直接bfs一边就能得出答案。

对于126题，会稍微复杂一些，在bfs因此需要记录变换到每个词需要的步数，而只有是通过最少的操作数达到某个词时才会将上一个词记录下来。

样例中的hit到cog，词表为hot, dot, dog, lot, log, cog，那么：

1、hit可以到hot，因此hot需要的步数为1，hot的上一个词为hit。

2、hot可以到dot与lot，因此dot与lot需要的步数为2，dot的上一个词为hot，lot的上一个词也是hot。

3-1、dot可以到dog，因此dog需要的步数为3，dog的上一个词为dot。

3-2、lot可以到log，因此log需要的步数为3，log的上一个词为lot。

4-1、dog可以到cog，因此cog需要的步数为4，cog的上一个词为dog。

4-2、log可以到cog，这里得到cog需要的步数为4，与4-1中得到cog需要的步数相同，因此cog的上一个词还需要额外记录log。

这样一来，就通过变换得到了最终的cog。

接下来，通过cog的上一个词开始反推，利用python的生成式写法得到最终的答案。

最后附上126题的python代码。其中，leak_dict会将每个词能形成的key组织起来，然后得到图g。之后再g中做bfs，通过level_dict记录到达每个词需要的最少步数，通过fa记录上一个词有哪些：

```python
class Solution(object):
    def findLadders(self, beginWord, endWord, wordList):
        """
        :type beginWord: str
        :type endWord: str
        :type wordList: List[str]
        :rtype: List[List[str]]
        """

        if beginWord not in wordList:
            wordList.append(beginWord)
        if endWord not in wordList:
            return []

        wordNum = len(wordList)
        wordLen = len(wordList[0])
        g = {word : [] for word in wordList}

        leak_dict = {}
        for word in wordList:
            for index in range(wordLen):
                key = word[:index] + '_' + word[index + 1:]
                if key not in leak_dict:
                    leak_dict[key] = []
                leak_dict[key].append(word)

        for key in leak_dict:
            leak_len = len(leak_dict[key])
            for i in range(leak_len - 1):
                for j in range(i + 1, leak_len):
                    g[leak_dict[key][i]].append(leak_dict[key][j])
                    g[leak_dict[key][j]].append(leak_dict[key][i])

        q = [beginWord]
        fa = {word : None for word in wordList}
        left = 0
        right = 1
        level_dict = {word : -1 for word in wordList}
        level_dict[beginWord] = 0
        while left < right:
            new_right = right
            for index in range(left, right):
                now = q[index]
                for next_word in g[now]:
                    if fa[next_word] is None:
                        q.append(next_word)
                        fa[next_word] = [now]
                        new_right += 1
                        level_dict[next_word] = level_dict[now] + 1
                    elif level_dict[next_word] == level_dict[now] + 1:
                        fa[next_word].append(now)
            if fa[endWord] is not None:
                break
            left = right
            right = new_right

        if fa[endWord] is None:
            return []

        res = [[endWord]]
        for index in range(level_dict[endWord]):
            res = [[y] + x for x in res for y in fa[x[0]]]

        return res
```

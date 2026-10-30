---
title: "1255. 得分最高的单词集合"
aliases: ["yiduobo的每日leetcode 1255.得分最高的单词集合"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/backtracking", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/四-回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/386284902"
zhihu_id: "386284902"
zhihu_title: "yiduobo的每日leetcode 1255.得分最高的单词集合"
question_id: "1255"
question: "得分最高的单词集合"
problem_url: "https://leetcode.cn/problems/maximum-score-words-formed-by-letters/"
difficulty: "Hard"
rating: 1882
created: "2021-07-03T13:46:50+08:00"
updated: "2021-07-03T13:46:50+08:00"
upvotes: 0
comments: 0
---

# 1255. 得分最高的单词集合

> **[yiduobo的每日leetcode 1255.得分最高的单词集合](https://zhuanlan.zhihu.com/p/386284902) · 知乎 · 2021-07-03 · 赞同 0**
> 力扣：[1255. 得分最高的单词集合](https://leetcode.cn/problems/maximum-score-words-formed-by-letters/) · Hard · 灵茶山艾府：[回溯三问：思考回溯问题的通用方法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1255.得分最高的单词集合

[力扣](https://leetcode-cn.com/problems/maximum-score-words-formed-by-letters/)

由于题目中的单词最多就14个，因此可以先预处理出每个单词需要消耗的字母集合以及其对应的得分。接下来直接进行dfs，每一轮都可以选择是否将当前单词加入到最后答案当中，那么最坏情况下也就2^14种状态，完全是可以接受的。

最后附上python代码：

```python
class Solution(object):
    def maxScoreWords(self, words, letters, score):
        """
        :type words: List[str]
        :type letters: List[str]
        :type score: List[int]
        :rtype: int
        """

        words_letter = []
        words_score = []
        for word in words:
            words_letter.append({})
            words_score.append(0)
            for char in word:
                words_letter[-1][char] = words_letter[-1].get(char, 0) + 1
                words_score[-1] += score[ord(char) - 97]

        letter_dict = {}
        for letter in letters:
            letter_dict[letter] = letter_dict.get(letter, 0) + 1

        n = len(words)
        self.res = 0
        self.dfs(0, n, letter_dict, 0, words_letter, words_score)
        return self.res

    def dfs(self, level, n, letter_dict, now, words_letter, words_score):
        if level == n:
            self.res = max(self.res, now)
            return
        
        self.dfs(level + 1, n, letter_dict, now, words_letter, words_score)

        flag = True
        for char, num in words_letter[level].items():
            if num > letter_dict.get(char, 0):
                flag = False
                break
        
        if flag:
            for char, num in words_letter[level].items():
                letter_dict[char] -= num
            self.dfs(level + 1, n, letter_dict, now + words_score[level], words_letter, words_score)
            for char, num in words_letter[level].items():
                letter_dict[char] += num
```

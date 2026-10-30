---
title: "843. 猜猜这个单词"
aliases: ["yiduobo的每日leetcode 843.猜猜这个单词"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/347513483"
zhihu_id: "347513483"
zhihu_title: "yiduobo的每日leetcode 843.猜猜这个单词"
question_id: "843"
question: "猜猜这个单词"
problem_url: "https://leetcode.cn/problems/guess-the-word/"
created: "2021-01-28T18:17:55+08:00"
updated: "2021-01-28T18:17:55+08:00"
upvotes: 0
comments: 1
---

# 843. 猜猜这个单词

> **[yiduobo的每日leetcode 843.猜猜这个单词](https://zhuanlan.zhihu.com/p/347513483) · 知乎 · 2021-01-28 · 赞同 0**
> 力扣：[843. 猜猜这个单词](https://leetcode.cn/problems/guess-the-word/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

843.猜猜这个单词

[力扣](https://leetcode-cn.com/problems/guess-the-word/)

很有意思的题目，之前应该是没有遇到过类似问题的。

首先，通过给出的guess方法可以知道某个单词有多少个字母处在正确的位置上。不妨设对于单词A，已知guess(A) \= k，那么对于另一个单词B，设二者匹配的字母数为match[A][B]。若此时的B恰好就是最终答案，那么A中所有与B匹配的字母都是正确的字母，而其他字母都是不正确的，也就是说guess(A) \= match[A][B]。

再根据之前的guess(A) \= k，那么对于单词C，若match[A][C]不等于k，那么单词C就必然不会是最终答案。

有了这一点，我们就可以预处理出所有单词两两之间的match程度，然后对于每次猜测的单词，我们都可以排除掉match程度不等于guess答案的单词。从这一点可知，我们每次应该尽可能先猜测与其他单词存在match的单词，从而可以在每次guess之后尽可能多地排除掉一些单词。这里的存在match我采用的是简单的match数目加权，当时也可以使用概率相关的做法来选择每次猜测的单词。

具体的做法为：

1、枚举所有单词，计算单词两两之间的match程度。

2、对于现在幸存的所有单词，统计每个单词与其他单词产生的match程度总和。统计完成后，从中选出一个match程度总和最大的单词，并进行guess。

3、若guess结果为6，那么该单词就是最终答案，否则需要从幸存单词中剔除掉match程度不等于guess结果的所有单词，然后回到步骤2直到猜测正确为止。

最后附上python代码：

```python
# """
# This is Master's API interface.
# You should not implement it, or speculate about its implementation
# """
#class Master(object):
#    def guess(self, word):
#        """
#        :type word: str
#        :rtype int
#        """

class Solution(object):
    def findSecretWord(self, wordlist, master):
        """
        :type wordlist: List[Str]
        :type master: Master
        :rtype: None
        """

        n = len(wordlist)
        candidate = set(range(n))

        match_list = [[0] * n for _ in range(n)]
        for i in range(n - 1):
            for j in range(i +1, n):
                cnt = 0
                for pos in range(6):
                    if wordlist[i][pos] == wordlist[j][pos]:
                        cnt += 1
                match_list[i][j] = cnt
                match_list[j][i] = cnt

        while True:
            guess_index = None
            max_cnt = 0
            for i in candidate:
                cnt = 0
                for j in candidate:
                    if i != j:
                        cnt += match_list[i][j]
                if cnt > max_cnt:
                    max_cnt = cnt
                    guess_index = i
            
            if guess_index is None:
                guess_index = candidate.pop()
            else:
                candidate.remove(guess_index)

            hits = master.guess(wordlist[guess_index])
            if hits == 6:
                return wordlist[guess_index]
            for i in list(candidate):
                if match_list[guess_index][i] != hits:
                    candidate.remove(i)
```

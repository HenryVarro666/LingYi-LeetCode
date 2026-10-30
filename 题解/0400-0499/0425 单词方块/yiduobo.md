---
title: "425. 单词方块"
aliases: ["yiduobo的每日leetcode 425.单词方块"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/599326351"
zhihu_id: "599326351"
zhihu_title: "yiduobo的每日leetcode 425.单词方块"
question_id: "425"
question: "单词方块"
problem_url: "https://leetcode.cn/problems/word-squares/"
created: "2023-01-16T04:04:08+08:00"
updated: "2023-01-16T04:04:08+08:00"
upvotes: 0
comments: 0
---

# 425. 单词方块

> **[yiduobo的每日leetcode 425.单词方块](https://zhuanlan.zhihu.com/p/599326351) · 知乎 · 2023-01-16 · 赞同 0**
> 力扣：[425. 单词方块](https://leetcode.cn/problems/word-squares/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

425.单词方块

[力扣](https://leetcode.cn/problems/word-squares/)

根据题目给出的数据规模来看，算法最终的时间复杂度只能是在O(n^2)的基础上再多出一点点，也就意味着本题的处理方式应该是枚举方块中的其中两个单词，然后再想办法处理剩下为填充的空格。

题目中单词的长度不超过4，当长度小于等于2时，枚举就可以处理了。当长度等于3时，枚举两个单词并检测合法性之后，方块中只剩下一个格子未填充，且这个格子必然位于左对角线上，无需考虑对称的问题，因此可以直接枚举这个格子中的字符，然后检测形成的单词是否出现在单词集合中。

接下来主要讨论一下单词长度为4的情况。

我在这里选择的是枚举第一个和第四个单词，分别记为w1和w4。只有在满足条件w1[3] \= w4[0]时才需要继续往下做，这个条件表示的是方块的右上角字符必须等于左下角字符。

接下来，根据单词对称的关系，就可以将方块的外层完全填充好，即

| w1[0] | w1[1] | w1[2] | w1[3] |
| --- | --- | --- | --- |
| w1[1] | @ | \# | w4[1] |
| w1[2] | \# | \* | w4[2] |
| w4[0] | w4[1] | w4[2] | w4[3] |

在这里还有三个字符需要确定，即上面标记出出来的@、\#以及\*。其中\#需要符合对称的规则。

同样的，在这里可以枚举\#表示什么字符，此时就确定好了w2和w3中的各三个字符。接下来如果继续枚举最后这个字符，时间复杂度会比较吃紧，更好的做法应该是在一开始就进行预处理，对于单词集合中的每个单词，分别去除掉下标位置为1和下标位置为2的字符，将剩余的部分作为key，使用哈希表将各个单词聚合起来。接下来，就可以通过哈希表高效地找到所有符合条件的w2和w3了。

最后附上python代码：

```python
class Solution(object):
    def wordSquares(self, words):
        """
        :type words: List[str]
        :rtype: List[List[str]]
        """

        n = len(words[0])
        
        res = []

        if n == 1:
            for word in words:
                res.append([word])
        elif n == 2:
            for word1 in words:
                for word2 in words:
                    if word2[0] == word1[1]:
                        res.append([word1, word2])
        elif n == 3:
            words_set = set(words)
            for word1 in words:
                for word3 in words:
                    if word3[0] == word1[2]:
                        for word2_mid in range(26):
                            word2 = word1[1] + chr(word2_mid + 97) + word3[1]
                            if word2 in words_set:
                                res.append([word1, word2, word3])
        else:
            remove1_words = {}
            remove2_words = {}
            for word in words:
                remove1 = word[0] + word[2] + word[3]
                remove2 = word[0] + word[1] + word[3]
                if remove1 not in remove1_words:
                    remove1_words[remove1] = set()
                if remove2 not in remove2_words:
                    remove2_words[remove2] = set()

                remove1_words[remove1].add(word)
                remove2_words[remove2].add(word)

            for word1 in words:
                for word4 in words:
                    if word4[0] == word1[3]:
                        for word2_mid in range(26):
                            word2_remove1 = word1[1] + chr(word2_mid + 97) + word4[1]
                            word3_remove2 = word1[2] + chr(word2_mid + 97) + word4[2]
                            if word2_remove1 in remove1_words and word3_remove2 in remove2_words:
                                for word2 in remove1_words[word2_remove1]:
                                    for word3 in remove2_words[word3_remove2]:
                                        res.append([word1, word2, word3, word4])
        
        return res
```

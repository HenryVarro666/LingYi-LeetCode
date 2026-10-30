---
title: "422. 有效单词方块"
aliases: ["yiduobo的每日leetcode 422.有效单词方块"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/599143253"
zhihu_id: "599143253"
zhihu_title: "yiduobo的每日leetcode 422.有效单词方块"
question_id: "422"
question: "有效单词方块"
problem_url: "https://leetcode.cn/problems/valid-word-square/"
created: "2023-01-15T04:06:50+08:00"
updated: "2023-01-15T04:06:50+08:00"
upvotes: 0
comments: 0
---

# 422. 有效单词方块

> **[yiduobo的每日leetcode 422.有效单词方块](https://zhuanlan.zhihu.com/p/599143253) · 知乎 · 2023-01-15 · 赞同 0**
> 力扣：[422. 有效单词方块](https://leetcode.cn/problems/valid-word-square/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

422.有效单词方块

[力扣](https://leetcode.cn/problems/valid-word-square/)

由于题目的数据规模较小，因此可以直接枚举方块中的每个字符word[i][j]。对于所有i与j不同的word[i][j]，其对应的字符应该是word[j][i]，那么若word没有j这一行，或者word[j]没有i这一列，或者word[i][j]不等于word[j][i]，那么就直接返回false。若成功遍历完了所有字符，那么就返回true。

最后附上python代码：

```python
class Solution(object):
    def validWordSquare(self, words):
        """
        :type words: List[str]
        :rtype: bool
        """

        m = len(words)
        for i in range(m):
            n = len(words[i])
            for j in range(n):
                if i == j:
                    continue
                if len(words) <= j:
                    return False
                if len(words[j]) <= i:
                    return False
                if words[j][i] != words[i][j]:
                    return False
        return True
```

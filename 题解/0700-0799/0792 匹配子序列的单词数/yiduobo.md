---
title: "792. 匹配子序列的单词数"
aliases: ["yiduobo的每日leetcode 792.匹配子序列的单词数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/341605606"
zhihu_id: "341605606"
zhihu_title: "yiduobo的每日leetcode 792.匹配子序列的单词数"
question_id: "792"
question: "匹配子序列的单词数"
problem_url: "https://leetcode.cn/problems/number-of-matching-subsequences/"
created: "2021-01-03T22:50:30+08:00"
updated: "2021-01-03T22:50:30+08:00"
upvotes: 0
comments: 0
---

# 792. 匹配子序列的单词数

> **[yiduobo的每日leetcode 792.匹配子序列的单词数](https://zhuanlan.zhihu.com/p/341605606) · 知乎 · 2021-01-03 · 赞同 0**
> 力扣：[792. 匹配子序列的单词数](https://leetcode.cn/problems/number-of-matching-subsequences/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

792.匹配子序列的单词数

[力扣](https://leetcode-cn.com/problems/number-of-matching-subsequences/)

对于字符串子序列匹配的问题，一般的做法是贪心法，即对于A和B两个字符串，如果要考察B是否可以由A的子序列组成，那么我们可以从头到尾遍历B，对于其中的每个字符，都尽可能地使用A中靠前的字符去匹配。理由也很直观，对于B[index]，若A[p]与A[q]都能与之匹配，且p \< q，那么若这里选择q能形成最终的完全匹配，那么在这里选择p也必然可以，反过来则不一定。

有了这个结论，我们可以通过预处理得到一个数组next，其中每一位都是一个dict，储存了从这一位开始到结尾的中，每个字符最早出现的位置。有了next之后，我们在考察是否匹配的时候就不需要逐个遍历，而是可以在next中不断跳跃，从而节省匹配过程的时间复杂度。

对于本题，做法也是类似，预处理出next数组之后，逐个考察words中的单词是否能形成匹配即可。

最后附上python代码：

```python
class Solution(object):
    def numMatchingSubseq(self, S, words):
        """
        :type S: str
        :type words: List[str]
        :rtype: int
        """

        n = len(S)
        next_pos = [{S[-1] : n - 1}]
        for index in range(n - 2, -1, -1):
            next_pos.append(next_pos[-1].copy())
            next_pos[-1][S[index]] = index
    
        next_pos.reverse()

        res = 0
        for word in words:
            now = 0
            flag = True
            for char in word:
                if now == n or char not in next_pos[now]:
                    flag = False
                    break
                else:
                    now = next_pos[now][char] + 1
            
            if flag:
                res += 1
        
        return res
```

---
title: "2052. 将句子分隔成行的最低成本"
aliases: ["yiduobo的每日leetcode 2052.将句子分隔成行的最低成本"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/625790838"
zhihu_id: "625790838"
zhihu_title: "yiduobo的每日leetcode 2052.将句子分隔成行的最低成本"
question_id: "2052"
question: "将句子分隔成行的最低成本"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-separate-sentence-into-rows/"
created: "2023-04-29T03:22:54+08:00"
updated: "2023-04-29T03:22:54+08:00"
upvotes: 0
comments: 0
---

# 2052. 将句子分隔成行的最低成本

> **[yiduobo的每日leetcode 2052.将句子分隔成行的最低成本](https://zhuanlan.zhihu.com/p/625790838) · 知乎 · 2023-04-29 · 赞同 0**
> 力扣：[2052. 将句子分隔成行的最低成本](https://leetcode.cn/problems/minimum-cost-to-separate-sentence-into-rows/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

2052.将句子分隔成行的最低成本

[力扣](https://leetcode.cn/problems/minimum-cost-to-separate-sentence-into-rows/)

题目中求解的问题与句子的内容无关，而是与分割单词的长度有关，因此可以先将字符串分割成单词，并将单词的长度收集起来得到长度数组v。

接下来令f[i]表示分割前i个单词所需的最低成本，需要注意这里的f[i]计算了最后一行的成本。对于f[i]：

1、首先是边界情况，f[0] \= 0

2、接下来对于i > 0的情况：

首先可以初始化f[i] \= f[i - 1] + (k - v[i])^2，表示最后这个单词单独成行。

除此之外，也可以枚举i之前的某个位置j，这里的j需要若满足v[j] + v[j + 1] + ... + v[i] + (j - i) \<\= k。

这种情况下就有f[i] \= min(f[i], f[j] + (k - (v[j] + v[j + 1] + ... + v[i] + (j - i)) ^2)

对于v[j] + v[j + 1] + ... + v[i] + (j - i)这个式子，则可以通过从i - 1开始向前枚举j，将其视为一个后缀和问题来进行求解。

另外需要特别注意的是，原题的最后这一行是不计成本的，因此在计算得到f[n - 1]之后，需要找出最优的i，这里的i需要满足v[i] + v[i + 1] + ... + v[n - 1] + (n - i - 1) \<\= k，同时f[i]最小。在这里可以套用上面相同的处理方法，从后向前遍历来找出最优的i。

最后附上python代码：

```python
class Solution(object):
    def minimumCost(self, sentence, k):
        """
        :type sentence: str
        :type k: int
        :rtype: int
        """

        v = [len(word) for word in sentence.split(' ')]
        f = [0]
        n = len(v)
        for i in range(n - 1):
            f.append(f[-1] + (k - v[i]) ** 2)
            now = v[i]
            for j in range(i - 1, -1, -1):
                now += v[j] + 1
                if now > k:
                    break
                f[-1] = min(f[-1], f[j] + (k - now) ** 2)
        
        res = f[-1]
        now = v[-1]
        for i in range(n - 2, -1, -1):
            now += v[i] + 1
            if now > k:
                break
            res = min(res, f[i])

        return res
```

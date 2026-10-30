---
title: "3579. 字符串转换需要的最小操作数"
aliases: ["yiduobo的每日leetcode 3579.字符串转换需要的最小操作数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/dynamic-programming", "题单/动态规划", "题单/字符串", "题单/动态规划/五-划分型-DP", "题单/字符串/三-Manacher-算法-回文串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1937914011363575039"
zhihu_id: "1937914011363575039"
zhihu_title: "yiduobo的每日leetcode 3579.字符串转换需要的最小操作数"
question_id: "3579"
question: "字符串转换需要的最小操作数"
problem_url: "https://leetcode.cn/problems/minimum-steps-to-convert-string-with-operations/"
difficulty: "Hard"
rating: 2493
created: "2025-08-10T17:11:48+08:00"
updated: "2025-08-10T17:11:48+08:00"
upvotes: 1
comments: 0
---

# 3579. 字符串转换需要的最小操作数

> **[yiduobo的每日leetcode 3579.字符串转换需要的最小操作数](https://zhuanlan.zhihu.com/p/1937914011363575039) · 知乎 · 2025-08-10 · 赞同 1**
> 力扣：[3579. 字符串转换需要的最小操作数](https://leetcode.cn/problems/minimum-steps-to-convert-string-with-operations/) · Hard · 灵茶山艾府：[O(n^2) 做法：划分型 DP + 贪心 + 中心扩展法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3579.字符串转换需要的最小操作数

[3579. 字符串转换需要的最小操作数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-steps-to-convert-string-with-operations/description/)

题目给出两个长度相等的字符串word1和word2，长度不超过100，现在要求将word1转换成word2。

为此，可以将word1分割成一个或多个连续子串，对于每个子串substr，可以执行以下操作：

1、替换：将substr中任意一个索引处的字符替换为另一个小写字母

2、交换：交换substr中任意两个字符的位置

3、反转：将substr反转

对于每种操作，每个字符串中的每个字符最多只能使用一次。问将word1转换为word2所需的最小操作数。

本题可以视为编辑距离的变种，但是没有插入或者删除操作，因此字符的匹配必须严格按照下标对应，也就是说在这里可以直接使用一维的状态表示，令f[index]表示前index个字符匹配所需的最少操作次数。

对于f[index]，则需要枚举其最后这个子串的左边界cut_pos，那么就有f[index] \= min(f[index], f[cut_pos - 1] + cost(cut_pos - 1, index - 1))，这里的cost为将word1中的cut_pos - 1到index - 1这一段转换为word2相同所需的操作次数。这里的减1是字符串的下标是从0开始的。

接下来考虑如何计算cost。注意到题目中有反转操作，因此在这里可以将子串反转，然后分别计算不反转和反转时对应的cost，取二者的较小值。

对于子串sub1和sub2，则只需一趟遍历，若当前的字符对(c1, c2)不同，且之前出现过没有配对的字符串(c2, c1)，那么就可以将这两个下标的字符进行交换，否则就需要将这个字符对记录下来，供后续的字符对交换。如果没有可交换的，就只能执行替换操作。

在具体实现上，可以使用一个哈希表记录出现的字符对，当出现不同的字符对(c1, c2)时，可以先将代价加上1，表示这个字符对需要执行替换或者交换操作，接下来若(c2, c1)在哈希表中出现的次数大于1，那么就将这两个下标交换，此时应该将代价减去1，同时将(c2, c1)出现的次数减一，表示当前的(c1, c2)和之前的(c2, c1)进行了交换；否则的话，就应该将(c1, c2)在哈希表中出现的次数加上1。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, word1, word2):
        """
        :type word1: str
        :type word2: str
        :rtype: int
        """
        
        def calc(s1, s2):
            pair = {}
            cnt = 0
            for c1, c2 in zip(s1, s2):
                if c1 == c2:
                    continue
                cnt += 1
                if pair.get((c2, c1), 0) > 0:
                    pair[(c2, c1)] -= 1
                    cnt -= 1
                else:
                    pair[(c1, c2)] = pair.get((c1, c2), 0) + 1
            
            return cnt

        n = len(word1)
        f = [0]
        for index in range(1, n + 1):
            f.append(None)
            for cut_pos in range(1, index + 1):
                s1 = word1[cut_pos - 1: index]
                rev_s1 = word1[cut_pos - 1: index][::-1]
                s2 = word2[cut_pos - 1: index]
                cost = min(calc(s1, s2), calc(rev_s1, s2) + 1)
                if f[-1] is None or f[-1] > cost + f[cut_pos - 1]:
                    f[-1] = cost + f[cut_pos - 1]

        return f[-1]
```

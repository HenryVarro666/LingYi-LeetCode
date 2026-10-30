---
title: "3081. 替换字符串中的问号使分数最小"
aliases: ["yiduobo的每日leetcode 3081.替换字符串中的问号使分数最小"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "leetcode/heap-priority-queue", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/五-堆-优先队列", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/698423886"
zhihu_id: "698423886"
zhihu_title: "yiduobo的每日leetcode 3081.替换字符串中的问号使分数最小"
question_id: "3081"
question: "替换字符串中的问号使分数最小"
problem_url: "https://leetcode.cn/problems/replace-question-marks-in-string-to-minimize-its-value/"
difficulty: "Medium"
rating: 1905
created: "2024-05-18T00:49:10+08:00"
updated: "2024-05-18T00:49:10+08:00"
upvotes: 0
comments: 0
---

# 3081. 替换字符串中的问号使分数最小

> **[yiduobo的每日leetcode 3081.替换字符串中的问号使分数最小](https://zhuanlan.zhihu.com/p/698423886) · 知乎 · 2024-05-18 · 赞同 0**
> 力扣：[3081. 替换字符串中的问号使分数最小](https://leetcode.cn/problems/replace-question-marks-in-string-to-minimize-its-value/) · Medium · 灵茶山艾府：[两种方法：从 O(nlogn) 到 O(n)（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3081.替换字符串中的问号使分数最小

[. - 力扣（LeetCode）](https://leetcode.cn/problems/replace-question-marks-in-string-to-minimize-its-value/description/)

对于题目中的某种字符char，若char最终出现的次数为freq[char]，那么char提供的分数就是freq[char] \* (freq[char] - 1) / 2。为了使得最终的分数最小，那么就应该将问号变为当前出现次数最少得字符，下面给出简单的证明。

对于两个字符x和y，不妨设freq[x] \< freq[y]，那么此时如果将一个问号变为x，分数之和就是

score_x \= (freq[x] + 1) \* freq[x] / 2 + (freq[y] - 1) \* freq[y] / 2

反之如果将一个问号变为y，分数之和就是

score_y \= (freq[x] - 1) \* freq[x] / 2 + (freq[y] + 1) \* freq[y] / 2

用score_x减去score_y，得到的就是

score_x - score_y \= freq[x] - freq[y] \< 0

也就是说应该让问号变为出现次数较少的字符x。

根据上面的结论，就可以先一趟遍历，统计每种字符出现的次数freq以及问号出现的次数r，接下来将字符的序按照出现次数为第一关键字，其自身为第二关键字进行排序。在这里需要第二关键字的理由是题目要求最终构造出来的字符串在分数最小的前提下字典序最小，因此在freq相同的情况下应该尽可能添加靠前的字符。

排序完成后，整个问号的分配过程就应该如下：

首先，分配足量的问号给rank\[0\]对应的字符，直到其出现次数freq\[rank\[0\]\]变为freq\[rank\[1\]\]为止

接下来，轮流分配问号给rank\[0\]和rank\[1\]对应的字符，直到这两种字符出现次数freq\[rank\[0\]\]和freq\[rank\[1\]\]都变为freq\[rank\[2\]\]为止

接下来，轮流分配问号给rank\[0\]、rank\[1\]、rank\[2\]去对标rank\[3\]，以此类推，直到所有字符出现次数都与freq\[rank\[25\]\]相同，或者r用完为止

对于上述的分配过程，每轮所需的问号数量分别是freq\[rank\[1\]\] - freq\[rank\[0\]\]、(freq\[rank\[2\]\] - freq\[rank\[1\]\]) \* 2、(freq\[rank\[3\]\] - freq\[rank\[2\]\]) \* 3，以此类推。

需要注意的是对于第index轮，由于上一轮的操作，freq\[rank\[0\]\]、freq\[rank\[1\]、...、freq\[rank\[index - 1\]\]都已经和freq\[rank\[index\]\]一样了，因此将二者都变为freq\[rank\[index + 1\]\]所需的问号数量就是上面的式子。

到了这里，就只需要从小到大遍历index，计算当前所需的问号数量diff。若diff \<\= r，那么就可以执行变换操作，此时应该将r减去diff，然后继续向后遍历；反之，说明问号数量不够了，记p为当前轮次对应的index + 1，也就是出现次数最少，且已经被操作变为一样的字符数目，接下来剩下的问号就应该被平均分配给这p种字符。

另外，在这里剩下的r不一定是p的倍数，那么就应该将余数的部分平均分配给钱r % p种字符。到了这里，就可以得知rank\[0\]到rank\[p - 1\]对应的p中字符中，字典序最小的r种最终的出现次数的目标值应该是freq\[rank\[p - 1\]\] + r / p + 1次，而剩下的p - r中出现的次数的目标值则应该是freq\[rank\[p - 1\]\] + r / p次，最后不属于这p种字符的其他字符出现次数的目标值应该保持不变。

有了每种字符出现的次数的目标值后，只需一趟遍历，使用一个变量x记录当前问号应该变成的字符。对于每个问号，先找出下一个当前出现次数比其最终出现次数的目标值要小的x，用x替换掉当前的问号，并更新其出现的次数。若替换后x出现的次数等于目标值，还需要将x向后移动。

最后附上python代码：

```python
class Solution(object):
    def minimizeStringValue(self, s):
        """
        :type s: str
        :rtype: str
        """

        freq = [0] * 26
        r = 0
        for char in s:
            if char == '?':
                r += 1
            else:
                freq[ord(char) - 97] += 1
        
        rank = sorted(range(26), key=lambda d:(freq[d], d))

        p = 1  
        for index in range(25):
            diff = (freq[rank[index + 1]] - freq[rank[index]]) * (index + 1)
            if diff <= r:
                r -= diff
                p += 1
            else:
                break
        
        v = freq[rank[p - 1]] + r / p
        r %= p

        res = []
        cnt = 0
        x = 0
        for char in s:
            if char == '?':
                if cnt < r:
                    bound = v + 1
                else:
                    bound = v
                
                while freq[x] >= bound:
                    x += 1
                
                res.append(chr(x + 97))
                freq[x] += 1
                if freq[x] == bound:
                    x += 1
                    cnt += 1
                
            else:
                res.append(char)

        return ''.join(res)
```

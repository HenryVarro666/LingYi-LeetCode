---
title: "2901. 最长相邻不相等子序列II"
aliases: ["yiduobo的每日leetcode 2901.最长相邻不相等子序列II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/hash-table", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/四-经典线性-DP", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/663590492"
zhihu_id: "663590492"
zhihu_title: "yiduobo的每日leetcode 2901.最长相邻不相等子序列II"
question_id: "2901"
question: "最长相邻不相等子序列 II"
problem_url: "https://leetcode.cn/problems/longest-unequal-adjacent-groups-subsequence-ii/"
difficulty: "Medium"
rating: 1899
created: "2023-10-27T03:07:43+08:00"
updated: "2023-10-27T03:07:43+08:00"
upvotes: 0
comments: 0
---

# 2901. 最长相邻不相等子序列II

> **[yiduobo的每日leetcode 2901.最长相邻不相等子序列II](https://zhuanlan.zhihu.com/p/663590492) · 知乎 · 2023-10-27 · 赞同 0**
> 力扣：[2901. 最长相邻不相等子序列 II](https://leetcode.cn/problems/longest-unequal-adjacent-groups-subsequence-ii/) · Medium · 灵茶山艾府：[两种方法：从 O(n^2) 到 O(n)（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2901.最长相邻不相等子序列II

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/longest-unequal-adjacent-groups-subsequence-ii/)

上一题的加强版，加强的地方包括groups中的取值不再是只有0和1、子序列相邻位置对应的单词需要满足长度相同、最多只有一个位置上的字符不同

对于本问题，交替取数的做法已经不再适用了，但是可以尝试经典的动态规划状态表示，即f[index]表示选定位置index结尾的子序列时，可用的最长子序列是多长。那么对于f[index]：

1、首先可以初始化f[index] \= 1，也就是前面的全都不要，这种情况必然是合法的

2、另外也可以遍历index左侧的所有下标pre_index，若此时的pre_index满足groups[index]和groups[pre_index]不同，且words[index]和words[pre_index]长度相同，同时这两个单词最多只有一个位置上的字符不同，那么在这里就有f[index] \= max(f[index], f[pre_index] + 1)，表示在以pre_index为末尾的最优子序列后面接上index

另外，题目要求输出最后构成的单词列表，因此除了f外，还需要一个数组pre记录每个状态的前一个状态是什么。对于上面的情况1，有pre[index] \= None，而对于上面的情况2，则需要在f[index]被f[pre_index] + 1更新时同时更新pre[index] \= pre_index。

计算完成后，首先遍历f找到最优的结尾位置p，然后从p开始利用pre数组往前倒推，从而构造出对应的单词列表。构造完成后需要将其倒转再返回。

最后附上python代码：

```python
class Solution(object):
    def getWordsInLongestSubsequence(self, n, words, groups):
        """
        :type n: int
        :type words: List[str]
        :type groups: List[int]
        :rtype: List[str]
        """

        f = []
        pre = []

        for index in range(n):
            f.append(1)
            pre.append(None)
            for pre_index in range(index):
                if groups[pre_index] != groups[index] and len(words[index]) == len(words[pre_index]) and f[-1] <= f[pre_index]:
                    diff = 0
                    for x, y in zip(words[index], words[pre_index]):
                        if x != y:
                            diff += 1
                            if diff == 2:
                                break

                    if diff < 2:
                        f[-1] = f[pre_index] + 1
                        pre[-1] = pre_index
        
        p = 0
        for index in range(1, n):
            if f[index] > f[p]:
                p = index
        
        res = []
        while p is not None:
            res.append(words[p])
            p = pre[p]
        
        res.reverse()
        return res
```

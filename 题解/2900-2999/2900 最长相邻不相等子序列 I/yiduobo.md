---
title: "2900. 最长相邻不相等子序列"
aliases: ["yiduobo的每日leetcode 2900.最长相邻不相等子序列"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/663590407"
zhihu_id: "663590407"
zhihu_title: "yiduobo的每日leetcode 2900.最长相邻不相等子序列"
question_id: "2900"
question: "最长相邻不相等子序列 I"
problem_url: "https://leetcode.cn/problems/longest-unequal-adjacent-groups-subsequence-i/"
difficulty: "Easy"
rating: 1469
created: "2023-10-27T02:56:58+08:00"
updated: "2023-10-27T02:56:58+08:00"
upvotes: 0
comments: 0
---

# 2900. 最长相邻不相等子序列

> **[yiduobo的每日leetcode 2900.最长相邻不相等子序列](https://zhuanlan.zhihu.com/p/663590407) · 知乎 · 2023-10-27 · 赞同 0**
> 力扣：[2900. 最长相邻不相等子序列 I](https://leetcode.cn/problems/longest-unequal-adjacent-groups-subsequence-i/) · Easy · 灵茶山艾府：[阅读理解，O(n) 一次遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2900.最长相邻不相等子序列

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/longest-unequal-adjacent-groups-subsequence-i/description/)

首先，题目要求的是子序列的长度最长，因此可以完全无视words中单词的长度，只需要考虑进来从group中选出最多的下标位置构成子序列就行了。由于题目选择子序列只需满足子序列中相邻位置对应group值不同，而group中只存在0和1，因此只需一趟遍历，若当前的groups[index]与groups[index - 1]相同，那么就跳过groups[index]，否则就将其对应的words[index]加入到答案中。这样一来，相当于每段相同的子数组中只选择了其中最左侧下标对应的单词，保证了子序列中相邻位置对应的group值不同，同时也可以使得子序列最长。

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

        res = [words[0]]
        for index in range(1, n):
            if groups[index] != groups[index - 1]:
                res.append(words[index])
        
        return res
```

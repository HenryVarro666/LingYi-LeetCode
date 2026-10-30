---
title: "2014. 重复K次的最长子序列"
aliases: ["yiduobo的每日leetcode 2014.重复K次的最长子序列"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/two-pointers", "leetcode/backtracking", "leetcode/enumeration", "题单/链表-二叉树与回溯", "题单/字符串", "题单/链表-二叉树与回溯/四-回溯", "题单/字符串/九-子序列自动机"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/505030229"
zhihu_id: "505030229"
zhihu_title: "yiduobo的每日leetcode 2014.重复K次的最长子序列"
question_id: "2014"
question: "重复 K 次的最长子序列"
problem_url: "https://leetcode.cn/problems/longest-subsequence-repeated-k-times/"
difficulty: "Hard"
rating: 2558
created: "2022-04-25T23:59:23+08:00"
updated: "2022-04-25T23:59:23+08:00"
upvotes: 0
comments: 0
---

# 2014. 重复K次的最长子序列

> **[yiduobo的每日leetcode 2014.重复K次的最长子序列](https://zhuanlan.zhihu.com/p/505030229) · 知乎 · 2022-04-25 · 赞同 0**
> 力扣：[2014. 重复 K 次的最长子序列](https://leetcode.cn/problems/longest-subsequence-repeated-k-times/) · Hard · 灵茶山艾府：[枚举排列 + 判断子序列（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2014.重复K次的最长子序列

[力扣](https://leetcode-cn.com/problems/longest-subsequence-repeated-k-times/)

没有什么特别好的做法，不过注意到题目中保证了n \< k \* 8，也就意味着这个子序列的长度至多为7，且至多由7种不同的字符组成。接下来则需要枚举这7种字符组成的子序列的每种情况，然后一趟遍历，检测当前枚举的子序列是否在字符串中出现了k次。

当然，直接暴力计算的话时间复杂度大概在n \* (7^7)这个量级，还是比较大的，那么需要想办法做一些优化。

首先，题目要找的是最长的，因此应该优先检测较长的子序列。除此之外，题目要找的是相同长度中字典序最大的那个，因此在枚举时应该优先尝试较大的字符。最后，当某种字符出现次数过多时，可以通过该字符出现的总数粗略过滤掉字符不够的情况。

最后附上python代码：

```python
class Solution(object):
    def longestSubsequenceRepeatedK(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: str
        """

        self.res = []
        n = len(s) / k
        char_dict = {}
        for char in s:
            char_dict[char] = char_dict.get(char, 0) + 1
        
        char_set = set()
        for char in char_dict:
            if char_dict[char] >= k:
                char_set.add(char)
        
        if len(char_set) == 0:
            return ""

        char_list = sorted(list(char_set), reverse=True)
        all_cnt = [char_dict[char] for char in char_list]

        now = []
        cnt_list = [0] * len(char_list)
        for res_l in range(n, 0, -1):
            if self.dfs(0, res_l, now, char_list, cnt_list, all_cnt, s, k):
                return "".join(now)

    def dfs(self, level, res_l, now, char_list, cnt_list, all_cnt, s, k):
        if level == res_l:
            p = 0
            cnt = 0
            flag = False
            for char in s:
                if char == now[p]:
                    p += 1
                    if p == len(now):
                        cnt += 1
                        p = 0
                        if cnt == k:
                            flag = True
                            break
            
            return flag
        
        for index, char in enumerate(char_list):
            now.append(char)
            cnt_list[index] += 1
            if cnt_list[index] * k <= all_cnt[index]:
                if self.dfs(level + 1, res_l, now, char_list, cnt_list, all_cnt, s, k):
                    return True
            cnt_list[index] -= 1
            now.pop()
        
        return False
```

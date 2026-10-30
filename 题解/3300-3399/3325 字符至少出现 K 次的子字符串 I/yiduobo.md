---
title: "3325. 字符串至少出现K次的子字符串I & 3329. 字符串至少出现K次的子字符串II"
aliases: ["yiduobo的每日leetcode 3325.字符串至少出现K次的子字符串I && 3329.字符串至少出现K次的子字符串II", "3325. 字符串至少出现K次的子字符串I", "3329. 字符串至少出现K次的子字符串II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口", "leetcode/hard"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2580924365"
zhihu_id: "2580924365"
zhihu_title: "yiduobo的每日leetcode 3325.字符串至少出现K次的子字符串I && 3329.字符串至少出现K次的子字符串II"
question_id: ["3325", "3329"]
question: ["字符至少出现 K 次的子字符串 I", "字符至少出现 K 次的子字符串 II"]
problem_url: ["https://leetcode.cn/problems/count-substrings-with-k-frequency-characters-i/", "https://leetcode.cn/problems/count-substrings-with-k-frequency-characters-ii/"]
difficulty: ["Medium", "Hard"]
created: "2024-10-22T23:22:26+08:00"
updated: "2024-10-24T00:14:02+08:00"
upvotes: 0
comments: 0
---

# 3325. 字符串至少出现K次的子字符串I & 3329. 字符串至少出现K次的子字符串II

> **[yiduobo的每日leetcode 3325.字符串至少出现K次的子字符串I && 3329.字符串至少出现K次的子字符串II](https://zhuanlan.zhihu.com/p/2580924365) · 知乎 · 2024-10-22 · 赞同 0**
> 力扣：[3325. 字符至少出现 K 次的子字符串 I](https://leetcode.cn/problems/count-substrings-with-k-frequency-characters-i/) · Medium · 灵茶山艾府：[O(n) 滑动窗口（Python/Java/C++/Go）](灵茶山艾府.md)
> 力扣：[3329. 字符至少出现 K 次的子字符串 II](https://leetcode.cn/problems/count-substrings-with-k-frequency-characters-ii/) · Hard · 灵茶山艾府：[滑动窗口（Python/Java/C++/Go）](../3329%20字符至少出现%20K%20次的子字符串%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3325.字符串至少出现K次的子字符串I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-substrings-with-k-frequency-characters-i/description/)

3329.字符串至少出现K次的子字符串II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-substrings-with-k-frequency-characters-ii/description/)

题目给出一个字符串s和一个整数k，要求找出s的所有子串中，至少有一个字符至少出现k次的子串的数量。

两题的题设一样，第二题的数据规模较大。

非常经典的变长滑动窗口问题，使用一个窗口从左向右滑动。对于当前的窗口左边界index，不妨设最小的满足条件的窗口右边界为p，那么：

1、以index为左边界，p到len(s) - 1之间任意位置为右边界的子串都是符合条件的子串，一共有len(s) - p个，那么对于每个index，都需要将对应的len(s) - p累加到答案中

2、s[p]必然是唯一一个恰好出现了k次的字符，因为若其他字符已经出现了k次，那么在p之前必然存在其他满足条件的右边界，与p的定义矛盾

3、随着index的向后移动，p必然也跟着向后移动的。另外根据结论2可以知道，只有当上一轮被移出窗口的字符恰好就是s[p]时，才有必要将p向后移动，其他情况下窗口内s[p]的数量依然是k个，无需移动

最后附上python代码：

```python
class Solution(object):
    def numberOfSubstrings(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """
        
        freq = {}
        p = 0
        res = 0

        for index, char in enumerate(s):
            while p < len(s) and freq.get(s[p], 0) < k:
                freq[s[p]] = freq.get(s[p], 0) + 1
                if freq[s[p]] == k:
                    break
                p += 1

            if p == len(s):
                break
            
            res += len(s) - p

            freq[char] -= 1
            if freq[char] == k - 1:
                p += 1

        return res
```

---
title: "3557. 不相交子字符串的最大数量"
aliases: ["yiduobo的每日leetcode 3557.不相交子字符串的最大数量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/bit-manipulation", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1909805047769989698"
zhihu_id: "1909805047769989698"
zhihu_title: "yiduobo的每日leetcode 3557.不相交子字符串的最大数量"
question_id: "3557"
question: "不相交子字符串的最大数量"
problem_url: "https://leetcode.cn/problems/find-maximum-number-of-non-intersecting-substrings/"
difficulty: "Medium"
rating: 1720
created: "2025-05-26T22:10:50+08:00"
updated: "2025-05-26T22:10:50+08:00"
upvotes: 0
comments: 0
---

# 3557. 不相交子字符串的最大数量

> **[yiduobo的每日leetcode 3557.不相交子字符串的最大数量](https://zhuanlan.zhihu.com/p/1909805047769989698) · 知乎 · 2025-05-26 · 赞同 0**
> 力扣：[3557. 不相交子字符串的最大数量](https://leetcode.cn/problems/find-maximum-number-of-non-intersecting-substrings/) · Medium · 灵茶山艾府：[划分型贪心+位运算优化，附题单（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3557.不相交子字符串的最大数量

[3557. 不相交子字符串的最大数量 - 力扣（LeetCode）](https://leetcode.cn/problems/find-maximum-number-of-non-intersecting-substrings/description/)

题目给出一个字符串word，要求返回首位字母相同且长度至少为4的不相交子串的最大数量。需要注意这些子串只需要不相交，并不需要用到字符串中的每个字符。

由于不需要用到字符串中的每个字符，那么就可以从左向右一趟遍历，当碰到可以分离的子串时就立马分离出去，因为剩下的字符串越长，可能分离出去的子串数量就越多。另一方面，分离子串的条件是子串长度大于等于4，且首位字符相同，那么就可以使用一个哈希表pre记录每种可用字符第一次出现的位置。

接下就可以对字符串进行一趟遍历，对于当前遍历到的是下标为index的字符c：

1、若c没有在pre中出现过

此时只需将pre[c]更新为index。

2、index - pre[c] + 1 >\= 4：

说明pre[c]到index之间至少有4个字符，那么就可以将pre[c]到index之间的子串分离出去，此时应该将答案加上1。另外需要注意的是，由于本次分离操作，那么index之前的所有字符都不能再用，因此还需要将pre清空。

最后附上python代码：

```python
class Solution(object):
    def maxSubstrings(self, word):
        """
        :type word: str
        :rtype: int
        """
        
        pre = {}
        res = 0
        for index, c in enumerate(word):
            if c not in pre:
                pre[c] = index
            elif index - pre[c] + 1 >= 4:
                res += 1
                pre = {}
        
        return res
```

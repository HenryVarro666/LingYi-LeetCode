---
title: "1898. 可移除字符的最大数目"
aliases: ["yiduobo的每日leetcode 1898.可移除字符的最大数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "题单/滑动窗口与双指针", "题单/二分算法", "题单/滑动窗口与双指针/四-双序列双指针", "题单/二分算法/二-二分答案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/479957679"
zhihu_id: "479957679"
zhihu_title: "yiduobo的每日leetcode 1898.可移除字符的最大数目"
question_id: "1898"
question: "可移除字符的最大数目"
problem_url: "https://leetcode.cn/problems/maximum-number-of-removable-characters/"
difficulty: "Medium"
rating: 1913
created: "2022-03-12T20:11:22+08:00"
updated: "2022-03-12T20:11:23+08:00"
upvotes: 0
comments: 0
---

# 1898. 可移除字符的最大数目

> **[yiduobo的每日leetcode 1898.可移除字符的最大数目](https://zhuanlan.zhihu.com/p/479957679) · 知乎 · 2022-03-12 · 赞同 0**
> 力扣：[1898. 可移除字符的最大数目](https://leetcode.cn/problems/maximum-number-of-removable-characters/) · Medium · 灵茶山艾府：[Go 二分](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1898.可移除字符的最大数目

[力扣](https://leetcode-cn.com/problems/maximum-number-of-removable-characters/)

由于题目移除的是removable中的前几个下标对应的字符，那么对于一组i和j，若i \< j，那么对于i而言，其移除的字符必然是j移除字符的一个子集。也就是说，若选择移除前j个下标对应的字符后p依然是s的子序列，那么移除前i个下标对应的字符后p必然也是s的子序列，即这里的答案满足二分的性质。

于是可以二分最后的答案，然后将对应的字符从s中移除，然后检测p是否依然是s的子序列。具体实现上，并不需要直接操作s，而是可以记录下s哪些位置不可用，在匹配时跳过这些位置即可。

设s的长度为n，removeable的长度为m，那么二分的时间复杂度为O(logm)，检测的时间复杂度为O(n)，因此最终的时间复杂度就是O(nlogm)。

最后附上python代码：

```python
class Solution(object):
    def maximumRemovals(self, s, p, removable):
        """
        :type s: str
        :type p: str
        :type removable: List[int]
        :rtype: int
        """

        l = 0
        r = len(removable)
        while l < r:
            mid = (l + r + 1) >> 1
            remove_set = set()
            for index in range(mid):
                remove_set.add(removable[index])
            
            pos = 0
            for index, char in enumerate(s):
                if index not in remove_set and char == p[pos]:
                    pos += 1
                    if pos == len(p):
                        break
            
            if pos == len(p):
                l = mid
            else:
                r = mid - 1

        return r
```

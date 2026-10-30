---
title: "2516. 每种字符至少取K个"
aliases: ["yiduobo的每日leetcode 2516.每种字符至少取K个"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/634851769"
zhihu_id: "634851769"
zhihu_title: "yiduobo的每日leetcode 2516.每种字符至少取K个"
question_id: "2516"
question: "每种字符至少取 K 个"
problem_url: "https://leetcode.cn/problems/take-k-of-each-character-from-left-and-right/"
difficulty: "Medium"
rating: 1948
created: "2023-06-07T23:22:30+08:00"
updated: "2023-06-07T23:22:30+08:00"
upvotes: 0
comments: 0
---

# 2516. 每种字符至少取K个

> **[yiduobo的每日leetcode 2516.每种字符至少取K个](https://zhuanlan.zhihu.com/p/634851769) · 知乎 · 2023-06-07 · 赞同 0**
> 力扣：[2516. 每种字符至少取 K 个](https://leetcode.cn/problems/take-k-of-each-character-from-left-and-right/) · Medium · 灵茶山艾府：[逆向思维（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

2516.每种字符至少取K个

[力扣](https://leetcode.cn/problems/take-k-of-each-character-from-left-and-right/)

首先考虑边界情况。一趟遍历，使用一个数组统计三种字符各自出现的次数。若其中某种字符出现的次数不足K个，那么答案必然为-1。

接下来考虑有解的情况。题目要求从数组的两端各取一些字符，那么剩下的就是一段连续子数组，同时这段子数组中各个字符出现的次数均不超过其出现总数减去k。为了使得最终答案最小，那么就要让这个子数组最长，于是问题就转化成了找出一个子数组，要求其中各字符出现次数不超过一个定值，且子数组长度最大。

对于这个问题，只需利用变长滑动窗口，一趟遍历枚举左边界，然后对于每个左边界计算出最大的合法右边界。随着左边界的向右移动，右边界必然也是单调不减的，因此可以在O(n)的时间内找出所有合法的子数组，然后使用原始数组的长度减去其中最长的合法子数组长度作为最终的答案。

最后附上python代码：

```python
class Solution(object):
    def takeCharacters(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """

        tot = [0] * 3
        for char in s:
            tot[ord(char) - 97] += 1
        
        if min(tot) < k:
            return -1
        
        cnt = [0] * 3
        right = 0
        res = len(s)
        for left in range(len(s)):
            if right < left:
                right = left
            
            while right < len(s) and cnt[ord(s[right]) - 97] + 1 + k <= tot[ord(s[right]) - 97]:
                cnt[ord(s[right]) - 97] += 1
                right += 1

            res = min(res, len(s) - (right - left))

            if left < right:
                cnt[ord(s[left]) - 97] -= 1
        
        return res
```

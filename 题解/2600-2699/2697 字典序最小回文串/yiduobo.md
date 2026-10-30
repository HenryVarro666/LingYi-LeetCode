---
title: "2697. 字典序最小回文串"
aliases: ["yiduobo的每日leetcode 2697.字典序最小回文串"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "题单/滑动窗口与双指针", "题单/贪心算法", "题单/滑动窗口与双指针/三-单序列双指针", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/650231860"
zhihu_id: "650231860"
zhihu_title: "yiduobo的每日leetcode 2697.字典序最小回文串"
question_id: "2697"
question: "字典序最小回文串"
problem_url: "https://leetcode.cn/problems/lexicographically-smallest-palindrome/"
difficulty: "Easy"
rating: 1304
created: "2023-08-15T19:49:16+08:00"
updated: "2023-08-15T19:49:17+08:00"
upvotes: 0
comments: 0
---

# 2697. 字典序最小回文串

> **[yiduobo的每日leetcode 2697.字典序最小回文串](https://zhuanlan.zhihu.com/p/650231860) · 知乎 · 2023-08-15 · 赞同 0**
> 力扣：[2697. 字典序最小回文串](https://leetcode.cn/problems/lexicographically-smallest-palindrome/) · Easy · 灵茶山艾府：[贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2697.字典序最小回文串

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/lexicographically-smallest-palindrome/description/)

从两侧向中心遍历，当出现不匹配的字符对时就需要进行修改。为了使得修改的总次数最小，每次就只能修改其中的一个字符。又因为要使得最终的字符串字典序最小，因此只能将字典序较大的那个修改成字典序较小的那个。

最后附上python代码：

```python
class Solution(object):
    def makeSmallestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """

        left = 0
        right = len(s) - 1
        res = list(s)
        while left < right:
            if res[left] < res[right]:
                res[right] = res[left]
            else:
                res[left] = res[right]
            
            left += 1
            right -= 1
        
        return ''.join(res)
```

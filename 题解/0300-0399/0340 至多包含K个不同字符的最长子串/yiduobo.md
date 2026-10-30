---
title: "340. 至多包含K个不同字符的最长子串"
aliases: ["yiduobo的每日leetcode 340.至多包含K个不同字符的最长子串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/596941913"
zhihu_id: "596941913"
zhihu_title: "yiduobo的每日leetcode 340.至多包含K个不同字符的最长子串"
question_id: "340"
question: "至多包含K个不同字符的最长子串"
problem_url: "https://leetcode.cn/problems/longest-substring-with-at-most-k-distinct-characters/"
created: "2023-01-06T02:40:35+08:00"
updated: "2023-01-06T02:40:35+08:00"
upvotes: 0
comments: 0
---

# 340. 至多包含K个不同字符的最长子串

> **[yiduobo的每日leetcode 340.至多包含K个不同字符的最长子串](https://zhuanlan.zhihu.com/p/596941913) · 知乎 · 2023-01-06 · 赞同 0**
> 力扣：[340. 至多包含K个不同字符的最长子串](https://leetcode.cn/problems/longest-substring-with-at-most-k-distinct-characters/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

340.至多包含K个不同字符的最长子串

[力扣](https://leetcode.cn/problems/longest-substring-with-at-most-k-distinct-characters/)

非常经典的变长滑动窗口的问题。

首先考虑边界情况。当k等于0时，任何子串都是不合法的，因此此时的答案为0。

接下来考虑k > 0的情况。从左向右枚举滑动窗口的右边界right，同时使用一个哈希表cnt记录当前窗口中每种字符出现的次数。随着right的向右移动，若当前窗口中出现的字符种数超过了k种，那么就需要将左边界left不断向右移动，直到窗口内出现的字符种树回到k种为止，此时的left就是以right为右边界的合法子串中的最小左边界，使用字符串长度，也就是窗口长度right - left + 1来更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def lengthOfLongestSubstringKDistinct(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """

        if k == 0:
            return 0
        
        cnt = {s[0] : 1}
        left = right = 0
        res = 1
        n = len(s)

        while right + 1 < n:
            right += 1
            cnt[s[right]] = cnt.get(s[right], 0) + 1
            while len(cnt) > k:
                cnt[s[left]] -= 1
                if cnt[s[left]] == 0:
                    cnt.pop(s[left])
                left += 1

            res = max(res, right - left + 1)
        
        return res
```

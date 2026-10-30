---
title: "3460. 最多删除一次后的最长公共前缀"
aliases: ["yiduobo的每日leetcode 3460.最多删除一次后的最长公共前缀"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1894849459910861217"
zhihu_id: "1894849459910861217"
zhihu_title: "yiduobo的每日leetcode 3460.最多删除一次后的最长公共前缀"
question_id: "3460"
question: "最多删除一次后的最长公共前缀"
problem_url: "https://leetcode.cn/problems/longest-common-prefix-after-at-most-one-removal/"
created: "2025-04-13T20:33:18+08:00"
updated: "2025-04-13T20:33:18+08:00"
upvotes: 1
comments: 0
---

# 3460. 最多删除一次后的最长公共前缀

> **[yiduobo的每日leetcode 3460.最多删除一次后的最长公共前缀](https://zhuanlan.zhihu.com/p/1894849459910861217) · 知乎 · 2025-04-13 · 赞同 1**
> 力扣：[3460. 最多删除一次后的最长公共前缀](https://leetcode.cn/problems/longest-common-prefix-after-at-most-one-removal/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3460.最多删除一次后的最长公共前缀

[3460. 最多删除一次后的最长公共前缀 - 力扣（LeetCode）](https://leetcode.cn/problems/longest-common-prefix-after-at-most-one-removal/)

题目给出两个字符串s和t，现在要求计算从s中删除最多一个字符后，s和t的最长公共前缀的长度。需要注意在这里也可以不执行删除操作。

若s的某个前缀可以与t的某个前缀相同，那么就不应该从这个前缀中删除任何字符。于是可以使用两个指针p和q分别从s和t的头部出发向后遍历，直到p或q来到s或t的末尾，或者s[p]不等于t[q]为止。

接下来，由于s[p]无法继续匹配t[q]，那么在这里就应该跳过s[p]，于是应该将p加上1，然后再从p和q开始向后遍历，直到p或q来到s或t的末尾，或者s[p]不等于t[q]为止。

遍历完成后，t中遍历过的字符即为最终公共前缀，其长度就是q。

最后附上python代码：

```python
class Solution(object):
    def longestCommonPrefix(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: int
        """
        
        p = 0
        q = 0
        while p < len(s) and q < len(t) and s[p] == t[q]:
            p += 1
            q += 1

        p += 1
        while p < len(s) and q < len(t) and s[p] == t[q]:
            p += 1
            q += 1
        
        return q
```

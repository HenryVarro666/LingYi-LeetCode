---
title: "2937. 使三个字符串相等"
aliases: ["yiduobo的每日leetcode 2937.使三个字符串相等"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/690887340"
zhihu_id: "690887340"
zhihu_title: "yiduobo的每日leetcode 2937.使三个字符串相等"
question_id: "2937"
question: "使三个字符串相等"
problem_url: "https://leetcode.cn/problems/make-three-strings-equal/"
difficulty: "Easy"
created: "2024-04-06T04:07:06+08:00"
updated: "2024-04-06T04:07:06+08:00"
upvotes: 1
comments: 0
---

# 2937. 使三个字符串相等

> **[yiduobo的每日leetcode 2937.使三个字符串相等](https://zhuanlan.zhihu.com/p/690887340) · 知乎 · 2024-04-06 · 赞同 1**
> 力扣：[2937. 使三个字符串相等](https://leetcode.cn/problems/make-three-strings-equal/) · Easy · 灵茶山艾府：[计算三个字符串的最长公共前缀（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2937.使三个字符串相等

[. - 力扣（LeetCode）](https://leetcode.cn/problems/make-three-strings-equal/description/)

题目中的删除操作只能从后向前进行，那么保留下来的字符串一定是原字符串的前缀。换言之，题目就是要找到最大的p，使得三个字符串长度为p的前缀相同。于是可以从头开始向后遍历，找到这个p。

接下来，若p等于0，那么答案为-1，否则就需要将这三个字符串都删减到长度为p，因此答案就是三个字符串的长度之和减去3倍的p。

最后附上python代码：

```python
class Solution(object):
    def findMinimumOperations(self, s1, s2, s3):
        """
        :type s1: str
        :type s2: str
        :type s3: str
        :rtype: int
        """

        p = 0
        while p < len(s1) and p < len(s2) and p < len(s3) and s1[p] == s2[p] == s3[p]:
            p += 1
        
        if p == 0:
            return -1
        else:
            return len(s1) + len(s2) + len(s3) - p * 3
```

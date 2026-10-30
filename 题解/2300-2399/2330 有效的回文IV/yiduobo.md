---
title: "2330. 有效的回文IV"
aliases: ["yiduobo的每日leetcode 2330.有效的回文IV"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/629919784"
zhihu_id: "629919784"
zhihu_title: "yiduobo的每日leetcode 2330.有效的回文IV"
question_id: "2330"
question: "有效的回文IV"
problem_url: "https://leetcode.cn/problems/valid-palindrome-iv/"
created: "2023-05-16T23:05:04+08:00"
updated: "2023-05-16T23:05:04+08:00"
upvotes: 0
comments: 0
---

# 2330. 有效的回文IV

> **[yiduobo的每日leetcode 2330.有效的回文IV](https://zhuanlan.zhihu.com/p/629919784) · 知乎 · 2023-05-16 · 赞同 0**
> 力扣：[2330. 有效的回文IV](https://leetcode.cn/problems/valid-palindrome-iv/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2330.有效的回文IV

[力扣](https://leetcode.cn/problems/valid-palindrome-iv/)

从两侧向中间遍历，对于每一组位置对，若二者不同，那么就需要就行一次修改。若s中有两处以上不同的位置，那么答案就是false，否则答案就是true。

最后附上python代码：

```python
class Solution(object):
    def makePalindrome(self, s):
        """
        :type s: str
        :rtype: bool
        """

        cnt = 0
        left = 0
        right = len(s) - 1
        while left < right:
            if s[left] != s[right]:
                cnt += 1
                if cnt > 2:
                    break
                
            left += 1
            right -= 1
        
        return cnt <= 2
```

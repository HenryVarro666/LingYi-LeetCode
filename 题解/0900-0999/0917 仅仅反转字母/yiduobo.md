---
title: "917. 仅仅反转字母"
aliases: ["yiduobo的每日leetcode 917.仅仅反转字母"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/355267553"
zhihu_id: "355267553"
zhihu_title: "yiduobo的每日leetcode 917.仅仅反转字母"
question_id: "917"
question: "仅仅反转字母"
problem_url: "https://leetcode.cn/problems/reverse-only-letters/"
created: "2021-03-07T16:17:25+08:00"
updated: "2021-03-07T16:17:25+08:00"
upvotes: 0
comments: 0
---

# 917. 仅仅反转字母

> **[yiduobo的每日leetcode 917.仅仅反转字母](https://zhuanlan.zhihu.com/p/355267553) · 知乎 · 2021-03-07 · 赞同 0**
> 力扣：[917. 仅仅反转字母](https://leetcode.cn/problems/reverse-only-letters/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

917.仅仅反转字母

[力扣](https://leetcode-cn.com/problems/reverse-only-letters/)

与之前的某一题类似，这个问题也可以使用类似快排的交换方式。使用两个指针l和r，l从头往后扫描，直到碰到一个字母；r从尾往头扫描，同样是碰到字母停止。若此时的l依然小于r，那么就交换l和r上的字母。重复此过程直到l大于等于r。

最后附上python代码：

```python
class Solution(object):
    def reverseOnlyLetters(self, S):
        """
        :type S: str
        :rtype: str
        """

        l = 0
        r = len(S) - 1

        s_list = list(S)

        while l < r:
            while l < r and not((S[l] >= 'a' and S[l] <= 'z') or (S[l] >= 'A' and S[l] <= 'Z')):
                l += 1
            if l == r:
                break
            
            while r > l and not((S[r] >= 'a' and S[r] <= 'z') or (S[r] >= 'A' and S[r] <= 'Z')):
                r -= 1
            if l == r:
                break
            
            s_list[l], s_list[r] = s_list[r], s_list[l]
            l += 1
            r -= 1
        
        return ''.join(s_list)
```

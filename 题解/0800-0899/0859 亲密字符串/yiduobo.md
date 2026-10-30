---
title: "859. 亲密字符串"
aliases: ["yiduobo的每日leetcode 859.亲密字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/349124189"
zhihu_id: "349124189"
zhihu_title: "yiduobo的每日leetcode 859.亲密字符串"
question_id: "859"
question: "亲密字符串"
problem_url: "https://leetcode.cn/problems/buddy-strings/"
created: "2021-02-06T23:48:52+08:00"
updated: "2021-02-06T23:48:52+08:00"
upvotes: 0
comments: 0
---

# 859. 亲密字符串

> **[yiduobo的每日leetcode 859.亲密字符串](https://zhuanlan.zhihu.com/p/349124189) · 知乎 · 2021-02-06 · 赞同 0**
> 力扣：[859. 亲密字符串](https://leetcode.cn/problems/buddy-strings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

859.亲密字符串

[力扣](https://leetcode-cn.com/problems/buddy-strings/)

可以发现，两个串A和B若为亲密字符串，那么其必然满足下面两个条件之一：

1、A和B中仅有两个位置的字符不一样，且这两个位置的字符满足A[i] \= B[j]、A[j] \= B[i]

2、A和B完全一致，且A中有个两相同的字符

只需要一趟扫描，分别判断A和B是否满足上面两种情况之一即可。

最后附上python代码：

```python
class Solution(object):
    def buddyStrings(self, A, B):
        """
        :type A: str
        :type B: str
        :rtype: bool
        """

        if len(A) != len(B):
            return False

        same_char = False
        char_set = set()
        diff_list = []

        for index in range(len(A)):
            if A[index] != B[index]:
                diff_list.append(index)
            elif A[index] not in char_set:
                char_set.add(A[index])
            else:
                same_char = True

        if not diff_list and same_char:
            return True
        
        if len(diff_list) == 2 and A[diff_list[0]] == B[diff_list[1]] and B[diff_list[0]] == A[diff_list[1]]:
            return True

        return False
```

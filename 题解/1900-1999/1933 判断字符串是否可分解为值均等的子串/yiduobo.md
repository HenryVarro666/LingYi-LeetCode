---
title: "1933. 判断字符串是否可分解为值均等的子串"
aliases: ["yiduobo的每日leetcode 1933.判断字符串是否可分解为值均等的子串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/623600363"
zhihu_id: "623600363"
zhihu_title: "yiduobo的每日leetcode 1933.判断字符串是否可分解为值均等的子串"
question_id: "1933"
question: "判断字符串是否可分解为值均等的子串"
problem_url: "https://leetcode.cn/problems/check-if-string-is-decomposable-into-value-equal-substrings/"
created: "2023-04-21T02:29:48+08:00"
updated: "2023-04-21T02:29:48+08:00"
upvotes: 0
comments: 2
---

# 1933. 判断字符串是否可分解为值均等的子串

> **[yiduobo的每日leetcode 1933.判断字符串是否可分解为值均等的子串](https://zhuanlan.zhihu.com/p/623600363) · 知乎 · 2023-04-21 · 赞同 0**
> 力扣：[1933. 判断字符串是否可分解为值均等的子串](https://leetcode.cn/problems/check-if-string-is-decomposable-into-value-equal-substrings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1933.判断字符串是否可分解为值均等的子串

[力扣](https://leetcode.cn/problems/check-if-string-is-decomposable-into-value-equal-substrings/)

首先，如果可以成功分解，那么字符串的长度必然是模3余2的。另一方面，对于所有由相同字符构成的连续子串，其要么是某个字符重复了3k次，要么是某个字符重复了3k + 2次，且这个重复3k + 2次的情况只能出现一次。于是只需一趟遍历，使用一个变量flag记录当前是否还没有出现过两字符落单的情况。对于当前位置p而言：

1、满足s[p] \= s[p + 1] \= s[p + 2]：这种情况下直接将p移动到p + 3即可

2、满足s[p] \= s[p + 1]，且flag为true：这种情况下将p移动到p + 2，然后置flag为false

3、其他情况：此时要么s[p]是落单字符，要么s[p]等于s[p + 1]但之前已经有一组长度为2的等值字符串，因此直接返回false

若可以成功遍历完整个字符串，那么就返回true。

最后附上python代码：

```python
class Solution(object):
    def isDecomposable(self, s):
        """
        :type s: str
        :rtype: bool
        """

        n = len(s)
        if n % 3 != 2:
            return False
        
        p = 0
        flag = True
        while p < n:
            if p + 2 < n and s[p] == s[p + 1] == s[p + 2]:
                p += 3
            elif s[p] == s[p + 1] and flag:
                flag = False
                p += 2
            else:
                return False
        
        return True
```

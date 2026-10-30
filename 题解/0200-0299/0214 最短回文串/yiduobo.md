---
title: "214. 最短回文串"
aliases: ["yiduobo的每日leetcode 214.最短回文串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/147957829"
zhihu_id: "147957829"
zhihu_title: "yiduobo的每日leetcode 214.最短回文串"
question_id: "214"
question: "最短回文串"
problem_url: "https://leetcode.cn/problems/shortest-palindrome/"
created: "2020-06-12T22:17:21+08:00"
updated: "2020-06-12T22:17:21+08:00"
upvotes: 1
comments: 0
---

# 214. 最短回文串

> **[yiduobo的每日leetcode 214.最短回文串](https://zhuanlan.zhihu.com/p/147957829) · 知乎 · 2020-06-12 · 赞同 1**
> 力扣：[214. 最短回文串](https://leetcode.cn/problems/shortest-palindrome/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

214.最短回文串<https://leetcode-cn.com/problems/shortest-palindrome/>

题目要求往字符串s前面加尽量少的字符，使得s能成为一个回文串。那么假设在s前面加上了k个字符使得s能成为一个回文串，那么就是最终的s就是下面这种形式：

[XXX....XX][YY...YYY][XXX..XX]

其中，第一个中括号里面的是加上的k个字符，后面两个括号则是字符串s。第一个中括号与最后一个中括号中的k个字符对应，而中间的len(s) - k个字符则是s的一个回文前缀。

例如样例一，在s前面加入了一个字符a，那么就是

[a][aacecaa][a]

其中第二个括号中的aacecaa是s的一个回文前缀。

要使得k尽量的小，实际上就要要让中间括号的子回文串尽可能长，于是题目就变成了求s的最长回文前缀。

一个直观的做法是从后往前扫描，验证以当前字符结尾的前缀是否是回文串，如果是那么就是s的最长回文前缀。不过，普通的判断方法需要O(n)的时间复杂度，那么一趟下来总的时间复杂度就是O(n^2)了，需要想办法优化。

设我们从后往前扫描，当前遇到了s的第p个字符，那么若s[:p]能形成回文串，其中心字符一定位于p/2，那么就需要判断以p/2为中心的最长回文串是否能够到第p个字符。很巧的是，很早之前做过的第五题最长回文子串中，使用马拉车算法计算出的f数组正好就是表示以当前字符为中心的最长回文串的半径是多少（传送门在这里[yiduobo：yiduobo的每日leetcode 5.最长回文子串](https://zhuanlan.zhihu.com/p/113060786)）。

至此就可以得到这样一种处理方法：

1、首先跑一遍马拉车算法，得到s中以每个字符为中心所能得到的最大回文串半径，这里的时间复杂度为O(n)。

2、从后往前扫描，依次检测以当前字符为结尾的前缀是否是回文串。设当前是第p个字符，那么就是检测步骤1中的f[p/2]是否正好等于p/2，如果是，那么说明s[:p]就是要找的回文串，否则s[:p]不是回文串，需要继续往前扫描。扫描的时间复杂度为O(n)，判断的时间复杂度为O(1)，所以这一步的时间复杂度也是O(n)。

3、找到p之后，将s[p:]翻转过来，加在s的前面就是最后的答案。

最终的时间复杂度为O(n)。

需要注意的是，对于长度为偶数的串，回文中心不好确定，于是在这里同样需要沿用第五题中的做法，在字符之间插入特殊字符，使得回文串的长度变成奇数，就可以确定回文中心了。在进行这个操作之后，从后往前扫描时需要注意不要扫描特殊字符。

最后附上python代码，其中第一个for循环中是马拉车算法，求出f数组。第二个while循环则是从后往前扫描，找到最长回文前缀：

```python
class Solution(object):
    def shortestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """

        origial_s = s
        s = '!' + '#'.join(list(s)) + '@'
        f = [0]
        mid = 0
        right = 0
        for index in range(1, len(s) - 1, 1):
            if index < right:
                f.append(min(f[2 * mid - index], right - index))
            else:
                f.append(1)
            while s[index - f[index]] == s[index + f[index]]:
                f[index] += 1
            if right < index + f[index]:
                right = index + f[index]
                mid = index

        end_pos = len(s) - 1
        while end_pos > 1:
            middle_pos = (end_pos + 1) / 2
            if f[middle_pos] == middle_pos:
                return origial_s[middle_pos:][::-1] + origial_s
            end_pos -= 2
        
        return origial_s[1:][::-1] + origial_s
```

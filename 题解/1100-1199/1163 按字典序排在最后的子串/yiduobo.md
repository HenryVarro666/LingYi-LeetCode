---
title: "1163. 按字典序排在最后的子串"
aliases: ["yiduobo的每日leetcode 1163.按字典序排在最后的子串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/379043216"
zhihu_id: "379043216"
zhihu_title: "yiduobo的每日leetcode 1163.按字典序排在最后的子串"
question_id: "1163"
question: "按字典序排在最后的子串"
problem_url: "https://leetcode.cn/problems/last-substring-in-lexicographical-order/"
created: "2021-06-08T23:46:56+08:00"
updated: "2021-06-08T23:46:56+08:00"
upvotes: 1
comments: 0
---

# 1163. 按字典序排在最后的子串

> **[yiduobo的每日leetcode 1163.按字典序排在最后的子串](https://zhuanlan.zhihu.com/p/379043216) · 知乎 · 2021-06-08 · 赞同 1**
> 力扣：[1163. 按字典序排在最后的子串](https://leetcode.cn/problems/last-substring-in-lexicographical-order/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1163.按字典序排在最后的子串

[力扣](https://leetcode-cn.com/problems/last-substring-in-lexicographical-order/)

首先可以明确的一点是，字典序最大的子串必然是一个后缀字符串。证明也很简单，若字典序最大的字符串不是后缀字符串，设其为s[p : q]，那么此时必然有s[q : len(s)]，其是由s[p : q]以及某些字符构成的后缀字符串，那么其字典序必然是大于s[p : q]的，这就产生了矛盾。

既然得知了答案必然是某个后缀字符串，那么一个很自然的想法就是利用后缀数组对所有后缀进行排序，然后输出最后一个。不过在这里也有更简洁的做法，直接枚举答案后缀字符串的起始字符位置res，然后从now \= res + 1开始对比s[res:]与s[now:]的字典序大小。对比的方法自然是逐个比较对应位置上字符的大小，因此还需要设l为当前两个字符串对比的位置偏移：

1、若s[res + l] \= s[now + l]，那么无法判断s[res:]与s[now:]的顺序，需要继续向后判断，因此此时需要l加上1之后继续检测。

2、若s[res] \< s[now + l]，此时说明s[res:]的字典序小于s[now + l:]，同时这里还有一个隐藏条件，就是在res + 1到now + l - 1之间不存在位置p满足s[res] \<s[p]，可以分两种情况讨论来进行证明：

若res \< p \< res + l \< now，那么我们在检测以p开头的后缀时就已经知道res不是最终答案了，而不可能一直向后检测到now这个位置

若res \< now \< p \< res + l，那么对于s[now : p + 1]这一段，从res开始必然也有一段与之对应，那么必然也存在某个q，满足res \< q \< now且res[q] \= res[p]，那么与上面类似，我们在检测以q开头的后缀时就已经知道res不是最终答案了，不可能一直向后检测到now这个位置。

根据以上两点，说明res + 1到now + l - 1之间不存在p满足s[res] \< s[p]，因此此时我们可以直接将res移动到now + l，同时重置now等于now + l + 1，l\=0，表示当前备选答案res变成了now + l，而此时应当从now + l + 1开始向后进行检测。

3、若s[res + l] \< s[now + l]，此时说明s[res:]的字典序是小于s[now:]的字典序的，因此应该将备选答案res置为now，同时将now置为now + 1，l置为0。

4、若s[res + l] > s[now + l]，此时说明s[res:]的字典序是大于s[now:]的字典序的。根据情况2中证明的两点，因此应该将now置为now + l + 1，l置为0，然后继续向后进行检测。

最后附上python代码：

```python
class Solution(object):
    def lastSubstring(self, s):
        """
        :type s: str
        :rtype: str
        """

        res = 0
        now = 1
        l = 0
        while now + l < len(s):
            if s[res + l] == s[now + l]:
                l += 1
            elif s[res] < s[now + l]:
                res = now + l
                now = res + 1
                l = 0
            elif s[res + l] < s[now + l]:
                res = now
                now += 1
                l = 0
            else:
                now += l + 1
                l = 0

        return s[res:]
```

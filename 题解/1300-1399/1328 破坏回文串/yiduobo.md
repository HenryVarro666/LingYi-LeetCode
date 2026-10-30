---
title: "1328. 破坏回文串"
aliases: ["yiduobo的每日leetcode 1328.破坏回文串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/394476493"
zhihu_id: "394476493"
zhihu_title: "yiduobo的每日leetcode 1328.破坏回文串"
question_id: "1328"
question: "破坏回文串"
problem_url: "https://leetcode.cn/problems/break-a-palindrome/"
difficulty: "Medium"
rating: 1474
created: "2021-07-29T23:36:48+08:00"
updated: "2021-07-29T23:36:48+08:00"
upvotes: 0
comments: 0
---

# 1328. 破坏回文串

> **[yiduobo的每日leetcode 1328.破坏回文串](https://zhuanlan.zhihu.com/p/394476493) · 知乎 · 2021-07-29 · 赞同 0**
> 力扣：[1328. 破坏回文串](https://leetcode.cn/problems/break-a-palindrome/) · Medium · 灵茶山艾府：[贪心（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1328.破坏回文串

[力扣](https://leetcode-cn.com/problems/break-a-palindrome/)

题目要求修改回文串中的一个字符，使得新串不再是回文串，同时字典序最小。

首先，对于一个回文串，若其长度为奇数，那么我们不能修改正中间的字符，例如样例中的aba，我们不能修改中间的b。而对于其他情况，修改任意字符都可以使得这个字符串变成非回文串。

接下来，为了使得新串字典序最小，因此我们应当从高位向下扫描，若当前字符不是a，那么就将其修改成a，否则继续向后扫描。另外，由于原始字符串是回文串，因此我们只需要检测前半部分，若其中有不是a的字符，那么就已经找到了答案。

若我们扫描玩前半部分之后没有找到答案，则说明前半部分全都是a。又由于原始字符串为回文串，因此后半部分也必然都是a，也就是说，若当字符串长度为偶数时，字符串全是a，当长度为奇数时，除了正中间的字符之外其他全都是a。对于这两种情况，我们只需将最后一个字符修改成b即可。

最后附上python代码：

```python
class Solution(object):
    def breakPalindrome(self, palindrome):
        """
        :type palindrome: str
        :rtype: str
        """

        n = len(palindrome)

        if n == 1:
            return ""
        
        for index in range(n / 2):
            if palindrome[index] != 'a':
                return palindrome[:index] + 'a' + palindrome[index + 1:]
        
        return palindrome[:n - 1] + 'b'
```

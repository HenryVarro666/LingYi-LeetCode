---
title: "1415. 长度为n的开心字符串中字典序第k小的字符串"
aliases: ["yiduobo的每日leetcode 1415.长度为n的开心字符串中字典序第k小的字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "题单/链表-二叉树与回溯", "题单/位运算", "题单/链表-二叉树与回溯/四-回溯", "题单/位运算/九-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/406885310"
zhihu_id: "406885310"
zhihu_title: "yiduobo的每日leetcode 1415.长度为n的开心字符串中字典序第k小的字符串"
question_id: "1415"
question: "长度为 n 的开心字符串中字典序第 k 小的字符串"
problem_url: "https://leetcode.cn/problems/the-k-th-lexicographical-string-of-all-happy-strings-of-length-n/"
difficulty: "Medium"
rating: 1576
created: "2021-09-04T21:41:53+08:00"
updated: "2021-09-04T21:41:53+08:00"
upvotes: 0
comments: 0
---

# 1415. 长度为n的开心字符串中字典序第k小的字符串

> **[yiduobo的每日leetcode 1415.长度为n的开心字符串中字典序第k小的字符串](https://zhuanlan.zhihu.com/p/406885310) · 知乎 · 2021-09-04 · 赞同 0**
> 力扣：[1415. 长度为 n 的开心字符串中字典序第 k 小的字符串](https://leetcode.cn/problems/the-k-th-lexicographical-string-of-all-happy-strings-of-length-n/) · Medium · 灵茶山艾府：[O(n) 简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1415.长度为n的开心字符串中字典序第k小的字符串

[力扣](https://leetcode-cn.com/problems/the-k-th-lexicographical-string-of-all-happy-strings-of-length-n/)

首先，以a、b、c开头的开心字符串的数目是一样多的，因此不妨先考虑以a开始的开心字符串的数目。

令f[n]表示以a开头，长度为n的开心字符串的数目，那么首先有f[1] \= 1。

接下来对于f[n - 1]中的任意开心字符串而言，其末尾字符必然是a、b、c之一，那么对于以a结尾的长度为n - 1的开心字符串，我们可以在其后面加上b或c形成长度为n的开心字符串，对于以b或c结尾的开心字符串也一样，因此就有f[n] \= f[n - 1] + f[n - 1]。

这样一来，一共有f[n] \* 3种开心字符串。其中以a、b、c开头的开心字符串都是f[n]种。那么此时可以得到一个结论是，如果对f[n] \* 3中开心字符串按字典序排列，那么

以a开头的开心字符串的顺序为1到f[n]，以b开头的开心字符串的顺序为f[n] + 1到f[n] + f[n]，而以c开头的开心字符串的顺序则是f[n] + f[n] + 1到f[n] \* 3

那么我们就可以根据k落在那个区间来判断答案的首位字符是什么。确定了首位字符之后，之后的字符就只有两种可行的方法，不过也可以用同样的方法，通过此时更新过的k以及f[n - 1]来确定。重复这个过程，直到确定最后一位字符为止。

例如样例5来举例：

首先我们计算出f，分别为

f[1] \= 1，f[2] \= 2，f[3] \= 4，f[4] \= 8，f[5] \= 16，

f[6] \= 32，f[7] \= 64，f[8] \= 128，f[9] \= 256，f[10] \= 512

接下来：

1、选择首位字符。此时的n \= 10，有f[n] \= 512，满足k \= 100 \<\= f[n]，因此首字符为'a'。此时的k无需更新。

2、第二位字符。由于上一位字符为'a'，因此这一位字符只能是'b'或者'c'。此时的n \= 9，有f[n] \= 256，满足k \= 100 \<\= f[n]，因此应该选择较小的那一种备选字符，即'b'。此时的k无需更新

3、第三位字符。由于上一位字符为'b'，因此这一位字符只能是'a'或者'c'。此时的n \= 8，有f[n] \= 128，满足k \= 100 \<\= f[n]，因此应该选择较小的那一种备选字符，即'a'。此时的k无需更新

4、第四位字符。由于上一位字符为'a'，因此这一位字符只能是'b'或者'c'。此时的n \= 7，有f[n] \= 64，满足k \= 100 > f[n]，因此应该选择较大的那一种备选字符，即'c'。此时的k需要更新为k \= k - f[n] \= 100 - 64 \= 36

5、第五位字符。由于上一位字符为'c'，因此这一位字符只能是'a'或者'b'。此时的n \= 6，有f[n] \= 32，满足k \= 36 > f[n]，因此应该选择较大的那一种备选字符，即'b'。此时的k需要更新为k \= k - f[n] \= 36 - 32 \= 4

6、第六位字符。由于上一位字符为'b'，因此这一位字符只能是'a'或者'c'。此时的n \= 5，有f[n] \= 16，满足k \= 4 \<\= f[n]，因此应该选择较小的那一种备选字符，即'a'。此时的k无需更新

7、第七位字符。由于上一位字符为'a'，因此这一位字符只能是'b'或者'c'。此时的n \= 4，有f[n] \= 8，满足k \= 4 \<\= f[n]，因此应该选择较小的那一种备选字符，即'b'。此时的k无需更新

8、第八位字符。由于上一位字符为'b'，因此这一位字符只能是'a'或者'c'。此时的n \= 3，有f[n] \= 4，满足k \= 4 \<\= f[n]，因此应该选择较小的那一种备选字符，即'a'。此时的k无需更新

9、第九位字符。由于上一位字符为'a'，因此这一位字符只能是'b'或者'c'。此时的n \= 2，有f[n] \= 2，满足k \= 4 > f[n]，因此应该选择较大的那一种备选字符，即'c'。此时的k需要更新为k \= k - f[n] \= 4 - 2 \= 2

10、最后一位字符。由于上一位字符为'c'，因此这一位字符只能是'a'或者'b'。此时的n \= 1，有f[n] \= 1，满足k \= 2 > f[n]，因此应该选择较大的那一种备选字符，即'b'

至此，就得到了最终答案，为'abacbabacb'

最后附上python代码：

```python
class Solution(object):
    def getHappyString(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: str
        """

        p = [1, 1]
        for index in range(2, n + 1):
            p.append(p[-1] + p[-1])

        last = ''
        if p[n] * 3 < k:
            res = ""
        else:
            if k > p[n] + p[n]:
                res = 'c'
                last = 'c'
                k -= p[n] + p[n]
            elif k > p[n]:
                res = 'b'
                last = 'b'
                k -= p[n]
            else:
                res = 'a'
                last = 'a'

            n -= 1
            while n > 0:
                if k > p[n]:
                    if last == 'c':
                        res += 'b'
                        last = 'b'
                    else:
                        res += 'c'
                        last = 'c'
                    k -= p[n]
                else:
                    if last == 'a':
                        res += 'b'
                        last = 'b'
                    else:
                        res += 'a'
                        last = 'a'
                
                n -= 1
        
        return res
```

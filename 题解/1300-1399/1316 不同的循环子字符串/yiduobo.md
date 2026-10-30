---
title: "1316. 不同的循环子字符串"
aliases: ["yiduobo的每日leetcode 1316.不同的循环子字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/392945837"
zhihu_id: "392945837"
zhihu_title: "yiduobo的每日leetcode 1316.不同的循环子字符串"
question_id: "1316"
question: "不同的循环子字符串"
problem_url: "https://leetcode.cn/problems/distinct-echo-substrings/"
created: "2021-07-25T13:06:03+08:00"
updated: "2021-07-25T13:06:03+08:00"
upvotes: 1
comments: 2
---

# 1316. 不同的循环子字符串

> **[yiduobo的每日leetcode 1316.不同的循环子字符串](https://zhuanlan.zhihu.com/p/392945837) · 知乎 · 2021-07-25 · 赞同 1**
> 力扣：[1316. 不同的循环子字符串](https://leetcode.cn/problems/distinct-echo-substrings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1316.不同的循环子字符串

[力扣](https://leetcode-cn.com/problems/distinct-echo-substrings/)

题目要求找出所有不同的，且可以写成某个子串重复一次的字符串。由于这里的text长度最多只有2000，那么一个可行的做法是先枚举答案字符串前半部分的长度l，再枚举前半部分的起点i。这样一来，前半部分就是text[i : i + l]，而后半部分则是text[i + l : i + l + l]。

接下来，若前半部分和后半部分相同，说明text[i : i + l + l + 1]就是一个合法的答案。但是这里还需要去重，因此需要使用一个哈希表来储存所有已经使用过的前半部分。

至于比较text[i : i + l]是否与text[i + l : i + l + l]相等，一个常见的做法就是哈希。简单来说，我们可以将字符串看做一个26进制数字进行解码，但是当字符串长度较长时，直接解码得到的数字太大，因此需要对其取模做哈希。当有了取模操作之后，这里的26进制可能就会有哈希冲突，因此我们可以选择一个大于26的质数作为进制，我在这里采用的是29进制。

例如样例中的abcabc，编码方式如下：

a -> 0

ab -> 0 \* 29 + 1 \= 1

abc -> 1 \* 29 + 2 \= 31

abca -> 31 \* 29 + 0 \= 899

abcab -> 899 \* 29 + 1 \= 26072

abcabc -> 26072 \* 29 + 2 \= 756090

那么这里左侧的abc编码为31，而右侧abc的编码则可以认为是

abcabc \= abc000 + abc

也就是abc \* 29^3 + abc

那么我们可以使用类似前缀和的做法，即

abc \= abcabc - abc000 \= 756090 - abc \* 29^3 \= 31

于是我们可以先一趟扫描，预处理出前缀解码数组s，其中s[i]表示将text[:i + 1]按照29进制解码得到的答案，那么对于text[i : i + l]以及text[i + l : i + l + l]而言，二者的解码就是

text[i : i + l] \= s[i + l - 1] - s[i - 1] \* 29^l

以及

text[i + l : i + l + l] \= s[i + l + l - 1] - s[i + l - 1] \* 29^l

当然，这里的解码计算会非常大，因此在过程中需要对一个大质数取模做哈希，我在这里用的是leetcode最喜欢的mod \= 10^9 + 7，于是这里解码的式子就变成了

text[i : i + l] \= (s[i + l - 1] - s[i - 1] \* 29^l % mod + mod) % mod

text[i + l : i + l + l] \= (s[i + l + l - 1] - s[i + l - 1] \* 29^l % mod + mod) % mod

最后附上python代码：

```python
class Solution(object):
    def distinctEchoSubstrings(self, text):
        """
        :type text: str
        :rtype: int
        """

        n = len(text)
        s = [ord(text[0]) - 97]
        mod = 10 ** 9 + 7
        for char in text[1:]:
            s.append((s[-1] * 29 + ord(char) - 97) % mod)

        res = 0
        power = 1
        for l in range(1, n / 2 + 1):
            power = power * 29 % mod
            used = set()
            for i in range(n - l - l + 1):
                j = i + l - 1
                if i == 0:
                    v = s[j]
                else:
                    v = (s[j] - s[i - 1] * power % mod + mod) % mod
                
                if v not in used:
                    next_i = j + 1
                    next_j = next_i + l - 1
                    next_v = (s[next_j] - s[next_i - 1] * power % mod + mod) % mod
                    if v == next_v:
                        res += 1
                        used.add(v)

        return res
```

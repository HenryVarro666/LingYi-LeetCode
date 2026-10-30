---
title: "2802. 找出第K个幸运数字"
aliases: ["yiduobo的每日leetcode 2802.找出第K个幸运数字"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/657495285"
zhihu_id: "657495285"
zhihu_title: "yiduobo的每日leetcode 2802.找出第K个幸运数字"
question_id: "2802"
question: "找出第K个幸运数字"
problem_url: "https://leetcode.cn/problems/find-the-k-th-lucky-number/"
created: "2023-09-21T04:08:13+08:00"
updated: "2023-09-21T04:08:13+08:00"
upvotes: 0
comments: 0
---

# 2802. 找出第K个幸运数字

> **[yiduobo的每日leetcode 2802.找出第K个幸运数字](https://zhuanlan.zhihu.com/p/657495285) · 知乎 · 2023-09-21 · 赞同 0**
> 力扣：[2802. 找出第K个幸运数字](https://leetcode.cn/problems/find-the-k-th-lucky-number/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2802.找出第K个幸运数字

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/find-the-k-th-lucky-number/description/)

由于每一位上都有4和7两种选择，那么对于一个长度为n为的幸运数字来说，其一共有2^n中可能。于是可以先将所有小于等于k的2^n都预处理出来，然后通过计算K落在2^n的前半部分，也就是0到2^(n - 1) - 1中，还是落在2^(n - 1) - 1到2^n - 1中，从而确定出答案的最高为，同时迭代计算出新的K。

另一种更优美的做法就是将其视为某种特殊的二进制表示。需要注意的是，常规二进制表示是不能出现00这种数的，因此在这里需要一些特殊处理，即将4视为1，而7则视为没有进位的2，那么类比下来，就有

4 \= 1(b)

7 \= 2(b) \= 10(b)

44 \= 11(b)

47 \= 12(b) \= 20(b) \= 100(b)

74 \= 21(b) \= 101(b)

77 \= 22(b) \= 110(b)

444 \= 111(b)

447 \= 112(b) \= 120(b) \= 210(b) \= 1000(b)

474 \= 121(b) \= 201(b) \= 1001(b)

477 \= 122(b) \= 210(b) \= 1010(b)

744 \= 211(b) \= 1011(b)

747 \= 212(b) \= 1020(b) \= 1100(b)

774 \= 221(b) \= 1101(b)

777 \= 222(b) \= 1110(b)

以此类推

可以发现，这种表示方法虽然比较奇怪，但是处理好7对应的进位后实际上与常规的二进制表示是完全相同的，也就是说只需将k的二进制表示计算出来就可以还原出4和7组成的字符串了。

需要注意的是，由于7在这里表示的是2而不是0，因此当k是2的倍数时，此时除了往答案中加入一个7之外，还需要先将k减去2之后，再将k除以2；反之若k不是2的倍数时，往答案中填充一个4，然后按照常规方法将k除以2即可。另外不要忘了通过模2取余的方法得到的二进制表示是反过来的，最后需要倒转后返回。

最后附上python代码：

```python
class Solution(object):
    def kthLuckyNumber(self, k):
        """
        :type k: int
        :rtype: str
        """

        res = []
        while k:
            v = k % 2
            if v == 0:
                res.append('7')
                k -= 2
            else:
                res.append('4')
            
            k /= 2

        return ''.join(res[::-1])
```

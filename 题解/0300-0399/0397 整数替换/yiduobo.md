---
title: "397. 整数替换"
aliases: ["yiduobo的每日leetcode 397.整数替换"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/180504903"
zhihu_id: "180504903"
zhihu_title: "yiduobo的每日leetcode 397.整数替换"
question_id: "397"
question: "整数替换"
problem_url: "https://leetcode.cn/problems/integer-replacement/"
created: "2020-08-11T20:34:39+08:00"
updated: "2020-08-11T20:34:39+08:00"
upvotes: 0
comments: 0
---

# 397. 整数替换

> **[yiduobo的每日leetcode 397.整数替换](https://zhuanlan.zhihu.com/p/180504903) · 知乎 · 2020-08-11 · 赞同 0**
> 力扣：[397. 整数替换](https://leetcode.cn/problems/integer-replacement/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

397.整数替换<https://leetcode-cn.com/problems/integer-replacement/>

找规律的题目。注意到题目中的三种操作为除以2，加1，减1，那么很自然就联想的位操作。

对于一个数n，若其为偶数，那么没有操作的余地，直接除以2。若其为奇数，那么一定可以写成XXXX11...111这种形式。

设n的末尾有k个1，那么：

若k\=1，那么n是XXXX01的形式，那么此时执行减1的话，总共需要三次操作才能得到XXXX。如果执行加1的话，则需要四次操作才能得到XXXX或者XXXX + 1。即使XXXX + 1才是此时的全局最优，在执行减1得到XXXX之后再执行加1，同样是4次操作，因此对于k \= 1的情况，执行减1是最优的。

若k > 1，那么n是XXXX011..11的形式。

此时执行加1的话，总共需要1 + k + 2次操作才能得到XXXX，具体为

XXXX011..111 -> XXXX100..000 -> XXXX1 -> XXXX0 -> XXXX

此时执行减1的话，则需要2k + 1次操作才能得到XXXX。

此时执行加1是最优的。

需要注意的是，这里有一个特例就是3。由于3在二进制中是11，因此XXXX011..1中的0实际上是不需要进行操作的，因此在这里应该执行减1。

到了这里，就有一种做法了。对于n，若其为偶数，那么直接除以2。若其为奇数，当其模4等于3，即末尾为11，且n本身不等于3时，执行加1操作，否则执行减1操作。

最后附上python代码：

```python
class Solution(object):
    def integerReplacement(self, n):
        """
        :type n: int
        :rtype: int
        """

        res = 0

        while n != 1:
            while n % 2 == 0:
                res += 1
                n /= 2
            if n == 1:
                break
                
            if n % 4 == 3 and n != 3:
                n += 1
            else:
                n -= 1
            res += 1

        return res
```

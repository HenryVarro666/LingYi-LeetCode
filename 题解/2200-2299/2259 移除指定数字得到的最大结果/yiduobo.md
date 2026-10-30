---
title: "2259. 移除指定数字得到的最大结果"
aliases: ["yiduobo的每日leetcode 2259.移除指定数字得到的最大结果"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "题单/贪心算法", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/548084279"
zhihu_id: "548084279"
zhihu_title: "yiduobo的每日leetcode 2259.移除指定数字得到的最大结果"
question_id: "2259"
question: "移除指定数字得到的最大结果"
problem_url: "https://leetcode.cn/problems/remove-digit-from-number-to-maximize-result/"
difficulty: "Easy"
created: "2022-07-30T23:51:59+08:00"
updated: "2022-07-30T23:52:09+08:00"
upvotes: 0
comments: 0
---

# 2259. 移除指定数字得到的最大结果

> **[yiduobo的每日leetcode 2259.移除指定数字得到的最大结果](https://zhuanlan.zhihu.com/p/548084279) · 知乎 · 2022-07-30 · 赞同 0**
> 力扣：[2259. 移除指定数字得到的最大结果](https://leetcode.cn/problems/remove-digit-from-number-to-maximize-result/) · Easy · 灵茶山艾府：[暴力（附 Python 一行）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2259.移除指定数字得到的最大结果

[力扣](https://leetcode.cn/problems/remove-digit-from-number-to-maximize-result/)

首先，移除的位置越靠近高位，对结果的影响就越大。因此在执行移除时应该遵循一个原则，如果存在若干种较优的移除方式，那么就应该选择影响最大的，也就是最靠近高位的数字来进行移除。反过来，如果所有移除都是不优的，同时又必须执行一次移除，那么就应该选择影响最小的，也就是最靠近低位的数字来进行移除。

接下来考察什么是较优的移除，什么是不优的移除。不妨设两种移除方案移除的位置分别为p和q，且p \< q，那么将原始数字的各个数位展开来写就是

num[0], num[1], ..., num[p - 1], num[p], num[p + 1], ..., num[q - 1], num[q], num[q + 1], ..., num[n - 1]

在移除了p之后，得到的数位分布可以分成三个部分，

高位上为 num[0], num[1], ..., num[p - 1]

中间部分为 num[p + 1], ..., nums[q - 1], num[q]

低位为 num[q + 1], num[q + 2], ..., num[n - 1]

而在移除了q之后，得到的为

高位上为num[0], num[1], ..., nums[p - 1]

中间部分为 num[p], num[p + 1], ..., num[q - 1]

低位为 num[q + 1], num[q + 2], ..., num[n - 1]

可以发现，二者的差别实际上就是中间部分，而这两部分的大小比较则取决于num[p]和num[p + 1]的大小关系。也就是说当num[p]小于num[p + 1]时，无论后面q的位置如何，移除后都可以得到更好的结果。反过来，若num[p]大于num[p + 1]，那么就不应该执行移除。对于num[p] \= num[p + 1]这种特殊情况，移除num[p]和移除num[p + 1]是等价的，因此可以跳过这次操作，向后考虑是否需要替换num[p + 1]。

到了这里就得到了一种算法。从左向右一趟遍历，对于所有等于digit的数位p，若num[p] \< num[p + 1]，那么就将num[p]移除，然后返回剩余的字符串，否则就继续向后遍历。如果遍历完成后都没有执行过移除，那么就只能被迫移除最后一个等于digit的字符了。

最后附上python代码：

```python
class Solution(object):
    def removeDigit(self, number, digit):
        """
        :type number: str
        :type digit: str
        :rtype: str
        """

        n = len(number)
        p = None
        for index in range(n):
            if number[index] == digit:
                p = index
                if index < n -1 and number[index] < number[index + 1]:
                    break
        
        return number[:p] + number[p + 1:]
```

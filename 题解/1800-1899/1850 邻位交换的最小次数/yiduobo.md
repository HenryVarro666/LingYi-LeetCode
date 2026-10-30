---
title: "1850. 邻位交换的最小次数"
aliases: ["yiduobo的每日leetcode 1850.邻位交换的最小次数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/471047579"
zhihu_id: "471047579"
zhihu_title: "yiduobo的每日leetcode 1850.邻位交换的最小次数"
question_id: "1850"
question: "邻位交换的最小次数"
problem_url: "https://leetcode.cn/problems/minimum-adjacent-swaps-to-reach-the-kth-smallest-number/"
created: "2022-02-22T23:42:31+08:00"
updated: "2022-02-22T23:42:31+08:00"
upvotes: 0
comments: 0
---

# 1850. 邻位交换的最小次数

> **[yiduobo的每日leetcode 1850.邻位交换的最小次数](https://zhuanlan.zhihu.com/p/471047579) · 知乎 · 2022-02-22 · 赞同 0**
> 力扣：[1850. 邻位交换的最小次数](https://leetcode.cn/problems/minimum-adjacent-swaps-to-reach-the-kth-smallest-number/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1850.邻位交换的最小次数

[力扣](https://leetcode-cn.com/problems/minimum-adjacent-swaps-to-reach-the-kth-smallest-number/)

题目首先需要找出一个排列的之后的第k个排列，然后判断需要多少次相邻数的交换才能使得原排列变为之后的第k个排列。

首先，对于求解某个排列之后的第k个排列，可以使用康拓展开，也可以按照寻找某个排列的下一个排列的做法执行k次。在这里由于字符串长度达到1000，那么如果使用康托展开，理论上需要计算1000阶乘这种规模的值，免不了要高精度乘法和高精度除法。虽然在时间复杂度上比较好但是实现起来太麻烦了。由于这里的数据规模并不大，那么执行k次O(n)的寻找下一个排列完全是可行的。

具体如何寻找某个排列的下一个排列这里就不展开了，印象中第一页的题目中应该有一个道题目就是要求解这个。

接下来，现在得到了之后的第k个排列，需要将原排列转换过去。那么在这里可以从头开始向后一趟遍历，若原排列中的某个位置上的字符与之后第k个排列上对应的字符不同，那么就需要将后面的某个相同字符交换过来。在这里一个直观的想法就是将最近的相同字符交换过来，这样做的原因是如果不交换最近的相同字符，那么最近的相同字符与实际交换的字符之间的字符也会发生交换，而这个交换很可能是没有必要执行的。而如果有必要执行，那么先交换最近的字符，再交换当前这个字符也是可行的。

对于这个字符交换问题，一个经典的做法就是将其视为排队，将这些数字插入到空位上去。这样一来就可以利用树状数组维护每个数字左侧有多少个数字已经进行过交换，从而计算出当前数字在遍历到的这一时刻所处的实际位置，从而计算出该数字需要执行的交换次数。

不过在这里，由于前一步的时间复杂度已经是O(kn)了，那么这一步直接使用O(n^2)的算法模拟交换就可以了。

最后附上python代码：

```python
class Solution(object):
    def getMinSwaps(self, num, k):
        """
        :type num: str
        :type k: int
        :rtype: int
        """

        now = list(num)
        n = len(now)
        for _ in range(k):
            for index in range(n - 2, -1, -1):
                if now[index] < now[index + 1]:
                    p = index + 1
                    while p < n and now[p] > now[index]:
                        p += 1
                    p -= 1
                    now[index], now[p] = now[p], now[index]
                    l = index + 1
                    r = n - 1
                    while l < r:
                        now[l], now[r] = now[r], now[l]
                        l += 1
                        r -= 1
                    break
        
        origin = list(num)
        res = 0
        for index in range(n):
            if origin[index] != now[index]:
                p = index + 1
                last = now[index]
                res += 1
                while p < n and now[p] != origin[index]:
                    now[p], last = last, now[p]
                    p += 1
                    res += 1
                now[p] = last

        return res
```

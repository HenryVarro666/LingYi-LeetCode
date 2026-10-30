---
title: "2513. 最小化两个数组中的最大值"
aliases: ["yiduobo的每日leetcode 2513.最小化两个数组中的最大值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/binary-search", "leetcode/number-theory", "题单/二分算法", "题单/数学算法", "题单/二分算法/二-二分答案", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/634317075"
zhihu_id: "634317075"
zhihu_title: "yiduobo的每日leetcode 2513.最小化两个数组中的最大值"
question_id: "2513"
question: "最小化两个数组中的最大值"
problem_url: "https://leetcode.cn/problems/minimize-the-maximum-of-two-arrays/"
difficulty: "Medium"
rating: 2302
created: "2023-06-05T16:16:26+08:00"
updated: "2023-06-05T16:16:26+08:00"
upvotes: 0
comments: 0
---

# 2513. 最小化两个数组中的最大值

> **[yiduobo的每日leetcode 2513.最小化两个数组中的最大值](https://zhuanlan.zhihu.com/p/634317075) · 知乎 · 2023-06-05 · 赞同 0**
> 力扣：[2513. 最小化两个数组中的最大值](https://leetcode.cn/problems/minimize-the-maximum-of-two-arrays/) · Medium · 灵茶山艾府：[两种方法：二分答案 / 数学公式](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2513.最小化两个数组中的最大值

[力扣](https://leetcode.cn/problems/minimize-the-maximum-of-two-arrays/)

为了是的最终答案最小，那么就应该将所有小于等于这个答案的正整数都充分利用起来。

对于这些正整数，可以分成四类：

1、可以同时被divisor1和divisor2整除的：

这类整数是不能加入arr1和arr2的，只能丢弃

2、可以被divisor1整除但不能被divisor2整除的：

这类整数只能加入到arr2中

3、可以被divisor2整除但不能被divisor1整除的：

这类整数只能加入到arr1中

4、既不能被divisor1整除，也不能被divisor2整除的：

这类整数可以加入到arr1或arr2中的其中一个

那么对于上面几类整数，很明显就应该先使用第二类和第三类整数优先填充arr2以及arr1，若不够，再从第四类整数中抽出一部分去填充不足的数组。

对于某个整数k：

1、第一类整数的数目为k / lcm，其中lcm为divisor1与divisor2的最小公倍数

2、第二类整数的数目为k / divisor1 - k / lcm，若这个数大于等于uniqueCnt2，那么就无需再使用第四类整数，否则就需要uniqueCnt2 - (k / divisor1 - k / lcm)个整数来填补空缺

3、第三类整数的数目为k / divisor2 - k / lcm，若这个数大于等于uniqueCnt1，那么就无需再使用第四类整数，否则就需要uniqueCnt1 - (k / divisor2 - k / lcm)个整数来填补空缺

4、第四类整数的数目就是k减去上面三类整数的数目之和，也就是k - (k / divisor1 + k / divisor2 - k / lcm)，若这个数大于等于需要用来填补空缺的数的数目，那么k就是一个可行解

注意到题目的k越大，可行性就越高，因此在这里可以二分答案，通过上面描述的计算方法检测当前二分的值是否可以得到可行解并调整二分边界即可。

最后附上python代码：

```python
class Solution(object):
    def minimizeSet(self, divisor1, divisor2, uniqueCnt1, uniqueCnt2):
        """
        :type divisor1: int
        :type divisor2: int
        :type uniqueCnt1: int
        :type uniqueCnt2: int
        :rtype: int
        """

        x, y = divisor1, divisor2
        while y > 0:
            x, y = y, x % y
        
        lcm = divisor1 * divisor2 / x

        left = 1
        right = (uniqueCnt1 + uniqueCnt2) * 2 + 1

        while left < right:
            mid = (left + right) >> 1
            cnt1 = mid / divisor2 - mid / lcm
            cnt2 = mid / divisor1 - mid / lcm

            cnt = max(0, uniqueCnt1 - cnt1) + max(0, uniqueCnt2 - cnt2)

            if cnt + mid / divisor1 + mid / divisor2 - mid / lcm <= mid:
                right = mid
            else:
                left = mid + 1
        
        return left
```

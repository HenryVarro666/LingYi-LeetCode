---
title: "1363. 形成三的最大倍数"
aliases: ["yiduobo的每日leetcode 1363.形成三的最大倍数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/399736341"
zhihu_id: "399736341"
zhihu_title: "yiduobo的每日leetcode 1363.形成三的最大倍数"
question_id: "1363"
question: "形成三的最大倍数"
problem_url: "https://leetcode.cn/problems/largest-multiple-of-three/"
created: "2021-08-14T14:32:16+08:00"
updated: "2021-08-14T14:32:16+08:00"
upvotes: 2
comments: 0
---

# 1363. 形成三的最大倍数

> **[yiduobo的每日leetcode 1363.形成三的最大倍数](https://zhuanlan.zhihu.com/p/399736341) · 知乎 · 2021-08-14 · 赞同 2**
> 力扣：[1363. 形成三的最大倍数](https://leetcode.cn/problems/largest-multiple-of-three/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1363.形成三的最大倍数

[力扣](https://leetcode-cn.com/problems/largest-multiple-of-three/)

3的倍数都满足各个位上数字加起来也是3的倍数，那么我们可以通过这个来选择应该使用哪些数字。为了使得最终答案最大，我们首先应该保证使用的数字尽量多，然后对于使用的数字，我们应该让较大的数字尽量排在高位上，因此在选择数字时也应当尽可能选择较大的数字。

首先，计算出所有数字的和s，那么对于s：

1、s是3的倍数，那么此时应该选择所有数字，并按从大到小的顺序进行排列

2、s模3余1，此时：

2-1）若存在模3余1的数字，那么我们应该从中选择最小的那个将其移除，然后将剩下的数字按从大到小的顺序排列

2-2）若不存在模3余1的数字，那么我们应该从中选择最小的两个模3余2的数字将其移除，这里可以证明必然是存在的，因为若不存在模3余1和模3余2的数字，那么说明所有数字都是3的倍数，那么s必然是3的倍数，产生了矛盾。

同样地，移除之后将剩下的数字按从大到小的顺序排列

3、s模3余2，与情况2类似：

3-1）若存在模3余2的数字，那么我们同样是从中选择最小的那个将其移除，然后将剩下的数字按从大到小的顺序排列

3-2)若不存在模3余2的数字，那么我们应该从中选择最小的两个模3余1的数字将其移除，然后将剩下的数字按从大到小的顺序排列

另外，处理完成之后还需要特别判断是否有前缀0的情况。由于上面所有的答案都是将数字从大到小排列得到的，那么若有前缀0，只可能是所有数字都是0，特别判断这种情况即可。

最后附上python代码：

```python
class Solution(object):
    def largestMultipleOfThree(self, digits):
        """
        :type digits: List[int]
        :rtype: str
        """

        digits = sorted(digits, reverse=True)
        s = 0
        p1_1 = None
        p1_2 = None
        p2_1 = None
        p2_2 = None
        char_list = [chr(x + 48) for x in digits]
        for index in range(len(digits) - 1, -1, -1):
            s += digits[index]
            if digits[index] % 3 == 1:
                if p1_1 is None:
                    p1_1 = index
                elif p1_2 is None:
                    p1_2 = index
            
            if digits[index] % 3 == 2:
                if p2_1 is None:
                    p2_1 = index
                elif p2_2 is None:
                    p2_2 = index

        if s % 3 == 0:
            res = ''.join(char_list)
        
        elif s % 3 == 1:
            if p1_1 is not None:
                res = ''.join(char_list[:p1_1]) + ''.join(char_list[p1_1 + 1:])
                s -= digits[p1_1]
            elif p2_1 is not None and p2_2 is not None:
                res = ''.join(char_list[:p2_2]) + ''.join(char_list[p2_2 + 1 : p2_1]) + ''.join(char_list[p2_1 + 1:])
                s -= digits[p2_1] + digits[p2_2]
            else:
                res = ''

        else:
            if p2_1 is not None:
                res = ''.join(char_list[:p2_1]) + ''.join(char_list[p2_1 + 1:])
                s -= digits[p2_1]
            elif p1_1 is not None and p1_2 is not None:
                res = ''.join(char_list[:p1_2]) + ''.join(char_list[p1_2 + 1 : p1_1]) + ''.join(char_list[p1_1 + 1:])
                s -= digits[p1_1] + digits[p1_2]
            else:
                res = ''
        
        if len(res) > 1 and s == 0:
            return '0'
        
        return res
```

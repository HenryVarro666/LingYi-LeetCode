---
title: "1088. 易混淆数II"
aliases: ["yiduobo的每日leetcode 1088.易混淆数II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/609256694"
zhihu_id: "609256694"
zhihu_title: "yiduobo的每日leetcode 1088.易混淆数II"
question_id: "1088"
question: "易混淆数II"
problem_url: "https://leetcode.cn/problems/confusing-number-ii/"
created: "2023-02-24T23:40:59+08:00"
updated: "2023-02-24T23:40:59+08:00"
upvotes: 0
comments: 0
---

# 1088. 易混淆数II

> **[yiduobo的每日leetcode 1088.易混淆数II](https://zhuanlan.zhihu.com/p/609256694) · 知乎 · 2023-02-24 · 赞同 0**
> 力扣：[1088. 易混淆数II](https://leetcode.cn/problems/confusing-number-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1088.易混淆数II

[力扣](https://leetcode.cn/problems/confusing-number-ii/)

题目要求找出1到n之间的易混淆数的数量，一个常见的想法就是将问题拆分成两个部分，分别为：

1、求出1到n之间由可翻转数字组成的数的数量

2、求出1到n之间在翻转之后与原数相同的数的数量

那么最终结果就是问题1的答案减去问题2的答案

方便起见，首先将n的各个数字分离出来，形成数组num_list，同时记num_list的长度为length。接下来分别讨论上面两个问题：

1、求出1到n之间由可翻转数字组成的数的数量：

可翻转数字有0、1、6、8、9一共5种，将其记为数组valid_digit。

对于一个k位数而言，如果可以存在前导0，那么一共就有5^k种合法的可翻转数。

有了这个结论，就可以从n的高位开始向后遍历。对于当前遍历到的位置index：

a）首先找出valid_digit中最大的满足valid_digit[p] \<\= num_list[index]的下标p。

b）此时如果选择将valid_digit[0]到valid_digit[p - 1]之间的任意数填充到最终形成数字的第index位上，得到的最终结果必然是小于n的，而index右侧一共length - index - 1位就可以形成5^(length - index - 1)种合法的可翻转数字，因此需要将p \* 5^(length - index - 1)累加到答案中

c）若此时的valid_digit[p] \< num_list[index]，那么就不需要继续向后遍历index了。反之如果valid_digit[p] \= num_list[index]，那么就需要继续向后遍历

若最终成功遍历完了所有的数位，那么就说明n自身也是一个合法的可翻转数，此时还需要将答案额外加上1

在这里值得说明的是，上面这种计算方式除了可以计算看上去的长度为length的满足条件的数之外，实际上也会将所有位数不足length的合法结果计算进去了，理由是在高位枚举时并没有将高位的前导0排除出去，而前导0的存在也并不会影响数的可翻转性质。

2、求出1到n之间在翻转之后与原数相同的数的数量：

需要注意的是，在这里就不能再忽略掉前导0了，因为这里计算的数需要进行翻转，而前导0的存在会影响到翻转的结果，因此前导0的存在是不合法的。换言之，这个问题的计算就需要分成两部分进行：

2-1、求出所有位数在1到length - 1之间的翻转之后与原数相同的数的数量

对于这个问题有两点需要注意。

第一点是奇偶性问题。对于一个长度为奇数的数，其中间位上的值只能是0、1、8这三种之一，而对于一个长度为偶数的数而言，其不存在中间位，而对称位上的值则有5种可行的选择。

第二点是前导0的问题。由于不能存在前导0，那么对于两位数需要特别注意，其高位上不能为0，因此只有11、69、88、96这一共4种合法的情况。另一方面，对于位数大于2的数而言，不妨设位数为k。那么当k为奇数时，可以认为是在所有合法的位数为length - 1的数中正中间插入0、1、8这三者之一。当k为偶数时，则可以认为是在这中间这两个位置插入00、11、69、88、96这五者之一。

根据上面这两点，就可以得到一种计算方法。

从1开始到length - 1遍历所有的位数k。

当k \= 1时，有3种符合条件的情况。

当k \= 2时，有4种符合条件的情况，同时初始化x \= 4，表示当前偶数长度的数有4中合法情况。

当k > 2且k为奇数时，有x \* 3种符合条件的情况。

当k > 2且k为偶数时，有x \* 5种符合条件的情况，同时需要将x更新为x \* 5。

2-2、求出所有位数为length且小于等于n的翻转之后与原数相同的数的数量

与上面问题1的计算方式类似，也是从逐位枚举，找到符合条件p，然后计算后续位置可用的合法数字的数量，不过在这里有几点不同的地方：

第一点是为了保持翻转后相同的性质，填充需要从两侧往中间同步进行，因此需要一组left、right从两侧往中间填充。由于填充结果的大小优先与高位挂钩，因此在枚举时应该使用num_list[left]来确定p的大小

第二点是由于位数奇偶性的存在，在left \= right时，可用的数字就从valid_digit中的5种变成了[0, 1, 8]中的3种。在这里可以使用一个candidate来表示当前位可用的数字。当left \= right时，candidate就是[0, 1, 8]，否则candidate就是valid_digit。另一方面，在确定了num_list[left]对应的candidate[p]之后，若left + 1到right - 1之间的位数为奇数时，那么合法数字的数量就是3 \* 5^((right - left - 1) / 2)，而如果位数为偶数，那么合法数字的数量就是5^((right - left - 1) / 2)

第三点是对于前导0的处理。当left \= 0时，由于0不能被填充到num_list[0]中，因此在累加合法数字时不能乘以p，而是需要乘以p - 1。另外，由于num_list[0]必然大于0，因此在这里p必然是大于等于1的，不需要担心越界的问题

第四点是当candidate[p] \< num_list[left]时，依然是直接退出遍历，否则就需要将candidate[p]填充到边界情况数组的下标left，同时需要将candidate[p]的翻转对称数字填充到边界情况数组的下标right。如果正常遍历完了每一位，说明n的前半部分全都是可翻转数字，此时就需要检测将这些数字翻转后形成的新数字，也就是边界情况数组中记录的数字是否小于等于n。若小于等于，那么还需要将答案额外加上1

最后附上python代码：

```python
class Solution(object):
    def confusingNumberII(self, n):
        """
        :type n: int
        :rtype: int
        """

        num_list = [int(x) for x in str(n)]
        length = len(num_list)
        res = 0
        
        flag = True
        valid_digit = [0, 1, 6, 8, 9]
        pow5 = [1]
        for index in range(1, length):
            pow5.append(pow5[-1] * 5)

        for index in range(length):
            p = len(valid_digit) - 1
            while valid_digit[p] > num_list[index]:
                p -= 1
            
            res += p * pow5[length - index - 1]
            if num_list[index] > valid_digit[p]:
                res += pow5[length - index - 1]
                flag = False
                break

        if flag:
            res += 1

        for k in range(1, length):
            if k == 1:
                res -= 3
            elif k == 2:
                x = 4
                res -= x
            elif k % 2 == 1:
                res -= x * 3
            else:
                x *= 5
                res -= x

        reverse_digit = {0: 0, 1: 1, 6: 9, 8: 8, 9: 6}
        middle_digit = [0, 1, 8]

        left = 0
        right = length - 1
        bound_list = [None] * length
        if length % 2 == 1:
            middle_choice = 3
        else:
            middle_choice = 1

        flag = True
        while left <= right:
            if left == right:
                candidate_digit = middle_digit
            else:
                candidate_digit = valid_digit

            p = len(candidate_digit) - 1
            while candidate_digit[p] > num_list[left]:
                p -= 1
            
            if left < right - 1:
                delta = middle_choice * pow5[(right - left - 1) / 2]
            else:
                delta = 1

            if left == 0:
                res -= (p - 1) * delta
            else:
                res -= p * delta

            if num_list[left] > candidate_digit[p]:
                res -= delta
                flag = False
                break
            else:
                bound_list[left] = candidate_digit[p]
                bound_list[right] = reverse_digit[candidate_digit[p]]

            left += 1
            right -= 1

        if flag and int(''.join([str(x) for x in bound_list])) <= n:
            res -= 1

        return res
```

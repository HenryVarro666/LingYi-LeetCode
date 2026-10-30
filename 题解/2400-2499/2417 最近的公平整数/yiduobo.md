---
title: "2417. 最近的公平整数"
aliases: ["yiduobo的每日leetcode 2417.最近的公平整数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/631102755"
zhihu_id: "631102755"
zhihu_title: "yiduobo的每日leetcode 2417.最近的公平整数"
question_id: "2417"
question: "最近的公平整数"
problem_url: "https://leetcode.cn/problems/closest-fair-integer/"
created: "2023-05-21T22:49:30+08:00"
updated: "2023-05-21T22:49:30+08:00"
upvotes: 0
comments: 0
---

# 2417. 最近的公平整数

> **[yiduobo的每日leetcode 2417.最近的公平整数](https://zhuanlan.zhihu.com/p/631102755) · 知乎 · 2023-05-21 · 赞同 0**
> 力扣：[2417. 最近的公平整数](https://leetcode.cn/problems/closest-fair-integer/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2417.最近的公平整数

[力扣](https://leetcode.cn/problems/closest-fair-integer/)

首先，若n的长度len为奇数，那么就不可能通过调整n的数字组成达到奇数位和偶数位相同，只能构造一个长度为len + 1的数。而对于这个长度为len + 1的数，为了实其最小，同时奇数位和偶数位相同，那么就应该构造100...0011...11这种形式的数，其中连续0的数量为(len + 1) / 2，而后续的连续1的数量则是(len + 1) / 2 - 1。

接下来讨论len为偶数的情况。

一趟遍历，统计偶数位的数量与奇数位的数量之差diff，这个diff必然为偶数，因为len为偶数，所以偶数位与奇数位必然同奇偶，二者之差diff也必然为偶数。对于diff：

1、若diff \= 0:

这种情况下无需进行任何调整，直接返回n即可

2、若diff > 0：

此时就应该将n中的diff / 2个偶数位修改为奇数位。为了使得最终结果大于等于n且最小，那么就应该将倒数第diff / 2个偶数位加上1，然后将其后面的所有数都改为1。于是只需从低位向高位一趟遍历，找到第diff / 2个偶数位然后执行上述操作即可

3、若diff \< 0：

这种情况相比情况2要复杂一些，因为在修改奇数位时，可能出现倒数第diff / 2个奇数位恰好等于9的情况，这种情况下就不能直接将其加上1，而需要继续向前寻找。更进一步的，如果出现了第diff / 2个奇数位恰好等于9的情况，此时就应该找到该位左侧第一个小于8的数位，理由是对于找到的这个数位，若其为奇数则需要加上1，若其为偶数则需要加上2，因此这个数位上的数必须要小于8。

若找不到，那么说明len位数n没有调整的余地了，只能构造出一个长度为len + 2的数100...0011...11，构造方案与len为奇数时构造长度为len + 1位数相同。

若找到了可用的数位，不妨设其为p，那么首先需要根据该位的奇偶性，将其加上1或者2，将其变为更大的偶数。接下来，需要从p开始向高位进行一趟遍历，重新统计当前不需要修改的数位中偶数位与奇数位之差diff。

由于从p开始到高位中，偶数位比奇数位多出diff位，因此在p + 1到最低位中，偶数位应该比奇数位少diff位。

另一方面，在p + 1到最低位中，一共有len - (p + 1)个数位，也就是偶数位与奇数位之和为len - (p + 1)，因此p + 1到最低位中的偶数就是(len - (p + 1) - diff) / 2，剩下的都是奇数位。于是从第p + 1位开始，将连续的(len - (p + 1) - diff) / 2位修改为0，然后将后续的所有数位修改为1即可。

最后附上python代码：

```python
class Solution(object):
    def closestFair(self, n):
        """
        :type n: int
        :rtype: int
        """

        digit_list = [int(x) for x in list(str(n))]
        diff = 0
        for digit in digit_list:
            if int(digit) % 2 == 0:
                diff += 1
            else:
                diff -= 1
            
        if diff == 0:
            return n
        
        def generate(length):
            res = 1
            for index in range(length / 2):
                res = res * 10
            
            for index in range(length / 2 - 1):
                res = res * 10 + 1
            
            return res

        if abs(diff) % 2 == 1:
            res = generate(len(digit_list) + 1)
            return res
        
        need_change = abs(diff) / 2
        odd = 0
        even = 0
        p = len(digit_list) - 1
        while True:
            if digit_list[p] % 2 == 0:
                odd += 1
            else:
                even += 1
            
            if (diff > 0 and odd == need_change) or (diff < 0 and even == need_change):
                break
            p -= 1
        
        if diff > 0:
            digit_list[p] += 1
            p += 1
            while p < len(digit_list):
                digit_list[p] = 1
                p += 1
            
            res = 0
            for digit in digit_list:
                res = res * 10 + digit
            
            return res

        while p >= 0 and digit_list[p] >= 8:
            p -= 1
        
        if p == -1:
            res = generate(len(digit_list) + 2)
            return res
        
        if digit_list[p] % 2 == 1:
            digit_list[p] += 1
        else:
            digit_list[p] += 2

        diff = 0
        for index in range(p, -1, -1):
            if digit_list[index] % 2 == 0:
                diff += 1
            else:
                diff -= 1

        r = len(digit_list) - (p + 1)

        zero_cnt = (r - diff) / 2
        for index in range(zero_cnt):
            p += 1
            digit_list[p] = 0
        
        p += 1
        while p < len(digit_list):
            digit_list[p] = 1
            p += 1
        
        res = 0
        for digit in digit_list:
            res = res * 10 + digit
        
        return res
```

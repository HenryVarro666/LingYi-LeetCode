---
title: "1342. 将数字变成0的操作次数"
aliases: ["yiduobo的每日leetcode 1342.将数字变成0的操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/math", "题单/位运算", "题单/位运算/一-基础题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/396444682"
zhihu_id: "396444682"
zhihu_title: "yiduobo的每日leetcode 1342.将数字变成0的操作次数"
question_id: "1342"
question: "将数字变成 0 的操作次数"
problem_url: "https://leetcode.cn/problems/number-of-steps-to-reduce-a-number-to-zero/"
difficulty: "Easy"
created: "2021-08-04T23:06:37+08:00"
updated: "2021-08-04T23:06:37+08:00"
upvotes: 0
comments: 2
---

# 1342. 将数字变成0的操作次数

> **[yiduobo的每日leetcode 1342.将数字变成0的操作次数](https://zhuanlan.zhihu.com/p/396444682) · 知乎 · 2021-08-04 · 赞同 0**
> 力扣：[1342. 将数字变成 0 的操作次数](https://leetcode.cn/problems/number-of-steps-to-reduce-a-number-to-zero/) · Easy · 灵茶山艾府：[两种方法：模拟 / O(1) 位运算（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1342.将数字变成0的操作次数

[力扣](https://leetcode-cn.com/problems/number-of-steps-to-reduce-a-number-to-zero/)

若当前数字为奇数，那么将最后一位减去1，否则将其除以2。如果从二进制位的角度来看，实际上就是对于num二进制表示中除了最高位的所有1都执行一次减法操作，然后并执行若干次右移操作使得num的位数变为1位，也就是说答案就等于num二进制表示中1的数目，加上num二进制表示的位数，然后再减去1。

最后附上python代码：

```python
class Solution(object):
    def numberOfSteps(self, num):
        """
        :type num: int
        :rtype: int
        """

        res = 0
        while num:
            if num & 1:
                res += 1
                if num == 1:
                    break
            
            num /= 2
            res += 1
        
        return res
```

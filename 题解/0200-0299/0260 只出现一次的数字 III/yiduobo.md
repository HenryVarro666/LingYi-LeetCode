---
title: "260. 只出现一次的数字 III"
aliases: ["yiduobo的每日leetcode 260.只出现一次的数字 III"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/graph", "题单/位运算", "题单/位运算/九-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/151429938"
zhihu_id: "151429938"
zhihu_title: "yiduobo的每日leetcode 260.只出现一次的数字 III"
question_id: "260"
question: "只出现一次的数字 III"
problem_url: "https://leetcode.cn/problems/single-number-iii/"
difficulty: "Medium"
created: "2020-06-28T22:36:26+08:00"
updated: "2020-06-28T22:36:26+08:00"
upvotes: 0
comments: 0
---

# 260. 只出现一次的数字 III

> **[yiduobo的每日leetcode 260.只出现一次的数字 III](https://zhuanlan.zhihu.com/p/151429938) · 知乎 · 2020-06-28 · 赞同 0**
> 力扣：[260. 只出现一次的数字 III](https://leetcode.cn/problems/single-number-iii/) · Medium · 灵茶山艾府：[【图解】一张图秒懂！转换成 136！（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

260.只出现一次的数字III <https://leetcode-cn.com/problems/single-number-iii/>

设这两个只出现一次的数字分别为num1和num2，那么将所有数字异或起来之后，出现两次的数字被抵消掉，那么异或的结果x就等于num1^num2。

由于num1肯定不等于num2，那么意味着x一定不为0，即x的二进制表示中一定存在1，而每一位1都表示当前位只在num1或者num2中为1。

例如10异或12，等于6，二进制下为

1010 ^ 1100 \= 0110

可以发现，6中低位的1来自10，而高位的1来自12。

于是在这里，我们可以任意取出x中的某一位1，然后将nums中所有该位为1的数异或起来。这次参与异或的数包括该位为1，且出现过两次的数，以及num1和num2中该位为1的那个数。由于出现过两次的数都会被抵消掉，那么异或的结果就正好是num1或者num2中的一个数，我们将其记为y。

由于x\=num1^num2，已知其中一个数为y，那么另一个数自然就是x^y了。

对于取出x中某一位1的操作，我在这里采用的是lowbit，即x&-x。其作用是取出x二进制表示中最低位的1，这个操作也是树状数组实现的关键。

最后附上python代码：

```python
class Solution(object):
    def singleNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        x = 0
        for num in nums:
            x ^= num

        lowbit = x & -x

        y = 0
        for num in nums:
            if lowbit & num:
                y ^= num

        return [y, x ^ y]
```

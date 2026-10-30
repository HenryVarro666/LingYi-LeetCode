---
title: "2429. 最小XOR"
aliases: ["yiduobo的每日leetcode 2429.最小XOR"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/bit-manipulation", "题单/位运算", "题单/位运算/二-异或-XOR-的性质"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/582659511"
zhihu_id: "582659511"
zhihu_title: "yiduobo的每日leetcode 2429.最小XOR"
question_id: "2429"
question: "最小异或"
problem_url: "https://leetcode.cn/problems/minimize-xor/"
difficulty: "Medium"
rating: 1532
created: "2022-11-11T22:36:02+08:00"
updated: "2022-11-11T22:36:02+08:00"
upvotes: 0
comments: 0
---

# 2429. 最小XOR

> **[yiduobo的每日leetcode 2429.最小XOR](https://zhuanlan.zhihu.com/p/582659511) · 知乎 · 2022-11-11 · 赞同 0**
> 力扣：[2429. 最小异或](https://leetcode.cn/problems/minimize-xor/) · Medium · 灵茶山艾府：[贪心 + O(1) 空间复杂度做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2429.最小XOR

[力扣](https://leetcode.cn/problems/minimize-xor/)

题目要求找出一个x，满足x和num2在二进制表示中1的数量一样多，且num1^x的异或结果最小。

首先可以通过分离num2中的1计算出x中最多有多少个1，然后再想办法将这些1分配到x的二进制位中。

根据异或的性质，即1^1 \= 0，0^1 \= 1，那么为了使得num1^x最小，就应该先尽量用x中的1来抵消掉num1中1的影响。很明显，这里应该按照从高位到低位的顺序来进行这个抵消操作。

当num1中所有的1都被抵消掉之后，如果还有多出的1，那么就应该从低位开始向高位分配在还没有分配过的位置上，直到用完所有的1。

最后附上python代码：

```python
class Solution(object):
    def minimizeXor(self, num1, num2):
        """
        :type num1: int
        :type num2: int
        :rtype: int
        """

        cnt = 0
        while num2:
            cnt += 1
            num2 -= num2 & -num2

        one_set = set()
        one_list = []
        now = num1
        while now:
            lowbit = now & -now
            one_set.add(lowbit)
            one_list.append(lowbit)
            now -= lowbit

        now = 1
        res = 0
        while cnt > 0:
            if one_list:
                res += one_list[-1]
                one_list.pop()
            else:
                while now in one_set:
                    now += now
                res += now
                now += now

            cnt -= 1
        
        return res
```

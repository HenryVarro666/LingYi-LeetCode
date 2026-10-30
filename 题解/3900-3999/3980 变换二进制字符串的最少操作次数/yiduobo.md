---
title: "3980. 变换二进制字符串的最少操作次数"
aliases: ["yiduobo的每日leetcode 3980.变换二进制字符串的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/动态规划", "题单/贪心算法", "题单/动态规划/六-状态机-DP", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2057170026864677815"
zhihu_id: "2057170026864677815"
zhihu_title: "yiduobo的每日leetcode 3980.变换二进制字符串的最少操作次数"
question_id: "3980"
question: "变换二进制字符串的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-transform-binary-string/"
difficulty: "Medium"
rating: 1846
created: "2026-07-07T00:28:28+08:00"
updated: "2026-07-07T00:28:29+08:00"
upvotes: 0
comments: 0
---

# 3980. 变换二进制字符串的最少操作次数

> **[yiduobo的每日leetcode 3980.变换二进制字符串的最少操作次数](https://zhuanlan.zhihu.com/p/2057170026864677815) · 知乎 · 2026-07-07 · 赞同 0**
> 力扣：[3980. 变换二进制字符串的最少操作次数](https://leetcode.cn/problems/minimum-operations-to-transform-binary-string/) · Medium · 灵茶山艾府：[从左到右贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3980.变换二进制字符串的最少操作次数

<https://leetcode.cn/problems/minimum-operations-to-transform-binary-string/>

题目给出两个长度都为n的二进制字符串s1和s2。

对于s1，可以执行以下操作任意次：

- 将任意位置上的'0'修改为'1'
- 将任意两个连续的'1'同时修改为'0'

问将s1变为s2所需的最少操作次数。若无法达成，则返回-1。

首先可以明确的是，由于本题中操作的代价都一样，因此不会有通过先铺垫小操作，然后执行一次大操作达到剩操作数的目的。反过来，在这里只存在，为了执行大操作，不得不执行小操作，浪费操作数的情况。

基于这一点，就可以从左往右，按直观理解进行贪心。具体来说，对于当前的下标p：

1、若s1[p]和s2[p]相同：

此时无需进行操作，将p向后移动即可。

2、若s1[p]为'0'，且s2[p]为'1'：

此时进行一次'0'变'1'的操作，更新答案然后将p向后移动即可。

3、若s1[p]为'1'，且s2[p]为'0'：

3-1）若s1[p + 1]存在，且s1[p + 1]和s2[p + 1]相同：

若s1[p + 1]为'1'，相当于要把'11'变为'01'，此时就可以直接执行'11'变'00'的操作，然后再对s[p + 1]执行'0'变'1'的操作，一共两次操作可以使得s1[p]以及s1[p + 1]归位。

若s1[p + 1]为'0'，相当于要把'10'变为'00'，此时就可以先对s[p + 1]执行'0'变'1'的操作，然后再执行'11'变'00'的操作，同样是两次操作可以使得s1[p]以及s1[p + 1]归位。

综合起来，这种情况下应该将答案加上2，然后将p移动到p + 2。

3-2）若s1[p + 1]存在，且s1[p + 1]为'0'，s2[p + 1]为'1'：

此时相当于要把'10'变为'01'，那么就需要经历'10'->'11'->'00'->'01'的过程，因此需要将答案加上3，然后将p移动到p + 2。

3-3）若s1[p + 1]存在，且s1[p + 1]为'1'，s2[p + 1]为'0'：

此时直接执行'11'变'00'就行了，因此需要将答案加上1，然后将p移动到p + 2。

3-4）若s1[p + 1]不存在，但s1[p - 1]存在：

此时需要借助s1[p - 1]来实现变换，但是s1[p - 1]已经归位了，实际上就相当于上面的3-1，因此需要两次操作，但是对应的p只需要向后移动一位。

3-5）若s1[p + 1]和s1[p - 1]都不存在：

此时无法变更s1[p]，直接返回-1即可。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, s1, s2):
        """
        :type s1: str
        :type s2: str
        :rtype: int
        """
        
        p = 0
        res = 0
        while p < len(s1):
            if s1[p] == s2[p]:
                p += 1
                continue
            if s1[p] == '0':
                res += 1
                p += 1
            else:
                if p + 1 < len(s1):
                    if s1[p + 1] == s2[p + 1]:
                        res += 2
                    elif s1[p + 1] == '0':
                        res += 3
                    else:
                        res += 1
                    p += 2
                    
                elif p > 0:
                    res += 2
                    p += 1
                else:
                    return -1
        
        return res
```

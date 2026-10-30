---
title: "3858. 按位或的最小值"
aliases: ["yiduobo的每日leetcode 3858.按位或的最小值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/bit-manipulation", "题单/位运算", "题单/位运算/五-试填法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2013644873367049538"
zhihu_id: "2013644873367049538"
zhihu_title: "yiduobo的每日leetcode 3858.按位或的最小值"
question_id: "3858"
question: "按位或的最小值"
problem_url: "https://leetcode.cn/problems/minimum-bitwise-or-from-grid/"
difficulty: "Medium"
rating: 1947
created: "2026-03-07T17:03:12+08:00"
updated: "2026-03-07T17:03:31+08:00"
upvotes: 1
comments: 0
---

# 3858. 按位或的最小值

> **[yiduobo的每日leetcode 3858.按位或的最小值](https://zhuanlan.zhihu.com/p/2013644873367049538) · 知乎 · 2026-03-07 · 赞同 1**
> 力扣：[3858. 按位或的最小值](https://leetcode.cn/problems/minimum-bitwise-or-from-grid/) · Medium · 灵茶山艾府：[试填法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3858.按位或的最小值

<https://leetcode.cn/problems/minimum-bitwise-or-from-grid/description/>

题目给出一个大小为m \* n的二维整数数组grid，其中所有元素都不超过10^5。

现在要求从grid的每一行中都选择恰好一个整数，要求这些整数的按位或最小。问可能得到的最小值是多少。

题目要求按位或的结果最小，那么就应该让二进制位的高位上尽量为0。由于题目保证了grid中的所有元素不超过10^5，也就是说最终按位或的结果必然小于2^16，因此可以从第15位开始向下遍历，对于当前位d，判断每一行中是否至少存在一个元素，在满足在第d + 1到第15位上不存在当前答案中不具备的1的前提下，在第d位为0。若满足，那么答案的第d位就为0，否则为1。

上面所说的，满足在第d + 1到第15位上不存在当前答案中不具备的1，理由是选择这个元素不能影响到高位上的1，因此若答案的某个高位上为1，那么该元素在这一位上可以为0，也可以为1，反之，若答案在某个高位上为0，那么该元素在这一位上只能为0。

具体来说，不妨设当前遍历到第d位，且高位上的结果为res，那么对于当前遍历到的元素x：

1、首先可以先右移d位，再左移d位，将x的第0到第d位都变为0。接下来再与res取按位或，判断结果是否恰好等于res。若不等于，就说明x的第d + 1到第15位上存在res不具备的1，也就是说x不可用。具体来说，就是判断(x >> d \<\< d) | res是否恰好等于res，若不等于，那么x不可用。

2、另外还需要判断第d位是否为0，这个比较好办，只需要检测x & (1 \<\< d)是否为0即可。

若么一行中都存在至少一个元素，满足以上两个条件，那么答案的第d位上就为1，否则答案的第d位上就为0。从高位到低位逐位遍历，就可以确定每一位上应该填充什么，从而得到最终答案。

最后附上python代码：

```python
class Solution(object):
    def minimumOR(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        
        res = 0
        for d in range(16, -1, -1):
            flag = True
            for r in grid:
                row_flag = False
                for v in r:
                    if ((v  >> d << d) | res) == res and (v & (1 <<d)) == 0:
                        row_flag = True
                        break
                
                if not row_flag:
                    flag = False
                    break
            
            if not flag:
                res |= (1 << d)
        
        return res
```

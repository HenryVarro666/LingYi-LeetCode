---
title: "2571. 将整数减少到零需要的最少操作数"
aliases: ["yiduobo的每日leetcode 2571.将整数减少到零需要的最少操作数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/位运算", "题单/贪心算法", "题单/位运算/八-思维题", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/641519342"
zhihu_id: "641519342"
zhihu_title: "yiduobo的每日leetcode 2571.将整数减少到零需要的最少操作数"
question_id: "2571"
question: "将整数减少到零需要的最少操作数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-reduce-an-integer-to-0/"
difficulty: "Medium"
rating: 1649
created: "2023-07-05T00:03:52+08:00"
updated: "2023-07-05T00:03:52+08:00"
upvotes: 0
comments: 0
---

# 2571. 将整数减少到零需要的最少操作数

> **[yiduobo的每日leetcode 2571.将整数减少到零需要的最少操作数](https://zhuanlan.zhihu.com/p/641519342) · 知乎 · 2023-07-05 · 赞同 0**
> 力扣：[2571. 将整数减少到零需要的最少操作数](https://leetcode.cn/problems/minimum-operations-to-reduce-an-integer-to-0/) · Medium · 灵茶山艾府：[位运算一行搞定！附记忆化搜索做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2571.将整数减少到零需要的最少操作数

[力扣](https://leetcode.cn/problems/minimum-operations-to-reduce-an-integer-to-0/)

由于题目中的操作都是基于2的幂次进行的，那么在这里就应该从二进制位的角度来考虑问题。

对于题目给出的n的二进制表示，每次可以选择某一位加上1或者减去1。对于原本为0的位，很明显不应该对其进行任何操作，而对于原本为1的位，可以考虑将其减1变为0，也可以考虑加上1产生进位，那么这里主要需要考虑的就是选择加1进位的时机。

对于落单的1而言，如果选择减去1，只需1个操作就能将其消除，而如果选择加上1，其进位后又产生了新的1需要消除，这样是不划算的。但是对于连续的1，如果在这一段1的最低位加上1，那么这一段1都会因为进位变为0，最终只剩下1个最高位进位后的1需要消除，这样的话就是很划算了。

综合起来，就可以从低位开始向高位遍历：

1、若当前位为0，那么直接跳过

2、若当前位为落单的1，那么就执行减1操作将其消去

3、若当前位以及其相邻为构成了长度大于等于2的连续1，那么就在当前位做一次加1操作，将这一段连续1变为其最高位进位后的1

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, n):
        """
        :type n: int
        :rtype: int
        """

        binary = []
        while n:
            binary.append(n % 2)
            n /= 2
        
        p = 0
        res = 0
        while p < len(binary):
            while binary[p] == 0:
                p += 1
            
            if p + 1 < len(binary) and binary[p + 1] == 1:
                res += 1
                while p < len(binary) and binary[p] == 1:
                    p += 1
                
                if p == len(binary):
                    return res + 1
                else:
                    binary[p] = 1
            
            else:
                res += 1
                p += 1
        
        return res
```

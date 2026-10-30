---
title: "2457. 美丽整数的最小增量"
aliases: ["yiduobo的每日leetcode 2457.美丽整数的最小增量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/math", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/586152705"
zhihu_id: "586152705"
zhihu_title: "yiduobo的每日leetcode 2457.美丽整数的最小增量"
question_id: "2457"
question: "美丽整数的最小增量"
problem_url: "https://leetcode.cn/problems/minimum-addition-to-make-integer-beautiful/"
difficulty: "Medium"
rating: 1680
created: "2022-11-23T23:04:15+08:00"
updated: "2022-11-23T23:04:15+08:00"
upvotes: 0
comments: 0
---

# 2457. 美丽整数的最小增量

> **[yiduobo的每日leetcode 2457.美丽整数的最小增量](https://zhuanlan.zhihu.com/p/586152705) · 知乎 · 2022-11-23 · 赞同 0**
> 力扣：[2457. 美丽整数的最小增量](https://leetcode.cn/problems/minimum-addition-to-make-integer-beautiful/) · Medium · 灵茶山艾府：[贪心 + 视频讲解](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2457.美丽整数的最小增量

[力扣](https://leetcode.cn/problems/minimum-addition-to-make-integer-beautiful/)

题目要找出最小的x，使得原整数n加上x得到的数是一个美丽整数。

首先，如果n本身就是个美丽整数，那么答案自然为0，否则就需要想办法让新得到的数每一位上数字之和变小。由于只能加上另一个整数x，这也就意味着变小的唯一途经是产生了进位，使得某一位上的数变成了0。同时，一旦某一位上出现过进位，那么这一位上不应该在加上其他的数。

另一方面，为了使得加上的数x最小，那么显然应该从低位开始考虑进位。于是可以从低位开始向高位枚举哪些低位的后缀产生了进位。在进位出现时，意味着出现进位的这一位数字归零了，同时其高一位上应该加上1，那么只需要一开始先将所有数位分离出来并计算初始数位和s，就可以通过对s进行加减在O(1)的时间内得到进位后的数位和了。重复这个过程，直到若干轮进位后数位之和小于等于target为止。此时只需要使用进位后得到的数减去原数n就是最终答案。

不过需要特别注意的是，这里有两种特殊情况需要考虑。

第一种是进位超过了最高位。例如n \= 3，target \= 2这种情况，此时产生进位之后n就变成了10，多出了一位。对于这种情况需要特殊处理。不过一旦出现了这种情况，说明所有的操作都完成了，此时可以计算最终答案。

第二种则是进位时的高一位遇到了9，甚至连续的9。这种情况下计算新的s是比较麻烦的事情，而且这种情况也可能与第一种特殊情况同时出现。在这里有一个偷懒的处理方法是利用一个标记inc_flag记录是否出现了高一位是9的进位。一旦出现了这种情况，此时对于s的计算就不应该加上那个额外的1，同时本轮s的结果不能与target进行比较，而是需要等到下一轮再进行处理。

最后附上python代码：

```python
class Solution(object):
    def makeIntegerBeautiful(self, n, target):
        """
        :type n: int
        :type target: int
        :rtype: int
        """

        digit_list = []
        now = n
        while now:
            digit_list.append(now % 10)
            now /= 10
        
        s = sum(digit_list)
        p = 0
        inc_flag = False
        while s > target or inc_flag:
            while digit_list[p] == 0:
                p += 1
            
            s -= digit_list[p]
            digit_list[p] = 0
            if p == len(digit_list) - 1:
                digit_list.append(1)
                break
            
            if digit_list[p + 1] != 9:
                s += 1
                digit_list[p + 1] += 1
                inc_flag = False
            else:
                inc_flag = True

        digit_list.reverse()
        now = 0
        for digit in digit_list:
            now = now * 10 + digit
        
        return now - n
```

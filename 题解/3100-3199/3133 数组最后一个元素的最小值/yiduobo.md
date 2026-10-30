---
title: "3133. 数组最后一个元素的最小值"
aliases: ["yiduobo的每日leetcode 3133.数组最后一个元素的最小值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "题单/位运算", "题单/位运算/三-与或-AND/OR-的性质"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/702405633"
zhihu_id: "702405633"
zhihu_title: "yiduobo的每日leetcode 3133.数组最后一个元素的最小值"
question_id: "3133"
question: "数组最后一个元素的最小值"
problem_url: "https://leetcode.cn/problems/minimum-array-end/"
difficulty: "Medium"
rating: 1935
created: "2024-06-08T22:18:56+08:00"
updated: "2024-06-08T22:18:56+08:00"
upvotes: 1
comments: 0
---

# 3133. 数组最后一个元素的最小值

> **[yiduobo的每日leetcode 3133.数组最后一个元素的最小值](https://zhuanlan.zhihu.com/p/702405633) · 知乎 · 2024-06-08 · 赞同 1**
> 力扣：[3133. 数组最后一个元素的最小值](https://leetcode.cn/problems/minimum-array-end/) · Medium · 灵茶山艾府：[位运算，两种简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3133.数组最后一个元素的最小值

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-array-end/description/)

题目给出两个整数n和x，要求构造出一个长度为n的单调递增的数组，使得数组各元素的按位与结果为x，问数组最后一个元素的最小值为多少。

首先，根据按位与的性质，数组中的每个元素在x二进制位1的数位上也必须为1。另一方面，由于数组是单调递增的，为了使得最后一个元素最小，那么就需要让数组中的每个元素都尽量小。换言之，对于数组中的元素，在保证x对应的数位上为1之外，其他的二进制位上则应该按从0到n - 1的顺序进行排布，才能使得数组元素尽量小。

例如样例1中的n \= 3，x \= 4，首先需要保证4的二进制表示100中的这个1必须存在于数组中的每个元素中。接下里对于值为0的位，则可以从0到n - 1进行排布，即100、101、110。

对于更一般的例子，例如n \= 6，x \= 5，首先需要保证5的二进制表示101中的这个1必须存在于数组中的每个元素中，接下来对于值为0的位，则可以从0到n - 1进行排布，即00101、00111、01101、01111、10101、10111。

可以发现，在无视x中对应的数位时，其他位上对应的数值实际上就是n - 1的二进制表示，那么只需要将n - 1的二进制表示穿插到x二进制中非1的位置上即可。

最后附上python代码：

```python
class Solution(object):
    def minEnd(self, n, x):
        """
        :type n: int
        :type x: int
        :rtype: int
        """

        res = x
        p = 0
        n -= 1
        while n:
            while res & (1 << p) == (1 << p):
                p += 1
            
            if n & 1:
                res |= (1 << p)
            
            n >>= 1
            p += 1
        
        return res
```

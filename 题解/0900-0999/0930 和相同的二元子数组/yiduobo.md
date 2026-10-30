---
title: "930. 和相同的二元子数组"
aliases: ["yiduobo的每日leetcode 930.和相同的二元子数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/常用数据结构", "题单/滑动窗口与双指针/二-不定长滑动窗口", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/357064138"
zhihu_id: "357064138"
zhihu_title: "yiduobo的每日leetcode 930.和相同的二元子数组"
question_id: "930"
question: "和相同的二元子数组"
problem_url: "https://leetcode.cn/problems/binary-subarrays-with-sum/"
difficulty: "Medium"
rating: 1592
created: "2021-03-14T22:25:42+08:00"
updated: "2021-03-14T22:25:42+08:00"
upvotes: 0
comments: 0
---

# 930. 和相同的二元子数组

> **[yiduobo的每日leetcode 930.和相同的二元子数组](https://zhuanlan.zhihu.com/p/357064138) · 知乎 · 2021-03-14 · 赞同 0**
> 力扣：[930. 和相同的二元子数组](https://leetcode.cn/problems/binary-subarrays-with-sum/) · Medium · 灵茶山艾府：[恰好型滑动窗口（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

930.和相同的二元子数组

[力扣](https://leetcode-cn.com/problems/binary-subarrays-with-sum/)

首先来讨论特殊情况。

当S \= 0时，得到的子数组中必然不能出现1，那么对于一段长为l且全都是0的子数组，可以产生出l \* (l + 1) / 2种合法的答案。那么此时只需要从头到尾一趟扫描，找到所有的连续0，然后计算出答案即可。

接下来考察S > 0的情况。

若此时A中1的个数之和都不足S的话，那么答案自然为0，否则此时的合法答案必然是形如

00...000 1 XX...XXX 1 00.000

的子数组，其中1 XX...XXX 1这一段当中一共有S个1，然后前缀和后缀分别有l和r个0，这里的l和r当然也可以是0。

那么对于这一段来说，1 XX...XXX 1是必须要的，而对于前缀0的个数，则可以是0到l中任意值，同样地，对于后缀0的个数也可以是0到r中的任意值，因此一共可以产生(l + 1) \* (r + 1)种合法的答案。

而对于1 XX...XXX 1这种结构，一个自然的想法就是使用滑动窗口。每次将窗口的右边界right移动到right右侧下一个1所在的位置，然后将窗口的左边界left也移动到left右侧下一个1所在的位置即可。

对于下一个1所在的位置，则可以事先通过一趟扫描预处理出来，同时得到这个位置之后，在每次窗口滑动时也可以顺便计算出当前窗口的前缀0的个数l以及后缀0的个数r，也就是窗口左边界滑动的距离以及右边界滑动的距离。

最后附上python代码：

```python
class Solution(object):
    def numSubarraysWithSum(self, A, S):
        """
        :type A: List[int]
        :type S: int
        :rtype: int
        """

        res = 0

        if S == 0:
            start_pos = None
            for index, num in enumerate(A):
                if num == 1:
                    if start_pos is None:
                        continue
                    l = index - start_pos
                    res += l * (l + 1) / 2
                    start_pos = None
                else:
                    if start_pos is None:
                        start_pos = index
            
            if start_pos is not None:
                l = len(A) - start_pos
                res += l * (l + 1) / 2
            return res
            
        last_pos = -1
        l = 0
        while l < len(A) and A[l] != 1:
            l += 1
        if l == len(A):
            return 0

        r = l
        now = 1
        while r + 1 < len(A) and now < S:
            r += 1
            now += A[r]
        
        if now < S:
            return 0

        next_pos = r + 1
        while next_pos < len(A) and A[next_pos] == 0:
            next_pos += 1
        
        res = (l - last_pos) * (next_pos - r)
        while next_pos < len(A):
            last_pos = l
            l += 1
            while l < len(A) and A[l] == 0:
                l += 1
            
            r = next_pos
            next_pos += 1
            while next_pos < len(A) and A[next_pos] == 0:
                next_pos += 1
            
            res += (l - last_pos) * (next_pos - r)
        
        return res
```

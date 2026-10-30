---
title: "3314. 构造最小位运算数组I & 3315. 构造最小位运算数组II"
aliases: ["yiduobo的每日leetcode 3314.构造最小位运算数组I && 3315.构造最小位运算数组II", "3314. 构造最小位运算数组I", "3315. 构造最小位运算数组II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/medium", "leetcode/number-theory", "题单/位运算", "题单/位运算/八-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1917446456"
zhihu_id: "1917446456"
zhihu_title: "yiduobo的每日leetcode 3314.构造最小位运算数组I && 3315.构造最小位运算数组II"
question_id: ["3314", "3315"]
question: ["构造最小位运算数组 I", "构造最小位运算数组 II"]
problem_url: ["https://leetcode.cn/problems/construct-the-minimum-bitwise-array-i/", "https://leetcode.cn/problems/construct-the-minimum-bitwise-array-ii/"]
difficulty: ["Easy", "Medium"]
rating: 1715
created: "2024-10-19T00:56:19+08:00"
updated: "2024-10-19T00:56:19+08:00"
upvotes: 1
comments: 0
---

# 3314. 构造最小位运算数组I & 3315. 构造最小位运算数组II

> **[yiduobo的每日leetcode 3314.构造最小位运算数组I && 3315.构造最小位运算数组II](https://zhuanlan.zhihu.com/p/1917446456) · 知乎 · 2024-10-19 · 赞同 1**
> 力扣：[3314. 构造最小位运算数组 I](https://leetcode.cn/problems/construct-the-minimum-bitwise-array-i/) · Easy · 灵茶山艾府：[O(1) 计算每个数（Python/Java/C++/Go）](灵茶山艾府.md)
> 力扣：[3315. 构造最小位运算数组 II](https://leetcode.cn/problems/construct-the-minimum-bitwise-array-ii/) · Medium · 灵茶山艾府：[O(1) 计算每个数（Python/Java/C++/Go）](../3315%20构造最小位运算数组%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3314.构造最小位运算数组I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/construct-the-minimum-bitwise-array-i/)

3315.构造最小位运算数组II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/construct-the-minimum-bitwise-array-ii/description/)

题目给出一个长度为n的质数数组nums，要求返回一个长度为n的数组ans，对于所有的i都有ans[i] OR (ans[i] + 1) \= nums[i]。另外还要求每个ans[i]都尽量小，若找不到可行的ans[i]，则将其置为-1。

两题的题设一样，第二题的数据规模较大。

由于计算使用的按位或运算，那么不妨从二进制位的角度来考虑。

对于一个偶数x而言，其二进制表示中的最低位一定为0，也就是说x可以写成XXXX....XXX0的形式，那么x + 1就是XXXX...XXX1，二者按位或之后为XXXX...XXX1，也就是说当nums[i]为奇数时，ans[i]取nums[i] - 1是一个可行的解。

对于一个奇数x而言，其二进制表示中的最后只有存在一个1，也就是说x可以写成XXXX...XXX0111...11的形式，那么x + 1就是XXXX...XXX1000...00，二者按位或之后为XXXX...XXX1111...111，也就是说当nums[i]为奇数时，将其低位上连续的1中任意一个变为0都是可以行的解。

综合上面的分析可以发现，当nums[i]为2时，答案一定为-1；当nums[i]为奇数时，为了使得答案最小，就应该让nums[i]低位连续的1中最高位的那个变为0。

最后附上python代码：

```python
class Solution(object):
    def minBitwiseArray(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        res = []
        for v in nums:
            if v == 2:
                res.append(-1)
            else:
                cnt = 0
                while v & 1:
                    cnt += 1
                    v >>= 1
                
                v <<= 1
                for _ in range(cnt - 1):
                    v <<= 1
                    v |= 1
                
                res.append(v)
        
        return res
```

---
title: "2897. 对数组执行操作使平方和最大"
aliases: ["yiduobo的每日leetcode 2897.对数组执行操作使平方和最大"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/bit-manipulation", "题单/位运算", "题单/贪心算法", "题单/位运算/八-思维题", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/663184239"
zhihu_id: "663184239"
zhihu_title: "yiduobo的每日leetcode 2897.对数组执行操作使平方和最大"
question_id: "2897"
question: "对数组执行操作使平方和最大"
problem_url: "https://leetcode.cn/problems/apply-operations-on-array-to-maximize-sum-of-squares/"
difficulty: "Hard"
rating: 2301
created: "2023-10-25T02:43:56+08:00"
updated: "2023-10-25T02:43:56+08:00"
upvotes: 0
comments: 0
---

# 2897. 对数组执行操作使平方和最大

> **[yiduobo的每日leetcode 2897.对数组执行操作使平方和最大](https://zhuanlan.zhihu.com/p/663184239) · 知乎 · 2023-10-25 · 赞同 0**
> 力扣：[2897. 对数组执行操作使平方和最大](https://leetcode.cn/problems/apply-operations-on-array-to-maximize-sum-of-squares/) · Hard · 灵茶山艾府：[把 1 都聚在一起（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2897.对数组执行操作使平方和最大

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/apply-operations-on-array-to-maximize-sum-of-squares/)

题目中的操作与位有关，那么就应该从位的角度来分析这个操作。

对于and和or操作，有

1 and 1 \= 1

0 and 0 \= 0

1 or 1 \= 1

0 or 0 \= 0

1 and 0 \= 0

0 and 1 \= 0

1 or 0 \= 1

0 or 1 \= 1

可以发现，对于操作中的某一位index，若nums[i]的index这一位与nums[j]的index这一位相同，那么无事发生，反之就相当于接受and结果的nums[i]中对应位变为0，而接受or结果的nums[j]中对应位变为1。更进一步的，就可以认为此时是nums[i]将所有nums[i]中为1，而在nums[j]中为0的位上的1传递给了nums[j]，自己变为了0。

另一方面，为了使得最终答案最大，则应该尽量构造出大的数字。由于题目中的交换操作不会改变两个数字的和，于是就变成了对于a > b，比较(a+t)^2 + (b-t)^2与a^2 + b^2的大小的问题。将括号打开之后是很直观的，有a^2 + 2at + b^2 + 2bt \= a^2 + b^2 + at(a - b) > a^2 + b^2。

综合上面两点，就应该通过交换操作尽量把1集中在同一个数字上，然后选择top k个这样的数字计算平方和。于是就可以先统计原数组中每个数字在各个二进制位上1的数目，接下来循环k次，每次都尝试从每一位上获取一个1，得到当前数字后计算平方然后累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def maxSum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        cnt = [0] * 30
        for v in nums:
            p = 0
            while v:
                if v % 2 == 1:
                    cnt[p] += 1
                
                p += 1
                v /= 2
        
        res = 0
        mod = 10 ** 9 + 7
        while k > 0:
            v = 0
            for index in range(30):
                if cnt[index] > 0:
                    cnt[index] -= 1
                    v |= (1 << index)
            
            res += v * v
            res %= mod
            k -= 1
        
        return res
```

---
title: "307. 区域和检索"
aliases: ["yiduobo的每日leetcode 307.区域和检索"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/design", "leetcode/binary-indexed-tree", "leetcode/math", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/158638574"
zhihu_id: "158638574"
zhihu_title: "yiduobo的每日leetcode 307.区域和检索"
question_id: "307"
question: "区域和检索 - 数组可修改"
problem_url: "https://leetcode.cn/problems/range-sum-query-mutable/"
difficulty: "Medium"
created: "2020-07-11T00:08:27+08:00"
updated: "2020-07-11T00:08:27+08:00"
upvotes: 0
comments: 0
---

# 307. 区域和检索

> **[yiduobo的每日leetcode 307.区域和检索](https://zhuanlan.zhihu.com/p/158638574) · 知乎 · 2020-07-11 · 赞同 0**
> 力扣：[307. 区域和检索 - 数组可修改](https://leetcode.cn/problems/range-sum-query-mutable/) · Medium · 灵茶山艾府：[带你发明树状数组！附数学证明（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

307.区域和检索<https://leetcode-cn.com/problems/range-sum-query-mutable/>

经典的数据结构问题，我在这里使用的是树状数组，简单来说原理是使用数组下标二进制位来表示某个区间的和。例如nums[1:9]这8个数，加入到树状数组中之后为

sum[1] \= nums[1]，二进制下数组下标为0001

sum[2] \= nums[1] + nums[2]，二进制下数组下标为0010

sum[3] \= nums[3]，二进制下数组下标为0011

sum[4] \= nums[1] + nums[2] + nums[3] + nums[4]，二进制下数组下标为0100

sum[5] \= nums[5],二进制下数组下标为0101

sum[6] \= nums[5] + nums[6]，二进制下数组下标为0110

sum[7] \= nums[7]，二进制下数组下标为0111

sum[8] \= nums[1] + nums[2] + nums[3] + nums[4] + nums[5] + nums[6] + nums[7] + nums[8]，二进制下数组下标为1000

可以发现，sum[index]等于index - 2^k + 1到index这一段的和，其中k为index末尾0的个数

而二进制下计算末尾0的个数可以通过lowbit操作获取到最低位的1来实现，即x &\= -x

于是对于每个数，使用O(logn)的时间就可以完成sum数组的更新了。

而对于查询操作，同样是使用lowbit操作逐位分离最低位的1，同时累加sum数组的值即可，例如求解nums[1] + ... + nums[7]，可以看做

(nums[1] + nums[2] + nums[3] + nums[4]) + (nums[5] + nums[6]) + nums[7]

可以通过sum[4], sum[6]以及sum[7]获得答案，而这三个下标在二进制下为0100，0110以及011，于是可以通过lowbit操作，从7开始逐个迭代，因此最终一次询问的时间复杂度同样是O(logn)。

最后附上python代码：

```python
class NumArray(object):

    def __init__(self, nums):
        """
        :type nums: List[int]
        """
        self.nums = nums[:]
        self.sum_list = [0] * (len(nums) + 1)
        self.length = len(nums)
        for index, num in enumerate(nums):
            self.add(index + 1, num)

    def add(self, pos, delta):
        while pos <= self.length:
            self.sum_list[pos] += delta
            pos += pos & -pos

    def update(self, i, val):
        """
        :type i: int
        :type val: int
        :rtype: None
        """
        delta = val - self.nums[i]
        self.add(i + 1, delta)
        self.nums[i] = val

    def sumRange(self, i, j):
        """
        :type i: int
        :type j: int
        :rtype: int
        """
        res = 0
        now = j + 1
        while now > 0:
            res += self.sum_list[now]
            now -= now & -now

        now = i
        while now > 0:
            res -= self.sum_list[now]
            now -= now & -now

        return res

# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# obj.update(i,val)
# param_2 = obj.sumRange(i,j)
```

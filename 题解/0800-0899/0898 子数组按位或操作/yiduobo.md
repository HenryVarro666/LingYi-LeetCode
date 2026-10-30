---
title: "898. 子数组按位或操作"
aliases: ["yiduobo的每日leetcode 898.子数组按位或操作"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/hash-table", "题单/位运算", "题单/位运算/三-与或-AND/OR-的性质"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/353232688"
zhihu_id: "353232688"
zhihu_title: "yiduobo的每日leetcode 898.子数组按位或操作"
question_id: "898"
question: "子数组按位或操作"
problem_url: "https://leetcode.cn/problems/bitwise-ors-of-subarrays/"
difficulty: "Medium"
rating: 2133
created: "2021-02-26T22:30:10+08:00"
updated: "2021-02-26T22:30:10+08:00"
upvotes: 0
comments: 0
---

# 898. 子数组按位或操作

> **[yiduobo的每日leetcode 898.子数组按位或操作](https://zhuanlan.zhihu.com/p/353232688) · 知乎 · 2021-02-26 · 赞同 0**
> 力扣：[898. 子数组按位或操作](https://leetcode.cn/problems/bitwise-ors-of-subarrays/) · Medium · 灵茶山艾府：[LogTrick 及其进阶：统计每个结果的出现次数（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

898.子数组按位操作

[力扣](https://leetcode-cn.com/problems/bitwise-ors-of-subarrays/)

题目说到了按位或，那么很自然想到利用按位或的某些性质。

设OR(i, j)表示arr中从下标i按位或到j，那么就有OR(i, j) \= OR(i, j - 1) | arr[j]。根据按位或的性质，我们可以认为OR(i, j)就是在OR(i, j - 1)的基础上将某些二进制位上的0变成了1。那么对于OR(i, i), OR(i, i + 1), ..., OR(i, len(arr) - 1)这一系列按位或结果而言：

OR(i, i)可以认为在0的基础上将某些二进制位从0变成了1

OR(i, i + 1)可以认为在OR(i, i)的基础上将某些二进制位从0变成了1

...

OR(i, len(arr) - 1)可以认为在OR(i, len(arr) - 2)的基础上将某些二进制位从0变成了1

由于这里的arr都小于等于10^9之内，因此对于arr中的所有数而言，其二进制表示最多只有32位，于是上面从OR(i, i)到OR(i, len(arr) - 1)这些数当中，即使每次都恰好只变了1个1，那么也最多只有32种不同的结果，因此完全可以使用一个哈希表储存计算的中间结果，于是现在就有了一种做法。初始化res为空，now为set(0)，接下来遍历arr中的每个数，对于当前的arr[index]：

1、首先将其与now中的所有数进行或操作然后覆盖掉原来的now。这一步的含义是计算出OR(0, index), OR(1, index), ..., OR(index - 1, index)。当然，这些数可能出现重复，但是now是一个set，正好完成了去重的工作

2、将arr[index]也加入到now中，表示的是OR(index, index)

3、将now中没有出现在res中的数加入到res当中

遍历完成后，res的长度即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def subarrayBitwiseORs(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """

        res = set()
        now = set([0])
        for num in arr:
            now = {x | num for x in now}
            now.add(num)
            for x in now:
                if x not in res:
                    res.add(x)
        return len(res)
```

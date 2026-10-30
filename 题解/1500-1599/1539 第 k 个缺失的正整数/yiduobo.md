---
title: "1539. 第k个缺失的正整数"
aliases: ["yiduobo的每日leetcode 1539.第k个缺失的正整数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/四-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/424232546"
zhihu_id: "424232546"
zhihu_title: "yiduobo的每日leetcode 1539.第k个缺失的正整数"
question_id: "1539"
question: "第 k 个缺失的正整数"
problem_url: "https://leetcode.cn/problems/kth-missing-positive-number/"
difficulty: "Easy"
created: "2021-10-21T22:48:43+08:00"
updated: "2021-10-21T22:48:43+08:00"
upvotes: 0
comments: 0
---

# 1539. 第k个缺失的正整数

> **[yiduobo的每日leetcode 1539.第k个缺失的正整数](https://zhuanlan.zhihu.com/p/424232546) · 知乎 · 2021-10-21 · 赞同 0**
> 力扣：[1539. 第 k 个缺失的正整数](https://leetcode.cn/problems/kth-missing-positive-number/) · Easy · 灵茶山艾府：[O(log n) 详细推导，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1539.第k个缺失的正整数

[力扣](https://leetcode-cn.com/problems/kth-missing-positive-number/)

由于这里的k的范围很小，因此直接模拟也是可行的。

由于这里的arr是升序的，因此可以计算相邻两个整数的差值来判断这两个整数间有多少个缺失的整数，并根据这个值与k的大小来确定最终答案。具体来说就是对于arr中的两个相邻整数arr[index]与arr[index + 1]，期间一共有arr[index] + 1到arr[index + 1] - 1这些整数时缺失的，其数量就是

(arr[index + 1] - 1) - (arr[index] + 1) + 1 \= arr[index + 1] - arr[index] - 1

若arr[index + 1] - arr[index] \= n，那么就说明arr[index]与arr[index + 1]之间一共有n - 1个缺失的整数。若n - 1 >\= k，那么答案就是从arr[index]开始向后数k个数，否则需要将k减去n - 1，然后继续考察arr[index + 1]与arr[index + 2]。

最后附上python代码：

```python
class Solution(object):
    def findKthPositive(self, arr, k):
        """
        :type arr: List[int]
        :type k: int
        :rtype: int
        """

        arr.append(2001)
        now = 0
        for num in arr:
            if num - now - 1 >= k:
                return now + k
            else:
                k -= num - now - 1
            now = num
```

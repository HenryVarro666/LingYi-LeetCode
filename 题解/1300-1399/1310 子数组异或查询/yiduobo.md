---
title: "1310. 子数组异或查询"
aliases: ["yiduobo的每日leetcode 1310.子数组异或查询"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/392279673"
zhihu_id: "392279673"
zhihu_title: "yiduobo的每日leetcode 1310.子数组异或查询"
question_id: "1310"
question: "子数组异或查询"
problem_url: "https://leetcode.cn/problems/xor-queries-of-a-subarray/"
created: "2021-07-22T22:50:22+08:00"
updated: "2021-07-22T22:50:22+08:00"
upvotes: 0
comments: 1
---

# 1310. 子数组异或查询

> **[yiduobo的每日leetcode 1310.子数组异或查询](https://zhuanlan.zhihu.com/p/392279673) · 知乎 · 2021-07-22 · 赞同 0**
> 力扣：[1310. 子数组异或查询](https://leetcode.cn/problems/xor-queries-of-a-subarray/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1310.子数组异或查询

[力扣](https://leetcode-cn.com/problems/xor-queries-of-a-subarray/)

注意到异或操作满足A^A \= 0，那么这里的区间异或就可以通过前缀操作来完成。

例如对于arr[l]^arr[l + 1]^arr[l + 2]^...^arr[r]这一段，我们可以将其视为

((arr[0]^arr[1]^...^arr[l - 1])^(arr[0]^arr[1]^...^arr[l - 1]))^arr[l]^arr[l + 1]^...^arr[r]

也就是

(arr[0]^arr[1]^...^arr[l - 1])^(arr[0]^arr[1]^...^arr[l - 1]^arr[l]^arr[l + 1]^...^arr[r])

可以发现这就变成了两个前缀异或了

于是我们可以先一趟扫描，计算出所有的前缀异或并储存在一个数组s当中。接下来对于每一个询问(l, r)，若l为0，那么答案就是s[r]，否则答案就是s[l - 1]^s[r]。

最后附上python代码：

```python
class Solution(object):
    def xorQueries(self, arr, queries):
        """
        :type arr: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        s = [arr[0]]
        for num in arr[1:]:
            s.append(s[-1] ^ num)
        
        return [s[r] if l == 0 else s[r] ^ s[l - 1] for l, r in queries]
```

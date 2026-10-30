---
title: "1458. 两个子序列的最大点积"
aliases: ["yiduobo的每日leetcode 1458.两个子序列的最大点积"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/四-经典线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/412435492"
zhihu_id: "412435492"
zhihu_title: "yiduobo的每日leetcode 1458.两个子序列的最大点积"
question_id: "1458"
question: "两个子序列的最大点积"
problem_url: "https://leetcode.cn/problems/max-dot-product-of-two-subsequences/"
difficulty: "Hard"
rating: 1824
created: "2021-09-21T13:49:44+08:00"
updated: "2021-09-21T13:49:44+08:00"
upvotes: 0
comments: 0
---

# 1458. 两个子序列的最大点积

> **[yiduobo的每日leetcode 1458.两个子序列的最大点积](https://zhuanlan.zhihu.com/p/412435492) · 知乎 · 2021-09-21 · 赞同 0**
> 力扣：[1458. 两个子序列的最大点积](https://leetcode.cn/problems/max-dot-product-of-two-subsequences/) · Hard · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推到空间优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1458.两个子序列的最大点积

[力扣](https://leetcode-cn.com/problems/max-dot-product-of-two-subsequences/)

涉及到两个子序列相关的问题通常都是用动态规划来处理，令f[i][j]表示nums1的前i个字符与nums2的前j个字符所能构成的最大点积，那么对于f[i][j]：

1、当i和j都为0时：

由于题目要求的子序列必须非空，因此这里必须选择nums1[0]以及nums2[0]，于是有

f[i][j] \= nums1[0] \* nums2[0]

2、当i为0，j不为0时：

此时必须选择nums1[0]，当选择nums2[j]时，就有

f[i][j] \= nums1[0] \* nums2[j]

当不选择nums2[j]时，就有

f[i][j] \= f[i][j - 1]

于是有

f[i][j] \= max(f[i][j - 1], nums1[0] \* nums2[j])

3、当i不为0，j为0时：

与情况2类似，有

f[i][j] \= max(f[i - 1][j], nums1[i] \* nums2[0])

4、当i和j都不为0时：

此时可以选择nums1[i]与nums2[j]配对，那么之前可以得到的最大答案就是f[i - 1][j - 1]。若这个值小于0，那么就没必要保留下来，于是有

f[i][j] \= max(f[i - 1][j - 1], 0) + nums1[i] \* nums2[j]

此时也可以放弃掉nums1[i]或者nums2[j]中的一个，于是有

f[i][j] \= max(f[i - 1][j], f[i][j - 1])

综合起来就有

f[i][j] \= max(max(f[i - 1][j - 1], 0) + nums1[i] \* nums2[j], f[i - 1][j], f[i][j - 1])

动态规划处理完之后，最终答案就是f[-1][-1]

最后附上python代码：

```python
class Solution(object):
    def maxDotProduct(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """

        m = len(nums1)
        n = len(nums2)

        f = [[None] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if i == 0:
                    if j == 0:
                        f[i][j] = nums1[i] * nums2[j]
                    else:
                        f[i][j] = max(f[i][j - 1], nums1[i] * nums2[j])
                elif j == 0:
                    f[i][j] = max(f[i - 1][j], nums1[i] * nums2[j])
                else:
                    f[i][j] = max(max(f[i - 1][j - 1], 0) + nums1[i] * nums2[j], f[i][j - 1], f[i - 1][j])
                    
        return f[-1][-1]
```

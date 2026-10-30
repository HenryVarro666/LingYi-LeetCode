---
title: "3202. 找出有效子序列的最大长度II"
aliases: ["yiduobo的每日leetcode 3202.找出有效子序列的最大长度II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/707445941"
zhihu_id: "707445941"
zhihu_title: "yiduobo的每日leetcode 3202.找出有效子序列的最大长度II"
question_id: "3202"
question: "找出有效子序列的最大长度 II"
problem_url: "https://leetcode.cn/problems/find-the-maximum-length-of-valid-subsequence-ii/"
difficulty: "Medium"
rating: 1974
created: "2024-07-07T00:47:48+08:00"
updated: "2024-07-07T00:47:48+08:00"
upvotes: 2
comments: 0
---

# 3202. 找出有效子序列的最大长度II

> **[yiduobo的每日leetcode 3202.找出有效子序列的最大长度II](https://zhuanlan.zhihu.com/p/707445941) · 知乎 · 2024-07-07 · 赞同 2**
> 力扣：[3202. 找出有效子序列的最大长度 II](https://leetcode.cn/problems/find-the-maximum-length-of-valid-subsequence-ii/) · Medium · 灵茶山艾府：[分析式子+动态规划，两种方法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3202.找出有效子序列的最大长度II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-maximum-length-of-valid-subsequence-ii/description/)

题目给出一个整数数组nums以及一个正整数k，要求从nums中找出一个子序列sub，满足

(sub[0] + sub[1]) % k \= (sub[1] + sub[2]) % k \= ... \= (sub[-2] + sub[-1]) % k

问sub最长可以是多少。

上一题的加强版，但是这里模k的结果有k种，不能分情况一个一个进行讨论，而是需要找出普适的处理方法。

方便起见，在这里可以想将nums中的每一项对k取模，不影响最终结果。

接下来可以尝试从0到k - 1枚举子序列相邻项之和对k的取模结果r。确定了这个r之后，就可以尝试用动态规划来求解了。

令f[i][j]表示前i项中选出以j为结尾，且子序列相邻项之和模k等于r时的最长子序列长度。对于f[i][j]：

1、首先有f[i][j] \= f[i - 1][j]，表示放弃掉nums[i]。

2、如果要选择nums[i]：

2-1）当nums[i] \<\= r时，其只能接在r - nums[i]的后面，即

f\[i\]\[nums\[i\]\] \= max(f\[i\]\[nums\[i\]\], f\[i - 1\]\[r - nums\[i\]\] + 1)

2-2）反之，当nums[i] > r时，其只能接在r + k - nums[i]的后面，即

f\[i\]\[nums\[i\]\] \= max(f\[i\]\[nums\[i\]\], f\[i - 1\]\[r + k - nums\[i\]\] + 1)

这样一来，只需一趟遍历就可以得到相邻项之和模k等于r的最长子序列的长度。对于每种r计算最优的子序列长度，取最大值作为最终答案即可。

另外注意到上面的f值都只与上一轮有关，同时f[i][j]必然大于等于f[i - 1][j]，因此在这里可以省去i这一维，直接在f数组中原地计算就可以了。

最后附上python代码：

```python
class Solution(object):
    def maximumLength(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        nums = [v % k for v in nums]

        res = 0
        for r in range(k):
            f = [0] * k
            for v in nums:
                if r >= v:
                    f[v] = f[r - v] + 1
                else:
                    f[v] = f[k + r - v] + 1
            
            res = max(res, max(f))
        
        return res
```

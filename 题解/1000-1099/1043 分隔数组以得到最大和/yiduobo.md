---
title: "1043. 分隔数组以得到最大和"
aliases: ["yiduobo的每日leetcode 1043.分隔数组以得到最大和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/五-划分型-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/370931981"
zhihu_id: "370931981"
zhihu_title: "yiduobo的每日leetcode 1043.分隔数组以得到最大和"
question_id: "1043"
question: "分隔数组以得到最大和"
problem_url: "https://leetcode.cn/problems/partition-array-for-maximum-sum/"
difficulty: "Medium"
rating: 1916
created: "2021-05-09T20:09:13+08:00"
updated: "2021-05-09T20:09:13+08:00"
upvotes: 0
comments: 0
---

# 1043. 分隔数组以得到最大和

> **[yiduobo的每日leetcode 1043.分隔数组以得到最大和](https://zhuanlan.zhihu.com/p/370931981) · 知乎 · 2021-05-09 · 赞同 0**
> 力扣：[1043. 分隔数组以得到最大和](https://leetcode.cn/problems/partition-array-for-maximum-sum/) · Medium · 灵茶山艾府：[教你一步步思考动态规划！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1043.分隔数组以得到最大和

[力扣](https://leetcode-cn.com/problems/partition-array-for-maximum-sum/)

动态规划的题目，令f[i]表示前i个数可以得到的最大和，那么对于f[i]:

1、可以将arr[i - 1]单独分出去，那么就有

f[i] \= max(f[i], f[i - 1] + arr[i - 1])

2、可以将arr[i - 1]以及arr[i - 2]分在一组，那么就有

f[i] \= max(f[i], f[i - 2] + max(arr[i - 1], arr[i - 2])) \* 2

3、可以将arr[i - 1]、arr[i - 2]以及arr[i - 3]分在一组，那么就有

f[i] \= max(f[i], f[i - 3] + max(arr[i - 1], arr[i - 2], arr[i - 3])) \* 3

...

K、可以将arr[i - 1]、arr[i - 2]、arr[i - 3]、...、arr[i - k + 1]分在一组，那么就有

f[i] \= max(f[i], f[i - k + 1] + max(arr[i - 1], arr[i - 2], arr[i - 3], ... , arr[i - k])) \* k

观察上面这些式子，可以发现对于随着分组的增大，arr取max的范围也是在逐渐增大，那么我们就可以按这个顺序进行计算，这样一来每一轮计算分组中arr的最大值时就可以利用上一次的结果。

举个例子，对于将arr[i - 1]、arr[i - 2]、...、arr[i - p + 1]分到一组时，有

f[i] \= max(f[i], f[i - p + 1] + max(arr[i - 1], arr[i - 2], ..., arr[i - p + 1]) \* p )

不妨设arr取max的结果为max_p，那么对于arr[i - 1]、arr[i - 2]、...、arr[i - p + 2]分到一组时，有

f[i] \= max(f[i], f[i - p + 1] + max(arr[i - 1], arr[i - 2], ..., arr[i - p + 2]) \* (p + 1))

其中 max(arr[i - 1], arr[i - 2], ..., arr[i - p + 2])也可以写成

max(max(arr[i - 1], arr[i - 2], ..., arr[i - p + 1]), arr[i - p + 2])

也就是max_p+1 \= max(max_p, arr[i - p + 2])

因此我们可以一边计算max_p一边计算f，从而在O(nk)的时间复杂度内完成动态规划。

最后附上代码：

```python
class Solution(object):
    def maxSumAfterPartitioning(self, arr, k):
        """
        :type arr: List[int]
        :type k: int
        :rtype: int
        """

        n = len(arr)
        f = [0] * (n + 1)
        for i in range(n):
            ma = arr[i]
            j = i
            f[i + 1] = f[j] + ma
            while j > 0 and j > i - k + 1:
                j -= 1
                ma = max(ma, arr[j])
                f[i + 1] = max(f[i + 1], f[j] + ma * (i - j + 1))
        
        return f[-1]
```

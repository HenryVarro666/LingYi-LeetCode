---
title: "1187. 使数组严格递增"
aliases: ["yiduobo的每日leetcode 1187.使数组严格递增"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/binary-search", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/四-经典线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/380358877"
zhihu_id: "380358877"
zhihu_title: "yiduobo的每日leetcode 1187.使数组严格递增"
question_id: "1187"
question: "使数组严格递增"
problem_url: "https://leetcode.cn/problems/make-array-strictly-increasing/"
difficulty: "Hard"
rating: 2316
created: "2021-06-13T15:22:20+08:00"
updated: "2021-06-13T15:22:20+08:00"
upvotes: 0
comments: 0
---

# 1187. 使数组严格递增

> **[yiduobo的每日leetcode 1187.使数组严格递增](https://zhuanlan.zhihu.com/p/380358877) · 知乎 · 2021-06-13 · 赞同 0**
> 力扣：[1187. 使数组严格递增](https://leetcode.cn/problems/make-array-strictly-increasing/) · Hard · 灵茶山艾府：[最长递增子序列的变形：选或不选/枚举选哪个（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1187.使数组严格递增

[力扣](https://leetcode-cn.com/problems/make-array-strictly-increasing/)

数组中的每一位的取值范围都取决于上一位的大小，那么很自然想到使用动态规划来解决，令f[i][j]表示使arr1前i位严格递增，且最后一位大小为j时所需的最小操作次数。

注意到这里arr中的数可以到10^9，但是数组的长度最多只有2000，也就是说arr1和arr2中总共最多只有4000个数，那么我们可以想将这些数收集起来进行排序，然后建立起数字到顺序的映射，这样一来就可以将这些数字离散到0到4000之间了。

对于f[i][j]，有三种情况：

1、若此时的arr1[i]恰好就等于j，那么此时就有：

f[i][j] \= min(f[i - 1][0], f[i - 1][1], ..., f[i - 1][j - 1])

2、若此时的arr1[i]不等于j，但j在arr2中出现过，那么我们可以进行一次替换：

f[i][j] \= min(f[i - 1][0], f[i - 1][1], ..., f[i -1][j - 1]) + 1

3、若上面两个条件都不满足，那么说明f[i][j]这个状态是不可能达成的，因此此时应该将f[i][j]置为无穷大

对于情况1和情况2中状态转移方程，看上去复杂度是比较高的，不过仔细观察可以发现括号里面是一个前缀最小值。

对于处理f[i][j]的情况，我们需要的是

mins[j] \= min(f[i - 1][0], f[i - 1][1], ..., f[i - 1][j - 1])

而对于处理f[i][j - 1]的情况，我们需要的是

mins[j - 1] \= min(f[i - 1][0], f[i - 1][1], ..., f[i - 1][j - 2])

可以mins[j] \= min(mins[j - 1], f[i - 1][j - 1])

因此我们可以使用一个变量mins来维护括号中的最小值，当处理到f[i][j]时，我们先用mins来更新f[i][j]，然后再用f[i - 1][j]来更新mins，这样mins就可以更新后续的f[i][j +1]了。

另外，注意到这里的f只与上一轮有关，因此可以压缩掉i这一维。

最后附上python代码：

```python
class Solution(object):
    def makeArrayIncreasing(self, arr1, arr2):
        """
        :type arr1: List[int]
        :type arr2: List[int]
        :rtype: int
        """

        num_set = set()
        for num in arr1:
            num_set.add(num)
        for num in arr2:
            num_set.add(num)
        
        num_dict = {}
        cnt = 1
        for num in sorted(list(num_set)):
            num_dict[num] = cnt
            cnt += 1
        
        for index in range(len(arr1)):
            arr1[index] = num_dict[arr1[index]]

        arr2_set = set()
        for index in range(len(arr2)):
            arr2[index] = num_dict[arr2[index]]
            arr2_set.add(arr2[index])

        f = [2001] * cnt
        f[0] = 0
        for i in range(len(arr1)):
            min_s = f[0]
            for j in range(1, cnt):
                tmp = f[j]
                f[j] = 2001
                if j == arr1[i]:
                    f[j] = min(f[j], min_s)
                elif j in arr2_set:
                    f[j] = min(f[j], min_s + 1)
                min_s = min(min_s, tmp)
            f[0] = 2001

        res = min(f)
        if res > 2000:
            res = -1
        return res
```

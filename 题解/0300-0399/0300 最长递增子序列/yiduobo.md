---
title: "300. 最长上升子序列"
aliases: ["yiduobo的每日leetcode 300.最长上升子序列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/recursion", "leetcode/memoization", "leetcode/binary-search", "leetcode/dynamic-programming", "题单/动态规划", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/动态规划/四-经典线性-DP", "题单/LeetCode-热题-100/动态规划", "题单/面试经典-150-题/一维动态规划"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/157613088"
zhihu_id: "157613088"
zhihu_title: "yiduobo的每日leetcode 300.最长上升子序列"
question_id: "300"
question: "最长递增子序列"
problem_url: "https://leetcode.cn/problems/longest-increasing-subsequence/"
difficulty: "Medium"
created: "2020-07-07T20:57:06+08:00"
updated: "2020-07-07T20:57:06+08:00"
upvotes: 1
comments: 0
---

# 300. 最长上升子序列

> **[yiduobo的每日leetcode 300.最长上升子序列](https://zhuanlan.zhihu.com/p/157613088) · 知乎 · 2020-07-07 · 赞同 1**
> 力扣：[300. 最长递增子序列](https://leetcode.cn/problems/longest-increasing-subsequence/) · Medium · 灵茶山艾府：[【视频】三种方法：记忆化搜索/递推/二分查找（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

300.最长上升子序列<https://leetcode-cn.com/problems/longest-increasing-subsequence/>

经典的动态规划问题，f[i]表示以第i个数结尾的最长上升子序列的长度，那么对于f[i]而言，由于需要以nums[i]结尾，那么需要枚举0到i - 1中小于nums[i]的数让nums[i]放在其后面，于是有f[i] \= max(f[j]) + 1，其中0 \<\= j \< i且nums[j] \< nums[i]。

两重循环，因此最终的时间复杂度为O(n^2)。

不过，这并不是最优的解法。

对于我们而言，要想得到更长的上升子序列，我们总是希望子序列中的数越小越好，于是可以维护一个数组res，其中res[index]表示长度为index + 1的上升子序列中某尾最小的数。

例如样例中的10,9,2,5,3,7,101,18，对于长度为3的上升子序列一共有

2，3，7

2，3，101

2，3，18

5，7，101

5，7，18

3，7，101

3，7，18

可以发现，最理想的长度为3的上升子序列就是2，3，7，因此res[2] \= 7

那么res的长度就是最终的答案，而初始的res则是res[0] \= nums[0]。

很明显，这个res数组一定是单调递增的，因为如果存在p > q且res[p] \< res[q]，那么设以res[p]为结尾的上升子序列为

x0，x1，...，xq，...，x(p-1)，res[p]

那么此时xq \< res[p] \< res[q]，而x0，x1，...，xq本身也是长度为q + 1的上升子序列，因此此时xq显然是比res[q]更符合res的定义的。

于是我们可以从左往右一趟扫描，对于当前处理到的nums[k]：

1、若nums[k] > res[-1]，说明nums[k]可以接在res[-1]的后面形成更长的上升子序列，此时将nums[k]加入到res的末尾即可

2、若nums[k] \= res[-1]，那么此时无事发生

3、若nums[k] \< res[-1]，那么说明res中存在比nums[k]大的数。不妨设res[p] \< nums[k] \<\= res[p +1]，那么对于由res[p + 1]为结尾的长度为p + 2的上升子序列，当nums[k] \< res[p + 1]时，将res[p + 1]替换成nums[k]之后一定是更优的。又由于res是单调递增的，因此我们可以通过二分找出这个p的位置，然后将res[p + 1]替换成nums[k]

一趟扫描，每次最多需要执行一次二分，因此最终的时间复杂度为O(nlogn)。

最后附上python代码：

```python
class Solution(object):
    def lengthOfLIS(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        if not nums:
            return 0

        res = [nums[0]]
        for num in nums[1:]:
            if num > res[-1]:
                res.append(num)
            elif num < res[-1]:
                l = 0
                r = len(res) - 1
                while l <= r:
                    mid = (l + r) / 2
                    if num <= res[mid]:
                        pos = mid
                        r = mid - 1
                    else:
                        l = mid + 1

                res[pos] = num

        return len(res)
```

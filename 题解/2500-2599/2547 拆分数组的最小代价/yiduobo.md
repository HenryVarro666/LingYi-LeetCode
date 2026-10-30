---
title: "2547. 拆分数组的最小代价"
aliases: ["yiduobo的每日leetcode 2547.拆分数组的最小代价"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/常用数据结构", "题单/动态规划", "题单/常用数据结构/八-树状数组和线段树", "题单/动态规划/五-划分型-DP", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/638943509"
zhihu_id: "638943509"
zhihu_title: "yiduobo的每日leetcode 2547.拆分数组的最小代价"
question_id: "2547"
question: "拆分数组的最小代价"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-split-an-array/"
difficulty: "Hard"
rating: 2020
created: "2023-06-22T22:35:22+08:00"
updated: "2023-06-22T22:35:22+08:00"
upvotes: 0
comments: 0
---

# 2547. 拆分数组的最小代价

> **[yiduobo的每日leetcode 2547.拆分数组的最小代价](https://zhuanlan.zhihu.com/p/638943509) · 知乎 · 2023-06-22 · 赞同 0**
> 力扣：[2547. 拆分数组的最小代价](https://leetcode.cn/problems/minimum-cost-to-split-an-array/) · Hard · 灵茶山艾府：[动态规划+线段树优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2547.拆分数组的最小代价

[力扣](https://leetcode.cn/problems/minimum-cost-to-split-an-array/)

经典的动态规划问题。对于这类问题，通常的处理方法是令f[i]表示划分前i个数的最小代价。对于f[i]，最朴素的处理方法就是枚举最后这个子数组的左边界j，那么就有f[i] \= min(f[i], f[j - 1] + cost(j, i))。由于本题的数据规模不大，因此只需保证计算cost(j, i)的复杂度为O(1)，就能将整个计算的复杂度控制在O(n^2)了。

对于本题，cost(j, i)的值取决于子数组中每个数字出现的次数，那么在这里只需使用一个哈希表记录子数组中每种数字出现的次数，然后后往前遍历j。对于j到i这一段中每种数字出现的次数，可以利用j + 1到i这一段中每种数字出现的次数，再加上位置j上这个数字的这一次来得到，因此只需更新哈希表中对应数字出现的次数，并根据其次数的变化更新cost值即可。

需要注意的是，落单数字并不会影响到cost的计算，而当某个数字出现次数由1变成2时，其对cost的影响则会从0变为2，需要对这两种情况进行特别处理。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        f = [0]
        n = len(nums)
        for i in range(n):
            mi = None
            s = 0
            cnt = {}
            for j in range(i, -1, -1):
                if nums[j] not in cnt:
                    cnt[nums[j]] = 1
                else:
                    if cnt[nums[j]] == 1:
                        s += 2
                    else:
                        s += 1
                    
                    cnt[nums[j]] += 1
                
                if mi is None or mi > f[j] + s + k:
                    mi = f[j] + s + k
            
            f.append(mi)

        return f[-1]
```

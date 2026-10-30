---
title: "3551. 数位和排序需要的最小交换次数"
aliases: ["yiduobo的每日leetcode 3551.数位和排序需要的最小交换次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/union-find", "leetcode/graph", "leetcode/sorting", "题单/常用数据结构", "题单/常用数据结构/七-并查集"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1909672887209669277"
zhihu_id: "1909672887209669277"
zhihu_title: "yiduobo的每日leetcode 3551.数位和排序需要的最小交换次数"
question_id: "3551"
question: "数位和排序需要的最小交换次数"
problem_url: "https://leetcode.cn/problems/minimum-swaps-to-sort-by-digit-sum/"
difficulty: "Medium"
rating: 1507
created: "2025-05-24T18:32:02+08:00"
updated: "2025-05-24T18:32:02+08:00"
upvotes: 0
comments: 0
---

# 3551. 数位和排序需要的最小交换次数

> **[yiduobo的每日leetcode 3551.数位和排序需要的最小交换次数](https://zhuanlan.zhihu.com/p/1909672887209669277) · 知乎 · 2025-05-24 · 赞同 0**
> 力扣：[3551. 数位和排序需要的最小交换次数](https://leetcode.cn/problems/minimum-swaps-to-sort-by-digit-sum/) · Medium · 灵茶山艾府：[建图+计算连通块的个数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3551.数位和排序需要的最小交换次数

[3551. 数位和排序需要的最小交换次数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-swaps-to-sort-by-digit-sum/description/)

题目给出一个由互不相同的正整数组成的数组nums，要求根据每个数字的数位和，按升序对数组进行排序。对于数位和相等的数字，则将较小的数字排在前面。

要求返回将nums按上面的要求完成排序的最小交换次数。

题目要求将nums按照数位和排序，那么就需要先一趟遍历，通过模10除10的方法计算出每个元素的数位和，记为数组digits_sum。

接下来可以设置一个目标位置数组target，target的初始值为0到n - 1。然后对于target中的每个元素，以其在digits_sum中的对应值为第一关键字，在nums中的对应值为第二关键字进行排序，排序后的target就表示原数组中处于下标index的元素nums[index]应该在最终排序后的数组中的下标应该是target[index]。

有了target之后，就只需要对0到n - 1之间的所有下标进行一趟遍历。对于当前遍历到的index，如果index刚好就位于target\[index\]，这种情况下就不需要进行交换了，直接跳过，否则就需要将其交换到target\[index\]，而对于原来位于target\[index\]的元素，其目标位置是target\[target\[index\]\]，若这个值不等于index，就需要继续执行交换，直到元素的目标位置恰好是index为止。若这个交换路径的长度为k，那么需要的交换次数就是k - 1。另外在具体实现上，并不需要真的执行交换，而是只需要记录哪个下标位置被访问过就行了。

最后附上python代码：

```python
class Solution(object):
    def minSwaps(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        n = len(nums)
        digits_sum = [0] * n
        for index, v in enumerate(nums):
            while v:
                digits_sum[index] += v % 10
                v //= 10
        
        target = [index for index in range(n)]
        target.sort(key=lambda d:(digits_sum[d], nums[d]))
        
        res = 0
        vis = [False] * n
        for index in range(n):
            if not vis[index]:
                vis[index] = True
                now = index
                while target[now] != index:
                    now = target[now]
                    vis[now] = True
                    res += 1
        
        return res
```

---
title: "3176. 求出最长好子序列I & 3177. 求出最长好子序列II"
aliases: ["yiduobo的每日leetcode 3176.求出最长好子序列I && 3177.求出最长好子序列II", "3176. 求出最长好子序列I", "3177. 求出最长好子序列II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP", "leetcode/hard", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/705648866"
zhihu_id: "705648866"
zhihu_title: "yiduobo的每日leetcode 3176.求出最长好子序列I && 3177.求出最长好子序列II"
question_id: ["3176", "3177"]
question: ["求出最长好子序列 I", "求出最长好子序列 II"]
problem_url: ["https://leetcode.cn/problems/find-the-maximum-length-of-a-good-subsequence-i/", "https://leetcode.cn/problems/find-the-maximum-length-of-a-good-subsequence-ii/"]
difficulty: ["Medium", "Hard"]
rating: ["1849", "2365"]
created: "2024-06-27T01:29:51+08:00"
updated: "2024-06-27T01:29:51+08:00"
upvotes: 0
comments: 0
---

# 3176. 求出最长好子序列I & 3177. 求出最长好子序列II

> **[yiduobo的每日leetcode 3176.求出最长好子序列I && 3177.求出最长好子序列II](https://zhuanlan.zhihu.com/p/705648866) · 知乎 · 2024-06-27 · 赞同 0**
> 力扣：[3176. 求出最长好子序列 I](https://leetcode.cn/problems/find-the-maximum-length-of-a-good-subsequence-i/) · Medium · 灵茶山艾府：[动态规划（Python/Java/C++/Go）](../3176%20求出最长好子序列%20I/灵茶山艾府.md)
> 力扣：[3177. 求出最长好子序列 II](https://leetcode.cn/problems/find-the-maximum-length-of-a-good-subsequence-ii/) · Hard · 灵茶山艾府：[动态规划+优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3176.求出最长好子序列I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-maximum-length-of-a-good-subsequence-i/description/)

3177.求出最长好子序列II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-maximum-length-of-a-good-subsequence-ii/description/)

题目给出一个数组nums以及一个非负整数k，要求从nums中找出一个最长的子序列，使得子序列中值不相等的相邻元素对不超过k组。

两题的题设一样，第二题数据规模较大，nums的长度n可以达到5000，而k则可以达到50。

比较原始的动态规划是比较好想的。令f[i][j]表示以nums[i]结尾，且其中最多出现j组不相等的相邻元素的最长子序列的长度。那么对于f[i][j]，可以从0到i - 1枚举前一个子序列的结尾p，那么:

当nums[i] \= nums[p]时，有

f[i][j] \= max(f[i][j], f[p][j] + 1)

表示将nums[i]接在f[p][j]后面。因为nums[p]与nums[i]相等，不会产生额外的不相等数对。

当nums[i] !\= nums[p]时，有

f[i][j] \= max(f[i][j], f[p][j - 1] + 1)

表示将nums[i]接在f[p][j - 1]后面。因为nums[p]与nums[i]不相等，所以需要预留一个位置给这一组不相等的数对，因此f[i][j]需要从f[p][j - 1]转移过来。

上面算法的状态表示是O(nk)的，转移时需要枚举p，复杂度也是O(n)的，因此总的时间复杂度为O(n^2 \* k)，对于本题而言这个复杂度比较勉强，需要进行优化。

状态表示方面，O(nk)的状态不太好优化，那么就应该从转移方面来想办法。

首先考虑nums[i] \= nums[p]的情况。

对于两个下标p \< q，若nums\[p\] \= nums\[q\]，那么f\[p\]\[j\]必然小于f\[q\]\[j\]，因为对于f\[q\]\[j\]，可以在f\[p\]\[j\]对应的子序列末尾直接加入nums\[q\]得到更长的子序列。换言之，如果选择与nums\[i\]使用相等的nums\[p\]对应的f\[p\]\[j\]来更新f\[i\]j\]，那么就应该选择nums\[i\]在0到i - 1中最后一次出现的下标对应的f值来更新f\[i\]\[j\]。于是只需添加一个哈希表last，其中last\[x\]\[j\]表示以数值x结尾且存在j组不相等的相邻元素的最长子序列长度，然后就可以用last\[nums\[i\]\]\[j\]来更新f\[i\]\[j\]了。

接下来考虑nums[i] !\= nums[p]的情况。可以发现，此时并不需要关心nums[p]具体等于多少，而是只需要选取f[0][j - 1]到f[i - 1][j - 1]中的最大值就可以了，这是一个静态的前缀最大值问题，于是可以使用一个数组best[i][j]记录f[0][j]到f[i][j]之间的最大值，那么f[i][j]就可以通过best[i - 1][j - 1]来更新了。

值得一提的是，这里有一种情况是best\[i - 1\]\[j - 1\]中记录的f\[p\]\[j - 1\]对应的nums\[p\]恰好等于nums\[i\]。在这种情况下，转移方程中的f\[i\]\[j\] \= max(f\[i\]\[j\], f\[p\]\[j - 1\] + 1)浪费掉了一组不相等的机会。但是可以发现，对于这种情况，已经在上面的讨论中的last\[nums\[p\]\]\[j\]必然等于f\[p\]\[j\]，也就是说已经用f\[p\]\[j\]更新过f\[i\]\[j\]了，所以这里浪费一次也无关紧要。

得到f\[i\]\[j\]后，使用f\[i\]\[j\]分别更新last\[nums\[i\]\]\[j\]以及best\[i\]\[j\]即可。到了这里，转移的复杂度就优化到了O(1)。

另外f\[i\]\[j\]的更新只取决于last\[nums\[i\]\]\[j\]以及best\[i - 1\]\[j - 1\]，而其作用只是用来更新最新的last以及best，那么就可以利用滚动数组以及反向遍历省去best中i这一维以及f数组，不过哈希表last无法进行优化。在最坏情况下，last占用的空间依然是O(nk)。

最后附上python代码：

```python
class Solution(object):
    def maximumLength(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        n = len(nums)

        last = {}
        best = [0] * (k + 1)

        for v in nums:
            last[v] = [0] * (k + 1)

        res = 0
        for i in range(len(nums)):
            for j in range(k, -1, -1):
                v = last[nums[i]][j] + 1
                if j > 0:
                    v = max(v, best[j - 1] + 1)
                
                last[nums[i]][j] = v
                best[j] = max(best[j], v)

        return best[-1]
```

---
title: "2945. 找到最大非递减数组的最大值"
aliases: ["yiduobo的每日leetcode 2945.找到最大非递减数组的最大值"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "leetcode/monotonic-queue", "题单/动态规划", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/691606381"
zhihu_id: "691606381"
zhihu_title: "yiduobo的每日leetcode 2945.找到最大非递减数组的最大值"
question_id: "2945"
question: "找到最大非递减数组的长度"
problem_url: "https://leetcode.cn/problems/find-maximum-non-decreasing-array-length/"
difficulty: "Hard"
rating: 2943
created: "2024-04-10T00:56:13+08:00"
updated: "2024-04-10T00:56:13+08:00"
upvotes: 1
comments: 1
---

# 2945. 找到最大非递减数组的最大值

> **[yiduobo的每日leetcode 2945.找到最大非递减数组的最大值](https://zhuanlan.zhihu.com/p/691606381) · 知乎 · 2024-04-10 · 赞同 1**
> 力扣：[2945. 找到最大非递减数组的长度](https://leetcode.cn/problems/find-maximum-non-decreasing-array-length/) · Hard · 灵茶山艾府：[单调队列优化 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2945.找到最大非递减数组的最大值

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-maximum-non-decreasing-array-length/description/)

首先可以明确的是，本题应该是没法用贪心法来处理的，理由是遇到逆序时，逆序的数既可以向前合并，也可以向后合并，没有一种方案可以保证当前选择的合并方向是最优的。也就是说，本题只能想办法使用动态规划来求解。

动态规划的状态表示是比较直观的。由于题目要求最终的数组最长，因此可以令f[i]表示前i个数可以得到的最长非递减数组。另外，仅有这个状态表示无法进行状态转移，因为还涉及到了数值大小，因此还需要使用另一个数组g[i]来表示f[i]对应的数组中最后这一项的值是多少。

那么对于f[i]和g[i]，就可以向前遍历找到最大的满足nums[j + 1] + nums[j + 2] + ... + nums[i] >\= g[j]的j，表达的意思是如果将nums[j + 1]开始到nums[i]合并成一项，就可以将其拼凑在g[j]的后面，此时就有f[i] \= f[j] + 1，而g[j] \= nums[j + 1] + nums[j + 2] + ... + nums[i]。

这里只取最大的满足条件的j的理由是f数组显然是单调不减的，而随着j的向前，f数组有减小的风险，而最终用来更新g[i]的nums[j + 1] + nums[j + 2] + ... + nums[i]则是单调递增的，也就是说越往前能找到的f[j]就越小，而最终得到的g[i]就越大，都是不优的，因此找到最大的j时就应该直接收手。

尽管如此，上面的算法依然是O(n^2)的，在本题的数据规模下依然需要进行优化。

观察转移的条件nums[j + 1] + nums[j + 2] + ... + nums[i] >\= g[j]，如果将其写作前缀和的形式，那么就是s[i] - s[j] >\= g[j]。对于这种情况，一种场景的技巧就是将下标相同的项放在一起，也就是s[i] >\= s[j] + g[j]，那么问题就变成了找出最大的满足s[j] + g[j] \<\= s[i]的j。

接下来不妨考虑一组下标j, k，设k \< j。那么当s[k] + g[k] >\= s[j] + g[j]时，所有可以通过f[k]和g[k]转移的i就都可以通过f[j]和g[j]来进行转移。又由于上面已经说明了在这里应该找到尽量靠后的位置来进行状态转移，换言之在这里后续的i都不可能通过k来进行转移，而可以用来转移的位置的s[j] + g[j]必然是单调递增的，也就是说可以使用一个单调队列q来保存所有可以用来转移的下标。

对于当前的下标i，若队列的第二位，也就是q\[1\]对应的s\[q\[1\]\]和g\[q\[1\]\]之和小于等于s\[i\]，那么说明队首对应的下标q\[0\]就已经没用了，因为s数组也是单调递增的，也就是说对于后续所有的s\[i'\]，都满足s\[q\[1\]\] + g\[q\[1\]\] \<\= s\[i'\]，而队首对应的下标q\[0\]是小于q\[1\]的，因此不会再从q\[0\]来进行状态转移，此时就应该将队首弹出队列。重复此过程直到队列中只剩下一个元素或者q\[1\]满足s\[q\[1\]\] + g\[q\[1\]\] > s\[i\]为止。

接下来使用f\[q\[0\]\] + 1来更新f\[i\]，使用nums\[q\[0\] + 1\] + nums\[q\[0\] + 2\] + ... + nums\[i\]，也就是s\[i\] - s\[q\[0\]\]来更新g\[i\]。

得到了f\[i\]和g\[i\]之后，则还需要使用s\[i\] + g\[i\]从后向前移除掉队尾不优的下标，也就是根据上面说到的下标组j, k表达的意思，从队尾开始移除掉所有满足s\[q\[-1\]\] + g\[q\[-1\]\] >\= s\[i\] + g\[i\]的元素。

最后，将i加入到单调栈中然后继续向后计算即可。

这样一来，由于每个下标只会进出队列一次，因此整体的复杂度被优化到了O(n)。

与之前使用单调队列进行优化的问题不同，本题中队首并不是因为不满足边界条件被弹出队列，而是因为队列中存在更优解而被弹出队列，是值得思考的地方。

最后附上python代码：

```python
class Solution(object):
    def findMaximumLength(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        s = [0]
        for v in nums:
            s.append(s[-1] + v)
        
        f = [0]
        g = [0]

        q = [0]
        p = 0

        for i in range(1, len(nums) + 1):
            while p + 1 < len(q) and s[q[p + 1]] + g[q[p + 1]] <= s[i]:
                p += 1
            
            f.append(f[q[p]] + 1)
            g.append(s[i] - s[q[p]])

            while len(q) > p and s[q[-1]] + g[q[-1]] >= s[i] + g[i]:
                q.pop()
            
            q.append(i)
        
        return f[-1]
```

---
title: "1787. 使所有区间的异或结果为零"
aliases: ["yiduobo的每日leetcode 1787.使所有区间的异或结果为零"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/memoization", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/463265181"
zhihu_id: "463265181"
zhihu_title: "yiduobo的每日leetcode 1787.使所有区间的异或结果为零"
question_id: "1787"
question: "使所有区间的异或结果为零"
problem_url: "https://leetcode.cn/problems/make-the-xor-of-all-segments-equal-to-zero/"
difficulty: "Hard"
rating: 2640
created: "2022-01-30T23:27:30+08:00"
updated: "2022-01-30T23:27:30+08:00"
upvotes: 1
comments: 0
---

# 1787. 使所有区间的异或结果为零

> **[yiduobo的每日leetcode 1787.使所有区间的异或结果为零](https://zhuanlan.zhihu.com/p/463265181) · 知乎 · 2022-01-30 · 赞同 1**
> 力扣：[1787. 使所有区间的异或结果为零](https://leetcode.cn/problems/make-the-xor-of-all-segments-equal-to-zero/) · Hard · 灵茶山艾府：[分类讨论：贪心+DP](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1787.使所有区间的异或结果为零

[力扣](https://leetcode-cn.com/problems/make-the-xor-of-all-segments-equal-to-zero/)

题目非常贴心地在样例中提示了最终答案必然是以长度k为区间循环出现的，具体证明也很容易。

对于任意位置p，有nums[p] ^ nums[p + 1] ^ ... ^ nums[p + k - 1] \= 0。两边异或上nums[p]，就有

nums[p + 1] ^ nums[p + 2] ^ ... ^ nums[p + k - 1] \= nums[p]

另一方面，由于nums[p + 1] ^ nums[p + 2] ^ ... ^ nums[p + k] \= 0，将上面的式子带入就有

nums[p] ^ nums[p + k] \= 0

从而可知nums[p] \= nums[p + k]

有了上面结论，就应该按下标模k的分组，然后此时又有两种选择方式：

1、从其中k - 1组中各选一个数，然后用剩下的这一组适配这些数的异或和。为了使得修改的数字最少，显然就应该选择各组中出现次数最多的那个数。此时一共选出了k个数，还需要去掉其中出现次数最少的那个数。这样以来，需要修改的数就是n减去留下的这k - 1个数出现的次数之和。

2、从k组中各选一个数，要求满足这k个数异或值为0。这种情况可以视为另类的背包问题。令f[i][j]表示从前i组中各选一个数，这些数异或结果为j时最多可以保留多少个数不变。对于f[i][j]，应该枚举第i组中的所有数。设当前枚举到num，其出现次数为cnt，那么就有f[i][j] \= max(f[i][j], f[i - 1][j ^ num] + cnt)。动态规划完成后，f[-1][0]就是最多保留下来的数，那么需要修改的数就是n - f[-1][0]。

另外，注意到这里f每一轮只与上一轮有关，因此可以滚动数组优化掉i这一维。

上面两种情况的答案计算完成后，选择其中较小的作为最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def minChanges(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        cnt_list = [{} for _ in range(k)]
        max_cnt = [0] * k

        for index, num in enumerate(nums):
            p = index % k
            cnt_list[p][num] = cnt_list[p].get(num, 0) + 1
            max_cnt[p] = max(max_cnt[p], cnt_list[p][num])

        f = [0] * 1024
        for num in cnt_list[0]:
            f[num] = cnt_list[0][num]

        for i in range(1, k):
            g = f[:]
            f = [0] * 1024
            for num, cnt in cnt_list[i].items():
                for j in range(1024):
                    if g[j] > 0:
                        f[j ^ num] = max(f[j ^ num], g[j] + cnt)
        
        return min(len(nums) - f[0], len(nums) - sum(max_cnt) + min(max_cnt))
```

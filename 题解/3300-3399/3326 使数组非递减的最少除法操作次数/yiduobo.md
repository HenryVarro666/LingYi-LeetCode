---
title: "3326. 使数组非递减的最少除法操作次数"
aliases: ["yiduobo的每日leetcode 3326.使数组非递减的最少除法操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/math", "leetcode/number-theory", "题单/数学算法", "题单/贪心算法", "题单/数学算法/一-数论", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2582322697"
zhihu_id: "2582322697"
zhihu_title: "yiduobo的每日leetcode 3326.使数组非递减的最少除法操作次数"
question_id: "3326"
question: "使数组非递减的最少除法操作次数"
problem_url: "https://leetcode.cn/problems/minimum-division-operations-to-make-array-non-decreasing/"
difficulty: "Medium"
rating: 1864
created: "2024-10-22T23:42:41+08:00"
updated: "2024-10-22T23:42:41+08:00"
upvotes: 0
comments: 0
---

# 3326. 使数组非递减的最少除法操作次数

> **[yiduobo的每日leetcode 3326.使数组非递减的最少除法操作次数](https://zhuanlan.zhihu.com/p/2582322697) · 知乎 · 2024-10-22 · 赞同 0**
> 力扣：[3326. 使数组非递减的最少除法操作次数](https://leetcode.cn/problems/minimum-division-operations-to-make-array-non-decreasing/) · Medium · 灵茶山艾府：[预处理 LPF + 从右到左贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3326.使数组非递减的最少除法操作次数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-division-operations-to-make-array-non-decreasing/description/)

题目给出一个整数数组nums。对于一个正整数x，所有严格小于x的正因子都是x的真因数。现在可以对nums的任意元素进行一次操作，将这个元素除以它最大的真因数。现在问至少需要执行多少次操作，才能将nums变为非递减的。若无法达成，则返回-1。

题目中描述操作实际上就是对于某个合数，将其变为其最小的质因子，对于质数则无法操作。那么在这里就可以先通过筛法或者直接暴力枚举计算出nums中每个元素的最小质因子，在这里记prime[x]为x的最小质因子。

接下来可以使用动态规划或者贪心法求解。

---

首先是动态规划。令f[i]和g[i]分别表示对nums[i]执行操作以及不对nums[i]执行操作时，保证nums[0]到nums[i]单调不减所需的最少操作次数，那么对于f[i]：

1、若nums[i] >\= nums[i - 1]：

这种情况下nums\[i\]可以直接放在nums\[i - 1\]或者prime\[nums\[i - 1\]\]的后面，于是有f\[i\] \= min(f\[i - 1\], g\[i - 1\])

2、若prime\[nums\[i - 1\]\] \<\= nums\[i\] \< nums\[i - 1\]：

此时nums\[i\]只能放在prime\[nums\[i - 1\]\]的后面，于是有f\[i\] \= g\[i - 1\]

3、若prime\[nums\[i - 1\]\] > nums\[i\]：

这种情况下无法构成可用的数组，直接返回-1。需要注意因为prime\[nums\[i\]\]必然小于等于nums\[i\]，因此此时也不存在可行的g\[i\]，所以可以直接返回-1。

另外对于g[i]，与上面f[i]的情况类似：

1、若prime\[nums\[i\]\] >\= nums\[i - 1\]：

此时有g[i] \= min(f[i - 1], g[i - 1]) + 1

2、若prime\[nums\[i - 1\]\] \<\= prime\[nums\[i\]\] \< nums\[i - 1\]:

此时有g[i] \= g[i - 1] + 1

3、若prime\[nums\[i - 1\]\] > prime\[nums\[i\]\]：

这种情况下无法构成g[i]，但是注意此时不能直接返回-1，因为此时还有可能构成f[i]

---

相比于动态规划，贪心法的思路更加巧妙。因为prime\[nums\[i\]\]必然小于等于nums\[i\]，且额外消耗了一次操作，那么如果从后往前看，对于每个元素能不执行操作就不应该执行操作，因为这样一来既使得操作的总数最小，又可以保留尽量大的元素值，让前面的元素有更大的选择空间。

于是可以直接保留nums\[-1\]，接下来从nums的倒数第二个元素向前一趟遍历，若当前元素值nums\[i\]小于等于nums\[i + 1\]，那么就需要执行操作，否则就需要执行操作，使用prime\[nums\[i\]\]替代nums\[i\]。若此时依然大于nums\[i + 1\]，则直接返回-1，否则更新答案然后继续向前遍历。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        res = 0
        now = nums[-1]
        prime = {}
        for index in range(len(nums) - 2, -1, -1):
            if nums[index] <= now:
                now = nums[index]
            else:
                if nums[index] not in prime:
                    p = 2
                    while p * p <= nums[index]:
                        if nums[index] % p == 0:
                            break
                        p += 1
                
                    if nums[index] % p == 0:
                        prime[nums[index]] = p
                    else:
                        return -1

                if  prime[nums[index]] <= now:
                    now = prime[nums[index]]
                    res += 1
                else:
                    return -1
        
        return res
```

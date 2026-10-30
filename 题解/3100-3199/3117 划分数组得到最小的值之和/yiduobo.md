---
title: "3117. 划分数组得到最小的值之和"
aliases: ["yiduobo的每日leetcode 3117.划分数组得到最小的值之和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/recursion", "leetcode/memoization", "leetcode/hash-table", "leetcode/dynamic-programming", "leetcode/monotonic-queue", "题单/动态规划", "题单/位运算", "题单/动态规划/五-划分型-DP", "题单/动态规划/十一-优化-DP", "题单/位运算/三-与或-AND/OR-的性质"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/701264461"
zhihu_id: "701264461"
zhihu_title: "yiduobo的每日leetcode 3117.划分数组得到最小的值之和"
question_id: "3117"
question: "划分数组得到最小的值之和"
problem_url: "https://leetcode.cn/problems/minimum-sum-of-values-by-dividing-array/"
difficulty: "Hard"
rating: 2735
created: "2024-06-03T02:05:23+08:00"
updated: "2024-06-03T02:05:23+08:00"
upvotes: 0
comments: 0
---

# 3117. 划分数组得到最小的值之和

> **[yiduobo的每日leetcode 3117.划分数组得到最小的值之和](https://zhuanlan.zhihu.com/p/701264461) · 知乎 · 2024-06-03 · 赞同 0**
> 力扣：[3117. 划分数组得到最小的值之和](https://leetcode.cn/problems/minimum-sum-of-values-by-dividing-array/) · Hard · 灵茶山艾府：[多维 DP：如何定义状态？（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3117.划分数组得到最小的值之和

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-sum-of-values-by-dividing-array/description/)

题目给出两个数组nums以及andValues，二者的长度分别为n和m。要求将nums划分为非空的m段，其中每段各不相交，同时段内数值按位与的结果与andValues中对应的值相等。记每一段中最后这个元素的值为这一段的值，需要找出一种划分方法，使得各段值之和最小。

这是非常标准的区间划分型的动态规划，最直观的做法自然是令f[i][j]表示nums中的前i个元素，划分为j段时的最小代价是多少。那么对于f[i][j]，可以枚举最后这一段的起点p，那么就有

f[i][j] \= min(f[i][j], f[p - 1][j - 1] + nums[i])，前提是nums[p] & nums[p + 1] & ... & nums[i] \= andValues[j]

这个算法的时间复杂度为O(n^2 \* m)，题目中m的取值范围虽然最大只有10，但是n的范围可以到10000，时间复杂度太高了，需要进行优化。

由于状态表示没有什么优化的空间，那么只能从转移方面来想办法。由于按位与结果是单调不增的，那么对于f[i][j]，不妨设now为以nums[i]为结尾的且大于等于andValues[j]的按位与结果，另外记最左侧满足nums[p] & nums[p + 1] & ... & nums[i] \= andValues[j]的p为left，最右侧满足nums[p] & nums[p + 1] & ... & nums[i] \= andValues[j]的p为right，那么当now \= andValues[j]时，就可以找出left - 1到right - 1中最小的f值best来更新f[i][j]。

随着i的向后移动，若nums[i]是区间起点，那么就应该初始化now为nums[i]，同时更新left和right为i；反之，则应该将nums[i]按位与到now中。接下来对于now：

1、now大于andValues[j]

此时不能更新f值，但是now在后面依然有机会变成andValues[j]，因此此时需要保留now、left、right不变然后继续向后考虑。

2、now等于andValues[j]

此时需要考虑更新f值了。

这种情况下，left无需移动，而right则有向后移动的可能，也就是说，这种情况下可以先尝试让right向后移动。

更进一步的，如果上一轮的now也等于andValues[j]，那么对于当前这一轮的[left, right]，left保持不变，而right则可能向后移动，换言之，本轮的[left, right]完全包含了上一轮的[left, right]，因此本轮的best就可以在上一轮best的基础上，考虑新老right之间这一段对应的f值就行了。

这种情况下，还有一个问题就是什么情况下可以让right向后移动。与常规的滑动窗口不同，本题中需要计算的是窗口中各元素的按位与结果，当i向后移动时，新元素加入可以直接按位与计算，但是当right移动时，nums[right]被弹出时需要计算弹出的其在哪些位上为1，因此需要再使用一个数组freq来记录区间内每一位上为1的元素的数量。

若随着nums[right]的弹出，now的某一位上唯一的0也被弹出，即freq中这一位对应的值等于right移动后的区间长度i - right，那么now在这一位上将从0变为1，从而使得now变为大于andValues[j]的数，这种情况下就不能向后移动right了。

3、now小于andValues[j]

这种情况下，后续的now也不可能再等于andValues，因此nums[i + 1]是无法用来构成andValues[j]的，此时就应该将now重新置为空表示按位与的区间被清空，然后计算向后考虑。

可以发现，只有情况2中会进行状态转移，而情况2中对于best是随着right的更新而更新的，right则是使用滑动窗口来更新的，转移的复杂度就优化到了均摊O(log(x))，其中x是nums中的最大值。

另外，由于f的每一轮只与上一轮有关，因此可以使用滚动数组优化掉i这一维。

最后附上python代码：

```python
class Solution(object):
    def minimumValueSum(self, nums, andValues):
        """
        :type nums: List[int]
        :type andValues: List[int]
        :rtype: int
        """

        n = len(nums)
        f = [-1] * (n + 1)
        f[0] = 0
        for v in andValues:
            g = f[:]
            f = [-1] * (n + 1)
            best = -1
            freq = [0] * 17
            now = None
            left = right = 0

            for index, x in enumerate(nums):
                if now is None:
                    now = nums[index]
                    left = right = index
                    best = -1
                else:
                    now &= x

                for t in range(17):
                    if x & (1 << t) == (1 << t):
                        freq[t] += 1

                if now == v:
                    if best == -1:
                        best = g[left]
                    while right < index:
                        tmp = 0
                        remove_pos = []
                        flag = True
                        for t in range(17):
                            if (nums[right] & (1 << t) == (1 << t)):
                                remove_pos.append(t)
                            elif freq[t] == index - right:
                                flag = False
                                break
                        
                        if flag:
                            for p in remove_pos:
                                freq[p] -= 1

                            right += 1
                            if best == -1 or (g[right] != -1 and best > g[right]):
                                best = g[right]
                        else:
                            break

                    if best != -1 and (f[index + 1] == -1 or f[index + 1] > best + x):
                        f[index + 1] = best + x
                    

                elif (now & v) < v:
                    now = None
                    freq = [0] * 17
            
        return f[-1]
```

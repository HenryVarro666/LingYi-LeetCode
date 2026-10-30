---
title: "3282. 到达数组末尾的最大得分"
aliases: ["yiduobo的每日leetcode 3282.到达数组末尾的最大得分"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/brainteaser", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/822720401"
zhihu_id: "822720401"
zhihu_title: "yiduobo的每日leetcode 3282.到达数组末尾的最大得分"
question_id: "3282"
question: "到达数组末尾的最大得分"
problem_url: "https://leetcode.cn/problems/reach-end-of-array-with-max-score/"
difficulty: "Medium"
rating: 1772
created: "2024-10-05T21:20:02+08:00"
updated: "2024-10-05T21:20:02+08:00"
upvotes: 1
comments: 0
---

# 3282. 到达数组末尾的最大得分

> **[yiduobo的每日leetcode 3282.到达数组末尾的最大得分](https://zhuanlan.zhihu.com/p/822720401) · 知乎 · 2024-10-05 · 赞同 1**
> 力扣：[3282. 到达数组末尾的最大得分](https://leetcode.cn/problems/reach-end-of-array-with-max-score/) · Medium · 灵茶山艾府：[【一图秒懂】贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3282.到达数组末尾的最大得分

[. - 力扣（LeetCode）](https://leetcode.cn/problems/reach-end-of-array-with-max-score/)

题目给出一个长度为n的整数数组nums，现在要从下标0开始跳转到下标n - 1，且只能往前跳不能往回跳。对于从下标i跳转到下标j的跳跃，可以得到(j - i) \* nums[i]的得分，问可以得到的最大总得分是多少。

第一眼看上去可以用动态规划解决，状态表示就是经典的f[i]表示从下标0跳到下标i可以得到的最大分数，那么对于f[i]，就有

f[i] \= max(f[0] + i \* nums[0], f[1] + (i - 1) \* nums[1], ..., f[i - 1] + nums[i - 1])

分别表示从0、1、...、i - 1这些下标跳转到i的情况下可以获得的最大得分。

这是一个O(n^2)的动态规划，必须要进行优化。

在这里实际上是要找出一个最优的中继点，那么不妨对比一下从j和k两个位置跳转到i时的得分情况。在这里先规定j \< k，那么对于

f[j] + (i - j) \* nums[j]

f[k] + (i - k) \* nums[k]

注意到nums前的系数不是对齐的，因此对比起来也比较麻烦。

一种可行的处理办法是强行填平这个系数，即对于f[k]，可以强行认为f[k] \= f[j] + (k - j) \* nums[j]，通过这次跳跃填平系数。这样一来，上面的式子就变成了

f[j] + (i - j) \* nums[j]

f[j] + (k - j) \* nums[j] + (i - k) \* nums[k] \= f[j] + (i - j) \* nums[j] + (i - k) \* (nums[k] - nums[j])

可以发现，上面两个式子可以约掉前面的所有项，只剩下最后的(i - k) \* (nums[k] - nums[j])。也就是说，在这里应该选择nums较大的那个位置作为中继点进行跳跃。

值得注意的是，上面的思路实际上是将不选择中继点，直接跳到目标位置这种情况视为选择目标位置作为中继点来进行考虑，并没有漏掉这种情况。

回到本题，从0出发到n - 1的中继点就应该选择nums最大的那个位置，不妨称为j[0]，那么在j[0]之后就不需要任何中继点了，但是从0到j[0]这一段依然是可以选择中继点的，最优的选择则是nums[0]到nums[j[0] - 1]之间最大值所在的下标，记为j[1]，然后从0到j[1]也是可以进行选择的，以此类推。

可以发现，在这里就是从下标0开始，每次都从当前下标now跳转到下一个大于nums[now]的下标index，直到跳到数组最大值所在的下标为止，然后完成最后一跳跳到n - 1结束。

于是只需一趟遍历，使用一个变量now记录目前是从哪个下标开始跳跃的。若当前遍历到的下标index为n - 1，或者nums[index] > nums[now]，那么就从now跳转到index并更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def findMaximumScore(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        now = 0
        res = 0
        for index in range(1, len(nums)):
            if index == len(nums) - 1 or nums[index] > nums[now]:
                res += (index - now) * nums[now]
                now = index
        
        return res
```

---
title: "3872. 替换最多一个元素后的最长等差子数组"
aliases: ["yiduobo的每日leetcode 3872.替换最多一个元素后的最长等差子数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/enumeration", "题单/滑动窗口与双指针", "题单/动态规划", "题单/滑动窗口与双指针/六-分组循环", "题单/动态规划/六-状态机-DP", "题单/动态规划/七-其他线性-DP", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2019114611111121125"
zhihu_id: "2019114611111121125"
zhihu_title: "yiduobo的每日leetcode 3872.替换最多一个元素后的最长等差子数组"
question_id: "3872"
question: "替换最多一个元素后的最长等差子数组"
problem_url: "https://leetcode.cn/problems/longest-arithmetic-sequence-after-changing-at-most-one-element/"
difficulty: "Medium"
rating: 2042
created: "2026-03-22T18:47:09+08:00"
updated: "2026-03-22T18:47:12+08:00"
upvotes: 0
comments: 0
---

# 3872. 替换最多一个元素后的最长等差子数组

> **[yiduobo的每日leetcode 3872.替换最多一个元素后的最长等差子数组](https://zhuanlan.zhihu.com/p/2019114611111121125) · 知乎 · 2026-03-22 · 赞同 0**
> 力扣：[3872. 替换最多一个元素后的最长等差子数组](https://leetcode.cn/problems/longest-arithmetic-sequence-after-changing-at-most-one-element/) · Medium · 灵茶山艾府：[前后缀分解 / 分组循环 / 状态机 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3872.替换最多一个元素后的最长等差子数组

<https://leetcode.cn/problems/longest-arithmetic-sequence-after-changing-at-most-one-element/description/>

题目给出一个整数数组nums，其长度为n。

若子数组中相邻元素的差值是一个常数，那么这个子数组被称为等差子数组。

现在可以将nums中的最多一个元素替换为任意一个整数，然后从nums中选择一个等差子数组。

要求返回可以得到的最长等差子数组的长度。

首先考虑特殊情况。

若nums本身就是一个等差数组，那么就无须进行任何修改，答案就是n。

接下来考虑一般情况。

第一种方案是在某个等差子数组的基础上，修改在其左侧或者右侧相邻的元素，使得这个等差子数组的长度加上1。对于这种情况，显然应该选择最长的等差子数组进行操作，又由于这个等差子数组长度不及n，因此必然有一侧可以进行修改。

第二种方案则是通过修改某个nums[index]来连接nums[index - 1]与nums[index + 1]，构成

以nums[index - 1]结尾的最长等差子数组 \<-> nums[index] \<-> 以nums[index + 1]开头的最长等差子数组

这样的三段结构。

这样做的前提是nums[index - 1]与nums[index + 1]同奇偶，此时就可以将nums[index]修改为二者的平均值，从而计算出目标等差子数组的公差d。

接下来，若nums[index - 1]减去nums[index - 2]恰好等于d，那么就可以将以nums[index - 1]结尾的最长等差子数组吸纳进来。同理，若nums[index + 2]减去nums[index + 1]恰好等于d，那么就可以将以nums[index + 1]开头的最长等差子数组吸纳进来。

基于上面的结论，就可以先一趟遍历，计算出以每个位置为结尾的最长等差子数组的长度数组left。

具体来说，对于当前遍历到的index，若nums[index]与nums[index - 1]之差恰好等于nums[index - 1]与nums[index - 2]之差，那么就有left[index] \= left[index - 1] + 1，否则就有left[index] \= 2。这里需要注意边界情况，left[0]只能等于1。

同理，可以反向一趟遍历，计算出以每个位置为开头的最长等差子数组的长度数组right，具体的计算方法与计算left类似。

得到left和right后，若left[-1]恰好等于n，说明nums本身就是等差数组，此时答案就是n。

否则，可以先初始化答案为left和right中的最大值加上1，也就是上面的第一种方案。

接下来再从1到n - 1之间枚举修改的位置index，尝试第二种方案。

对于当前遍历到的index，记s为nums[index - 1]与nums[index + 1]之和，若s为偶数，那么此时就应该将nums[index]修改为s // 2，同时可以计算出等差子数组的公差d。在初始状态下，这个等差子数组的长度length为3。

若index > 1，且nums[index - 1]与nums[index - 2]之差恰好等于d，那么就可以将左侧这一段吸纳进来，此时应该将left[index - 1] - 1累加到length中。这里减去1是因为nums[index - 1]被计算了两次，需要减去。

若index \< n - 2，且nums[index + 2]与nums[index + 1]之差恰好等于d，那么就可以将右侧这一段吸纳进来，此时应该将right[index + 1] - 1累加到length中。同样的，因为nums[index + 1]被计算了两次，所以也需要额外减去1。

最后，使用length更新答案，然后计算下一个index即可。

最后附上python代码：

```python
class Solution(object):
    def longestArithmetic(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        left = [1, 2]
        for index in range(2, len(nums)):
            if nums[index] - nums[index - 1] == nums[index - 1] - nums[index - 2]:
                left.append(left[-1] + 1)
            else:
                left.append(2)
        
        if left[-1] == len(nums):
            return len(nums)

        right = [1, 2]
        for index in range(len(nums) - 3, -1, -1):
            if nums[index] - nums[index + 1] == nums[index + 1] - nums[index + 2]:
                right.append(right[-1] + 1)
            else:
                right.append(2)
        right.reverse()

        res = max(max(left), max(right)) + 1
        for index in range(1, len(nums) - 1):
            s = nums[index - 1] + nums[index + 1]
            if s % 2 == 0:
                v = s // 2
                d = v - nums[index - 1]
                length = 3
                if index > 1 and nums[index - 1] - nums[index - 2] == d:
                    length += left[index - 1] - 1
                if index + 2 < len(nums) and nums[index + 2] - nums[index + 1] == d:
                    length += right[index + 1] - 1
                res = max(res, length)
        
        return res
```

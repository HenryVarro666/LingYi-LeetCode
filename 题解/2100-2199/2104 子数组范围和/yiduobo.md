---
title: "2104. 子数组范围和"
aliases: ["yiduobo的每日leetcode 2104.子数组范围和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/array", "leetcode/monotonic-stack", "leetcode/bao-li", "题单/单调栈", "题单/单调栈/三-贡献法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/522288504"
zhihu_id: "522288504"
zhihu_title: "yiduobo的每日leetcode 2104.子数组范围和"
question_id: "2104"
question: "子数组范围和"
problem_url: "https://leetcode.cn/problems/sum-of-subarray-ranges/"
difficulty: "Medium"
rating: 2000
created: "2022-05-31T00:09:04+08:00"
updated: "2022-05-31T00:09:04+08:00"
upvotes: 1
comments: 0
---

# 2104. 子数组范围和

> **[yiduobo的每日leetcode 2104.子数组范围和](https://zhuanlan.zhihu.com/p/522288504) · 知乎 · 2022-05-31 · 赞同 1**
> 力扣：[2104. 子数组范围和](https://leetcode.cn/problems/sum-of-subarray-ranges/) · Medium · 灵茶山艾府：[从 O(n^2) 到 O(n)：单调栈+计算每个元素对答案的贡献](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2104.子数组范围和

[力扣](https://leetcode.cn/problems/sum-of-subarray-ranges/)

O(n^2)的做法是很容易想到的，不过既然题目提到了O(n)的做法，那么不妨尝试想想O(n)的做法应该怎么做。

首先，既然是O(n)的做法，那么显然不可能是从子数组入手，而应该改成从每个数入手。题目对范围和的定义是子数组中最大值减去最小值，那么在这里如果要从单个数入手，一个自然的想法就是对于每个数，想办法求解出这个数在多少子数组中充当最大值，又在多少子数组中充当最小值，然后通过这二者的差值乘以这个数自身的大小，就能得到这个数对最终答案的贡献。

以样例1为例，对于[1, 2, 3]：

1、数字1在子数组[1]中充当最大值，在子数组[1]、[1, 2]、[1, 2, 3]中充当最小值，那么1对最终答案的贡献就是(1 - 3) \* 1 \= -2

2、数字2在子数组[1, 2]、[2]中充当最大值，在子数组[2]、[2, 3]中充当最小值，那么2对最终答案的贡献就是(2 - 2) \* 2 \= 0

3、数字3在子树组[1, 2, 3]、[2, 3]、[3]中充当最大值，在子数组[3]中充当最小值，那么3对最终答案的贡献就是(3 - 1) \* 3 \= 6

综合起来，最终答案就是-2 + 0 + 6 \= 4

不过上面描述的这种方法有一个缺陷，就是对于重复数字会出现重复计算的情况，例如样例2。那么在这里不妨稍微修改一下关于最大值和最小值的定义。在这里对于包含nums[index]的某个子数组，若nums[index]大于等于左侧的所有数，严格大于其右侧的所有数，nums[index]才被认为是其中的最大值。同样的，若nums[index]小于等于左侧的说有数，严格小于其右侧的所有数，nums[index]才被认为是其中的最小值。

这样一来，重复计算的问题就解决了。

接下来，需要想办法确定nums[index]在多少个子数组中充当最大值和最小值。

由于充当最大值和充当最小值的求解方式是类似的，在这里就以求解充当最大值的情况来进行说明。

首先，可以先找到nums[index]左侧最近的大于nums[index]的数nums[l]，以及右侧最近的大于等于nums[index]的数nums[r]，那么从nums[index]向左延伸，有index - l个子数组以nums[index]为最大值；同样的，从nums[index]向右延伸，有r - index个子数组以nums[index]为最大值，那么组合起来一共就有(index - l) \* (r - index)个子数组以nums[index]为最大值。而对于nums[l]以及nums[r]的求解，则可以利用单调栈进行辅助，之前有完全相同的题目，这里就不展开了。

于是最终的做法就是：

1、正序一趟遍历，利用单调栈分别求出每个数左侧比这个数大/小的最近的数的下标

2、逆序一趟遍历，利用单调栈分别求出每个数右侧比这个数大/小的最近的数的下标

3、遍历每个数，利用上面两步求解出的下标以及最上面给出的计算公式求解每个数对答案的贡献并累加

最后附上python代码：

```python
class Solution(object):
    def subArrayRanges(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        max_stack = [0]
        left_max = [1]
        min_stack = [0]
        left_min = [1]
        for index in range(1, n):
            while max_stack and nums[index] >= nums[max_stack[-1]]:
                max_stack.pop()
            
            if not max_stack:
                left_max.append(index + 1)
            else:
                left_max.append(index - max_stack[-1])

            max_stack.append(index)

            while min_stack and nums[index] <= nums[min_stack[-1]]:
                min_stack.pop()
            
            if not min_stack:
                left_min.append(index + 1)
            else:
                left_min.append(index - min_stack[-1])

            min_stack.append(index)

        max_stack = [n - 1]
        right_max = [1]
        min_stack = [n - 1]
        right_min = [1]
        for index in range(n - 2, -1, -1):
            while max_stack and nums[index] > nums[max_stack[-1]]:
                max_stack.pop()
            
            if not max_stack:
                right_max.append(n - index)
            else:
                right_max.append(max_stack[-1] - index)

            max_stack.append(index)

            while min_stack and nums[index] < nums[min_stack[-1]]:
                min_stack.pop()
            
            if not min_stack:
                right_min.append(n - index)
            else:
                right_min.append(min_stack[-1] - index)

            min_stack.append(index)

        right_max.reverse()
        right_min.reverse()

        res = 0
        for index in range(n):
            res += (left_max[index] * right_max[index] - left_min[index] * right_min[index]) * nums[index]
        
        return res
```

---
title: "2122. 还原原数组"
aliases: ["yiduobo的每日leetcode 2122.还原原数组"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/滑动窗口与双指针", "题单/贪心算法", "题单/滑动窗口与双指针/三-单序列双指针", "题单/贪心算法/六-构造题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/525139652"
zhihu_id: "525139652"
zhihu_title: "yiduobo的每日leetcode 2122.还原原数组"
question_id: "2122"
question: "还原原数组"
problem_url: "https://leetcode.cn/problems/recover-the-original-array/"
difficulty: "Hard"
rating: 2159
created: "2022-06-06T23:26:13+08:00"
updated: "2022-06-06T23:26:13+08:00"
upvotes: 1
comments: 0
---

# 2122. 还原原数组

> **[yiduobo的每日leetcode 2122.还原原数组](https://zhuanlan.zhihu.com/p/525139652) · 知乎 · 2022-06-06 · 赞同 1**
> 力扣：[2122. 还原原数组](https://leetcode.cn/problems/recover-the-original-array/) · Hard · 灵茶山艾府：[[灵茶山艾府题解/solutions/2122 还原原数组 · 枚举 higher-0- + 双指针|枚举 higher[0] + 双指针]]

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2122.还原原数组

[力扣](https://leetcode.cn/problems/recover-the-original-array/)

本题与之前遇到过的某题很相似，但是记不清楚之前那题的题号了。不过做法还是类似的，先从最小值开始考虑。

为了方便讨论，记sorted_nums为nums从小到大排序后的结果，记sorted_arr为arr从小到大排序后的结果。

由于题目中所有的数都是正整数，那么必然有sorted_nums[0] \= arr[0] - k。

接下来对于sorted_nums[1]，则有两种可能，分别是

1、sorted_nums[1] \= arr[1] - k

对于这种情况，没有办法继续往下计算

2、sorted_nums[1] \= arr[0] + k

对于这种情况，sorted_nums[1] - sorted_nums[0] \= arr[0] + k - (arr[0] - k) \= 2k，因此可以尝试通过sorted_nums[1] - sorted_nums[0]计算出k，然后在sorted_nums中向后遍历验证k是否合法。

当然，在这种情况下可能出现sorted_nums[1] - sorted_nums[0]是奇数，或者在计算得到k之后在sorted_nums中验证不合法的情况，此时就说明此时遇到了情况1，即sorted_nums[1] \= arr[1] - k。那么只需继续向后考虑sorted_nums[2]，此时的sorted_nums[2]要么等于arr[2] - k，要么等于arr[0] + k，可以发现此时又可以通过sorted_nums[2] - sorted_nums[0]来尝试计算k并验证是否合法。

由于题目保证存在合法的arr，那么按照上面的流程依次尝试计算k，直到找到合法的arr就行了。

另外，对于验证k是否合法，在这里由于k是正整数，那么随着index的向后推进，sorted_arr[index] + k也是越来越大的，因此其在sorted_nums中的位置也是单调递增的。于是在这里利用单调性，就可以在O(n)的时间复杂度内完成k的合法性验证。

最后附上python代码：

```python
class Solution(object):
    def recoverArray(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        def check(double_k):
            used = set()
            p = 0
            for index in range(len(sorted_nums)):
                if index not in used:
                    if p <= index:
                        p = index + 1
                    while p < len(sorted_nums) and sorted_nums[p] != sorted_nums[index] + double_k:
                        p += 1
                    if p == len(sorted_nums):
                        return False

                    used.add(p)
                    p += 1
                    res.append(sorted_nums[index] + double_k / 2)
            
            return True
        
        sorted_nums = sorted(nums)
        for num in sorted_nums[1:]:
            double_k = num - sorted_nums[0]
            res = []
            if double_k % 2 == 0 and double_k > 0 and check(double_k):
                break
        
        return res
```

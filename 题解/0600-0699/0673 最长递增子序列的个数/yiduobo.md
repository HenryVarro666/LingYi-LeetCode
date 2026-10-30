---
title: "673. 最长递增子序列的个数"
aliases: ["yiduobo的每日leetcode 673.最长递增子序列的个数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/296955754"
zhihu_id: "296955754"
zhihu_title: "yiduobo的每日leetcode 673.最长递增子序列的个数"
question_id: "673"
question: "最长递增子序列的个数"
problem_url: "https://leetcode.cn/problems/number-of-longest-increasing-subsequence/"
created: "2020-11-16T22:46:37+08:00"
updated: "2020-11-16T22:46:37+08:00"
upvotes: 1
comments: 0
---

# 673. 最长递增子序列的个数

> **[yiduobo的每日leetcode 673.最长递增子序列的个数](https://zhuanlan.zhihu.com/p/296955754) · 知乎 · 2020-11-16 · 赞同 1**
> 力扣：[673. 最长递增子序列的个数](https://leetcode.cn/problems/number-of-longest-increasing-subsequence/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

673.最长递增子序列的个数

[力扣](https://leetcode-cn.com/problems/number-of-longest-increasing-subsequence/)

题目要求最长递增子序列的个数，可以直接套用经典的动态规划算法得到一个平方的做法。

具体为f[i]表示以nums[i]结尾的最长递增子序列的长度，而g[i]表示以nums[i]为结尾的最长递增子序列的个数。

对于f[i]和g[i]，我们枚举nums[0]到nums[i - 1]，若当前的nums[j] \< nums[i]，那么：

1、若maxl为空或maxl \< f[j]，那么令maxl \= f[j]，同时f[i] \= f[j] + 1，g[i] \= g[j]

2、若maxl \= f[j]，那么g[i] +\= g[j]

注意观察上面这个过程，实际上对于每个i，我们要找的是0到i - 1中值，nums的值位于0到nums[i] - 1之间的最大的f[i]，那么在从0开始往后遍历的过程中，我们可以将问题转化为求0到nums[i] - 1这个区间中的最大值的问题，可以使用线段树或者树状数组来进行优化。不过在这之前，由于nums[i]本身可能非常大，直接使用数据结构会有空间上的问题，因此需要先进行离散化。

注意到这里保证数组的长度不超过2000，同时我们并不关心每个数的绝对值大小，而只需要知道他们之间的相对大小关系，因此可以先对nums从小到大进行排序，然后将nums中的每个数映射到其对应的大小排位上。

例如样例中的[1, 3, 5, 4, 7]，排序后得到[1, 3, 4, 5, 7]，那么根据这里的大小顺序，我们建立以下的映射

1 -> 1

3 -> 2

4 -> 3

5 -> 4

7 -> 5

然后将其替换回nums中，最后得到新的nums为[1, 2, 4, 3, 5]

完成上面的离散化操作之后，所有的数都被映射到了1到2000之内，因此可以安心使用线段树或树状数组了。我在这里使用的是树状数组，其大致原理可以参考这一篇文章：

[yiduobo：yiduobo的每日leetcode 307.区域和检索](https://zhuanlan.zhihu.com/p/158638574)

我们在这里直接就认为是某种可以在O(logn)的时间内找出前缀区间中的最大值的数据结构。那么上面的平方动态规划就可以进行对应的优化，具体为从0开始往后扫描离散化之后的nums数组，对于nums[i]，我们现在树状数组中查找0到nums[i] - 1中的最大值now_len以及频率now_cnt，然后我们将nums[i]加入其中之后就可以得到长度为now_len + 1的递增子序列一共now_cnt条，将其更新到树状数组当中。

扫描完成后，我们从中找出最大的长度max_len以及答案个数res即可。

最后附上python代码：

```python
class Solution(object):
    def findNumberOfLIS(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        num_dict = {}
        now = 1
        last = None
        for index, num in enumerate(sorted(nums)):
            if index > 0 and num == last:
                continue
            else:
                num_dict[num] = now
                now += 1
                last = num

        for index in range(len(nums)):
            nums[index] = num_dict[nums[index]]

        index_array = [[0, 0] for _ in range(len(nums) + 1)]

        for num in nums:
            index = num - 1
            now_len, now_cnt = 0, 1
            while index > 0:
                if index_array[index][0] > now_len:
                    now_len = index_array[index][0]
                    now_cnt = index_array[index][1]
                elif index_array[index][0] == now_len:
                    now_cnt += index_array[index][1]
                index -= index & -index
            
            now_len += 1
            index = num
            while index <= len(nums):
                if now_len > index_array[index][0]:
                    index_array[index][0] = now_len
                    index_array[index][1] = now_cnt
                elif now_len == index_array[index][0]:
                    index_array[index][1] += now_cnt
                index += index & -index

        res, max_len = 0, 0
        index = len(nums)
        while index > 0:
            if index_array[index][0] > max_len:
                max_len = index_array[index][0]
                res = index_array[index][1]
            elif index_array[index][0] == max_len:
                res += index_array[index][1]
            index -= index & -index
        return res
```

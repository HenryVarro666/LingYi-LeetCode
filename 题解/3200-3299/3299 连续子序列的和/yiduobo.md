---
title: "3299. 连续子序列的和"
aliases: ["yiduobo的每日leetcode 3299.连续子序列的和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/942283446"
zhihu_id: "942283446"
zhihu_title: "yiduobo的每日leetcode 3299.连续子序列的和"
question_id: "3299"
question: "连续子序列的和"
problem_url: "https://leetcode.cn/problems/sum-of-consecutive-subsequences/"
created: "2024-10-12T03:08:01+08:00"
updated: "2024-10-12T03:08:01+08:00"
upvotes: 1
comments: 0
---

# 3299. 连续子序列的和

> **[yiduobo的每日leetcode 3299.连续子序列的和](https://zhuanlan.zhihu.com/p/942283446) · 知乎 · 2024-10-12 · 赞同 1**
> 力扣：[3299. 连续子序列的和](https://leetcode.cn/problems/sum-of-consecutive-subsequences/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3299.连续子序列的和

[. - 力扣（LeetCode）](https://leetcode.cn/problems/sum-of-consecutive-subsequences/description/)

题目定义如果一个长度为n的数组arr满足下面二者之一，就称arr是连续的：

1、对于所有的1 \<\= i \< n，都有arr[i] - arr[i - 1] \= 1

2、对于所有的1 \<\= i \< n，都有arr[i] - arr[i - 1] \=\= -1

另外定义arr的值为arr中所有元素之和，现在给出一个整数数组nums，要求找出其中所有的连续非空子序列之和。另外长度为1的数组也被认为是连续的。

题目要求处理递增和递减两种子序列，对于这种问题，一种常见的做法是先处理递增的子序列，然后翻转数组，这样一来再处理一次递增的子序列就相当于处理了递减的子序列。

也就是说，在这里只需要考虑如何处理递增的子序列。需要特别注意的是，本题中长度为1的数组也被认为是连续的，因此在处理递增子序列时不应该处理长度为1的数组，因此数组翻转后又会处理一次将会产生重复。因此在这里只需要考虑长度大于等于2的递增子序列，在处理完后再累加数组之和就行了。

接下来考虑如何处理长度大于等于2的递增子序列。本题要求计算的是子序列的和，由于子序列的数目众多，因此在这里使用贡献法是比较合适的。

令f[index]表示以nums[index]结尾的递增子序列的数目，那么对于f[index]，其可以形成单独的子序列，也就是1个，另外也可以接在所有满足prev \< index且nums[prev] \= nums[index] - 1的后面，也就是f[index] \= sum(f[prev]) + 1，其中0 \<\= prev \< index且nums[prev] \= nums[index] - 1。

由于题目的数据规模很大，在这里枚举prev显然是不行的，不过nums\[index\] - 1这个值是固定的，因此可以使用一个哈希表cnt_f\[index\]\[v\]来表示通过nums\[0\]到nums\[index\]构成的所有递增子序列中，以v为结尾的子序列数量。根据这个定义，上面的f\[index\]就等于cnt_f\[index - 1\]\[nums\[index\] - 1\] + 1，而得到f\[index\]之后，就可以用cnt_f\[index - 1\]\[nums\[index\]\] + f\[index\]来更新cnt_f\[index\]\[nums\[index\]\]了，另外对于cnt_f\[index\]中其他的v，本轮是无法得到更新的，因此就有cnt_f\[index\]\[v\] \= cnt_f\[index - 1\]\[v\]。

由于这里的cnt_f只是用来辅助计算f的，同时cnt_f每一轮的结果只与上一轮有关，因此可以省去i这一维。

得到f数组后，可以通过同样的方法从后向前一趟遍历，计算出对应的g数组，其中g[index]表示以nums[index]开头的递增子序列的数目。

得到f和g之后，对于数组中的某个元素nums[index]，从f[index]中任选一个子序列，然后从g[index]中任选一个子序列，组合起来都可以构成包含nums[index]的连续递增子序列，因此一共可以构成f[index] \* g[index]个连续递增子序列。但是需要注意在计算f[index]和g[index]时将nums[index]单独形成的子序列也计算进来了，当f[index]和g[index]同时选中这种情况时，将会得到一个长度仅为1的子序列，为了避免重复计算在这里需要剔除掉，因此nums[index]在长度大于等于2的连续递增子序列中可以提供的贡献值为(f[index] \* g[index] - 1) \* nums[index]。

到了这里就只需要一趟遍历，累加nums[index]在长度大于等于2的连续递增子序列中的贡献就行了。

计算完毕后，将nums翻转，按相同的方法再累加数组中每个元素在长度大于等于2的连续递减子序列中的贡献，最后再加上数组之和即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def getSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        mod = 10 ** 9 + 7

        def calc(nums):
            f = []
            cnt_f = {}

            for v in nums:
                f.append(cnt_f.get(v - 1, 0) + 1)
                cnt_f[v] = cnt_f.get(v, 0) + f[-1]
            
            g = []
            cnt_g = {}
            for v in nums[::-1]:
                g.append(cnt_g.get(v + 1, 0) + 1)
                cnt_g[v] = cnt_g.get(v, 0) + g[-1]
            g.reverse()

            res = 0
            for index, v in enumerate(nums):
                res = (res + (f[index] * g[index] % mod - 1 + mod) % mod * v) % mod

            return res

        res = calc(nums)
        res = (res + calc(nums[::-1])) % mod
        res = (res + sum(nums) % mod) % mod
        return res
```

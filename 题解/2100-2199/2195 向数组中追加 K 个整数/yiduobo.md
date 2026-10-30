---
title: "2195. 向数组中追加K个整数"
aliases: ["yiduobo的每日leetcode 2195.向数组中追加K个整数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/math", "leetcode/sorting", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/538058419"
zhihu_id: "538058419"
zhihu_title: "yiduobo的每日leetcode 2195.向数组中追加K个整数"
question_id: "2195"
question: "向数组中追加 K 个整数"
problem_url: "https://leetcode.cn/problems/append-k-integers-with-minimal-sum/"
difficulty: "Medium"
rating: 1659
created: "2022-07-06T01:42:01+08:00"
updated: "2022-07-06T01:42:01+08:00"
upvotes: 0
comments: 0
---

# 2195. 向数组中追加K个整数

> **[yiduobo的每日leetcode 2195.向数组中追加K个整数](https://zhuanlan.zhihu.com/p/538058419) · 知乎 · 2022-07-06 · 赞同 0**
> 力扣：[2195. 向数组中追加 K 个整数](https://leetcode.cn/problems/append-k-integers-with-minimal-sum/) · Medium · 灵茶山艾府：[只用到排序的做法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2195.向数组中追加K个整数

[力扣](https://leetcode.cn/problems/append-k-integers-with-minimal-sum/)

为了使得数组之和最小，同时不能出现重复的数字，因此最优的方案肯定是从1开始，逐个向数组中追加当前数组中没出现过的数。不过由于题目中nums和k的规模都很大，直接模拟这个过程肯定是行不通的。

一个自然的想法是先找出数组中最小的数m，然后按上面的做法应该是将1到m - 1加入到数组中。在这里就可以通过判断当前剩下的k与m - 1的大小来决定最后应该追加哪些整数。若k \<\= m - 1，那么只需要将1到k追加进去就得到了最终答案。反过来若k > m - 1，那么就需要将1到m - 1全部追加进去，并将k更新为k - (m - 1)，然后继续考虑m + 1到数组中的次大值之间应该如何追加剩下的k个数。

更一般的，可以先将数组从小到大进行排序，然后在数组头部添加一个0，接下来从头开始向后一趟遍历，对于当前遍历到的nums[index]，其与nums[index + 1]之间一共有nums[index + 1] - nums[index] - 1个数，接下来根据这个数量与k的大小关系选择对应的处理方式。

另外，还有一种情况是遍历完整个数组后k依然大于0，此时就应该从nums[-1] + 1开始再往数组中追加k个数。

最后附上python代码：

```python
class Solution(object):
    def minimalKSum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        nums.append(0)
        nums = sorted(list(set(nums)))
        res = 0
        for index in range(1, len(nums)):
            if nums[index] - nums[index - 1] - 1 >= k:
                res += (nums[index - 1] + 1 + nums[index - 1] + k) * k / 2
                return res
            else:
                res += (nums[index - 1] + 1 + nums[index] - 1) * (nums[index] - nums[index - 1] - 1) / 2
                k -= nums[index] - nums[index - 1] - 1

        if k > 0:
            res += (nums[-1] + 1 + nums[-1] + k) * k / 2
        
        return res
```

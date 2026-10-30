---
title: "327. 区间和的个数"
aliases: ["yiduobo的每日leetcode 327.区间和的个数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/161089325"
zhihu_id: "161089325"
zhihu_title: "yiduobo的每日leetcode 327.区间和的个数"
question_id: "327"
question: "区间和的个数"
problem_url: "https://leetcode.cn/problems/count-of-range-sum/"
created: "2020-07-16T22:53:19+08:00"
updated: "2020-07-16T22:53:19+08:00"
upvotes: 0
comments: 0
---

# 327. 区间和的个数

> **[yiduobo的每日leetcode 327.区间和的个数](https://zhuanlan.zhihu.com/p/161089325) · 知乎 · 2020-07-16 · 赞同 0**
> 力扣：[327. 区间和的个数](https://leetcode.cn/problems/count-of-range-sum/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

327.区间和的个数<https://leetcode-cn.com/problems/count-of-range-sum/>

对于区间和，很直观地就能想到利用前缀和来处理，于是可以先计算出前缀和数组sum_list，那么区间和S(i，j)就等于sum_list[j] - sum_list[i - 1]。

于是现在就变成了，求解sum_list中存在多少对(i，j)，满足i >\= j且sum_list[i] - sum_list[j]在lower到upper之间。

到了这里，可以联想到一道经典的分治题求逆序对。求数组中的逆序对可以理解成求解数组a中存在多少对(i，j)，满足i > j且a[i] - a[j] \< 0，而这里则是lower \<\= sum_list[i] - sum_list[j] \<\= upper。

对于逆序对的题目通常是利用归并排序，在二路归并过程中利用两个数组的有序性来求得最终的解，那么这一题也可以如法炮制：

1、设当前归并的两个部分为left_sum和right_sum，那么首先递归求解left_sum与right_sum，得出两个部分内部满足题目要求的数对的同时也完成对left_sum和right_sum的排序。

2、接下来开始对left_sum和right_sum进行二路归并。设当前处理到left_sum[i]和right_sum[j]，那么我们首先不断迭代j，直到right_sum[j] > left_sum[i]，同时将right_sum[j]加入到排序的答案数组中。这一步的目的是完成归并排序。

3、在步骤2的同时，找到right_sum中第一个满足

right_sum[lower_pos] - left_sum[i] >\= lower

且

right_sum[lower_pos - 1] - left_sum[i] \< lower

的lower_pos。由于right_sum是单调递增的，那么从lower_pos开始直到right_sum的末尾都一定满足其减去left_sum[i]之后大于等于lower。另外，由于left_sum也是单调递增的，那么对于每个i，这个lower_pos也是单调递增的，于是可以每次求解lower_pos的时候都可以从上一个lower_pos开始。

4、除了lower_pos，还需要找出right_sum中第一个满足

right_sum[upper_pos] - left_sum[i] > upper

且

right_sum[upper_pos] - left_sum[i] \<\= upper

的upper_pos。还是通过right_sum的单调性可以知道从0开始到upper_pos - 1这一段减去left_sum[i]之后一定是小于等于upper的。与上面相同，upper_pos也是单调递增的，于是每次也可以从上一个upper_pos开始求解。

到了这里，可以发现从lower_pos开始到末尾时满足sum_list[p] - sum_list[i] >\= lower的，而从0到upper_pos - 1则是满足sum_list[q] - sum_list[i] \<\= upper的，于是两个区间的交集就是区间(lower_pos，upper_pos - 1)是满足题目要求的，即对于sum_list[i]一共可以产生区间长度个满足条件的数对，这个区间的长度就是

(upper_pos - 1) - (lower_pos) + 1 \= upper_pos - lower_pos

由于上面发现每次求解lower_pos和upper_pos都可以从上一次结果开始往后扫描，于是这个操作与二路归并的操作一样，也是O(n)的。一共需要执行logn次分治，每次需要排序、求解lower_pos以及求解upper_pos一共三次扫描，而每次扫描的复杂度都是O(n)的，因此最终的时间复杂度为O(nlogn)。

另外，需要特别注意题目里面对于i \= j的情况也可能成为解，于是在分治时对于left\=right的情况需要进行特别判断，不能漏掉了可行的答案。

最后附上python代码：

```python
class Solution(object):
    def countRangeSum(self, nums, lower, upper):
        """
        :type nums: List[int]
        :type lower: int
        :type upper: int
        :rtype: int
        """

        if not nums:
            return 0

        sum_list = nums[:]
        for index in range(1, len(nums)):
            sum_list[index] += sum_list[index - 1]
        
        return self.mergeSort(0, len(nums) - 1, lower, upper, sum_list)

    def mergeSort(self, l, r, lower, upper, sum_list):
        if l == r:
            if sum_list[l] >= lower and sum_list[l] <= upper:
                return 1
            return 0

        mid = (l + r) / 2
        res = self.mergeSort(l, mid, lower, upper, sum_list) + self.mergeSort(mid + 1, r, lower, upper, sum_list)

        merge_pos = lower_pos = upper_pos = mid + 1
        tmp_list = []
        for index in range(l, mid + 1):
            while merge_pos <= r and sum_list[merge_pos] < sum_list[index]:
                tmp_list.append(sum_list[merge_pos])
                merge_pos += 1
            while lower_pos <= r and sum_list[lower_pos] - sum_list[index] < lower:
                lower_pos += 1
            while upper_pos <= r and sum_list[upper_pos] - sum_list[index] <= upper:
                upper_pos += 1
            
            res += upper_pos - lower_pos
            tmp_list.append(sum_list[index])

        for index in range(len(tmp_list)):
            sum_list[l + index] = tmp_list[index]

        return res
```

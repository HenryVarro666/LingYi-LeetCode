---
title: "3048. 标记所有下标的最早秒数"
aliases: ["yiduobo的每日leetcode 3048.标记所有下标的最早秒数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/二-二分答案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/696470758"
zhihu_id: "696470758"
zhihu_title: "yiduobo的每日leetcode 3048.标记所有下标的最早秒数"
question_id: "3048"
question: "标记所有下标的最早秒数 I"
problem_url: "https://leetcode.cn/problems/earliest-second-to-mark-indices-i/"
difficulty: "Medium"
rating: 2263
created: "2024-05-08T03:54:55+08:00"
updated: "2024-05-08T03:54:55+08:00"
upvotes: 1
comments: 0
---

# 3048. 标记所有下标的最早秒数

> **[yiduobo的每日leetcode 3048.标记所有下标的最早秒数](https://zhuanlan.zhihu.com/p/696470758) · 知乎 · 2024-05-08 · 赞同 1**
> 力扣：[3048. 标记所有下标的最早秒数 I](https://leetcode.cn/problems/earliest-second-to-mark-indices-i/) · Medium · 灵茶山艾府：[两种方法：二分答案+正序/逆序（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3048.标记所有下标的最早秒数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/earliest-second-to-mark-indices-i/)

首先，由于题目中存在什么都不干的操作，因此本题的答案是满分二分的条件的，于是可以二分最早可以满足条件的时间mid。二分的下界可以设置成nums的长度，当然设置为0也不影响最终结果。二分的上界则应该设置为changeIndices的长度m，其中在0到m - 1之间表示正常的标记尝试，而m则表示无法完成标记操作，对应的是答案中的-1。

接下来观察题目中给出的操作，由于减1操作可以随时进行，因此需要优先满足标记操作。又由于每个下标的标记操作只需要执行一次，因此对于单个下标，执行标记操作的最佳时间必然是小于等于mid且最靠后的时间，因为这样才能预留出尽量多的时间来执行减1操作。

另一方面，对于这些标记操作，应该尽量先将其中靠前的下标位置对应的nums值减小到0，因为标记操作必须在nums对应的值减小到0之后才能进行。

根据上面的结论，就可以对changeIndices进行一趟遍历，计算nums中所有位置在mid内的可标记的最晚的时机并记录在哈希表last中。接下来将nums的所有下标index按照last[index]从小到大进行排序，然后一趟遍历，同时使用一个变量r记录当前可用的减1操作次数，以及另一个变量pre记录上一次标记操作对应的时机。

对于当前遍历到的标记位置index，首先通过last[index]与pre计算出可用的额外减1次数，并累加到r中。接下来若r \< nums[index]，说明减1操作的次数不够，无法标记所有数字，此时就应该更新二分的下界left为mid + 1；反之，若r >\= nums[index]，那么就应该将r减去nums[index]，并将pre更新为last[index]，继续向后考虑标记下一个数。若全都可以标记，则更新二分的上界为mid。

另外需要注意的，本题中数组的下标是从1开始的，因此在实现时需要注意下标加1。

最后附上python代码：

```python
class Solution(object):
    def earliestSecondToMarkIndices(self, nums, changeIndices):
        """
        :type nums: List[int]
        :type changeIndices: List[int]
        :rtype: int
        """

        m = len(changeIndices)
        n = len(nums)

        left = 0
        right = m
        while left < right:
            mid = (left + right) // 2
            last = {}
            for index in range(mid + 1):
                last[changeIndices[index]] = index
            
            if len(last) != n:
                left = mid + 1
                continue
            
            index_list = sorted(range(n), key=lambda d:last[d + 1])
            r = 0
            pre = -1
            flag = True
            for index in index_list:
                r += last[index + 1] - pre - 1
                if r < nums[index]:
                    flag = False
                    break
                else:
                    r -= nums[index]
                
                pre = last[index + 1]
            
            if flag:
                right = mid
            else:
                left = mid + 1
        
        if left == m:
            return -1
        return left + 1
```

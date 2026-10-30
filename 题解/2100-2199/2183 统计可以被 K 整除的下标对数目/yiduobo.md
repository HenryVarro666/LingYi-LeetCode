---
title: "2183. 统计可以被K整除的下标对数目"
aliases: ["yiduobo的每日leetcode 2183.统计可以被K整除的下标对数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/math", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/536101723"
zhihu_id: "536101723"
zhihu_title: "yiduobo的每日leetcode 2183.统计可以被K整除的下标对数目"
question_id: "2183"
question: "统计可以被 K 整除的下标对数目"
problem_url: "https://leetcode.cn/problems/count-array-pairs-divisible-by-k/"
difficulty: "Hard"
rating: 2246
created: "2022-07-01T01:25:57+08:00"
updated: "2022-07-01T01:25:57+08:00"
upvotes: 0
comments: 0
---

# 2183. 统计可以被K整除的下标对数目

> **[yiduobo的每日leetcode 2183.统计可以被K整除的下标对数目](https://zhuanlan.zhihu.com/p/536101723) · 知乎 · 2022-07-01 · 赞同 0**
> 力扣：[2183. 统计可以被 K 整除的下标对数目](https://leetcode.cn/problems/count-array-pairs-divisible-by-k/) · Hard · 灵茶山艾府：[统计因子出现次数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2183.统计可以被K整除的下标对数目

[力扣](https://leetcode.cn/problems/count-array-pairs-divisible-by-k/)

本题的数据规模较大，因此直接枚举i和j，再判断nums[i] \* nums[j]是否为k的倍数的做法是行不通的。

对于这类问题，通常的做法是枚举其中的一方，然后想办法高效求出满足条件的另一方的组数。在这里就是枚举所有的nums[i]，找出满足nums[i] \* nums[j]为k的倍数的j有多少个，相当于固定了nums[i]和k，需要寻找满足条件的nums[j]。

在这里可以先将nums[i]和k进行约分，即求出二者的最大公约数g，那么nums[j]就只需要满足是t \= k / g的倍数就行了。用于题目中的数取值范围都在十万以内，因此可以提前预处理出对于每一个t，nums中有多少个数为t的倍数，记这个结果为cnt[t]。

对于这个问题，则可以采用类似筛法的处理方法，先从1到max(nums)枚举t，然后对于当前的t，依次检测t、2t、3t、...、mt在nums中出现的次数，同时根据这个出现次数来更新cnt[t]。

这样一来，就可以在O(nlogn)的时间内预处理出cnt[t]了。

另外需要注意的是，使用这个做法对于每一组nums[i]和nums[j]都会计算两次，即枚举到nums[i]时会将nums[j]作为合法结果累加一次，在枚举到nums[j]时又会将nums[i]作为合法结果累加一次。除此之外，还可能将nums[i] \* nums[i] % k \= 0这种情况计算进去。因此在具体处理时，在将cnt[t]累加到答案之后，若nums[i]自身就是t的倍数，那么需要将答案减去1，表示消除nums[i] \* nums[i]这种情况的影响。在全部计算完成后，还需要将答案除以2，表示消除nums[i]和nums[j]的重复计算。

最后附上python代码：

```python
class Solution(object):
    def countPairs(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        cnt_list = [0] * (k + 1)
        cnt_list[1] = len(nums)
        num_dict = {}
        for num in nums:
            num_dict[num] = num_dict.get(num, 0) + 1

        max_num = max(nums)
        for num in range(2, k + 1):
            now = num
            while now <= max_num:
                cnt_list[num] += num_dict.get(now, 0)
                now += num

        res = 0
        for num in nums:
            x, y = num, k
            if x < y:
                x, y = y, x
            while y:
                x, y = y, x % y

            tmp = k / x
            res += cnt_list[tmp]
            if num % tmp == 0:
                res -= 1
        
        return res / 2
```

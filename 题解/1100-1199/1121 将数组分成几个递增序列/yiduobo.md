---
title: "1121. 将数组分成几个递增序列"
aliases: ["yiduobo的每日leetcode 1121.将数组分成几个递增序列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/609954839"
zhihu_id: "609954839"
zhihu_title: "yiduobo的每日leetcode 1121.将数组分成几个递增序列"
question_id: "1121"
question: "将数组分成几个递增序列"
problem_url: "https://leetcode.cn/problems/divide-array-into-increasing-sequences/"
created: "2023-02-27T22:43:19+08:00"
updated: "2023-02-27T22:43:19+08:00"
upvotes: 0
comments: 0
---

# 1121. 将数组分成几个递增序列

> **[yiduobo的每日leetcode 1121.将数组分成几个递增序列](https://zhuanlan.zhihu.com/p/609954839) · 知乎 · 2023-02-27 · 赞同 0**
> 力扣：[1121. 将数组分成几个递增序列](https://leetcode.cn/problems/divide-array-into-increasing-sequences/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1121.将数组分成几个递增序列

[力扣](https://leetcode.cn/problems/divide-array-into-increasing-sequences/)

题目并没有限制最终拆分出来的序列的数量，那么为了使得最短的序列尽可能的长，就应该尽量少拆分序列。由于拆分出来的序列必须递增，因此相同的值不能放在同一个序列中，从而得到了拆分序列数量的下限，也就是数组中每种数出现频率的最大值，在这里将其记为n。

那么在这里是否必然能构造出n个序列呢？答案是肯定的。一种最简单的构造方法就是对于数组中出现每种数num，设其一共出现了cnt[num]次，那么就将这个num分配给前num个序列，这样一来就必然可以得到n个递增的序列。

当然，这种构造方式并不是最优的，很可能无法满足最短长度尽量长的要求。一种更好的分配方式是从小到大枚举这些num，然后从第0个序列开始逐个进行分配。对于当前分配的num，设其出现了cnt[num]次，而当前分配到了第p个序列，那么就将这cnt[num]个num分配给第p到第p + cnt[num] - 1个序列。若这里的p + cnt[num] - 1大于等于n，那么就从第0个序列重头开始进行分配。这样一来，就可以保证各个序列的长度尽可能的接近，换言之，这就是最优的分配方案之一。

分配完成后，只需检测下一个待分配的序列，也就是当前最短的序列中的数字个数是否大于等于k即可。

更进一步的，由于上面这种分配方案一定可以构造出n个长度最接近的序列，那么就没有必要模拟这个分配的过程，只需要一趟遍历找出n，使用数组长度除以n就可以得到最短序列的长度，然后使用这个长度与k进行比较就能得到最终答案了。

最后附上python代码：

```python
class Solution(object):
    def canDivideIntoSubsequences(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: bool
        """

        last = nums[0]
        cnt = 1
        n = 1
        for num in nums[1:]:
            if num == last:
                cnt += 1
            else:
                n = max(n, cnt)
                last = num
                cnt = 1
        
        n = max(n, cnt)
        return len(nums) / n >= k
```

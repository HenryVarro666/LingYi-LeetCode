---
title: "315. 计算右侧小于当前元素的个数"
aliases: ["yiduobo的每日leetcode 315.计算右侧小于当前元素的个数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/158891973"
zhihu_id: "158891973"
zhihu_title: "yiduobo的每日leetcode 315.计算右侧小于当前元素的个数"
question_id: "315"
question: "计算右侧小于当前元素的个数"
problem_url: "https://leetcode.cn/problems/count-of-smaller-numbers-after-self/"
created: "2020-07-12T13:43:55+08:00"
updated: "2020-07-12T13:43:55+08:00"
upvotes: 0
comments: 0
---

# 315. 计算右侧小于当前元素的个数

> **[yiduobo的每日leetcode 315.计算右侧小于当前元素的个数](https://zhuanlan.zhihu.com/p/158891973) · 知乎 · 2020-07-12 · 赞同 0**
> 力扣：[315. 计算右侧小于当前元素的个数](https://leetcode.cn/problems/count-of-smaller-numbers-after-self/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

315.计算右侧小于当前元素的个数<https://leetcode-cn.com/problems/count-of-smaller-numbers-after-self/>

很经典的题目。对于这类带顺序的问题，一种常见的做法是排序之后，根据顺序建立每个具体元素到其对应rank的映射，那么之后的比较中就可以对比rank而需要对比元素自身的数值。这样做的好处是，对于n个数，其中最大的rank也必然是小于等于n的，相当于将元素的值缩减到了1到n之间，这位后续数据结构的运用提供了可能。

回到题目上来。题目要求对于nums\[index\]，需要求出nums\[index + 1\]到nums\[-1\]之间有多少个小于nums\[index\]的数。在进行上面的操作之后，可以看做对于rank\[nums\[index\]\]，在rank\[nums\[index + 1\]\]，rank\[nums\[index + 2\]\]，...，rank\[nums\[-1\]\]中有多少个数小于rank\[nums\[index\]\]，而这里的rank都在1到n之间。

这个问题也可以看做，对于一个数rank\[nums\[index\]\]，其右侧有多少个数在1到rank\[nums\[index\]\] - 1之间。由于rank的值在1到n之间，于是我们可以用一个cnt_list来保存每个rank对应的元素个数，那么实际上这里就是求

sum(cnt_list\[1\]，cnt_list\[2\]，...，cnt_list\[rank\[nums\[index\]\] - 1\])

而在求出这个值之后，还需要将rank\[nums\[index\]\]也加入到cnt_list中来

求解动态的区间和，很自然就联想到了使用树状数组。那么现在的做法就是：

1、对于nums排序之后获取到nums中每个元素对应的rank

2、从右往左一趟扫描，使用树状数组计算nums\[index\]右侧有多少个数位于1到rank\[nums\[index\]\] - 1之间，并将rank\[nums\[index\]\]加入到树状数组中。

3、翻转步骤二求得的list，即为最终答案。

步骤1排序的时间复杂度为O(nlogn)，步骤2需要一趟扫描，对于每个nums[index]都需要进行两次树状数组操作，而树状数组操作的复杂度为O(logn)，因此步骤2的时间复杂度也是O(nlogn)。因此，最终的时间复杂度就是O(nlogn)。

最后附上python代码：

```python
class Solution(object):
    def countSmaller(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        last = None
        rank = 1
        rank_dict = {}

        for num in sorted(nums):
            if num == last:
                continue

            rank_dict[num] = rank
            rank += 1
            last = num
        
        res = []
        sum_list = [0] * rank

        for index in range(len(nums) - 1, -1, -1):
            now = rank_dict[nums[index]] - 1

            tmp = 0
            while now > 0:
                tmp += sum_list[now]
                now -= now & -now
            res.append(tmp)

            now = rank_dict[nums[index]]
            while now < rank:
                sum_list[now] += 1
                now += now & -now
            
        res.reverse()
        return res
```

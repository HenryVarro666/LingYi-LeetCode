---
title: "2121. 相同元素的间隔之和"
aliases: ["yiduobo的每日leetcode 2121.相同元素的间隔之和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/array", "leetcode/hash-table", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/525136721"
zhihu_id: "525136721"
zhihu_title: "yiduobo的每日leetcode 2121.相同元素的间隔之和"
question_id: "2121"
question: "相同元素的间隔之和"
problem_url: "https://leetcode.cn/problems/intervals-between-identical-elements/"
difficulty: "Medium"
created: "2022-06-06T23:09:29+08:00"
updated: "2022-06-06T23:09:29+08:00"
upvotes: 0
comments: 0
---

# 2121. 相同元素的间隔之和

> **[yiduobo的每日leetcode 2121.相同元素的间隔之和](https://zhuanlan.zhihu.com/p/525136721) · 知乎 · 2022-06-06 · 赞同 0**
> 力扣：[2121. 相同元素的间隔之和](https://leetcode.cn/problems/intervals-between-identical-elements/) · Medium · 灵茶山艾府：[O(n) 做法：考虑间隔和的变化量（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2121.相同元素的间隔之和

[力扣](https://leetcode.cn/problems/intervals-between-identical-elements/)

由于题目只关心相同元素的间隔，那么首先可以通过排序或者哈希表将想用元素的下标按从左到右的顺序聚合在一起。不妨设对于某个元素得到的下标数组为nums[index]，其长度为cnt，那么对于其中的nums[index]而言，该下标与其他下标间隔之和可以分为左右两个部分，分别为

(nums[index] - nums[0]) + (nums[index] - nums[1]) + ... +(nums[index] - nums[index - 1])

以及

(nums[index + 1] - nums[index]) + (nums[index + 2] - nums[index]) + ... + (nums[cnt - 1] - nums[index])

去除括号之后，就是

nums[index] \* index - (nums[0] + nums[1] + ... + nums[index - 1])

以及

(nums[index + 1] + nums[index + 2] + ... + nums[cnt - 1]) - nums[index] \* (cnt - index - 1)

可以发现，在这里就变成了求解两个区间和。对于区间和问题，经典的做法就是采用前缀和来进行优化。当然在这里左侧的前缀和可以随着遍历的进行顺便计算，而右侧的区间和则可以通过nums的总和减去左边的前缀和得到，因此无需预处理前缀和数组，只需随着遍历的进行同步计算即可。

最后附上python代码：

```python
class Solution(object):
    def getDistances(self, arr):
        """
        :type arr: List[int]
        :rtype: List[int]
        """

        pos_dict = {}
        for index, num in enumerate(arr):
            if num not in pos_dict:
                pos_dict[num] = []
            pos_dict[num].append(index)
        
        res = [0] * len(arr)
        for num in pos_dict:
            cnt = len(pos_dict[num])
            all_sum = sum(pos_dict[num])
            now_sum = 0
            for index in range(cnt):
                left_res = index * pos_dict[num][index] - now_sum
                now_sum += pos_dict[num][index]

                right_res = all_sum - now_sum - (cnt - index - 1) * pos_dict[num][index]

                res[pos_dict[num][index]] = left_res + right_res
        
        return res
```

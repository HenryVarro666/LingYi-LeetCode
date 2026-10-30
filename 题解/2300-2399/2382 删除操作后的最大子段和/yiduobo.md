---
title: "2382. 删除操作后的最大子段和"
aliases: ["yiduobo的每日leetcode 2382.删除操作后的最大子段和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/union-find", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/七-并查集", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/564881037"
zhihu_id: "564881037"
zhihu_title: "yiduobo的每日leetcode 2382.删除操作后的最大子段和"
question_id: "2382"
question: "删除操作后的最大子段和"
problem_url: "https://leetcode.cn/problems/maximum-segment-sum-after-removals/"
difficulty: "Hard"
rating: 2136
created: "2022-09-16T00:57:56+08:00"
updated: "2022-09-16T00:57:56+08:00"
upvotes: 0
comments: 0
---

# 2382. 删除操作后的最大子段和

> **[yiduobo的每日leetcode 2382.删除操作后的最大子段和](https://zhuanlan.zhihu.com/p/564881037) · 知乎 · 2022-09-16 · 赞同 0**
> 力扣：[2382. 删除操作后的最大子段和](https://leetcode.cn/problems/maximum-segment-sum-after-removals/) · Hard · 灵茶山艾府：[倒序回答 + 并查集（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2382.删除操作后的最大子段和

[力扣](https://leetcode.cn/problems/maximum-segment-sum-after-removals/)

对于这类不断删东西并要求找出删除过程中的中间结果的问题，一种常见的做法是从最终态开始往前倒推，逐个将删去的东西加回来。对于本题也可以使用这种做法。

当某个数被加回到数组中时，可能出现四种情况：

1、加回来的数自身形成了一个孤立的子段

2、加回来的数与左侧的子段相邻，相当于左侧子段向右扩充了一格

3、加回来的数与右侧的子段相邻，相当于右侧子段向左扩充了一格

4、加回来的数左右两侧都有相邻的子段，相当于将这两个子段连接起来，形成了一个新的子段

可以发现，上面的区间操作中，每个区间只有边界的两个位置在发挥作用，其他非边界的位置是可以忽略的，因此在这里可以只维护区间的边界。令left[i]表示以i为右边界的区间对应的左边界的位置，right[i]则表示以i为左边界的区间对应的右边界的位置。设加回来的数下标为remove，那么对于上面四种情况：

1、remove自身形成了新的子段，因此left[remove] \= right[remove] \= remove

2、remove被容纳进左侧区间。左侧区间原始的右边界为remove - 1，那么对应的左边界自然就是left\[remove - 1\]。吸收remove之后，新的区间左边界不变，依然是left\[remove - 1\]，而右边界则变成了remove，因此在这里需要更新right\[left\[remove - 1\]\]为remove

3、remove被容纳进右侧区间。与情况2完全对称，因此需要更新left\[right\[remove + 1\]\]为remove

4、remove连接了左右两侧的区间。这种情况实际下，新区间的左右边界分别为左侧区间的左边界以及右侧区间的右边界，即left\[remove - 1\]以及right\[remove + 1\]，那么就需要更新right\[left\[remove - 1\]\]为right\[remove + 1\]，同时更新left\[right\[remove + 1\]\]为left\[remove - 1\]

观察上面这四种情况，完全可以将新区间的左边界和新区间的右边界计算出来，然后互相更新left和right就行了。更新完区间信息后，当前这一轮删除后的最大子段和，就必然是下一轮删除后的最大子段和，与本轮产生了变化的区间的子段和中的较大值。本轮产生变化的只有与remove相关的新区间，而这个区间对应的子段和则可以通过区间边界，利用区间和转化为前缀和的思路进行求解。

于是现在就有了一种做法：

1、首先计算nums的前缀和，记为s

2、接下来倒序遍历removeQueries，对于当前遍历到的移除位置remove，先通过判断remove - 1和remove + 1是否分别存在于left和right中来判断remove两侧是否存在相邻的区间，然后根据具体情况确定新区间的左右边界new_left和new_right，最后更新left[new_right]为new_left，right[new_left]为new_right

3、更新完区间信息后，新区间的子段和就是s[new_right] - s[new_left - 1]，与上一轮的结果对比，取较大值作为本轮结果即可

最后附上python代码：

```python
class Solution(object):
    def maximumSegmentSum(self, nums, removeQueries):
        """
        :type nums: List[int]
        :type removeQueries: List[int]
        :rtype: List[int]
        """

        left = {}
        right = {}
        res = [0]
        
        n = len(nums)
        s = [nums[0]]
        for num in nums[1:]:
            s.append(s[-1] + num)

        for index in range(n - 1, 0, -1):
            remove = removeQueries[index]
            if remove - 1 in left:
                new_left = left[remove - 1]
            else:
                new_left = remove
            
            if remove + 1 in right:
                new_right = right[remove + 1]
            else:
                new_right = remove
            
            left[new_right] = new_left
            right[new_left] = new_right

            new_s = s[new_right]
            if new_left > 0:
                new_s -= s[new_left - 1]
            
            res.append(max(res[-1], new_s))

        return res[::-1]
```

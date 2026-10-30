---
title: "363. 矩形区域不超过K的最大数值和"
aliases: ["yiduobo的每日leetcode 363.矩形区域不超过K的最大数值和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/164638020"
zhihu_id: "164638020"
zhihu_title: "yiduobo的每日leetcode 363.矩形区域不超过K的最大数值和"
question_id: "363"
question: "矩形区域不超过K的最大数值和"
problem_url: "https://leetcode.cn/problems/max-sum-of-rectangle-no-larger-than-k/"
created: "2020-07-27T23:10:38+08:00"
updated: "2020-07-27T23:10:38+08:00"
upvotes: 0
comments: 0
---

# 363. 矩形区域不超过K的最大数值和

> **[yiduobo的每日leetcode 363.矩形区域不超过K的最大数值和](https://zhuanlan.zhihu.com/p/164638020) · 知乎 · 2020-07-27 · 赞同 0**
> 力扣：[363. 矩形区域不超过K的最大数值和](https://leetcode.cn/problems/max-sum-of-rectangle-no-larger-than-k/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

363.矩形区域不超过K的最大数值和<https://leetcode-cn.com/problems/max-sum-of-rectangle-no-larger-than-k/>

最朴素的做法当然是枚举左上角和右下角的坐标，然后计算其中的数值和并判断与k的大小情况，是O((mn)^2)的算法。

由于题目后面有说到行数远大于列数的情况，因此自然的想法就是通过枚举固定住列的两侧，然后在行上面做文章。

当列固定住之后，原来二维矩阵的题目就可以通过累加和转化为一维数组上的问题，即对于一个长度为m的数组nums，需要选择两点i和j，使得nums[i] + nums[i + 1] + ... + nums[j]小于等于k，且最大。

注意到上面涉及到了区间和的运算，于是一个自然的想法就是将其进一步转化为前缀和的问题，那么现在就变成了对于前缀和数组sum_list，需要选择两点i和j，是的sum_list[j] - sum_list[i - 1]小于等于k，且最大。

这个问题似乎在哪里见到过，不过遗憾的是，这里有一点不同时数值中存在负数，因此sum_list并不是单调递增的，因此不能通过滑动窗口来做。

在这里，对于一个sum_list[j]，我们的目标是找到对应的i，其满足sum_list[i - 1] >\= sum_list[j] - k，sum_list[i - 1]是最大的那一个。

于是一个自然的想法就是一趟扫描，通过平衡树来维护之前的sum_list。设当前处理到sum_list[j]，那么每次先在平衡树中查找比sum_list[j] - k小的最大的值并对比其与答案的大小，然后将sum_list[j]插入到平衡树中。

最终的时间复杂度是O(mlogm)，于是整个问题最终的时间复杂度就是O(n^2 \* mlogm)。

我在这里又是使用的数组加二分查找的方式（主要还是对python的了解还不够深刻，可能存在某种类平衡树的东西我不知道用），这里数组插入的时间复杂度可以到O(m)，因此最坏情况下时间复杂度还是O((mn)^2)。

当然，也可以加入一些先做最大子段和确定上界之类的剪枝操作，不过最坏情况下这些剪枝操作都不会影响到最终的时间复杂度，因此就不在这里展开了。

最后附上python代码：

```python
class Solution(object):
    def maxSumSubmatrix(self, matrix, k):
        """
        :type matrix: List[List[int]]
        :type k: int
        :rtype: int
        """

        if not matrix:
            return 0

        m = len(matrix)
        n = len(matrix[0])

        res = -2147483647
        for left in range(n):
            row_sum = [0] * m
            for right in range(left, n):
                pre_sum = 0
                sum_list = []
                for index in range(m):
                    row_sum[index] += matrix[index][right]
                    pre_sum += row_sum[index]

                    if pre_sum <= k:
                        res = max(res, pre_sum)
                        if res == k:
                            return res

                    if not sum_list:
                        sum_list.append(pre_sum)
                    else:
                        tmp = pre_sum - k
                        if tmp <= sum_list[-1]:
                            l = 0
                            r = len(sum_list) - 1
                            while l < r:
                                mid = (l + r) / 2
                                if sum_list[mid] == tmp:
                                    return k
                                if sum_list[mid] < tmp:
                                    l = mid + 1
                                else:
                                    r = mid
                            res = max(res, pre_sum - sum_list[l])

                        if pre_sum > sum_list[-1]:
                            sum_list.append(pre_sum)
                        else:
                            l = 0
                            r = len(sum_list) - 1
                            insert_flag = True
                            while l < r:
                                mid = (l + r) / 2
                                if sum_list[mid] == pre_sum:
                                    insert_flag = False
                                    break
                                if sum_list[mid] < pre_sum:
                                    l = mid + 1
                                else:
                                    r = mid
                            sum_list = sum_list[:l] + [pre_sum] + sum_list[l:]

        return res
```

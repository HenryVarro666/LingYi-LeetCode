---
title: "1093. 大样本统计"
aliases: ["yiduobo的每日leetcode 1093.大样本统计"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/373681157"
zhihu_id: "373681157"
zhihu_title: "yiduobo的每日leetcode 1093.大样本统计"
question_id: "1093"
question: "大样本统计"
problem_url: "https://leetcode.cn/problems/statistics-from-a-large-sample/"
created: "2021-05-19T22:33:33+08:00"
updated: "2021-05-19T22:33:33+08:00"
upvotes: 0
comments: 9
---

# 1093. 大样本统计

> **[yiduobo的每日leetcode 1093.大样本统计](https://zhuanlan.zhihu.com/p/373681157) · 知乎 · 2021-05-19 · 赞同 0**
> 力扣：[1093. 大样本统计](https://leetcode.cn/problems/statistics-from-a-large-sample/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1093.大样本统计

[力扣](https://leetcode-cn.com/problems/statistics-from-a-large-sample/)

桶排的练习题。题目要求找出最小值、最大值、平均值、中位数以及众数。

其中最小值和最大值是最好求的，一趟扫描，对于第一个count[index]不等于0的index就是最小值，而最后一个count[index]不等于0的index就是最大值。

在扫描过程中，也可以找出count[index]最大的index，就是众数。

对于平均数，则可以在扫描过程中累加当前的count[index] \* index，先求出所有数的和sum。同时在扫描过程中使用桶排，执行count[index] +\= count[index - 1]，这样一来count[index]就表示小于等于index的数一共有多少个，那么最终的平均数就是sum / count[255]。

最后是求解中位数，我们可以利用求众数时得到的新的count数组，已知一共有count[255]个数。将总数记为tot，那么当tot为奇数时，中位数就是从小到大排名第(tot + 1) / 2的数；当tot为偶数时，中位数则是从小到大排名第(tot + 1) / 2以及第(tot + 1) / 2 + 1这两个数的平均值。由于这里一共就256个数，也没必要使用二分法，直接从0开始扫描，若当前的index第一次满足count[index] >\= target，那么就说明从小到大排名第target的数就是index。利用上面的结论，一趟扫描找到对应的数即可。

最后附上python代码：

```python
class Solution(object):
    def sampleStats(self, count):
        """
        :type count: List[int]
        :rtype: List[float]
        """

        mi = None
        ma = None
        avg = 0.0
        max_cnt = 0
        mode = None
        
        for index in range(256):
            cnt = count[index]
            if cnt > 0:
                if mi is None:
                    mi = float(index)
                ma = float(index)
                avg += index * cnt
                if cnt > max_cnt:
                    max_cnt = cnt
                    mode = float(index)
            if index > 0:
                count[index] += count[index - 1]

        avg /= count[-1]
        index = 0
        while index < 256 and count[index] < (count[-1] + 1) / 2:
            index += 1
        if count[-1] % 2 == 1 or count[index] >= (count[-1] + 1) / 2 + 1:
            median = float(index)
        else:
            median = float(index)
            while index < 256 and count[index] < (count[-1] + 1) / 2 + 1:
                index += 1
            median += float(index)
            median /= 2.0
        
        return mi, ma, avg, median, mode
```

---
title: "702. 搜索长度未知的有序数组"
aliases: ["yiduobo的每日leetcode 702.搜索长度未知的有序数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/604354740"
zhihu_id: "604354740"
zhihu_title: "yiduobo的每日leetcode 702.搜索长度未知的有序数组"
question_id: "702"
question: "搜索长度未知的有序数组"
problem_url: "https://leetcode.cn/problems/search-in-a-sorted-array-of-unknown-size/"
created: "2023-02-07T23:14:11+08:00"
updated: "2023-02-07T23:14:11+08:00"
upvotes: 0
comments: 0
---

# 702. 搜索长度未知的有序数组

> **[yiduobo的每日leetcode 702.搜索长度未知的有序数组](https://zhuanlan.zhihu.com/p/604354740) · 知乎 · 2023-02-07 · 赞同 0**
> 力扣：[702. 搜索长度未知的有序数组](https://leetcode.cn/problems/search-in-a-sorted-array-of-unknown-size/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

702.搜索长度未知的有序数组

[力扣](https://leetcode.cn/problems/search-in-a-sorted-array-of-unknown-size/)

非常标准的二分查找的问题。由于题目保证了数组长度不超过10000，因此二分的初始边界可以设定为left \= 0，right \= 9999，接下来开始进行二分。

对于当前处理到的mid，通过reader获取数组中下标为mid的数的值v。v的取值有以下几种可能：

1、v \= 2^31 - 1：说明mid超出了数组的边界，此时应该调整二分上界为right \= mid - 1

2、v > target：说明答案位于mid的左侧，此时应该调整二分上界为right \= mid - 1

3、v \< target：说明答案位于mid的右侧，此时应该调整二分下界为left \= mid + 1

4、v \= target：说明找到了答案，此时直接返回mid即可

若二分结束后仍没有找到答案，说明target不存在与数组中，此时返回-1

最后附最后附上python代码：

```python
# """
# This is ArrayReader's API interface.
# You should not implement it, or speculate about its implementation
# """
#class ArrayReader(object):
#    def get(self, index):
#        """
#        :type index: int
#        :rtype int
#        """

class Solution(object):
    def search(self, reader, target):
        """
        :type reader: ArrayReader
        :type target: int
        :rtype: int
        """

        left = 0
        right = 9999
        while left <= right:
            mid = (left + right) >> 1
            v = reader.get(mid)
            if v == 2147483647 or v > target:
                right = mid - 1
            elif v < target:
                left = mid + 1
            else:
                return mid
        
        return -1
```

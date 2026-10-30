---
title: "1533. 找到最大整数的索引"
aliases: ["yiduobo的每日leetcode 1533.找到最大整数的索引"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/617518116"
zhihu_id: "617518116"
zhihu_title: "yiduobo的每日leetcode 1533.找到最大整数的索引"
question_id: "1533"
question: "找到最大整数的索引"
problem_url: "https://leetcode.cn/problems/find-the-index-of-the-large-integer/"
created: "2023-03-28T00:35:26+08:00"
updated: "2023-03-28T00:35:26+08:00"
upvotes: 1
comments: 0
---

# 1533. 找到最大整数的索引

> **[yiduobo的每日leetcode 1533.找到最大整数的索引](https://zhuanlan.zhihu.com/p/617518116) · 知乎 · 2023-03-28 · 赞同 1**
> 力扣：[1533. 找到最大整数的索引](https://leetcode.cn/problems/find-the-index-of-the-large-integer/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1533.找到最大整数的索引

[力扣](https://leetcode.cn/problems/find-the-index-of-the-large-integer/)

题目中只有一个最大的整数与其他的整数，那么一个可行的思路就是将这些数分为两个长度相同的部分，哪边的和越大，这个最大的整数就属于那边。接下来就只需不断迭代边界直到找出最终答案为止。

对于这种处理方法，在剩余数的数量为奇数时，将这些数分为两个部分后还会剩下一个落单的数，此时则多出了一种情况，也就是这两个部分之和相等时，最大的数就是这个落单的数。

更进一步的，当剩余的数大于等于三个时，可以将这些数均分成三份，且必须保证前两份数的数量相同。接下来同样是比较前两份的数之和的大小关系，这样一来每轮迭代后就可以将数据规模缩减到三分之一，而不是常规二分法的二分之一，效率更好。

最后附上python代码：

```python
# """
# This is ArrayReader's API interface.
# You should not implement it, or speculate about its implementation
# """
#class ArrayReader(object):
#	 # Compares the sum of arr[l..r] with the sum of arr[x..y]
#	 # return 1 if sum(arr[l..r]) > sum(arr[x..y])
#	 # return 0 if sum(arr[l..r]) == sum(arr[x..y])
#	 # return -1 if sum(arr[l..r]) < sum(arr[x..y])
#    def compareSub(self, l, r, x, y):
#        """
#        :type l, r, x, y: int
#        :rtype int
#        """
#
#	 # Returns the length of the array
#    def length(self):
#        """
#        :rtype int
#        """

class Solution(object):
    def getIndex(self, reader):
        """
        :type reader: ArrayReader
        :rtype: integer
        """

        n = reader.length()

        left = 0
        right = n - 1
        while left < right:
            if left == right - 1:
                if reader.compareSub(left, left, right, right) > 0:
                    right = left
                else:
                    left = right

            else:
                part_len = (right - left + 1) / 3
                p1 = left + part_len - 1
                p2 = p1 + 1 + part_len - 1
                com_res = reader.compareSub(left, p1, p1 + 1, p2)
                if com_res == -1:
                    left = p1 + 1
                    right = p2
                elif com_res == 0:
                    left = p2 + 1
                else:
                    right = p1
        
        return left
```

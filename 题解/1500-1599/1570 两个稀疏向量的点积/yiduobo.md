---
title: "1570. 两个稀疏向量的点积"
aliases: ["yiduobo的每日leetcode 1570.两个稀疏向量的点积"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/618088481"
zhihu_id: "618088481"
zhihu_title: "yiduobo的每日leetcode 1570.两个稀疏向量的点积"
question_id: "1570"
question: "两个稀疏向量的点积"
problem_url: "https://leetcode.cn/problems/dot-product-of-two-sparse-vectors/"
created: "2023-03-30T01:07:48+08:00"
updated: "2023-03-30T01:07:48+08:00"
upvotes: 0
comments: 0
---

# 1570. 两个稀疏向量的点积

> **[yiduobo的每日leetcode 1570.两个稀疏向量的点积](https://zhuanlan.zhihu.com/p/618088481) · 知乎 · 2023-03-30 · 赞同 0**
> 力扣：[1570. 两个稀疏向量的点积](https://leetcode.cn/problems/dot-product-of-two-sparse-vectors/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1570.两个稀疏向量的点积

[力扣](https://leetcode.cn/problems/dot-product-of-two-sparse-vectors/)

0是不会对向量点积产生影响的，因此稀疏向量只需要储存非0列的下标以及数值。在具体运算时，则需要使用两个变量p1和p2分别表示当前的运算来到了这两个稀疏向量的哪个位置。若p1在当前向量中对应的下标与p2在另一个向量中对应的下标相同，那么就将p1和p2对应的数值相乘并累加到答案中，否则就将对应下标较小的那一方向后移动，直到p1移动到当前向量的末尾，或者p2移动到另一个向量的末尾。

最后附上python代码：

```python
class SparseVector:
    def __init__(self, nums):
        """
        :type nums: List[int]
        """

        self.digit_list = []
        for index, num in enumerate(nums):
            if num > 0:
                self.digit_list.append([index, num])

    # Return the dotProduct of two sparse vectors
    def dotProduct(self, vec):
        """
        :type vec: 'SparseVector'
        :rtype: int
        """
        p1 = p2 = 0
        res = 0
        while p1 < len(self.digit_list) and p2 < len(vec.digit_list):
            if self.digit_list[p1][0] == vec.digit_list[p2][0]:
                res += self.digit_list[p1][1] * vec.digit_list[p2][1]
                p1 += 1
                p2 += 1
            elif self.digit_list[p1][0] < vec.digit_list[p2][0]:
                p1 += 1
            else:
                p2 += 1
        
        return res
        

# Your SparseVector object will be instantiated and called as such:
# v1 = SparseVector(nums1)
# v2 = SparseVector(nums2)
# ans = v1.dotProduct(v2)
```

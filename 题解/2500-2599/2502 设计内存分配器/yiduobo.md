---
title: "2502. 设计内存分配器"
aliases: ["yiduobo的每日leetcode 2502.设计内存分配器"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/design", "leetcode/segment-tree", "leetcode/hash-table", "leetcode/simulation", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/634051033"
zhihu_id: "634051033"
zhihu_title: "yiduobo的每日leetcode 2502.设计内存分配器"
question_id: "2502"
question: "设计内存分配器"
problem_url: "https://leetcode.cn/problems/design-memory-allocator/"
difficulty: "Medium"
created: "2023-06-02T02:09:22+08:00"
updated: "2023-06-02T02:09:22+08:00"
upvotes: 0
comments: 0
---

# 2502. 设计内存分配器

> **[yiduobo的每日leetcode 2502.设计内存分配器](https://zhuanlan.zhihu.com/p/634051033) · 知乎 · 2023-06-02 · 赞同 0**
> 力扣：[2502. 设计内存分配器](https://leetcode.cn/problems/design-memory-allocator/) · Medium · 灵茶山艾府：[两种方法：模拟 / 线段树二分（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2502.设计内存分配器

[力扣](https://leetcode.cn/problems/design-memory-allocator/)

由于题目的数据规模不大，因此直接使用O(n^2)的暴力算法是完全可行的。

对于分配操作，从头部开始遍历分配区间的起点left，找出从left开始的连续空闲内存的终点right。若left到right之间空闲的位置大于等于申请的大小size，那么就从left开始划分size的空间给mID并返回left。若找不到可用的left则返回-1。

对于释放操作，则只需一趟遍历，统计值为mId的位置出现的次数同时将这些位置重新置为0即可。

最后附上python代码：

```python
class Allocator(object):

    def __init__(self, n):
        """
        :type n: int
        """
        self.n = n
        self.mem = [0] * n

    def allocate(self, size, mID):
        """
        :type size: int
        :type mID: int
        :rtype: int
        """
        left = 0
        while left < self.n:
            while left < self.n and self.mem[left] != 0:
                left += 1
            if left == self.n:
                break
            
            right = left + 1
            while right < self.n and right - left < size and self.mem[right] == 0:
                right += 1
            
            if right - left >= size:
                for index in range(left, right):
                    self.mem[index] = mID
                return left
            
            left = right
        
        return -1

    def free(self, mID):
        """
        :type mID: int
        :rtype: int
        """
        cnt = 0
        for index in range(self.n):
            if self.mem[index] == mID:
                self.mem[index] = 0
                cnt += 1
        
        return cnt

# Your Allocator object will be instantiated and called as such:
# obj = Allocator(n)
# param_1 = obj.allocate(size,mID)
# param_2 = obj.free(mID)
```

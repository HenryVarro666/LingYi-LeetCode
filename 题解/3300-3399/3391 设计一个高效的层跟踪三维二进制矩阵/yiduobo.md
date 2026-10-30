---
title: "3391. 设计一个高效的层跟踪三维二进制矩阵"
aliases: ["yiduobo的每日leetcode 3391.设计一个高效的层跟踪三维二进制矩阵"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/30105186188"
zhihu_id: "30105186188"
zhihu_title: "yiduobo的每日leetcode 3391.设计一个高效的层跟踪三维二进制矩阵"
question_id: "3391"
question: "设计一个高效的层跟踪三维二进制矩阵"
problem_url: "https://leetcode.cn/problems/design-a-3d-binary-matrix-with-efficient-layer-tracking/"
created: "2025-03-14T00:34:55+08:00"
updated: "2025-03-14T00:34:55+08:00"
upvotes: 1
comments: 0
---

# 3391. 设计一个高效的层跟踪三维二进制矩阵

> **[yiduobo的每日leetcode 3391.设计一个高效的层跟踪三维二进制矩阵](https://zhuanlan.zhihu.com/p/30105186188) · 知乎 · 2025-03-14 · 赞同 1**
> 力扣：[3391. 设计一个高效的层跟踪三维二进制矩阵](https://leetcode.cn/problems/design-a-3d-binary-matrix-with-efficient-layer-tracking/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3391.设计一个高效的层跟踪三维二进制矩阵

[3391. 设计一个高效的层跟踪三维二进制矩阵 - 力扣（LeetCode）](https://leetcode.cn/problems/design-a-3d-binary-matrix-with-efficient-layer-tracking/description/)

题目给出一个n \* n \* n的二进制三维数组matrix，n的规模不超过100。要求实现matrix3D类：

1、Matrix3D(int n)：使用三维二进制数组matrix初始化对象，其中所有元素初始化为0。

2、setCell(int x, int y, int z)：将matrix[x][y][z]的值设为1。

3、unsetCell(int x, int y, int z)：将matrix[x][y][z]的值设为0。

4、int largestMatrix()：返回包含最多1的matrix[x]的下标x，若存在多个，则返回最大的x。

由于题目中n的规模不大，那么对于题目中的前3种操作，完全可以模拟一个二进制的三维数组，按题目要求置0或者置1。而对于第4种操作，则可以使用一个计数数组cnt来就来每种x对应的matrix[x]中1的数量，然后使用一个堆来储存所有的(cnt[x], x)对，用来高效获取其中的最大值。另外由于python原生的堆不支持删除指定元素的操作，于是在这里采用懒删除的方法比较方便。

那么就有：

1、Matrix3D(int n)：

初始化n \* n \* n的三维数组matrix，其中元素值都为0。

另外初始化cnt为全0，然后从0遍历到n - 1，对于当前遍历到的x，将(0, -x)插入到堆heap中。这里取-x的理由是为了使得次数相同时x最大，默认为小根堆时就应该将值取反。

2、setCell(int x, int y, int z)：

若matrix[x][y][z]为1，此时无事发生。

若matrix[x][y][z]为0，则应该将matrix[x][y][z]置为1，然后将cnt[x]加上1，最后将(-cnt[x], -x)加入到堆中。

3、unsetCell(int x, int y, int z)：

若matrix[x][y][z]为0，此时无事发生。

若matrix[x][y][z]为1，则应该将matrix[x][y][z]置为0，然后将cnt[x]减去1，最后将(-cnt[x], -x)加入到堆中。

4、largestMatrix()：

首先检测堆顶元素-heap\[0\]\[1\]对应的出现次数，即cnt\[-heap\[0\]\[1\]\]是否与-heap\[0\]\[0\]相等，若不相等，说明对应元素之前被更新过但是还没来得及删除，此时应该将其从堆中删除。

去掉待删除的堆顶元素后，最终答案就是-heap[0][1]。

最后附上python代码：

```python
class Matrix3D(object):

    def __init__(self, n):
        """
        :type n: int
        """
        self.matrix = [[[0] * n for _ in range(n)] for _ in range(n)]
        self.cnt = [0] * n
        self.heap = []
        for x in range(n):
            heapq.heappush(self.heap, (0, -x))

    def setCell(self, x, y, z):
        """
        :type x: int
        :type y: int
        :type z: int
        :rtype: None
        """
        if self.matrix[x][y][z] == 1:
            return

        self.matrix[x][y][z] = 1
        self.cnt[x] += 1
        heapq.heappush(self.heap, (-self.cnt[x], -x))

    def unsetCell(self, x, y, z):
        """
        :type x: int
        :type y: int
        :type z: int
        :rtype: None
        """
        if self.matrix[x][y][z] == 0:
            return
        
        self.matrix[x][y][z] = 0
        self.cnt[x] -= 1
        heapq.heappush(self.heap, (-self.cnt[x], -x))

    def largestMatrix(self):
        """
        :rtype: int
        """
        while self.cnt[-self.heap[0][1]] != -self.heap[0][0]:
            heapq.heappop(self.heap)
        return -self.heap[0][1]

# Your Matrix3D object will be instantiated and called as such:
# obj = Matrix3D(n)
# obj.setCell(x,y,z)
# obj.unsetCell(x,y,z)
# param_3 = obj.largestMatrix()
```

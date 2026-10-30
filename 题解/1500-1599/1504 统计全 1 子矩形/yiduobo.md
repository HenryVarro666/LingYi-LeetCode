---
title: "1504. 统计全1子矩形"
aliases: ["yiduobo的每日leetcode 1504.统计全1子矩形"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/dynamic-programming", "leetcode/enumeration", "leetcode/sliding-window", "leetcode/monotonic-stack", "题单/单调栈", "题单/单调栈/二-矩形"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/419250864"
zhihu_id: "419250864"
zhihu_title: "yiduobo的每日leetcode 1504.统计全1子矩形"
question_id: "1504"
question: "统计全 1 子矩形"
problem_url: "https://leetcode.cn/problems/count-submatrices-with-all-ones/"
difficulty: "Medium"
created: "2021-10-08T23:49:07+08:00"
updated: "2021-10-08T23:49:07+08:00"
upvotes: 1
comments: 0
---

# 1504. 统计全1子矩形

> **[yiduobo的每日leetcode 1504.统计全1子矩形](https://zhuanlan.zhihu.com/p/419250864) · 知乎 · 2021-10-08 · 赞同 1**
> 力扣：[1504. 统计全 1 子矩形](https://leetcode.cn/problems/count-submatrices-with-all-ones/) · Medium · 灵茶山艾府：[【图解】两种方法：枚举上下边界 / 单调栈（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1504.统计全1子矩形

[力扣](https://leetcode-cn.com/problems/count-submatrices-with-all-ones/)

之前好像做过一道类似的题目，在这里做法也是比较类似，具体来说就是利用起高度以及之前得到的答案。

例如样例2中的

0 1 1 0

0 1 1 1

1 1 1 0

下标按0开始标号，那么以mat[2][1]为右下角的全1子矩形数目为4个，分别是以mat[2][1]为水平边，竖直方向上高度为1、2、3的3个子矩形，再加上以mat[2][1]以及mat[2][0]为水平边，竖直方向上高度为1的子矩形。

而对于mat[2][2]为右下角的全1子矩形数目则为7个，分别是以mat[2][2]为水平边的3个，以mat[2][2]以及mat[2][1]为水平边的3个，再加上mat[2][2]、mat[2][1]、mat[2][0]共同构成的水平边，竖直高度为1的1个。

更一般的，设f[i][j]表示以mat[i][j]为右下角的全1子矩形数目。为了方便计算，记前i行每一列的最长连续后缀1为h。那么对于第i行的各个位置j而言，就有：

1、若mat[i][j]不为0，那么就可以形成h[j]个以mat[i][j]为水平边的全1矩形

2、接下来从j - 1开始向前遍历，设当前处于位置p，那么以mat[2][j]到mat[2][p]为水平边的全1子矩形就有min(h[j], h[j - 1], ..., h[p])个

更进一步的，若q是第一个满足h[q] \< h[j]的位置，那么显然就有

min(h[j], h[j - 1]) \= h[j]

min(h[j], h[j - 1], h[j - 2]) \= h[j]

...

min(h[j], h[j - 1], h[j - 2], ... , h[q + 1]) \= h[j]

对于上面这些情况，子矩形的水平长度分别为2到j - q，而高度则可以从1到h[j]，因此一共可以形成(j - q) \* h[j]个以mat[i][j]为右下角的全1子矩形。例如样例中统计得到的h为

1 3 3 1

其中后面这个3对应的q \= 0，因此这里就有(2 - 0) \* 3 \= 6，对应了后面这两个3可以形成的6个子矩形。

而对于q而言，以mat[i][q]为右下角的全1子矩形的最大高度必然是小于h[j]的，也就是说对于f[i][q]表示的任意情况，都可以在其右侧填充上适当的全1子矩形，从而得到以mat[i][j]为右下角的子矩形。对应到样例中，也就是最后一行的前三个1构成的子矩形。

综合起来，就有f[i][j] \= f[i][q] + (j - q) \* h[j]

到了这里，问题就变成了求出h以后，找出h中每个数h[j]左侧的第一个小于h[j]的位置q，这个经典的问题可以通过单调栈来解决。

另外，f中i这一维是完全可以省去的。

最后附上python代码：

```python
class Solution(object):
    def numSubmat(self, mat):
        """
        :type mat: List[List[int]]
        :rtype: int
        """

        m = len(mat)
        n = len(mat[0])
        
        res = 0
        height = [0] * n
        for i in range(m):
            f = [0] * n
            stack = []
            for j in range(n):
                if mat[i][j] == 0:
                    height[j] = 0
                elif i == 0:
                    height[j] = mat[i][j]
                else:
                    height[j] += 1
                while stack and height[stack[-1]] >= height[j]:
                    stack.pop()
                
                if not stack:
                    f[j] = height[j] * (j + 1)
                else:
                    f[j] = f[stack[-1]] + height[j] * (j - stack[-1])

                res += f[j]

                stack.append(j)
            
        return res
```

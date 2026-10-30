---
title: "48. 旋转图像"
aliases: ["yiduobo的每日leetcode 48.旋转图像"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/matrix", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/LeetCode-热题-100/矩阵", "题单/面试经典-150-题/矩阵"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/125769995"
zhihu_id: "125769995"
zhihu_title: "yiduobo的每日leetcode 48.旋转图像"
question_id: "48"
question: "旋转图像"
problem_url: "https://leetcode.cn/problems/rotate-image/"
difficulty: "Medium"
created: "2020-04-05T23:58:54+08:00"
updated: "2020-04-05T23:58:54+08:00"
upvotes: 0
comments: 0
---

# 48. 旋转图像

> **[yiduobo的每日leetcode 48.旋转图像](https://zhuanlan.zhihu.com/p/125769995) · 知乎 · 2020-04-05 · 赞同 0**
> 力扣：[48. 旋转图像](https://leetcode.cn/problems/rotate-image/) · Medium · 灵茶山艾府：[数学本质：两次翻转等于一次旋转（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

48.旋转图像<https://leetcode-cn.com/problems/rotate-image/>

找规律的题目。我的做法是从外向内一圈一圈地进行旋转。由于题目保证是正方形，因此可以将其看成是四条等长的边在轮转。例如

1 2 3 4

5 6 7 8

9 10 11 12

13 14 15 16

对于外面这个4 \* 4的正方形，四条边分别是

(a) 1、 2、 3

(b) 4、 8、12

(c) 16、15、14

(d) 13、 9、 5

可以发现，竖着看下来的话正好就是数字轮换的位置，即

1 -> 4 -> 16 -> 13 -> 1

2 -> 8 -> 15 -> 9 -> 2

3 -> 12 -> 14 -> 5 -> 3

接下来确定每一组数的坐标。不妨设此时我们处理到了第i个正方形，当前这一组数中，位于上边的数为(x1, y1)，位于右边的数为(x2, y2)，位于下边的数为(x3, y3)，位于左边的数为(x4, y4)。

首先考察x1与y1。

显然有x1 \= i。

然后考察y1的取值范围。左边界同样是i，右边界与左边界是对称的，但需要注意排除掉正方形右上角的那个点，因此y1的取值范围为i到n - 1 - i - 1 \= n - i - 2。

接下来考察x2与y2。

可以发现(x1, y1)离左边的距离y1等于(x2, y2)离上边的距离x2，即x2 \= y1

而(x1, y1)离上边的距离x1等于(x2, y2)离右边的距离n - 1 - y2，于是有y2 \= n - 1 - x1

再往下考察x3与y3。

可以发现(x2, y2)离右边的距离n - 1 - y2等于(x3, y3)离下边的距离n - 1 - x3，即x3 \= y2

而(x2, y2)离上边的距离x2等于(x3, y3)离右边的距离n - 1 - y3，于是有y3 \= n - 1 - x2

最后考察x4与y4。

可以发现(x3, y3)离右边的距离n - 1 - y3等于(x4, y4)离下边的距离n - 1 - x4，即x4 \= y3

而(x3, y3)离下边的距离n - 1 - x3等于(x4, y4)离左边的距离y4，于是有y4 \= n - 1 - x3

这样一来就确定好了一个组数中位置的变化规律。接下来只需要逐个遍历正方形，然后对于每个正方形再遍历正方形的上边，逐个轮换4个一组的数即可。由于每个数字都轮换了一次，因此最后的时间复杂度为O(n^2)。

最后附上python代码：

```python
class Solution(object):
    def rotate(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: None Do not return anything, modify matrix in-place instead.
        """

        n = len(matrix)
        for i in range(n / 2):
            for j in range(i, n - i - 1):
                x1 = i
                y1 = j
                
                x2 = y1
                y2 = n - 1 - x1
                
                x3 = y2
                y3 = n - 1 - x2
                
                x4 = y3
                y4 = n - 1 - x3

                tmp = matrix[x1][y1]
                matrix[x1][y1] = matrix[x4][y4]
                matrix[x4][y4] = matrix[x3][y3]
                matrix[x3][y3] = matrix[x2][y2]
                matrix[x2][y2] = tmp
```

---
title: "1886. 判断矩阵经轮转后是否一致"
aliases: ["yiduobo的每日leetcode 1886.判断矩阵经轮转后是否一致"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/enumeration"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/477845854"
zhihu_id: "477845854"
zhihu_title: "yiduobo的每日leetcode 1886.判断矩阵经轮转后是否一致"
question_id: "1886"
question: "判断矩阵经轮转后是否一致"
problem_url: "https://leetcode.cn/problems/determine-whether-matrix-can-be-obtained-by-rotation/"
difficulty: "Easy"
created: "2022-03-08T22:35:53+08:00"
updated: "2022-03-08T22:35:53+08:00"
upvotes: 1
comments: 0
---

# 1886. 判断矩阵经轮转后是否一致

> **[yiduobo的每日leetcode 1886.判断矩阵经轮转后是否一致](https://zhuanlan.zhihu.com/p/477845854) · 知乎 · 2022-03-08 · 赞同 1**
> 力扣：[1886. 判断矩阵经轮转后是否一致](https://leetcode.cn/problems/determine-whether-matrix-can-be-obtained-by-rotation/) · Easy · 灵茶山艾府：[两种方法：先旋转再比较 / 直接比较（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1886.判断矩阵经轮转后是否一致

[力扣](https://leetcode-cn.com/problems/determine-whether-matrix-can-be-obtained-by-rotation/)

对于矩阵中的格子(x, y)，经过一次轮转之后是(y, n - x - 1)

将(y, n - x - 1)带入上面的变换，就可以直到两次轮转之后是(n - x - 1, n - y - 1)

同样的，可知三次轮转之后是(n - y - 1, x)

第四次轮转就回到了原位(x, y)

也就是说，只需要考察轮转0到3次的可能性。若原矩阵中的某个位置在轮转k次之后不等于target中对应位置的值，那么就说明原矩阵轮转k次不能得到target，于是只需要对每个格子都判断轮转0到3次时是否与target中对应格子相同，若不相同，则排除这种轮转次数。

若最后还存在某种可能的轮转次数，说明就按这个轮转次数轮转就能使得原矩阵变为target。

最后附上python代码：

```python
class Solution(object):
    def findRotation(self, mat, target):
        """
        :type mat: List[List[int]]
        :type target: List[List[int]]
        :rtype: bool
        """

        n = len(mat)
        impossible = set()
        for i in range(n):
            for j in range(n):
                if mat[i][j] != target[i][j]:
                    impossible.add(0)
                if mat[i][j] != target[j][n - i - 1]:
                    impossible.add(1)
                if mat[i][j] != target[n - i - 1][n - j - 1]:
                    impossible.add(2)
                if mat[i][j] != target[n - j - 1][i]:
                    impossible.add(3)
                
                if len(impossible) == 4:
                    return False

        return True
```

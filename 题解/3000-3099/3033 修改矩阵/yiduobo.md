---
title: "3033. 修改矩阵"
aliases: ["yiduobo的每日leetcode 3033.修改矩阵"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/695651388"
zhihu_id: "695651388"
zhihu_title: "yiduobo的每日leetcode 3033.修改矩阵"
question_id: "3033"
question: "修改矩阵"
problem_url: "https://leetcode.cn/problems/modify-the-matrix/"
difficulty: "Easy"
created: "2024-05-02T00:41:37+08:00"
updated: "2024-05-02T00:41:37+08:00"
upvotes: 1
comments: 0
---

# 3033. 修改矩阵

> **[yiduobo的每日leetcode 3033.修改矩阵](https://zhuanlan.zhihu.com/p/695651388) · 知乎 · 2024-05-02 · 赞同 1**
> 力扣：[3033. 修改矩阵](https://leetcode.cn/problems/modify-the-matrix/) · Easy · 灵茶山艾府：[简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3033.修改矩阵

[. - 力扣（LeetCode）](https://leetcode.cn/problems/modify-the-matrix/description/)

按列遍历整个矩阵，对于当前列，先按行遍历获取列中的最大值ma，接下来再将列中值为-1的数修改成ma即可。

最后附上python代码：

```python
class Solution(object):
    def modifiedMatrix(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: List[List[int]]
        """

        m = len(matrix)
        n = len(matrix[0])

        for j in range(n):
            ma = -1
            for i in range(m):
                ma = max(ma, matrix[i][j])
            
            for i in range(m):
                if matrix[i][j] == -1:
                    matrix[i][j] = ma
        
        return matrix
```

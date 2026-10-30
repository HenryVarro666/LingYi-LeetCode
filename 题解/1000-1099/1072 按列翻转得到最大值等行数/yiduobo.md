---
title: "1072. 按列翻转得到最大值等行数"
aliases: ["yiduobo的每日leetcode 1072.按列翻转得到最大值等行数"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/372414064"
zhihu_id: "372414064"
zhihu_title: "yiduobo的每日leetcode 1072.按列翻转得到最大值等行数"
question_id: "1072"
question: "按列翻转得到最大值等行数"
problem_url: "https://leetcode.cn/problems/flip-columns-for-maximum-number-of-equal-rows/"
difficulty: "Medium"
created: "2021-05-14T21:53:48+08:00"
updated: "2021-05-14T21:53:48+08:00"
upvotes: 0
comments: 0
---

# 1072. 按列翻转得到最大值等行数

> **[yiduobo的每日leetcode 1072.按列翻转得到最大值等行数](https://zhuanlan.zhihu.com/p/372414064) · 知乎 · 2021-05-14 · 赞同 0**
> 力扣：[1072. 按列翻转得到最大值等行数](https://leetcode.cn/problems/flip-columns-for-maximum-number-of-equal-rows/) · Medium · 灵茶山艾府：[逆向思维（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1072.按列翻转得到最大值等行数

[力扣](https://leetcode-cn.com/problems/flip-columns-for-maximum-number-of-equal-rows/)

由于这里一次要翻转一整列，那么若两行初始状况下完全一致，那么翻转之后也将是完全一致。同样地，若两行初始状态下正好互补，那么翻转之后也将是正好互补。

不妨设我们最终将第k行翻转到了行相等，那么我们的目标就是找出其他行相等的行，而其他行相等的行要么全0要么全1，即要么与第k行完全一致，要么与第k行正好互补，这就是说找出初始状况下与第k行一致以及互补的行数，那么将第k行翻转到行相等之后就会有对应行数的行是相等的。

那么我们可以使用一个哈希表储存每一行以及其互补行出现的次数，其中次数的最大值就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxEqualRowsAfterFlips(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: int
        """

        m = len(matrix)
        row_dict = {}
        for index in range(m):
            s = ''
            t = ''
            for num in matrix[index]:
                if num == 0:
                    s += '1'
                    t += '0'
                else:
                    t += '1'
                    s += '0'
            
            if s in row_dict:
                row_dict[s] += 1
            elif t in row_dict:
                row_dict[t] += 1
            else:
                row_dict[s] = 1
        
        return max(row_dict.values())
```

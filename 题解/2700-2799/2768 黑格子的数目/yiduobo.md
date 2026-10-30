---
title: "2768. 黑格子的数目"
aliases: ["yiduobo的每日leetcode 2768.黑格子的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/655201435"
zhihu_id: "655201435"
zhihu_title: "yiduobo的每日leetcode 2768.黑格子的数目"
question_id: "2768"
question: "黑格子的数目"
problem_url: "https://leetcode.cn/problems/number-of-black-blocks/"
difficulty: "Medium"
created: "2023-09-09T03:26:04+08:00"
updated: "2023-09-09T03:26:04+08:00"
upvotes: 0
comments: 0
---

# 2768. 黑格子的数目

> **[yiduobo的每日leetcode 2768.黑格子的数目](https://zhuanlan.zhihu.com/p/655201435) · 知乎 · 2023-09-09 · 赞同 0**
> 力扣：[2768. 黑格子的数目](https://leetcode.cn/problems/number-of-black-blocks/) · Medium · 灵茶山艾府：[枚举](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2768.黑格子的数目

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/number-of-black-blocks/)

题目的网格规模非常大，不可能逐个枚举2\*2的网格，不过其中黑色格子的数目有限，那么就可以想办法计算出含有1、2、3、4个黑色格子的2 \* 2的网格的数量，然后用网格总数减去这些数得到全白2\*2网格的数量。

对于含有黑色格子的网格的计算，则可以从单个格子出发，分别处理这个网格是当前2\*2网格的左上角、右上角、左下角以及右下角这四种情况，统计这四种情况下对应网格中黑色格子的数量并更新答案。

需要注意的是，这种做法会产生大量重复。当处理的2\*2网格中存在两个黑色格子时，这两个黑色格子都会将当前这个2\*2网格计算一次，一共就计算了两次，样例2中的左上角2\*2网格就可以很好的说明这一点。

类似的，对于存在三个黑色格子的2\*2网格，将会被计算三次，而全黑的2\*2网格则会被计算四次。因此在遍历完所有黑色格子并计算完成后，需要将有两个黑色格子的网格数量除以二、三个黑色格子的网格数量除以、四个黑色格子的网格数量除以四。

最后附上python代码：

```python
class Solution(object):
    def countBlackBlocks(self, m, n, coordinates):
        """
        :type m: int
        :type n: int
        :type coordinates: List[List[int]]
        :rtype: List[int]
        """

        black_set = set()
        for x, y in coordinates:
            black_set.add((x, y))
        
        res = [0] * 5
        dx = [[1, 0, 1], [1, 0, 1], [-1, 0, -1], [-1, 0, -1]]
        dy = [[0, 1, 1], [0, -1, -1], [0, 1, 1], [0, -1, -1]]

        for x, y in coordinates:
            for d in range(4):
                cnt = 1
                flag = True
                for index in range(3):
                    xx = x + dx[d][index]
                    yy = y + dy[d][index]
                    if xx >= 0 and xx < m and yy >= 0 and yy < n:
                        if (xx, yy) in black_set:
                            cnt += 1
                    else:
                        flag = False
    
                if flag:
                    res[cnt] += 1

        
        res[2] /= 2
        res[3] /= 3
        res[4] /= 4
        res[0] = (m - 1) * (n - 1) - res[1] - res[2] - res[3] - res[4]
        return res
```

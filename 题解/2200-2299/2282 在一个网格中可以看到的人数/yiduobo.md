---
title: "2282. 在一个网格中可以看到的人数"
aliases: ["yiduobo的每日leetcode 2282.在一个网格中可以看到的人数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/629164812"
zhihu_id: "629164812"
zhihu_title: "yiduobo的每日leetcode 2282.在一个网格中可以看到的人数"
question_id: "2282"
question: "在一个网格中可以看到的人数"
problem_url: "https://leetcode.cn/problems/number-of-people-that-can-be-seen-in-a-grid/"
created: "2023-05-13T21:16:50+08:00"
updated: "2023-05-13T21:16:50+08:00"
upvotes: 0
comments: 0
---

# 2282. 在一个网格中可以看到的人数

> **[yiduobo的每日leetcode 2282.在一个网格中可以看到的人数](https://zhuanlan.zhihu.com/p/629164812) · 知乎 · 2023-05-13 · 赞同 0**
> 力扣：[2282. 在一个网格中可以看到的人数](https://leetcode.cn/problems/number-of-people-that-can-be-seen-in-a-grid/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2282.在一个网格中可以看到的人数

[力扣](https://leetcode.cn/problems/number-of-people-that-can-be-seen-in-a-grid/)

题目需要找出网格中每个位置能看到的右侧以及下方的人数，那么在这里可以先枚举每一行，求解单行中每个人能看到的右侧的人数，再枚举每一列，求解单列中每个人能看到的下方的人数。

由于求解的方式可以直接照搬，因此在这里不妨就考虑如何求解对于当行如何求解每个人能看到的右侧的人数。题目中关于能看到的定义为二人之间的其他人高度都小于这两个人的高度，那么对于行中第i个人以及第j个人，不妨设i \< j，那么当height[i] > height[j]时，在i左侧的所有人就不可能再看到j，理由是i左侧的所有人与j之间存在比j更高的i。

换言之，如果使用一个单调栈来维护当前可能被左侧的人看到的位置，就可以从右向左一趟遍历求解。对于当前遍历到的位置：

1、若当前的高度比栈顶位置的高度要高，那么说明当前位置可以看到栈顶位置，因此需要将当前位置能看到的人数加上1。另外，由于当前位置的高度更高，因此栈顶位置不可能再被当前位置左侧的位置看到，因此可以将其从栈中弹出。重复此过程直到栈为空或者当前高度比栈顶位置的高度要矮。

2、若栈非空，说明栈顶位置的高度比当前位置高度要高，因此当前位置无法看到栈中的其他位置，但是可以看到栈顶位置，因此需要再将当前位置能看到的人数加上1。

3、接下来，由于看到的条件是中间位置的高度严格更矮，因此若当前位置的高度与栈顶位置的高度相同，那么同样需要将栈顶弹出。重复此过程直到栈为空或者当前高度小于栈顶高度。值得一提的是，这一步不与步骤1合并的理由是步骤2中这个额外的1。

4、最后，将当前位置加入到栈中，然后继续向左处理。

最后附上python代码：

```python
class Solution(object):
    def seePeople(self, heights):
        """
        :type heights: List[List[int]]
        :rtype: List[List[int]]
        """

        m = len(heights)
        n = len(heights[0])
        res = [[0] * n for _ in range(m)]

        for i in range(m):
            stack = [n - 1]
            for j in range(n - 2, -1, -1):
                while stack and heights[i][stack[-1]] < heights[i][j]:
                    stack.pop()
                    res[i][j] += 1
                
                if stack:
                    res[i][j] += 1

                while stack and heights[i][stack[-1]] == heights[i][j]:
                    stack.pop()

                stack.append(j)

        for j in range(n):
            stack = [m - 1]
            for i in range(m - 2, -1, -1):
                while stack and heights[stack[-1]][j] < heights[i][j]:
                    stack.pop()
                    res[i][j] += 1
                
                if stack:
                    res[i][j] += 1
                
                while stack and heights[stack[-1]][j] == heights[i][j]:
                    stack.pop()
                
                stack.append(i)
        
        return res
```

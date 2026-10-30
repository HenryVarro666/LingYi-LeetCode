---
title: "1944. 队列中可以看到的人数"
aliases: ["yiduobo的每日leetcode 1944.队列中可以看到的人数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/monotonic-stack", "题单/单调栈", "题单/单调栈/一-单调栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/490418825"
zhihu_id: "490418825"
zhihu_title: "yiduobo的每日leetcode 1944.队列中可以看到的人数"
question_id: "1944"
question: "队列中可以看到的人数"
problem_url: "https://leetcode.cn/problems/number-of-visible-people-in-a-queue/"
difficulty: "Hard"
rating: 2105
created: "2022-03-30T18:47:51+08:00"
updated: "2022-03-30T18:47:51+08:00"
upvotes: 0
comments: 0
---

# 1944. 队列中可以看到的人数

> **[yiduobo的每日leetcode 1944.队列中可以看到的人数](https://zhuanlan.zhihu.com/p/490418825) · 知乎 · 2022-03-30 · 赞同 0**
> 力扣：[1944. 队列中可以看到的人数](https://leetcode.cn/problems/number-of-visible-people-in-a-queue/) · Hard · 灵茶山艾府：[单调栈的本质：及时去掉无用数据（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1944.队列中可以看到的人数

[力扣](https://leetcode-cn.com/problems/number-of-visible-people-in-a-queue/)

题目要找往右侧可以看到的人数，对于这类问题常规的做法就是从对应的那一侧开始一趟遍历，使用某种数据结构来储存可能被看到的候选集。

对于本题，有一个结论是对于队列中位置i和j的两个人，若i \< j，且heights[i] \< heights[j]，那么对于i之前的所有位置k，k都不可能再看到j，因为中间夹着一个i的高度大于j的高度，也就是说此时j已经没必要再保存在候选集里面了。

根据上面这个结论，那么很自然想到使用单调栈来维护可能被看到的候选集。从右向左一趟扫描，对于当前的index，若heights\[index\]比栈顶对应的高度heights\[stack\[-1\]\]要高，那么说明：

1、index可以看到栈顶的人，因此需要将答案加上1

2、栈顶的人不再可能被index之前的人看到了，因此需要将index弹出

重复这个过程直到栈为空或者index的高度小于栈顶对应的高度。若此时的栈不为空，那么index还可以看到此时栈顶的人，还需要再将答案加上1。

接下来，将index加入到栈中，然后继续向前考虑即可。

最后附上python代码：

```python
class Solution(object):
    def canSeePersonsCount(self, heights):
        """
        :type heights: List[int]
        :rtype: List[int]
        """

        n = len(heights)
        stack = [n - 1]

        res = [0]
        for index in range(n - 2, -1, -1):
            cnt = 0
            while stack and heights[index] > heights[stack[-1]]:
                stack.pop()
                cnt += 1
            
            if stack:
                cnt += 1
            res.append(cnt)
            stack.append(index)
        
        res.reverse()
        return res
```

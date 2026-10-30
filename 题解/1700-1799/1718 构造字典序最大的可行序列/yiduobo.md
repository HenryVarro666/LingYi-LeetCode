---
title: "1718. 构造字典序最大的可行序列"
aliases: ["yiduobo的每日leetcode 1718.构造字典序最大的可行序列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/450550319"
zhihu_id: "450550319"
zhihu_title: "yiduobo的每日leetcode 1718.构造字典序最大的可行序列"
question_id: "1718"
question: "构造字典序最大的可行序列"
problem_url: "https://leetcode.cn/problems/construct-the-lexicographically-largest-valid-sequence/"
created: "2021-12-27T22:23:46+08:00"
updated: "2021-12-27T22:23:46+08:00"
upvotes: 0
comments: 0
---

# 1718. 构造字典序最大的可行序列

> **[yiduobo的每日leetcode 1718.构造字典序最大的可行序列](https://zhuanlan.zhihu.com/p/450550319) · 知乎 · 2021-12-27 · 赞同 0**
> 力扣：[1718. 构造字典序最大的可行序列](https://leetcode.cn/problems/construct-the-lexicographically-largest-valid-sequence/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1718.构造字典序最大的可行序列

[力扣](https://leetcode-cn.com/problems/construct-the-lexicographically-largest-valid-sequence/)

构造可行序列是比较容易的事情。

很容易可以发现以[n, n - 2, n - 4, ..., n - 4, n - 2, n]这种形式开头的序列总是合法的，而最中间的部分在n为奇数时会剩下两个空位，即3 Y X 3这种形式，而对于n为偶数的情况会剩下一个空位，即2 X 2这种形式。此时可以将n - 1填到X的位置来跳出这个包围。

不过上面这个构造的方法不一定是字典序最大的，能构造出最大字典序的做法目前还没有想出来。好在本题的数据规模并不大，可以直接使用dfs搜索回溯。根据上面的结论，最终答案必然是以[n, n - 2]开头的，因此也算是在某种程度上进行了一点小小的优化。

具体实现上则是从头开始向后搜索每一个格子应该填什么数字。若当前格子是之前某次填充的闭合位置，那么就直接跳过，否则从大到小枚举当前剩下的数字并尝试填充。需要注意填充该数字之后对应的闭合位置不能越界，也不能已经被使用过。如果能成功完成填充，那么当前尝试的填充方法就是最终答案。

除此之外，还需要特别注意数字1是没有闭合位置的，需要特殊处理。

最后附上python代码：

```python
class Solution(object):
    def constructDistancedSequence(self, n):
        """
        :type n: int
        :rtype: List[int]
        """

        if n == 1:
            return [1]
        elif n == 2:
            return [2, 1, 2]
        else:
            res = [n, n - 2] + [0] * (n * 2 - 3)
            res[n] = n
            if n > 3:
                res[n - 1] = n - 2
            rest = set(range(n))
            rest.remove(n - 2)
            self.dfs(2, res, n, rest)
            return res
    
    def dfs(self, now, res, n, rest):
        if now == n * 2 - 1:
            return True
        
        if res[now]:
            return self.dfs(now + 1, res, n, rest)

        for num in range(n - 1, 1, -1):
            if num in rest and now + num < n * 2 - 1 and res[now + num] == 0:
                res[now] = res[now + num] = num
                rest.remove(num)
                if self.dfs(now + 1, res, n, rest):
                    return True
                rest.add(num)
                res[now] = res[now + num] = 0
        
        if 1 in rest:
            res[now] = 1
            rest.remove(1)
            if self.dfs(now + 1, res, n, rest):
                return True
            rest.add(1)
            res[now] = 0

        return False
```

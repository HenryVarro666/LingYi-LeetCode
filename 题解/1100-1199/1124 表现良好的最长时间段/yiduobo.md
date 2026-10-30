---
title: "1124. 表现良好的最长时间段"
aliases: ["yiduobo的每日leetcode 1124.表现良好的最长时间段"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/常用数据结构", "题单/单调栈", "题单/常用数据结构/一-前缀和", "题单/单调栈/一-单调栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/376141414"
zhihu_id: "376141414"
zhihu_title: "yiduobo的每日leetcode 1124.表现良好的最长时间段"
question_id: "1124"
question: "表现良好的最长时间段"
problem_url: "https://leetcode.cn/problems/longest-well-performing-interval/"
difficulty: "Medium"
rating: 1908
created: "2021-05-28T21:19:55+08:00"
updated: "2021-05-28T21:19:55+08:00"
upvotes: 0
comments: 0
---

# 1124. 表现良好的最长时间段

> **[yiduobo的每日leetcode 1124.表现良好的最长时间段](https://zhuanlan.zhihu.com/p/376141414) · 知乎 · 2021-05-28 · 赞同 0**
> 力扣：[1124. 表现良好的最长时间段](https://leetcode.cn/problems/longest-well-performing-interval/) · Medium · 灵茶山艾府：[两种做法，两张图秒懂！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

因为1123题与之前的865题重复，在这里就跳过了。

1124.表现良好的最长时间段

[力扣](https://leetcode-cn.com/problems/longest-well-performing-interval/)

这题目描述也是很妙了。

题目中虽然给出了具体的小时数，但是实际上我们只关心其是否大于8，因此转化之后题目就变成了给出一串由1和-1组成的数组，问子段和大于0的最长子段的长度。

对于子段和相关的问题，很自然就想到使用前缀和。我们求这个数组的前缀和，那么问题就进一步转化成了给出一个数组s，需要找出一组下标对(i, j)，其满足s[i] \< s[j]且i和j之间的距离最远。对于这个问题，我们可以发现在左边界i这一侧存在单调性。

不妨设存在i和k满足i \< k，且s[i] \< s[k]，那么此时若存在某个j满足j > k且s[j] > s[k]，那么必然就有s[j] > s[k] > s[i]，且j > k > i，那么由(k, j)组成的答案显然不如(i, j)组成的答案，因此位置k就不应该成为左边界的备选答案。

根据这一点，我们就一趟扫描，维护一个单调栈来保存所有可能成为左边界的下标。

接下来我们从末尾开始向前扫描，枚举答案的右边界index。若此时的栈顶元素(stack\[-1\], index)满足s\[index\] > s\[stack\[-1\]\]，那么说明以栈顶元素stack\[-1\]为左边界的最优右边界就是index，那么此时应该使用stack\[-1\]与index更新答案，同时弹出栈顶元素，直到stack\[-1\] >\= s\[index\]或者栈为空。

需要注意的是，有一种特殊情况是左边界为0，那么此时只需要s[index]大于0，就可以使用(0, index)来更新答案了。这种特殊情况也可以放在计算左边界的栈时处理。

最后附上python代码：

```python
class Solution(object):
    def longestWPI(self, hours):
        """
        :type hours: List[int]
        :rtype: int
        """

        s = [1 if hours[0] > 8 else -1]
        for hour in hours[1:]:
            s.append(s[-1])
            if hour > 8:
                s[-1] += 1
            else:
                s[-1] -= 1
        
        stack = []
        res = 0
        for index in range(len(s)):
            if not stack or s[stack[-1]] > s[index]:
                stack.append(index)
            if s[index] > 0:
                res = max(res, index + 1)

        for index in range(len(s) - 1, -1, -1):
            while stack and s[index] > s[stack[-1]]:
                p = stack.pop()
                if p < index:
                    res = max(res, index - p)
            if not stack:
                break
        
        return res
```

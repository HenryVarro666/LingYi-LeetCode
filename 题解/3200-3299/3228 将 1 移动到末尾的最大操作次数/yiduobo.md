---
title: "3228. 将1移动到末尾的最大操作次数"
aliases: ["yiduobo的每日leetcode 3228.将1移动到末尾的最大操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/720054327"
zhihu_id: "720054327"
zhihu_title: "yiduobo的每日leetcode 3228.将1移动到末尾的最大操作次数"
question_id: "3228"
question: "将 1 移动到末尾的最大操作次数"
problem_url: "https://leetcode.cn/problems/maximum-number-of-operations-to-move-ones-to-the-end/"
difficulty: "Medium"
rating: 1593
created: "2024-09-13T23:18:50+08:00"
updated: "2024-09-13T23:18:50+08:00"
upvotes: 2
comments: 0
---

# 3228. 将1移动到末尾的最大操作次数

> **[yiduobo的每日leetcode 3228.将1移动到末尾的最大操作次数](https://zhuanlan.zhihu.com/p/720054327) · 知乎 · 2024-09-13 · 赞同 2**
> 力扣：[3228. 将 1 移动到末尾的最大操作次数](https://leetcode.cn/problems/maximum-number-of-operations-to-move-ones-to-the-end/) · Medium · 灵茶山艾府：[堵车模型（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3228.将1移动到末尾的最大操作次数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-number-of-operations-to-move-ones-to-the-end/description/)

题目给出一个由0和1构成的字符串，对于字符串中的某个1，若其右侧为0，那么就可以执行一次操作，将这个1移动到其右侧最近的1左边，若其右侧没有1，则将其移动到字符串的末尾。问最多能执行多少次操作。

通过样例可以发现，最终字符串必然是前0后1的形式，而题目要求执行操作的次数最多，也就是说应该尽量避免一步到位的操作。换言之，在这里应该先执行字符串头部的操作而不是尾部的操作。

从动态规划的角度来理解，如果某个1与其右侧最近的1相邻，那么当前的1可移动的次数就等于其右侧的1可移动的次数，否则当前的1可移动的次数等于其右侧的1可移动的次数加上1。

对于后面这种情况，即当前1与右侧的1不相邻时，如果先移动右侧的1，就相当于当前1的可移动次数少了1次，明显是不优的，所以需要按照从头到尾的顺序来移动这些1。

根据这个结论，就可以从头开始向后一趟遍历，若当前遍历到的字符为1，且左侧的字符为0，那么就可以将应该将当前字符左侧所有的1都移动过来。令cnt表示当前字符左侧1的数量，那么对于上面这种情况，就可以执行cnt次操作，需要将cnt累加到答案。另外若当前字符为1，则需要更新cnt。

需要注意的是，上面的算法无法处理字符串最后一个字符为0时将所有的1移动到字符串末尾的情况。此时就需要在字符串末尾额外添加一个1，这样一来就可以形成最后这一组01来移动前面所有的1。另外如果字符串最后一个字符一开始就是1的话，额外添加一个1也不会影响最终结果。

最后附上python代码：

```python
class Solution(object):
    def maxOperations(self, s):
        """
        :type s: str
        :rtype: int
        """

        cnt = 0
        res = 0
        s += '1'
        for index in range(len(s)):
            if s[index] == '1' and index > 0 and s[index - 1] == '0':
                res += cnt
            if s[index] == '1':
                cnt += 1
            
        return res
```

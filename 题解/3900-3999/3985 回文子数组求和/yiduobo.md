---
title: "3985. 回文子数组求和"
aliases: ["yiduobo的每日leetcode 3985.回文子数组求和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/prefix-sum", "leetcode/string-matching", "题单/字符串", "题单/字符串/三-Manacher-算法-回文串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2057230355514516338"
zhihu_id: "2057230355514516338"
zhihu_title: "yiduobo的每日leetcode 3985.回文子数组求和"
question_id: "3985"
question: "回文子数组求和"
problem_url: "https://leetcode.cn/problems/palindromic-subarray-sum/"
difficulty: "Hard"
rating: 2202
created: "2026-07-08T21:45:22+08:00"
updated: "2026-07-08T21:45:22+08:00"
upvotes: 3
comments: 0
---

# 3985. 回文子数组求和

> **[yiduobo的每日leetcode 3985.回文子数组求和](https://zhuanlan.zhihu.com/p/2057230355514516338) · 知乎 · 2026-07-08 · 赞同 3**
> 力扣：[3985. 回文子数组求和](https://leetcode.cn/problems/palindromic-subarray-sum/) · Hard · 灵茶山艾府：[【模板】Manacher 算法 + 前缀和（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3985.回文子数组求和

<https://leetcode.cn/problems/palindromic-subarray-sum/>

题目给出一个正整数数组nums。

现在要求找出nums中的一个回文子数组，这个子数组的元素和最大。

由于nums中都是正整数，且题目的目标是使得回文子数组的元素和最大，那么当确定了回文子数组的中心后，就应该让这个子数组的回文半径尽可能大，于是问题就变成了枚举回文中心，计算对应的最大回文半径的问题。

对于这个问题，可以使用马拉车算法解决。

使用一个数组f维护每个位置的回文半径，同时使用两个变量right和mid，分别表示当前扩招到的最右侧的回文边界，以及对应的回文中心。

接下来一趟遍历，对于当前遍历到的index：

若index \< right，那么就可以想办法利用之前已知的回文信息来初始化index对应的回文半径。具体来说，对于当前的index，从index - (right - index)到index这一段以index为中心，right - index为半径的子数组，将会和以mid - (index - mid)为中心的子数组关于mid对称。这是因为mid是一个大回文子数组的中心，两端的部分关于mid对称。

基于已经计算好的f，可以知道以mid - (index - mid)为中心的回文半径为f[mid - (index - mid)]，那么就可以通过这个值初始化f[index]，理由是回文子数组关于mid中心对称后还是还是回文子数组。但是需要注意的是，因为基于mid的对称只能在不超出right的范围内成立，因此在这里不能直接初始化f[index]为f[mid - (index - mid))]，而是需要与right - index取较小值作为f[index]的初始值。

反之，若index >\= right，那么就前面的f就没有参考意义了，只能初始化f[index]为1。

接下来，在不超出边界的前提下，尝试从f[index]开始向两侧扩展，计算以index为中心的最大回文半径。

计算完成得到f[index]后，若f[index] + index超过了当前的right，则更新right和mid为f[index] + index以及index。

这样一来，就可以在O(n)的时间内计算得到以每个元素为回文中心的最长回文半径了。需要注意的是，由于可能出现2112这种偶数中心的情况，在这里可以在原数组相邻的元素之间插入0，这样一来就可以解决偶数中心的情况，同时又不会影响到子数组的和。另外为了方便处理边界情况，可以在数组的两侧分别插入-1和-2，这样做的好处是不会形成不必要的回文，同时向两侧扩展时会自然在负数的位置停下保证不会越界。

得到每个位置对应的回文半径后，剩下的就是计算子数组的和了。在这里依然是转化为前缀和进行求解，令s为nums的前缀和，那么对于回文中心index，若其最大回文半径为f\[index\]，那么对应的子数组和就是s\[index + f\[index\] - 1\] - s\[index - f\[index\]\]。

在具体实现上，可以先改造nums，然后计算前缀和数组s，最后在执行马拉车算法的过程中同步计算对应的子数组和并更新答案。

最后附上python代码：

```
class Solution(object):
    def getSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        f = [-1]
        for v in nums:
            f.append(v)
            f.append(0)
        f[-1] = -2

        s = [0]
        for v in f[1:]:
            s.append(s[-1] + v)
        
        mid = 0
        right = 0
        r = [0]
        res = 0
        for index in range(1, len(f) - 1):
            if index < right:
                r.append(min(right - index, r[mid * 2 - index]))
            else:
                r.append(1)

            while f[index - r[index]] == f[index + r[index]]:
                r[index] += 1

            res = max(res, s[index + r[index] - 1] - s[index - r[index]])

            if right < index + r[index]:
                mid = index
                right = index + r[index]

        return res
```

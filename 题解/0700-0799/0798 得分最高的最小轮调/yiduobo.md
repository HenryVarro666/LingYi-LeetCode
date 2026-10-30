---
title: "798. 得分最高的最小轮调"
aliases: ["yiduobo的每日leetcode 798.得分最高的最小轮调"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/常用数据结构", "题单/常用数据结构/二-差分"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/342403745"
zhihu_id: "342403745"
zhihu_title: "yiduobo的每日leetcode 798.得分最高的最小轮调"
question_id: "798"
question: "得分最高的最小轮调"
problem_url: "https://leetcode.cn/problems/smallest-rotation-with-highest-score/"
difficulty: "Hard"
rating: 2130
created: "2021-01-06T21:55:19+08:00"
updated: "2021-01-06T21:55:19+08:00"
upvotes: 1
comments: 0
---

# 798. 得分最高的最小轮调

> **[yiduobo的每日leetcode 798.得分最高的最小轮调](https://zhuanlan.zhihu.com/p/342403745) · 知乎 · 2021-01-06 · 赞同 1**
> 力扣：[798. 得分最高的最小轮调](https://leetcode.cn/problems/smallest-rotation-with-highest-score/) · Hard · 灵茶山艾府：[差分数组（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

798.得分最高的最小轮调

[力扣](https://leetcode-cn.com/problems/smallest-rotation-with-highest-score/)

题目给出一个数组，可以对这个数组进行向左的旋转操作，需要旋转之后的得分最大。

首先，这里旋转的次数必然在0到n - 1之间，因为旋转n次与旋转0次时一样的。

接下来对于数组中的某个数A[index]，可以分为两种情况：

1、A[index] \<\= index：

此时设delta \= index - A[index]，那么在旋转0到delta次之后，A[index]都是可以得分的。另外，也可将A[index]旋转到数组的后面，也是可以得分的，此时可行的旋转次数区间则为index + 1到n - 1。

2、A[index] > index：

此时就只能将A[index]旋转到数组的后面了。首先选择index + 1次可以让A[index]位于n - 1这个位置，而可以得分的位置为A[index] + 1到n - 1，因此在这里可行的旋转次数区间为index + 1到index + 1 + (n - 1 - (A[index] + 1) + 1) \= index + n - A[index]之间。

于是现在问题就变成了给出若干段区间，问这些区间最多会重叠多少次。一般来说这种问题可以使用动态区间相关的数据结构来解决，但是注意到这里的区间重叠次数，实际上相当于对区间中所有的数加一，那么可以反过来利用前缀和的思想，使用差分系统来处理。

例如区间2到4，我们将f[2]加上1，将f[5]减去1，那么我们计算前缀和s的时候，就有

f \= 0, 0, 1, 0, 0, -1, ...

s \= 0, 0, 1, 1, 1, 0, ...

可以发现这里的区间2到4就已经体现在s的当中的。

这样一来，对于本题，就可以针对A[index]的两种情况来修改f的值：

1、A[index] \<\= index：

此时有两段区间\[0, index - A\[index\]\]以及\[index + 1, n - 1\]，那么我们将

f[0]、f[index+ 1]加上1，将f[index - A[index] + 1]、f[n]减去1。

2、A[index] > index:

此时只有一段区间\[index + 1, index + n - A\[index\]\]，那么我们将f\[index + 1\]加上1，将f\[index + n - A\[index\] + 1\]\]减去1。

得到f数组之后，从头开始遍历计算前缀和，最大的前缀和对应的下标即为最终的答案。

例如样例一中的[2, 3, 1, 4, 0]：

1、对于A[0] \= 2，有A[0] > 0，因此合法区间为[1, 3]，此时应该将f[1]加上1，将f[4]减去1，得到f为[0, 1, 0, 0, -1, 0]

2、对于A[1] \= 3，有A[1] > 1，因此合法区间为[2, 3]，此时应该将f[2]加上1，将f[4]减去1，得到f为[0, 1, 1, 0, -2, 0]

3、对于A[2] \= 1，有A[2] \<\= 2，因此有两个合法区间，分别为[0, 1]以及[3, 4]，此时应该将f[0]以及f[3]加上1，将f[2]以及f[5]减去1，得到f为[1, 1, 0, 1, -2, -1]

4、对于A[3] \= 4，有A[3] > 3，因此合法区间为[4, 4]，此时应该将f[4]加上1，将f[5]减去1，得到f为[1, 1, 0, 1, -1, -2]

5、对于A[4] \= 0，有A[4] \<\= 4，因此有两个合法区间，但是移动到末尾表示的这一段区间[5, 4]是没有意义的区间，那么实际上就只有一段区间[0, 4]，此时应该将f[0]加上1，将f[5]减去1，得到f为[2, 1, 0, 1, -1, -3]

接下来，求解f的前缀和，得到s为[2, 3, 3, 4, 3, 0]，其中最大值为4，因此答案就是其对应的下标3。

最后附上python代码：

```python
class Solution(object):
    def bestRotation(self, A):
        """
        :type A: List[int]
        :rtype: int
        """

        n = len(A)
        cnt = [0] * (n + 1)

        for index, num in enumerate(A):
            if index >= num:
                delta = index - num
                cnt[0] += 1
                cnt[delta + 1] -= 1
            else:
                cnt[index + 1 + n - num] -= 1
            cnt[index + 1] += 1
        
        s = now = cnt[0]
        res = 0
        for index in range(1, len(cnt)):
            now += cnt[index]
            if now > s:
                s = now
                res = index
        
        return res
```

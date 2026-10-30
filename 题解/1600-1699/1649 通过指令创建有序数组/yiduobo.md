---
title: "1649. 通过指令创建有序数组"
aliases: ["yiduobo的每日leetcode 1649.通过指令创建有序数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/440608503"
zhihu_id: "440608503"
zhihu_title: "yiduobo的每日leetcode 1649.通过指令创建有序数组"
question_id: "1649"
question: "通过指令创建有序数组"
problem_url: "https://leetcode.cn/problems/create-sorted-array-through-instructions/"
created: "2021-12-02T23:57:14+08:00"
updated: "2021-12-02T23:57:14+08:00"
upvotes: 1
comments: 0
---

# 1649. 通过指令创建有序数组

> **[yiduobo的每日leetcode 1649.通过指令创建有序数组](https://zhuanlan.zhihu.com/p/440608503) · 知乎 · 2021-12-02 · 赞同 1**
> 力扣：[1649. 通过指令创建有序数组](https://leetcode.cn/problems/create-sorted-array-through-instructions/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1649.通过指令创建有序数组

[力扣](https://leetcode-cn.com/problems/create-sorted-array-through-instructions/)

题目给出一个数组，问对于每个数而言其前面有多少个数大于这个数，又有多少个数小于这个数。这是一个很典型的动态区间最大最小值问题，通常来说需要用到线段树之类的东西。

不过注意到有一个隐藏条件就是，对于当前处理的数num，不妨设这个数是数组中的第k个数，那么其前方一共就有k - 1个数。这些数可以分成三个部分，分别是大于num的，小于num的，以及等于num的。显然，在这里等于num的数是最容易求的，直接使用一个哈希表记录当前num之前出现过的num数量就好了。而对于题目要求的大于num和小于num的，实际上可以只求其中的某一种，而另一种则可以用k - 1减去等于num的数，再减去求出来的这一种得到。由于只需要求其中一侧，那么结合最容易实现的树状数组来考虑的话，显然就应该求小于num的数有多少个，于是现在就有了一种做法。

一趟遍历，对于当前数组中第index个数num，首先通过树状数组求出在index之前小于等于num - 1的数有多少个，记为smaller。另外，通过一个哈希表记录在index之前出现过多少个num，记为same，那么大于num的数bigger就等于index - same - smaller。使用bigger和smaller中的较小值更新答案，然后使用num更新树状数组即可。

最后附上python代码：

```python
class Solution(object):
    def createSortedArray(self, instructions):
        """
        :type instructions: List[int]
        :rtype: int
        """

        index_array = [0] * 100001
        cnt_dict = {}
        res = 0
        mod = 10 ** 9 + 7
        for index, num in enumerate(instructions):
            tmp = num - 1
            smaller = 0
            while tmp > 0:
                smaller += index_array[tmp]
                tmp -= tmp & -tmp
            
            same = cnt_dict.get(num, 0)
            bigger = index - same - smaller
            res += min(smaller, bigger)
            if res >= mod:
                res -= mod

            cnt_dict[num] = same + 1
            tmp = num
            while tmp <= 100001:
                index_array[tmp] += 1
                tmp += tmp & -tmp

        return res
```

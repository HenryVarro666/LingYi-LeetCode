---
title: "2790. 长度递增组的最大数目"
aliases: ["yiduobo的每日leetcode 2790.长度递增组的最大数目"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/656831262"
zhihu_id: "656831262"
zhihu_title: "yiduobo的每日leetcode 2790.长度递增组的最大数目"
question_id: "2790"
question: "长度递增组的最大数目"
problem_url: "https://leetcode.cn/problems/maximum-number-of-groups-with-increasing-length/"
created: "2023-09-18T05:43:59+08:00"
updated: "2023-09-18T05:43:59+08:00"
upvotes: 0
comments: 0
---

# 2790. 长度递增组的最大数目

> **[yiduobo的每日leetcode 2790.长度递增组的最大数目](https://zhuanlan.zhihu.com/p/656831262) · 知乎 · 2023-09-18 · 赞同 0**
> 力扣：[2790. 长度递增组的最大数目](https://leetcode.cn/problems/maximum-number-of-groups-with-increasing-length/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2790.长度递增组的最大数目

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/maximum-number-of-groups-with-increasing-length/description/)

由于题目中每组的数字不能出现重复，比较理想的构造方法就是构造出形如下面三角形的组

...

a[2] ...

a[1] a[2] ...

a[0] a[1] a[2] ...

那么一个自然的想法就是先将数组按照出现次数从小到大进行排序。但是可能会出现一个问题，就是斜线上的数字数量不够。例如理想中的a[1]需要有两个，但是数组中排序后第二小的数只有一个，此时就需要使用更大的数来填充，例如

...

a[2] ...

a[2] a[3] ...

a[0] a[1] a[2] ...

此时相当于从下往上数第二层的a[2]往前挤了一轮

另一方面，填充当前斜线的数可能多余，此时则可以使用这些数来尝试帮助填充下一轮，例如

...

a[1] ...

a[1] a[2] ...

a[0] a[1] a[2] ...

此时相当于从下往上数第三层的a[2]往后挤了一轮

对于前面这种情况没有什么太多需要注意的，就是统计现在的数字个数是否足够构成下一组斜线，而对于后面这种情况，则可能存在某个数a[p]的数量大于最终组数k的情况，此时a[p]可用的最大数量只能是k个，但是计算组数的时候是计算的所有可用数字的总数，这二者之间可能存在偏差。

但是实际上，由于次数以及按照从小到大的顺序排序好了，因此从a[p + 1]到a[k - 1]这些数出现的次数都大于等于a[p]出现的次数，可以使用这些数来填充外侧的斜线。此时就只需保证鸽笼原理得到的上限，也就是a[p]在a[0]到a[p - 1]构成的组的基础上最多只能新增一组，就可以保证a[p]不会被重复使用。

下面给出证明：

不妨设当前的a[0]到a[p - 1]可以构成的最大组数为m，这也意味着a[0]到a[p - 1]这些数不能再额外构造一条长度为m + 1的斜线，要么是数字的数量不足，要么是可能出现重复。

接下来对于新来的a[p]：

1、若a[p]的数量与之前剩余数字的数量之和大于等于m + 1，那么一定可以构造出长度为m + 1的斜线：

1-1）若a[p]自身的数量足够，那么全部用a[p]填充就行了

1-2）若a[p]的数量不足，那么需要借助部分之前的剩余数组来帮忙构造。此时可能出现的情况是剩余数组在构造新斜线的过程中，与老的组出现了重复。一旦重复出现，说明这个数字初始的可用次数已经大于等于m + 1，而a[p]可用的数量必然大于等于这个数字可用的次数，这也就意味着a[p]的数量其实是充足的，产生了矛盾

2、若a[p]的数量与之前剩余数字的数量之和大于等于(m + 1) + (m + 2)，那么依然无法新构造出长度为m + 1和m + 2的斜线：

2-1）若充分使用了a[p]，此时a[p]使用了m + 2次，那么将a[p]交换到最外侧，相当于a[p]全权负责最外侧的斜线，此时的问题又变成了a[0]到a[p - 1]来填充m + 1的这条斜线，从初始的假设来看，这些数无法构造长度为m + 1的斜线

2-2）若没有充分使用a[p]，那么同样是将a[p]交换到最外侧，此时除了要使用a[0]到a[p - 1]来构造m + 1的斜线外，还有额外的位置需要填充，更加不可能实现

综合一起就得到结论，每次只需将新来的a[p]的数量加入到剩余可用数字的统计值中，若这些数字的量足够构成新的斜线，那么就进行构造。

具体实现上，将usageLimits从小到大排序，使用一个变量now统计空闲的数字的个数，初始化usageLimits[0] - 1并初始化答案res也为1。接下来从1开始向后遍历，每次将now加上当前usageLimits[i]，然后判断当前的now是否足够大于等于res + 1，也就是构造长度为res + 1的斜线。若足够，那么将now减去res + 1，同时将res加上1。

最后附上python代码：

```python
class Solution(object):
    def maxIncreasingGroups(self, usageLimits):
        """
        :type usageLimits: List[int]
        :rtype: int
        """

        usageLimits.sort()
        now = usageLimits[0] - 1
        res = 1
        for index in range(1, len(usageLimits)):
            now += usageLimits[index]
            if now >= res + 1:
                now -= res + 1
                res += 1
            
        return res
```

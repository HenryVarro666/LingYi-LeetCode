---
title: "3937. 使数组变为模交替数组的最少操作次数I & 3944. 使数组变为模交替数组的最少操作次数II"
aliases: ["yiduobo的每日leetcode 3937.使数组变为模交替数组的最少操作次数I && 3944.使数组变为模交替数组的最少操作次数II", "3937. 使数组变为模交替数组的最少操作次数I", "3944. 使数组变为模交替数组的最少操作次数II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/math", "leetcode/binary-search", "leetcode/number-theory", "leetcode/prefix-sum", "leetcode/sorting", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/一-前缀和", "题单/贪心算法/四-数学贪心", "leetcode/hard"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2043109030969730035"
zhihu_id: "2043109030969730035"
zhihu_title: "yiduobo的每日leetcode 3937.使数组变为模交替数组的最少操作次数I && 3944.使数组变为模交替数组的最少操作次数II"
question_id: ["3937", "3944"]
question: ["使数组变为模交替数组的最少操作次数 I", "使数组变为模交替数组的最少操作次数 II"]
problem_url: ["https://leetcode.cn/problems/minimum-operations-to-make-array-modulo-alternating-i/", "https://leetcode.cn/problems/minimum-operations-to-make-array-modulo-alternating-ii/"]
difficulty: ["Medium", "Hard"]
created: "2026-05-27T23:48:05+08:00"
updated: "2026-05-27T23:48:06+08:00"
upvotes: 1
comments: 0
---

# 3937. 使数组变为模交替数组的最少操作次数I & 3944. 使数组变为模交替数组的最少操作次数II

> **[yiduobo的每日leetcode 3937.使数组变为模交替数组的最少操作次数I && 3944.使数组变为模交替数组的最少操作次数II](https://zhuanlan.zhihu.com/p/2043109030969730035) · 知乎 · 2026-05-27 · 赞同 1**
> 力扣：[3937. 使数组变为模交替数组的最少操作次数 I](https://leetcode.cn/problems/minimum-operations-to-make-array-modulo-alternating-i/) · Medium · 灵茶山艾府：[两种方法：枚举 / 贪心+维护最小次小（Python/Java/C++/Go）](../3937%20使数组变为模交替数组的最少操作次数%20I/灵茶山艾府.md)
> 力扣：[3944. 使数组变为模交替数组的最少操作次数 II](https://leetcode.cn/problems/minimum-operations-to-make-array-modulo-alternating-ii/) · Hard · 灵茶山艾府：[贪心+维护最小次小，O(nlogn) 时间（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3937.使数组变为模交替数组的最少操作次数I

<https://leetcode.cn/problems/minimum-operations-to-make-array-modulo-alternating-i/description/>

3944.使数组变为模交替数组的最少操作次数II

<https://leetcode.cn/problems/minimum-operations-to-make-array-modulo-alternating-ii/>

题目给出一个整数数组nums以及一个整数k。

在一步操作中，可以将nums中的任意元素增加或者减少1。

若存在两个不同的整数x和y，使得nums中所有的偶数下标index都满足nums[index] % k \=\= x，且所有奇数下标index都满足nums[index] % k \=\= y，那么就称数组是模交替的。

问使得nums变为模交替数组所需的最少操作次数。

两题的题设一致，第二题的数据规模较大，nums的长度与k的大小可达10^5。

首先，由于题目中需要关注的是对k取模后的结果，且只需要分奇偶，对具体的下标位置并不做要求，因此在这里就可以先将nums中所有元素对k取模，然后按奇偶下标分为两个数组even以及odd，并将这两个数组排序。

接下来的问题就可以认为是对于一条环形公路，上面有若干点，找出最优与次优的两个位置，使得所有点到这两个位置的距离之和最小/次小。

需要注意，这里说的是两个位置而不是两点，是因为最优解必然处于某个已有的点上，但是次优解不一定。例如k \= 100，even \= [1, 4, 7]这种情况，最优解位于4是很明显的，而次优解并不位于1或者7，而是位于3或者5。基于这一点，需要在计算得到最优解之后，再额外计算次优解。

我在这里采用的是更为暴力的手段：直接枚举0到k - 1作为目标点，计算所有点到目标点的距离之和，然后取最优和次优。

基于题目的数据规模，直接暴力计算显然是不行的。由于even和odd是等价的，在这里以even的计算方法来进行说明。

由于已经将even排好了序，那么对于目标点t，整个even可以分为4段：

- 最左侧的一段：这一段的元素，需要通过减法套圈，也就是不断减1直到变为0，在模k的意义下就相当于k，然后套个圈从k - 1下降到t
- 中间靠左这一段：这一段的元素，直接通过加法变为t
- 中间靠右这一段：这一段的元素，直接通过减法变为t
- 最右侧的一端：这一段 元素，需要通过加法套团，也就是不断加1直到变为k，在模k的意义下就相当于0，然后套个圈从0上升到t

不妨设这四段的分界点分别为p、index、q，那么基于even是有序的这个前提条件，p、index、q都应该随着t的增加而向右移动，也就是说，维护p、index、q的时间复杂度是均摊O(1)的。

理解起来也非常直观。

首先，随着t的增大，index作为中间直接增减这一段的分割点，就相当于even[index]及左侧的元素小于等于t，右侧的元素大于t，因此index显然是随着t单调不减的。

接下来，随着t的增大，通过0套圈后下降到t这个操作中，需要下降的步数也跟着变少了，而反过来，直接通过增大自身变为t的代价就变多了，也就是说，第二段中的部分元素，改成变为0然后下降到t此时是更划算的。另一方面，随着p的增大，变为0的代价在上升，而直接通过增大自身变为t的代价在下降，因此到某个临界点后，变为0就不划算了，因此p在这里是随着t单调不减的。

同样的，随着t的增大，最后一段元素的数量也跟着减小，而代价的对比也符合单调性，因此q也是单调不减的。

那么对于当前的t，计算得到p、index、q之后，就可以计算总的代价了:

1、第一段：

其代价是将even[0]到even[p - 1]都变为0，然后再变为t的代价，也就是

even[0] + even[1] + ... + even[p - 1] + (k - t) \* p

前面这一段显然可以用前缀和来优化。记s为even的前缀和，另外规定s[0] \= 0方便计算，那么在这里代价就是

s[p] + (k - t) \* p

2、第二段：

其代价是将even[p]到even[index - 1]直接通过加1操作变为t，也就是

(t - even[p]) + (t - even[p + 1]) + ... + (t - even[index - 1])

拆开括号后就是

t \* (index - p) - (even[p] + even[p + 1] + ... + even[index - 1]) \= t \* (index - p) - (s[index] - s[p])

3、第三段：

其代价是将even[index]到even[q - 1]直接通过减1操作变为t，也就是

(even[index] - t) + (even[index + 1] - t) + ... + (even[q - 1] - t)

拆开括号后就是

even[index] + even[index + 1] + ... + even[q - 1] - t \* (q - index) \= s[q] - s[index] - t \* (q - index)

4、第四段：

其代价是将even[q]到even[n - 1]都变为k，然后再变为t的代价，也就是

(k - even[q]) + (k - even[q + 1]) + ... + (k - even[n - 1]) + t \* (n - q)

拆开括号后就是

(k + t) \* (n - q) - even[q] - even[q + 1] - ... - even[n - 1] \= (k + t) \* (n - q) - (s[-1] - s[q])

将四段的代价累加起来，即为选取t作为目标点的代价之和c。

对于0到k - 1之间的所有t，计算出对应的c，然后取最小与次小记录下来。

对even和odd分别计算后，将得到even对应的两组最优决策点与最优代价et1、ec1、et2、ec2，以及odd对应的ot1、oc1、ot2、oc2。接下来，若et1和ot1不同，那么两边都可以取到最优，此时的答案就是ec1 + oc1，否则的话有一边必须取次优，此时的答案就是min(ec1 + oc2, ec2 + oc1)。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        r = [v % k for v in nums]
        odd = []
        even = []
        for index, v in enumerate(r):
            if index % 2 == 0:
                even.append(v)
            else:
                odd.append(v)

        even.sort()
        odd.sort()

        def calc(nums):
            if not nums:
                return None, 0, None, None

            s = [0]
            for v in nums:
                s.append(s[-1] + v)

            n = len(nums)
            index = 0
            p = 0
            q = 0
            c1, t1, c2, t2 = None, None, None, None
            for t in range(k):
                while index < n and nums[index] <= t:
                    index += 1

                while p < index and t - nums[p] > nums[p] + k - t:
                    p += 1

                if q < index:
                    q = index
                while q < n and nums[q] - t < k - nums[q] + t:
                    q += 1

                c = s[p] + (k - t) * p
                c += t * (index - p) - (s[index] - s[p])
                c += s[q] - s[index] - t * (q - index)
                c += (n - q) * (k + t) - (s[-1] - s[q])

                if c1 is None or c < c1:
                    t1, c1, t2, c2 = t, c, t1, c1
                elif c2 is None or c < c2:
                    t2, c2 = t, c
            
            return t1, c1, t2, c2

        et1, ec1, et2, ec2 = calc(even)
        ot1, oc1, ot2, oc2 = calc(odd)

        if et1 != ot1:
            return ec1 + oc1
        
        return min(ec1 + oc2, ec2 + oc1)
```

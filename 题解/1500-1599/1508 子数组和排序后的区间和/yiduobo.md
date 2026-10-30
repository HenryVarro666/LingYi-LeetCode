---
title: "1508. 子数组和排序后的区间和"
aliases: ["yiduobo的每日leetcode 1508.子数组和排序后的区间和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/419890130"
zhihu_id: "419890130"
zhihu_title: "yiduobo的每日leetcode 1508.子数组和排序后的区间和"
question_id: "1508"
question: "子数组和排序后的区间和"
problem_url: "https://leetcode.cn/problems/range-sum-of-sorted-subarray-sums/"
created: "2021-10-10T19:53:22+08:00"
updated: "2021-10-10T19:53:22+08:00"
upvotes: 0
comments: 0
---

# 1508. 子数组和排序后的区间和

> **[yiduobo的每日leetcode 1508.子数组和排序后的区间和](https://zhuanlan.zhihu.com/p/419890130) · 知乎 · 2021-10-10 · 赞同 0**
> 力扣：[1508. 子数组和排序后的区间和](https://leetcode.cn/problems/range-sum-of-sorted-subarray-sums/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1508.子数组和排序后的区间和

[力扣](https://leetcode-cn.com/problems/range-sum-of-sorted-subarray-sums/)

由于问题的规模并不大，那么直接求解出所有的子数组和并排序，然后求解区间和也是可行的做法。这个做法的时间复杂度为O(n^2 \* log(n))

不过注意到这里数组中的数都是正数，那么这些子数组和之间就具有某些性质。

对于起点相同的子数组而言，终点越靠后的子数组和就越大。而对于终点相同的子数组而言，则是起点越靠前的子数组和就越大。为了体现这两个性质，不妨将所有子数组和按同样起点为同一行，同样终点为同一列进行排布，那么就能得到如下的矩阵m。为了方便表示，这里将原始数组nums写作数组a。

| a[0] | a[0]+a[1] | a[0]+a[1]+a[2] | ... | sum(a[0 : n]) |
| --- | --- | --- | --- | --- |
|  | a[1] | a[1] + a[2] | ... | sum(a[1 : n]) |
|  |  | a[2] | ... | sum(a[2 : n]) |
|  |  |  | ... | ... |
|  |  |  |  | a[n - 1] |

也就是对同一行的m[i][p]和m[i][q]而言，当p \< q时必然有m[i][p] \< m[i][q]。对于同一类的m[p][j]和m[q][j]而言，当p \< q时必然有m[p][j] > m[q][j]。

另一方面，由于这里的所有数都是区间和，那么也就意味着可以使用前缀和来进行代替。令s表示a的前缀和。另外，为了方便计数，设s[0] \= 0，前缀和下标从1开始计算：

| s[1] - s[0] | s[2] - s[0] | s[3] - s[0] | ... | s[n] - s[0] |
| --- | --- | --- | --- | --- |
|  | s[2] - s[1] | s[3] - s[1] | ... | s[n] - s[1] |
|  |  | s[3] - s[2] | ... | s[n] - s[2] |
|  |  |  | ... | ... |
|  |  |  |  | s[n] - s[n - 1] |

不妨让行i从0开始计数，列j从1开始计数，那么第i行第j列的值就是s[j] - s[i]

题目要求上面矩阵中第l到第r小的数之和，对于这类问题经典的处理方法同样是运用前缀和，也就是找到上面矩阵中第1到第l - 1小的数之和，以及第1到第r小的数之和，然后用后者减去前者。那么首先，就需要想办法找到第r小以及第l - 1小的数是多少。

由于上面矩阵行和列的单调性，对于给出的一个数x，是很容易判断矩阵中有多少个数小于等于x。具体来说就是从矩阵左上角开始逐行确定。

对于当前的m[i][j]，若m[i][j] \<\= x，那么就将j向后移动，直到j抵达边界或者m[i][j] > x。此时将j减去1，就得到了第i行中最大的满足m[i][j] \<\= x的j。对于第i行而言，其最前方的i个位置是空白的，因此实际上第i行小于等于x的数就有j - i个。

接下来考虑第i + 1行。由于m[i + 1][j]必然是小于m[i][j]的，因此就有m[i + 1][j] \< x，因此对于第i + 1行而言，无需从头开始寻找满足条件的最大的j，而是直接从第i行的j开始向后找就行了。

这样一来，就可以在O(n + n)的时间复杂度内找出每一行小于等于x的数的数量，从而确定整个矩阵中有多少个数小于等于x。

有了上面的结论，那么很自然想到使用二分这个x，使用上面的做法确定矩阵中有多少个数小于等于x，并根据这个数目与r或者l - 1的大小关系来调整二分的上下界，从而最终确定第r小以及第l - 1小的数是多少。

当然，仅仅确定了这两个数还是不够的，还需要计算矩阵中的小于等于这些数的和。不过这个说法并不准确。例如矩阵中的数为1, 2, 8, 8, 8，那么前3小的数之和为1 + 2 + 8，而前5小的数的和为1 + 2 + 8 + 8 + 8，而第3小和第5小的数都是8，不太好进行区分。

一个可行的思路是对于第r小的数x，先将矩阵中所有严格小于x的数的和求出来，并统计这些数的数量cnt，最后再补充r - cnt个x进来。那么对于上面例子中前3小的数之后以及前5小的数之后而言，第3小的数和第5小的数都是8，小于8的数之和为1 + 2 \= 3，一共有2个数，那么前3小的数之后就是3 + (3 - 2) \* 8 \= 11，而前5小的数之后为3 + (5 - 2) \* 8 \= 27。这样一来就解决了重复的问题。

同样的，求解小于x的数的方式与上面小于等于的求解方式是一样的。接下来还需要解决的问题是如何将这些小于x的数的和计算出来。不妨设矩阵中每一行严格小于x的j的位置为

m\[0\]\[p\[0\]\]，m\[1\]\[p\[1\]\]，...，m\[n - 1\]\[p\[n - 1\]\]

那么对于每一行，要求的和就是

第0行：

(s\[1\] - s\[0\]) + (s\[2\] - s\[0\]) + ... + (s\[p\[0\]\] - s\[0\])

\= s\[1\] + s\[2\] + ... + s\[p\[0\]\]

第1行：

(s\[2\] - s\[1\]) + (s\[3\] - s\[1\]) + ... + (s\[p\[1\]\] - s\[1\])

\= s\[2\] + s\[3\] + ... + s\[p\[1\]\] - s\[1\] \* (p\[1\] - 2 + 1)

第2行：

(s\[3\] - s\[2\]) + (s\[4\] - s\[2\]) + ... + (s\[p\[2\]\] - s\[2\])

\= s\[3\] + s\[4\] + ... + s\[p\[2\]\] - s\[2\] \* (p\[2\] - 3 + 1)

更一般的，对于第i行：

(s\[i + 1\] - s\[i\]) + (s\[i + 2\] - s\[i\]) + ... + (s\[p\[i\]\] - s\[i\])

\= s\[i + 1\] + s\[i + 2\] + ... + s\[p\[i\]\] - s\[i\] \* (p\[i\] - i)

对于这个式子而言，前面连加的部分可以再次使用前缀和，也就是对于前缀和s再次计算前缀和得到的二级前缀和，即为two_s，那么就有

s\[i + 1\] + s\[i + 2\] + ... + s\[p\[i\]\] - s\[i\] \* (p\[i\] - i) \= two_s\[p\[i\]\] - two\[s\[i\]\] - s\[i\] \* (p\[i\] - i)

这样一来，在求解出每一行最大的满足mat\[i\]\[p\[i\]\]小于x的位置p\[i\]之后，就可以利用上面的式子计算出这一行所有小于x的数之和了。将每一行的和累加起来，就得到了矩阵中所有小于x的数之后。然后再根据这些数的数量补充一些x，就得到了要求的前r小或者前l - 1小的数之和。

最后附上python代码：

```python
class Solution(object):
    def rangeSum(self, nums, n, left, right):
        """
        :type nums: List[int]
        :type n: int
        :type left: int
        :type right: int
        :rtype: int
        """

        one_prefix_s = [0]
        for num in nums:
            one_prefix_s.append(one_prefix_s[-1] + num)
        
        two_prefix_s = [0]
        for s in one_prefix_s[1:]:
            two_prefix_s.append(two_prefix_s[-1] + s)
        
        mod = 10 ** 9 + 7
        res = self.get(n, one_prefix_s, two_prefix_s, right, mod)
        if left > 1:
            res -= self.get(n, one_prefix_s, two_prefix_s, left - 1, mod)
        
        return res
    
    def get(self, n, one_prefix_s, two_prefix_s, target, mod):
        l = 1
        r = one_prefix_s[-1]

        while l < r:
            mid = (l + r) >> 1
            i = 0
            j = 1
            cnt = 0
            while i < n:
                while j <= n and one_prefix_s[j] - one_prefix_s[i] <= mid:
                    j += 1

                j -= 1

                cnt += j - i
                i += 1

            if cnt < target:
                l = mid + 1
            else:
                r = mid

        res = 0
        i = 0
        j = 1
        cnt = 0
        while i < n:
            while j <= n and one_prefix_s[j] - one_prefix_s[i] < l:
                j += 1
            
            j -= 1

            res = (res + two_prefix_s[j] - two_prefix_s[i] - one_prefix_s[i] * (j - i) + mod) % mod
            cnt += j - i
            i += 1

        res = (res + (target - cnt) * l) % mod

        return res
```

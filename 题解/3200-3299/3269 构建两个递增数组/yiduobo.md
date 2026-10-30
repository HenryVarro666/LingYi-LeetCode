---
title: "3269. 构建两个递增数组"
aliases: ["yiduobo的每日leetcode 3269.构建两个递增数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/764197825"
zhihu_id: "764197825"
zhihu_title: "yiduobo的每日leetcode 3269.构建两个递增数组"
question_id: "3269"
question: "构建两个递增数组"
problem_url: "https://leetcode.cn/problems/constructing-two-increasing-arrays/"
created: "2024-09-30T00:41:58+08:00"
updated: "2024-09-30T00:41:58+08:00"
upvotes: 1
comments: 0
---

# 3269. 构建两个递增数组

> **[yiduobo的每日leetcode 3269.构建两个递增数组](https://zhuanlan.zhihu.com/p/764197825) · 知乎 · 2024-09-30 · 赞同 1**
> 力扣：[3269. 构建两个递增数组](https://leetcode.cn/problems/constructing-two-increasing-arrays/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3269.构建两个递增数组

[. - 力扣（LeetCode）](https://leetcode.cn/problems/constructing-two-increasing-arrays/description/)

题目给出两个由0和1构成的数组nums1和nums2，现在要求将这两个数组中的0都替换成偶数，1都替换成奇数，使得这两个数组都单调递增，且每个数字最多只能使用一次。

问替换完成后，两个数组中最大元素可以取到的最小值是多少。

---

一开始想到的是贪心，毕竟对于单个数组来说，一趟遍历利用贪心就能直接推上去了，那么对于两个数组，可以考虑计算出各自的下限，然后合并这两个数组。

不过在合并时值相同的项应该如何合并就没有找出可行的方案了。

第一种思路是将优先填充剩余元素较多的数组。例如样例2中的两个数组[0, 1, 0, 1]以及[1, 0, 0, 1]，二者各自的下限为[2, 3, 4, 5]以及[1, 2, 4, 5]。

接下来对这两个数组进行合并。首先是1，接下来2遇到冲突时由于第一个数组剩余4个数，多余第二个数组剩余的3个数，所以优先使用第一个数组中的2，此时两个数组分别变成了[3, 4, 5]以及[4, 6, 7]。接下来是3，然后4遇到冲突时则应该使用第二个数组中的4，此时两个数组都变成了[6, 7]，到了这里我就发现不对劲了。因为此时两个数组剩余的元素数量相同，这种情况下无法根据根据剩余元素的数量决定先使用哪一边。

基于上面这一点，加了一些改进，改成两个元素相等时，对比下一个元素，以此类推。但是这样依然不行，例如两个数组分别为[1, 1, 0, 0, 0]以及[1, 0, 0, 0]时，数组下限分别为[1, 3, 4, 6, 8]以及[1, 2, 4, 6]，此时对于相同的1，选择第二个数组中的1是更优的，而如果按照长度优先的原则会选择第一个数组中的1。

那么此时直接按照后续元素大小优先的原则是否可行呢？答案也是否定的。例如两个数组分别为[1, 1, 0, 0, 0]以及[1, 1, 0, 1]时，数组下限分别为[1, 3, 4, 6, 8]以及[1, 3, 4, 5]，此时对于相同的1，选择第一个数组中的1更优。

到了这里，感觉就没有比较直观的贪心思路了，只能转而去想能否使用动态规划。

---

动态规划的状态表示是比较直观的。令f[i][j]表示填充nums1的前i个数字和nums2的前j个数字后，最大值出现在nums1时是多少，g[i][j]则表示填充后最大值出现在nums2时是多少。

那么对于f[i][j]：

1、如果是从f[i - 1][j]过来：

这种情况比较直观，当nums1[i + 1]与f[i - 1][j]同奇偶时，f[i][j]取f[i - 1][j] + 2，反之f[i][j]取f[i - 1][j] + 1

2、如果是从g[i - 1][j]过来：

需要注意此时g[i - 1][j]对应的是nums2[j + 1]填充的元素值，这个值一定大于nums1[i]填充的元素值，因为此时的状态g表示规定了最大值出现在nums2中。另一方面，根据f的定义，f[i][j]的取值必须要大于g[i - 1][j]的取值，也就是说这里f的取值无需考虑nums1[i]，而是考虑g[i - 1][j]与nums1[i + 1]的奇偶性就行了。当nums1[i + 1]与g[i - 1][j]同奇偶时，f[i][j]取g[i - 1][j] + 2，反之取g[i - 1][j] + 1。

可以发现，f和g的转移方程不仅完全相同，就转移过程而言也是可以完全无视掉不是最大值的那一边，因此在这里可以重新定义f数组，令f[i][j]表示填充nums1的前i个数以及nums2的前j个数后，数组中最大值最小可以是多少，那么f[i][j]就是直接从f[i][j - 1]和f[i - 1][j]来进行转移了。

最后附上python代码：

```python
class Solution(object):
    def minLargest(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """

        m = len(nums1)
        n = len(nums2)

        f = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0:
                    if j == 0:
                        continue
                    elif j == 1:
                        if nums2[0] == 0:
                            f[i][j] = 2
                        else:
                            f[i][j] = 1
                    elif nums2[j - 2] == nums2[j - 1]:
                        f[i][j] = f[i][j - 1] + 2
                    else:
                        f[i][j] = f[i][j - 1] + 1
                
                elif j == 0:
                    if i == 1:
                        if nums1[0] == 0:
                            f[i][j] = 2
                        else:
                            f[i][j] = 1
                    elif nums1[i - 2] == nums1[i - 1]:
                        f[i][j] = f[i - 1][j] + 2
                    else:
                        f[i][j] = f[i - 1][j] + 1
                
                else:
                    if (nums1[i - 1] + f[i - 1][j]) % 2 == 0:
                        f[i][j] = f[i - 1][j] + 2
                    else:
                        f[i][j] = f[i - 1][j] + 1

                    if (nums2[j - 1] + f[i][j - 1]) % 2 == 0:
                        f[i][j] = min(f[i][j], f[i][j - 1] + 2)
                    else:
                        f[i][j] = min(f[i][j], f[i][j - 1] + 1)
                    
        return f[-1][-1]
```

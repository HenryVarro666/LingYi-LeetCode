---
title: "3224. 使差值相等的最少数组改动次数"
aliases: ["yiduobo的每日leetcode 3224.使差值相等的最少数组改动次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/二-差分"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/719639170"
zhihu_id: "719639170"
zhihu_title: "yiduobo的每日leetcode 3224.使差值相等的最少数组改动次数"
question_id: "3224"
question: "使差值相等的最少数组改动次数"
problem_url: "https://leetcode.cn/problems/minimum-array-changes-to-make-differences-equal/"
difficulty: "Medium"
rating: 1996
created: "2024-09-12T00:27:35+08:00"
updated: "2024-09-12T00:27:35+08:00"
upvotes: 1
comments: 0
---

# 3224. 使差值相等的最少数组改动次数

> **[yiduobo的每日leetcode 3224.使差值相等的最少数组改动次数](https://zhuanlan.zhihu.com/p/719639170) · 知乎 · 2024-09-12 · 赞同 1**
> 力扣：[3224. 使差值相等的最少数组改动次数](https://leetcode.cn/problems/minimum-array-changes-to-make-differences-equal/) · Medium · 灵茶山艾府：[两种方法：枚举 X / 差分数组（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3224.使差值相等的最少数组改动次数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-array-changes-to-make-differences-equal/description/)

题目给出一个长度为偶数n的数组nums以及一个整数k，保证nums中每个元素大小都在0到k之间。接下来每次操作，可以将nums中的任意元素替换成0到k之间的任意整数，问最少需要执行多少次操作，使得nums满足

abs(nums[0] - nums[n - 1]) \= abs(nums[1] - nums[n - 2]) \= ... \= abs(nums[n - 1] - nums[0]) \= X

由于nums中所有元素的初始值都处在0到k之间，因此每一组数的初始差值都必然处在0到k之间。另一方面，对任意一组数执行两次操作后，必然可以使得二者的差值变为0到k之间的特点整数。当然，在这里也可以选择不进行操作或者仅对某组数中的一个执行操作，那么在这里实际上是需要找出一个最优的X。

对于其中某组数对nums[i]以及nums[n - i - 1]而言：

1、若不进行任何操作，二者的差值为diff \= abs(nums[i] - nums[n - i - 1])

2、若执行两次操作，二者的差值可以覆盖到0到k之间的任意整数

3、若仅执行一次操作：

3-1、若修改nums[i]：

当0 \<\= nums[i] \<\= nums[n - i - 1]时，二者差值的范围为[nums[n - i - 1], 0]

当nums\[n - i - 1\] \< nums\[i\] \<\= k时，二者差值的范围为\[1, k - nums\[n - i - 1\]\]

3-2、若修改nums[n - i - 1]：

当0 \<\= nums[n - i - 1] \<\= nums[i]时，二者差值的范围为[nums[i], 0]

当nums\[i\] \< nums\[n - i - 1\] \<\= k时，二者差值的范围为\[1, k - nums\[i\]\]

综合上面两种情况，令v \= max(nums[i], nums[n - i - 1], k - nums[i], k - nums[n - i - 1])，那么仅执行一次操作时可以使得差值覆盖到0到v之间的任意整数

令cnt[x]表示将数对的差值修改成x时所需的最少操作次数，那么对于nums[i]以及nums[n - i - 1]这一组数对，就应该将cnt[0]到cnt[v]这一段都加上1，将cnt[v + 1]到cnt[k]这一段都加上2，另外其中cnt[diff]应该置为0。

到了这里，问题就变成了针对每一组nums[i]以及nums[n - i - 1]来修改cnt数组，然后计算cnt中的最小值作为最终答案。注意到这是一个离线的区间同值修改，然后单点求值的问题，可以利用差分数组来高效求解。

不妨设f为差分数组，那么对于需要修改的区间，可以先将区间重组一下，变成[0, diff - 1]，[diff + 1, k]，[v + 1, k]，接下来只需将f[0]加上1，将f[diff]减去1，再将f[diff + 1]以及f[v + 1]分别加上1即可。

得到f数组后，只需一趟遍历，计算f的前缀和，取其中的最小值作为答案即可。

最后附上python代码：

```python
class Solution(object):
    def minChanges(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        f = [0] * (k + 1)
        left, right = 0, len(nums) - 1
        while left < right:
            v = max(nums[left], nums[right], k - nums[left], k - nums[right])
            diff = abs(nums[left] - nums[right])
            f[0] += 1
            f[diff] -= 1
            if diff < k:
                f[diff + 1] += 1
            if v < k:
                f[v + 1] += 1
            
            left += 1
            right -= 1

        now = 0
        res = None
        for d in range(0, k + 1):
            now += f[d]
            if res is None or res > now:
                res = now
            
        return res
```

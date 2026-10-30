---
title: "3875. 构造奇偶一致的数组I & 3876. 构造奇偶一致的数组II"
aliases: ["yiduobo的每日leetcode 3875.构造奇偶一致的数组I && 3876.构造奇偶一致的数组II", "3875. 构造奇偶一致的数组I", "3876. 构造奇偶一致的数组II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/brainteaser", "题单/贪心算法", "题单/贪心算法/五-思维题", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2019546272718143833"
zhihu_id: "2019546272718143833"
zhihu_title: "yiduobo的每日leetcode 3875.构造奇偶一致的数组I && 3876.构造奇偶一致的数组II"
question_id: ["3875", "3876"]
question: ["构造奇偶一致的数组 I", "构造奇偶一致的数组 II"]
problem_url: ["https://leetcode.cn/problems/construct-uniform-parity-array-i/", "https://leetcode.cn/problems/construct-uniform-parity-array-ii/"]
difficulty: ["Easy", "Medium"]
rating: ["1200", "1444"]
created: "2026-03-23T23:00:58+08:00"
updated: "2026-03-23T23:00:59+08:00"
upvotes: 0
comments: 0
---

# 3875. 构造奇偶一致的数组I & 3876. 构造奇偶一致的数组II

> **[yiduobo的每日leetcode 3875.构造奇偶一致的数组I && 3876.构造奇偶一致的数组II](https://zhuanlan.zhihu.com/p/2019546272718143833) · 知乎 · 2026-03-23 · 赞同 0**
> 力扣：[3875. 构造奇偶一致的数组 I](https://leetcode.cn/problems/construct-uniform-parity-array-i/) · Easy · 灵茶山艾府：[脑筋急转弯（Python/Java/C++/Go）](灵茶山艾府.md)
> 力扣：[3876. 构造奇偶一致的数组 II](https://leetcode.cn/problems/construct-uniform-parity-array-ii/) · Medium · 灵茶山艾府：[分类讨论，简洁写法（Python/Java/C++/Go）](../3876%20构造奇偶一致的数组%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3875.构造奇偶一致的数组I

<https://leetcode.cn/problems/construct-uniform-parity-array-i/description/>

3876.构造奇偶一致的数组II

<https://leetcode.cn/problems/construct-uniform-parity-array-ii/>

题目给出一个长度为n的数组nums1，其中包含互不相同的整数。

现在要求构造一个长度为n的数组nums2，使得nums2中的元素要么全为奇数，要么全为偶数。

对于每个下标i，必须从以下两种选择种任选一种：

- 令nums2[i] \= nums1[i]
- 令nums2[i] \= nums1[i] - nums1[j]，这里j与i不同。对于3876题，还额外要求nums1[i] - nums1[j] >\= 1

问能否构造出符合题目要求的nums2。

3876题除了上面nums1[i] - nums1[j] >\= 1的要求之外，其数据规模也更大。

首先来看较为简单的3875题。

若nums1中的元素本身就是全奇或者全偶，那么直接套用第一种操作复制一遍，得到的nums2就是符合条件的，此时答案显然为true。

否则，若其中既有奇数也有偶数，那么在这里就可以保持所有的奇数不变，而对于所有偶数，都让这个偶数与某个奇数做减法，这样一来得到的结果必然为奇数，从而使得nums2中的所有元素都变为奇数。

也就是说，无论什么情况，答案必然为true。

接下来考虑3876题。

首先依然是特殊情况，若nums1中的元素本身就是全奇或者全偶，那么答案为true。

否则，由于与偶数做减法不会改变一个元素的奇偶性，那么在这里就要么需要让所有偶数减去某个奇数从而使得nums2全奇，要么就要让所有奇数减去某个奇数从而使得nums2全偶。

又由于nums1[i] - nums1[j] >\= 1的限制，后面这种操作是不可能达成的，因为不存在更小的奇数，可以用来被nums1中最小的奇数减去，因此在这里只能考虑让所有的偶数减去某个奇数。依然是考虑到nums1[i] - nums1[j] >\= 1的限制，在这里就应该取nums1中的最小的奇数来作为nums1[j]，那么此时有解的情况就是nums1中最小的偶数大于这个最小的奇数。

基于上面的结论，就可以先对nums1进行一趟遍历，找出其中最小的奇数mi_o以及最小的偶数mi_e。若其中一方不存在，则说明nums1全奇或者全偶，此时应该返回true。否则，若mi_e > mi_o，那么就可以通过让nums1中所有偶数都减去mi_o得到全奇的nums2，此时应该返回true，否则返回false。

最后附上python代码：

3875:

```
class Solution(object):
    def uniformArray(self, nums1):
        """
        :type nums1: List[int]
        :rtype: bool
        """
        
        return True
```

3876:

```python
class Solution(object):
    def uniformArray(self, nums1):
        """
        :type nums1: List[int]
        :rtype: bool
        """
        
        mi_o, mi_e = None, None
        for v in nums1:
            if v % 2 == 1:
                if mi_o is None or mi_o > v:
                    mi_o = v
            else:
                if mi_e is None or mi_e > v:
                    mi_e = v
        
        return mi_e is None or mi_o is None or mi_e > mi_o
```

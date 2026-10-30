---
title: "3012. 通过操作使数组长度最小"
aliases: ["yiduobo的每日leetcode 3012.通过操作使数组长度最小"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/brainteaser", "leetcode/math", "题单/数学算法", "题单/贪心算法", "题单/数学算法/七-杂项", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/693969859"
zhihu_id: "693969859"
zhihu_title: "yiduobo的每日leetcode 3012.通过操作使数组长度最小"
question_id: "3012"
question: "通过操作使数组长度最小"
problem_url: "https://leetcode.cn/problems/minimize-length-of-array-using-operations/"
difficulty: "Medium"
rating: 1833
created: "2024-04-22T23:46:34+08:00"
updated: "2024-04-22T23:46:34+08:00"
upvotes: 1
comments: 0
---

# 3012. 通过操作使数组长度最小

> **[yiduobo的每日leetcode 3012.通过操作使数组长度最小](https://zhuanlan.zhihu.com/p/693969859) · 知乎 · 2024-04-22 · 赞同 1**
> 力扣：[3012. 通过操作使数组长度最小](https://leetcode.cn/problems/minimize-length-of-array-using-operations/) · Medium · 灵茶山艾府：[O(n) 脑筋急转弯（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3012.通过操作使数组长度最小

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimize-length-of-array-using-operations/description/)

对于题目中的操作，如果选择一组(x, y)，其中x \< y，那么就相当于消除掉了y，因此一种可行的操作就是选出数组中的最小值，然后用来消除掉数组中的其他数。但是这个做法有个问题是如果数组中最小值出现了多次，那么就不一定是最优解。例如数组[2, 2, 2, 2, 2, 3]，其中2是最小值，但是在这里可以先通过选择(3, 2)得到1，然后再用这个1与其他值进行计算。

换言之，如果数组中存在某个数不是最小值的倍数，那么就可以先取这两个数进行取模，得到的结果必然小于原来的最小值，也就是说此时得到了一个唯一的新的最小值，接下来使用这个新的最小值与其他数进行操作，就可以将数组的长度缩减到1。

反之，如果数组中所有数都是最小值的倍数，那么无论怎么操作，最小值都不应该处在模数的位置上，因为这样会得到0，而0不能再次参与运算，相比让最小值处于被摸数的位置上是更好的选择。因此在这里就只能让最小值对其他所有数取模，然后再两两组合进行消化，得到的最终结果就是最小值出现次数除以2向上取整。

最后附上python代码：

```python
class Solution(object):
    def minimumArrayLength(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        mi = None
        freq = 0
        for v in nums:
            if mi is None or mi > v:
                mi = v
                freq = 1
            elif mi == v:
                freq += 1
        
        for v in nums:
            if v > mi and v % mi != 0:
                return 1
        
        return (freq + 1) // 2
```

---
title: "2202. K次操作后最大化顶端元素"
aliases: ["yiduobo的每日leetcode 2202.K次操作后最大化顶端元素"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/array", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/539395580"
zhihu_id: "539395580"
zhihu_title: "yiduobo的每日leetcode 2202.K次操作后最大化顶端元素"
question_id: "2202"
question: "K 次操作后最大化顶端元素"
problem_url: "https://leetcode.cn/problems/maximize-the-topmost-element-after-k-moves/"
difficulty: "Medium"
rating: 1717
created: "2022-07-08T22:42:50+08:00"
updated: "2022-07-08T22:42:50+08:00"
upvotes: 0
comments: 0
---

# 2202. K次操作后最大化顶端元素

> **[yiduobo的每日leetcode 2202.K次操作后最大化顶端元素](https://zhuanlan.zhihu.com/p/539395580) · 知乎 · 2022-07-08 · 赞同 0**
> 力扣：[2202. K 次操作后最大化顶端元素](https://leetcode.cn/problems/maximize-the-topmost-element-after-k-moves/) · Medium · 灵茶山艾府：[分类讨论](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2202.K次操作后最大化顶端元素

[力扣](https://leetcode.cn/problems/maximize-the-topmost-element-after-k-moves/)

注意到样例2，那么应该先考虑数组长度n \= 1的情况。此时若k为奇数，那么答案就是-1，否则就是nums中的唯一元素nums[0]。

接下来考虑n > 1的情况。

在操作数k足够大的情况下，最理想的做法就是先将栈中所有的元素弹出，并找出其中的最大值ma。对于剩下的k - n次操作次数，从中预留出一次，用来将ma置于栈顶，其他的操作数则可以通过让除ma之外的任意元素反复进出栈来消耗掉，从而保证最终结果就是数组中的最大值ma。基于这个考虑，所需的操作数至少需要n + 1次，即弹出的n次以及留给最大值的1次，于是当k > n时，最终答案就是max(nums)。

当然，还存在k不够大的情况。

当k \= 0时，没有任何操作空间，答案就是nums[0]。

当k \= 1时，同样没有任何操作空间，只能移除掉nums[0]，因此答案就是nums[1]。

至此，就只剩下1 \< k \<\= n的情况需要考虑。对于这种情况，可以仿照k足够大时的做法，先使用k - 1次操作弹出栈顶的k - 1个元素，然后用最后一次操作将其中的最大值置于栈顶。按这种操作方式得到的最大值就是max(nums[:k - 1])。

另外还有一种情况是当k \< n时，可以选择移除栈顶的k个元素，也就是移除掉nums[0]到nums[k - 1，此时答案就是nums[k]。需要注意的是当k \= n时不能采取这种策略，因为这样做会将栈中元素全部弹出。

总结一下，就有：

1、当n \= 1时，若k为奇数，那么答案为-1，否则答案为nums[0]

2、当n > 1时：

2-1）若k \= 0，那么答案为nums[0]

2-2）若k \= 1，那么答案为nums[1]

2-3）若1 \< k \< n，那么答案为max(nums[:k - 1], nums[k])

2-4）若k \= n，那么答案为max(nums[:k - 1])

2-5）若k > n，那么答案为max(nums)

最后附上python代码：

```python
class Solution(object):
    def maximumTop(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        n = len(nums)
        if n == 1:
            if k % 2 == 0:
                return nums[0]
            else:
                return -1

        if k == 0:
            return nums[0]
        elif k == 1:
            return nums[1]
        elif k < n:
            return max(nums[k], max(nums[:k - 1]))
        elif k == n:
            return max(nums[:n - 1])
        else:
            return max(nums)
```

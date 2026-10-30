---
title: "3022. 给定操作次数内使剩余元素的或值最小"
aliases: ["yiduobo的每日leetcode 3022.给定操作次数内使剩余元素的或值最小"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "题单/位运算", "题单/位运算/五-试填法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/694793950"
zhihu_id: "694793950"
zhihu_title: "yiduobo的每日leetcode 3022.给定操作次数内使剩余元素的或值最小"
question_id: "3022"
question: "给定操作次数内使剩余元素的或值最小"
problem_url: "https://leetcode.cn/problems/minimize-or-of-remaining-elements-using-operations/"
difficulty: "Hard"
rating: 2918
created: "2024-04-27T00:57:51+08:00"
updated: "2024-04-27T00:57:51+08:00"
upvotes: 1
comments: 0
---

# 3022. 给定操作次数内使剩余元素的或值最小

> **[yiduobo的每日leetcode 3022.给定操作次数内使剩余元素的或值最小](https://zhuanlan.zhihu.com/p/694793950) · 知乎 · 2024-04-27 · 赞同 1**
> 力扣：[3022. 给定操作次数内使剩余元素的或值最小](https://leetcode.cn/problems/minimize-or-of-remaining-elements-using-operations/) · Hard · 灵茶山艾府：[试填法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3022.给定操作次数内使剩余元素的或值最小

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimize-or-of-remaining-elements-using-operations/description/)

题目要求使得最终结果最小，那么就需要尽量让二进制位的高位上的数尽量取0。又因为采用的是按位或运算，因此最终结果的某一位为零就意味着所有参与运算的数的这一位都必须为0，也就是原始有1的数都被与运算给消除掉了。

在这里就可以从高位开始向低位逐位考虑，使用一个变量prefix记录当前已经确定可以消除掉的前缀是什么。对于当前位index，如果要将其消除掉，prefix就变成prefix | (1 \<\< p)，接下来遍历nums，计算其中的每个v是否有位数需要消除，也就是v & prefix是否为0。方便起见，在这里记为tmp。若tmp不为零，那么这个按位与的结果就是需要通过按位与消除掉。

在这里需要特别注意的是，由于消除时会选择一个区间内的数通过按位与进行消除，那么一旦当前区间内的数互相按位与得到了0，那么就无需借助其他的数提供的零来进行额外的消除。

一个简单的例子：

如果是10、10、00，前两个10按位与之后的结果10依然需要最后的00来执行第二次的按位与，也就是说m个数就需要执行m次消除。

但是如果是10、01、00，前两个数10和01按位与之后已经变成0了，无需执行第二次的按位与，在这里m个数只需要m - 1次消除，也就是相当于01按位与之后的结果如果为0，就可以省去这次消除。

根据上面这一点，就需要使用一个变量interval_prefix记录区间内的按位与结果。对于当前需要消除的结果tmp：

若tmp本来就为0，那么说明一个区间结束了，此时置interval_prefix为None。

若tmp不为0，且interval_prefix为None，说明这是一个新区间的开始，需要置interval_prefix为tmp，否则说明此时处于区间中，需要将tmp按位与到interval_prefix中。无论哪种情况，最后都需要检测interval_prefix是否为0。若为0，那么说明一个区间结束了，此时置interval_prefix为None，否则就将需要执行操作的次数加上1。

遍历完成后，若得到的需要执行操作的次数小于等于k，说明当前的prefix是可以被消除的，否则的话就需要从prefix中异或掉(1 \<\< p)，表示p这一位无法被消除。

从高位到低位遍历，计算得到prefix后，最终答案就是11...111异或prefix。

最后附上python代码：

```python
class Solution(object):
    def minOrAfterOperations(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        prefix = 0
        ma = max(nums)
        length = len(bin(ma)) - 2
        for index in range(length - 1, -1, -1):
            prefix |= (1 << index)
            need_merge = 0
            interval_prefix = None
            for v in nums:
                tmp = prefix & v
                if tmp:
                    if interval_prefix is None:
                        interval_prefix = tmp
                    else:
                        interval_prefix &= tmp

                    if interval_prefix:
                        need_merge += 1
                    else:
                        interval_prefix = None
                else:
                    interval_prefix = None

            if need_merge > k:
                prefix ^= (1 << index)
        
        return ((1 << length) - 1) ^ prefix
```

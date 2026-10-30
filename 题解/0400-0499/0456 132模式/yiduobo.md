---
title: "456. 132模式"
aliases: ["yiduobo的每日leetcode 456. 132模式"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/216578927"
zhihu_id: "216578927"
zhihu_title: "yiduobo的每日leetcode 456. 132模式"
question_id: "456"
question: "132模式"
problem_url: "https://leetcode.cn/problems/132-pattern/"
created: "2020-09-05T01:10:43+08:00"
updated: "2020-09-05T01:10:43+08:00"
upvotes: 1
comments: 0
---

# 456. 132模式

> **[yiduobo的每日leetcode 456. 132模式](https://zhuanlan.zhihu.com/p/216578927) · 知乎 · 2020-09-05 · 赞同 1**
> 力扣：[456. 132模式](https://leetcode.cn/problems/132-pattern/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

456\. 132模式<https://leetcode-cn.com/problems/132-pattern/>

处理这类问题，一个常见的思路就是枚举其中某一个数的位置，然后通过数据结构高效地得到区间中的某些信息。

那么在这一题中，首先需要确定应当枚举哪一个数。

首先是考察枚举'1'的情况。设我们枚举到nums[index]，其对应'1'，那么我们现在的目标就是在nums[index + 1]到nums[-1]中找到'3'和'2'。遗憾的是，在这里并不太好找，因为我们既不能直接确定'3'的位置，也不能直接确定'2'的位置，因此还需要一趟扫描枚举'3'或者'2'的位置，才能最终确定另一个数是否存在。这样做的时间复杂度就太高了。

接下来考察枚举'3'的情况。设我们枚举到nums[index]，其对应'3'，那么可以确定的是，此时的'1'取nums[0]到nums[index - 1]中的最小值必然是最优的，而这一步可以通过前缀操作进行预处理，于是现在就可以在O(1)时间内确定'1'的最优值。现在有了'1'和'3'，就只需要判断'2'是否存在即可。于是离散化加树状数组或者平衡树都能很好解决这个问题，于是此时就有了一种O(nlogn)的做法。

不过，这种做法也还不是最优的做法。

在这里，由于我们确定'1'可以直接通过预处理来做，因此我们枚举'3'时应该从后往前枚举，这样一来'2'的候选集就会在枚举'3'的时候被扫描过一遍，可能可以从中获取到某些有效的信息。不妨设我们现在枚举到nums[index]，同时我们使用某种数据结构在扫描过程中保留住了nums[index + 1]到nums[-1]中的某些数，作为'2'的备选答案。

那么对于当前nums[index]的'3'，首先通过前缀min操作获取到'1'的值。

若'1'不小于nums[index]，说明nums[index]不能作为'3'，直接跳过。

若'1'小于nums[index]，那么首先将所有'2'的备选答案中，小于等于'1'的元素全部移除掉，因为随着index的往前移动，'1'的值必然是单调不减的，因此这些'2'的备选答案在之后也不可能派上用场了。接下来我们继续要从之前维护的数据结构中找出'2'的值。这里有一个隐藏条件，就是这些'2'的备选答案必然是单调不增的，因为若存在nums[p]与nums[q]，满足index \< p \< q且nums[p] > nums[q]，那么将'1'，nums[p]，nums[q]组合起来就已经形成了'132'的形式，index就不可能枚举到当前位置。有了这个单调性质，同时考虑到要高效地清除里面小于等于'1'的数据，自然就想到通过单调栈来维护这些'2'的备选答案。

于是现在的做法如下：

1、首先从前往后一趟扫描，预处理出前缀最小值数组min，其中min[index]表示nums[0]到nums[index]中的最小值。

2、将nums[-1]入栈，作为'2'的备选集合，同时从nums[-2]开始往前扫描，枚举'3'的位置。设当前枚举到nums[index]，那么'1'就等于min[index - 1]。

3、接下来对比'1'与栈顶元素，若栈顶元素小于等于'1'，那么弹出栈顶元素，直到栈为空或者栈顶元素大于'1'。此时，栈顶元素就是nums[index + 1]到nums[-1]中大于'1'的数里面最小的那一个。接下来判断nums[index]是否大于栈顶元素，若大于，那么'1'，nums[index]以及栈顶元素就形成了一组'132'，返回true即可，否则将nums[index]压入栈中，并回到步骤2继续往前枚举'3'。

这样一来，预处理需要一趟扫描，时间复杂度为O(n)。从后往前扫描一趟，每个元素至多入栈出栈一次，因此时间复杂度也是O(n)，因此最终的时间复杂度就是O(n)，是最优的做法了。

最后，我们也象征性地考察一下枚举'2'的情况。这种做法与枚举'1'类似，无法直接确定出其他两个数其中一个的位置，因此还需要一趟扫描，导致时间复杂度过高。

最后附上python代码：

```python
class Solution(object):
    def find132pattern(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        if len(nums) < 3:
            return False

        min_num = [nums[0]]
        for num in nums[1:]:
            min_num.append(min(min_num[-1], num))

        stack = [nums[-1]]
        for index in range(len(nums) - 2, -1, -1):
            now = nums[index]
            if now > min_num[index]:
                while stack and stack[-1] <= min_num[index]:
                    stack.pop()

                if stack and stack[-1] < now:
                    return True

                stack.append(now)

        return False
```

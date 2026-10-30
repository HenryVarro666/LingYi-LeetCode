---
title: "3867. 数对的最大公约数之和"
aliases: ["yiduobo的每日leetcode 3867.数对的最大公约数之和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/number-theory"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2017787502740653307"
zhihu_id: "2017787502740653307"
zhihu_title: "yiduobo的每日leetcode 3867.数对的最大公约数之和"
question_id: "3867"
question: "数对的最大公约数之和"
problem_url: "https://leetcode.cn/problems/sum-of-gcd-of-formed-pairs/"
difficulty: "Medium"
created: "2026-03-19T02:28:07+08:00"
updated: "2026-03-19T02:28:07+08:00"
upvotes: 1
comments: 0
---

# 3867. 数对的最大公约数之和

> **[yiduobo的每日leetcode 3867.数对的最大公约数之和](https://zhuanlan.zhihu.com/p/2017787502740653307) · 知乎 · 2026-03-19 · 赞同 1**
> 力扣：[3867. 数对的最大公约数之和](https://leetcode.cn/problems/sum-of-gcd-of-formed-pairs/) · Medium · 灵茶山艾府：[模拟（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3867.数对的最大公约之和

<https://leetcode.cn/problems/sum-of-gcd-of-formed-pairs/description/>

题目给出一个长度为n的整数数组nums。

要求先构造一个数组prefixGcd，对于其中的prefixGcd[index]：

- 令mx \= max(nums[0], nums[1], ..., nums[index])
- prefixGcd \= gcd(nums[index], mx)

在构造了prefixGcd之后：

- 将prefixGcd按非递减的顺序排序
- 通过取最小的未配对元素和最大的未配对元素，形成数对
- 重复此过程，直到无法得到更多数对为止
- 对于每个数对，计算两个元素的最大公约数gcd
- 若n是奇数，那么prefixGcd的中间元素应该被忽略

问所有形成数对的最大公约数之和

题目的描述比较复杂，但是其中并没有过份的要求，只需按照描述逐步模拟就行了。

具体来说，先对nums进行一趟遍历，使用一个变量ma记录当前前缀的最大值。对于当前遍历到的元素v，先使用v更新ma，然后计算v和ma的最大公约数，加入到prefixGcd数组中。

接下来，将prefixGcd按从大到小的顺序排序，然后使用两个指针left和right从两侧向中间扫。每一轮，都计算当前的prefixGcd[left]与prefixGcd[right]的最大公约数，将其累加到答案中，然后将left向右移动，将right向左移动，直到left大于等于right为止。

最后附上python代码：

```python
class Solution(object):
    def gcdSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        def gcd(x, y):
            while y > 0:
                x, y = y, x % y
            return x

        ma = nums[0]
        pre = [nums[0]]
        for v in nums[1:]:
            ma = max(ma, v)
            pre.append(gcd(ma, v))
        
        pre.sort()
        res = 0
        left, right = 0, len(pre) - 1
        while left < right:
            res += gcd(pre[left], pre[right])
            left += 1
            right -= 1
        
        return res
```

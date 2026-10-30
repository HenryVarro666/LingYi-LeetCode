---
title: "189. 旋转数组"
aliases: ["yiduobo的每日leetcode 189.旋转数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/two-pointers", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/LeetCode-热题-100/普通数组", "题单/面试经典-150-题/数组-/-字符串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/145670955"
zhihu_id: "145670955"
zhihu_title: "yiduobo的每日leetcode 189.旋转数组"
question_id: "189"
question: "轮转数组"
problem_url: "https://leetcode.cn/problems/rotate-array/"
difficulty: "Medium"
created: "2020-06-03T21:48:14+08:00"
updated: "2020-06-03T21:48:14+08:00"
upvotes: 1
comments: 0
---

# 189. 旋转数组

> **[yiduobo的每日leetcode 189.旋转数组](https://zhuanlan.zhihu.com/p/145670955) · 知乎 · 2020-06-03 · 赞同 1**
> 力扣：[189. 轮转数组](https://leetcode.cn/problems/rotate-array/) · Medium · 灵茶山艾府：[【图解】负负得正，一图秒懂！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

189.旋转数组<https://leetcode-cn.com/problems/rotate-array/>

比较基础的题目，不过我目前只想到了两种线性时间常数空间的做法。

方法一：三次reverse

整个旋转操作可以看成是整体reverse一次，然后前k个与后n - k个分别reverse一次。具体想法是由于旋转后的结果呈现出

a[n - k]，a[n - k + 1]，...，a[n - 1]，a[0]，a[1]，...，a[n - k - 1]

这种形式，可以发现将前k个与后n - k个都reverse之后就变成了了

a[n - 1]，a[n - 2]，...，a[n - k]，a[n - k - 1]，...，a[1]，a[0]

这就是原始数组reverse后的结果了

方法二：环形替换

从0开始做替换。对于当前的数a[pos]，其下一个位置为next_pos \= (pos + k)% n。将a[pos]移动到a[next_pos]后再计算next_pos的下一个位置，往复计算直到走回到pos为止。如果当前交换过的数已经达到了n个，说明交换完成，否则可以从pos + 1开始往后计算，因为此时pos + 1必然没有被交换过。这里可以给出不严谨的证明，若pos能通过若干次交换走到pos + 1，那么pos + 1同样可以通过若干次交换走到pos + 2，于是整个数组都可以在第一次交换中走遍了，而现在的情况是走回pos并未走遍整个数组，说明pos一定是走不到pos + 1的。

最后附上方法二的python代码：

```python
class Solution(object):
    def rotate(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: None Do not return anything, modify nums in-place instead.
        """

        if not nums:
            return []

        k %= len(nums)

        cnt = 0
        for index in range(len(nums)):
            last_pos, last_num = index, nums[index]
            while True:
                next_pos = (last_pos + k) % len(nums)
                last_num, nums[next_pos] = nums[next_pos], last_num
                last_pos = next_pos
                cnt += 1
                if next_pos == index:
                    break
            if cnt == len(nums):
                return
```

---
title: "3936. 将0移到末尾的最少交换次数"
aliases: ["yiduobo的每日leetcode 3936.将0移到末尾的最少交换次数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/two-pointers", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2043107122536256491"
zhihu_id: "2043107122536256491"
zhihu_title: "yiduobo的每日leetcode 3936.将0移到末尾的最少交换次数"
question_id: "3936"
question: "将 0 移到末尾的最少交换次数"
problem_url: "https://leetcode.cn/problems/minimum-swaps-to-move-zeros-to-end/"
difficulty: "Easy"
rating: 1346
created: "2026-05-27T23:19:01+08:00"
updated: "2026-05-27T23:19:02+08:00"
upvotes: 0
comments: 0
---

# 3936. 将0移到末尾的最少交换次数

> **[yiduobo的每日leetcode 3936.将0移到末尾的最少交换次数](https://zhuanlan.zhihu.com/p/2043107122536256491) · 知乎 · 2026-05-27 · 赞同 0**
> 力扣：[3936. 将 0 移到末尾的最少交换次数](https://leetcode.cn/problems/minimum-swaps-to-move-zeros-to-end/) · Easy · 灵茶山艾府：[两种方法：两次遍历 / 一次遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3936.将0移到末尾的最少交换次数

<https://leetcode.cn/problems/minimum-swaps-to-move-zeros-to-end/description/>

题目给出一个整数数组nums。

再一次操作中，可以选择任意两个不同下标i和j并交换nums[i]与nums[j]。

问将所有0移动到数组末尾所需的最少操作次数。

题目要求将所有的0都移动到数组的末尾，那么在这里就可以从后往前一趟遍历，每碰到一个非0的元素，就让其与最左侧的0进行交换，直到其左侧不存在0为止。之所以选择最左侧的0，是因为右侧的0可能已经处在正确的位置上，例如[0, 0, 1]，在这里应该选择最左侧的0交换，只需一次操作就变成了[1, 0, 0]，但是如果选择右侧的0，会先变成[0, 1, 0]，再变成[1, 0, 0]，多用了一次操作。

基于这一点，就可以使用一个变量p记录当前最左侧0的位置，接下来从后往前遍历。对于当前遍历到的nums[index]，若其非0，那么就将p向右侧移动，直到nums[p]为0，或者p等于index为止。若p等于index，说明index左侧不存在0了，已经完成了移动，此时应该退出循环；反之，则需要交换nums[p]与nums[index]并更新答案，然后index继续向前移动。

最后附上python代码：

```python
class Solution(object):
    def minimumSwaps(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        p = 0
        res = 0
        for index in range(len(nums) - 1, -1, -1):
            if nums[index] != 0:
                while p < index and nums[p] != 0:
                    p += 1
                if p == index:
                    break
                res += 1
                nums[p] = nums[index]
        
        return res
```

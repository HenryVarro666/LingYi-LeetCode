---
title: "3431. 对数字排序的最小解锁下标"
aliases: ["yiduobo的每日leetcode 3431.对数字排序的最小解锁下标"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1890558418588262907"
zhihu_id: "1890558418588262907"
zhihu_title: "yiduobo的每日leetcode 3431.对数字排序的最小解锁下标"
question_id: "3431"
question: "对数字排序的最小解锁下标"
problem_url: "https://leetcode.cn/problems/minimum-unlocked-indices-to-sort-nums/"
created: "2025-04-02T00:29:31+08:00"
updated: "2025-04-02T00:29:31+08:00"
upvotes: 1
comments: 0
---

# 3431. 对数字排序的最小解锁下标

> **[yiduobo的每日leetcode 3431.对数字排序的最小解锁下标](https://zhuanlan.zhihu.com/p/1890558418588262907) · 知乎 · 2025-04-02 · 赞同 1**
> 力扣：[3431. 对数字排序的最小解锁下标](https://leetcode.cn/problems/minimum-unlocked-indices-to-sort-nums/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3431.对数字排序的最小解锁下标

[3431. 对数字排序的最小解锁下标 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-unlocked-indices-to-sort-nums/description/)

题目给出一个仅包含1、2、3的整数数组nums，以及一个相同长度的二进制数组locked。

对于nums中的某个下标index，若nums[index] - nums[index + 1] \= 1，且locked[index] \= 0，那么就可以将nums[index]与nums[index + 1]交换。如果可以通过交换可以使得nums变为非降序的，那么就认为nums是可排序的。

现在可以对locked进行若干次操作，每次操作可以将locked中的某个locked[index]从1变为0，问最少需要执行多少次操作，才能让nums变为可排序的。若不可能，则返回-1。

题目中交换的规则要求相邻元素之差为1，也就意味着3不能和1直接进行交换。更进一步的，如果nums中存在某个3出现在某个1的左侧，那么这个3是不可能交换到1的右侧去的，也就是说不可能让nums变为可排序的，这种情况应该直接返回-1。

基于这一点，nums的组成就可以认为是左侧一部分1，加上右侧一部分3，然后2可以穿插在nums中的任意位置。为了让nums变为非降序，就需要将1左侧所有的2都交换到1的后面，也就是说需要将最右侧的1左边所有的2都交换过来，因此在这里需要保证第一个2的下标first_two到最后一个1的下标last_one之间的locked都为0；同样的，还需要将3右侧所有的2都交换到3的前面，也就是说需要将最左侧的3右边所有的2都交换过来，因此在这里需要保证第一个3的下标first_three到最后一个2的下标last_two之间的locked都为0。

根据上面的结论，就可以先对nums进行一趟遍历，分别记录最后一个1的下标last_one、第一个和最后一个2的下标first_two和last_two、以及第一个3的下标first_three。

接下来，若first_three小于last_one，说明有3在1的左侧，此时直接返回-1。否则从first_three到last_two以及first_two到last_one执行一趟遍历，将这些下标中locked为1的项修改为0并更新答案。需要注意依照题目中交换的规则，last_two以及last_one这两个位置是不用解锁的。

最后附上python代码：

```python
class Solution(object):
    def minUnlockedIndices(self, nums, locked):
        """
        :type nums: List[int]
        :type locked: List[int]
        :rtype: int
        """
        
        first_three = None
        first_two = None
        last_two = None
        last_one = None
        for index, v in enumerate(nums):
            if v == 3 and first_three is None:
                first_three = index
            if v == 2:
                if first_two is None:
                    first_two = index
                last_two = index
            if v == 1:
                last_one = index
        
        if first_three is not None and last_one is not None and first_three < last_one:
            return -1
        
        res = 0
        if first_three is not None and last_two is not None:
            for index in range(first_three, last_two):
                if locked[index] == 1:
                    locked[index] = 0
                    res += 1
        
        if first_two is not None and last_one is not None:
            for index in range(first_two, last_one):
                if locked[index] == 1:
                    res += 1
        
        return res
```

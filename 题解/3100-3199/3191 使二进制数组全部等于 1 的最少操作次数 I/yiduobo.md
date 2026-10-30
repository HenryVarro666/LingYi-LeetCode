---
title: "3191. 使二进制数组全部等于1的最少操作次数I"
aliases: ["yiduobo的每日leetcode 3191.使二进制数组全部等于1的最少操作次数I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/bit-manipulation", "leetcode/simulation", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/706510980"
zhihu_id: "706510980"
zhihu_title: "yiduobo的每日leetcode 3191.使二进制数组全部等于1的最少操作次数I"
question_id: "3191"
question: "使二进制数组全部等于 1 的最少操作次数 I"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-binary-array-elements-equal-to-one-i/"
difficulty: "Medium"
rating: 1312
created: "2024-07-02T04:05:27+08:00"
updated: "2024-07-02T04:05:27+08:00"
upvotes: 1
comments: 0
---

# 3191. 使二进制数组全部等于1的最少操作次数I

> **[yiduobo的每日leetcode 3191.使二进制数组全部等于1的最少操作次数I](https://zhuanlan.zhihu.com/p/706510980) · 知乎 · 2024-07-02 · 赞同 1**
> 力扣：[3191. 使二进制数组全部等于 1 的最少操作次数 I](https://leetcode.cn/problems/minimum-operations-to-make-binary-array-elements-equal-to-one-i/) · Medium · 灵茶山艾府：[从左到右修改，附证明（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3191.使二进制数组全部等于1的最少操作次数I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-operations-to-make-binary-array-elements-equal-to-one-i/description/)

题目给出一个二进制数组nums，每一轮操作可以选择其中任意三个连续的元素，将这三个元素反转，问最少需要多少次操作可以使得nums变为全1。若做不到，则返回-1。

对于同一个起点位置，其要么不执行操作，要么只执行一次操作，因为对同一个起点执行偶数次操作相当于什么都没干。另一方面，对于下标0而言，只有在选择以0为起点的操作时才能修改其数值，在处理完下标0之后，由于以某个下标为起点的操作不应该执行多次，那么此时想要修改下标1的值就不应该回过头去再以0为起点执行操作，而是只能执行以1为起点的操作。接下来对于下标2也是类似，只能执行以2为起点的操作，以此类推。于是只需一趟遍历，若当前位置的数需要修改，就以当前位置为起点执行操作。

需要注意的是，按照上面的操作方法数组的最后两个数只能被动修改，因此若最终数组的最后两个数不都为1，那么答案就是-1。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 0

        for index in range(0, len(nums) - 2):
            if nums[index] == 0:
                nums[index + 1] ^= 1
                nums[index + 2] ^= 1
                res += 1
        
        if nums[-1] == 0 or nums[-2] == 0:
            return -1
        return res
```

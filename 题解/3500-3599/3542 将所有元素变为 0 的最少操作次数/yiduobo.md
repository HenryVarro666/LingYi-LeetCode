---
title: "3542. 将所有元素变为0的最少操作次数"
aliases: ["yiduobo的每日leetcode 3542.将所有元素变为0的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/greedy", "leetcode/monotonic-stack", "题单/单调栈", "题单/单调栈/一-单调栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1907587231029400449"
zhihu_id: "1907587231029400449"
zhihu_title: "yiduobo的每日leetcode 3542.将所有元素变为0的最少操作次数"
question_id: "3542"
question: "将所有元素变为 0 的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-convert-all-elements-to-zero/"
difficulty: "Medium"
rating: 1890
created: "2025-05-19T22:32:12+08:00"
updated: "2025-05-19T22:32:12+08:00"
upvotes: 2
comments: 0
---

# 3542. 将所有元素变为0的最少操作次数

> **[yiduobo的每日leetcode 3542.将所有元素变为0的最少操作次数](https://zhuanlan.zhihu.com/p/1907587231029400449) · 知乎 · 2025-05-19 · 赞同 2**
> 力扣：[3542. 将所有元素变为 0 的最少操作次数](https://leetcode.cn/problems/minimum-operations-to-convert-all-elements-to-zero/) · Medium · 灵茶山艾府：[从分治到单调栈，简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3542.将所有元素变为0的最少操作次数

[3542. 将所有元素变为 0 的最少操作次数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-operations-to-convert-all-elements-to-zero/description/)

题目给出一个大小为n的非负整数数组nums，现在要求对其执行若干次操作，直到其中所有元素都变为0。

每次操作中，可以任选一个子数组[i, j]，将子数组中所有的最小非负整数都变为0。

问最少需要执行多少次操作。

首先可以明确的是，每次操作中选取的子数组不能存在0，否则操作的对象就变成0了。

另一方面，为了使得操作次数最少，就应该尽量在一次操作中将多个相同的非0元素变为0。而为了同时消除两个相同的元素x，一个前提条件就是这两个x之间不能存在小于x的元素y，否则由于y的存在，最终操作的对象就不可能是x。

更进一步的，对于数组中的某个元素nums\[index\]，不妨设其下一个更小的元素下标为f\[index\]，而下一个nums\[index\]出现的下标为nxt\[index\]，那么当f\[index\] \< nxt\[index\]时，就说明nums\[index\]以及nums\[nxt\[index\]\]这两个相同元素之间存在小于nums\[index\]的元素nums\[f\[index\]\]，因此这两个元素就不可能在同一次操作中消除。这样一来，就需要一次操作来消除nums\[index\]，而对于nums\[nxt\[index\]\]，则可以继续用这种方法考察其能否与nums\[nxt\[nxt\[index\]\]\]来消除掉，以此类推。

这样一来，就可以通过一趟遍历，计算数组nxt，同时利用单调栈计算数组f。得到nxt以及f后，只需再进行一趟遍历，对于当前遍历到的nums[index]，若其不为0，且nxt[index]不存在，或者f[index] \< nxt[index]，那么就必须使用一次操作来消除掉nums[index]，此时将答案加上1即可。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        n = len(nums)

        f = [None] * n
        stack = []
        last = {}
        nxt = [None] * n
        for index in range(n):
            while stack and nums[stack[-1]] > nums[index]:
                f[stack.pop()] = index
            
            stack.append(index)
        
            if nums[index] in last:
                nxt[last[nums[index]]] = index
            last[nums[index]] = index
        
        res = 0
        for index in range(n):
            if nums[index] > 0 and nxt[index] is None or (f[index] is not None and f[index] < nxt[index]):
                res += 1
        
        return res
```

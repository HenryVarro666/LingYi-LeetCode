---
title: "3576. 数组元素相等转换"
aliases: ["yiduobo的每日leetcode 3576.数组元素相等转换"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/enumeration", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1937284160956924551"
zhihu_id: "1937284160956924551"
zhihu_title: "yiduobo的每日leetcode 3576.数组元素相等转换"
question_id: "3576"
question: "数组元素相等转换"
problem_url: "https://leetcode.cn/problems/transform-array-to-all-equal-elements/"
difficulty: "Medium"
rating: 1489
created: "2025-08-08T23:05:07+08:00"
updated: "2025-08-08T23:05:07+08:00"
upvotes: 0
comments: 0
---

# 3576. 数组元素相等转换

> **[yiduobo的每日leetcode 3576.数组元素相等转换](https://zhuanlan.zhihu.com/p/1937284160956924551) · 知乎 · 2025-08-08 · 赞同 0**
> 力扣：[3576. 数组元素相等转换](https://leetcode.cn/problems/transform-array-to-all-equal-elements/) · Medium · 灵茶山艾府：[两种情况：都变成 1 或者都变成 -1（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3576.数组元素相等转换

[3576. 数组元素相等转换 - 力扣（LeetCode）](https://leetcode.cn/problems/transform-array-to-all-equal-elements/description/)

题目给出一个大小为n的整数数组nums，其中只包含1和-1。

另外给出一个整数k，表示可以执行最多k次操作。每次操作中，可以从0到n - 2中选取一个下标index，将nums[index]以及nums[index + 1]同时乘以-1。相同的下标index可以选择多次。

问能否在最多k次操作后将数组的所有元素变为相等。

由于数组中仅有1和-1这两种元素，因此可以分别考虑能否将数组全部变为1或者全部变为-1。对于这两种情况，检测的方法是完全相同的，因此在这里不妨设准备将数组中的所有元素都变为target，考虑应该如何执行操作。

题目中操作可以修改的是nums[index]以及nums[index + 1]，也就是说nums[0]如果不等于target，只能选择下标0执行一次操作，而如果nums[0]一开始就等于target，或者通过操作等于target后，之后就不应该再对下标0进行操作了。更进一步的，之前已经遍历过的下标就不应该再次修改，因此在这里就只需从左向右进行一趟遍历，若当前下标index对应的nums[index]不等于target，那么就必须对target执行一次操作，将nums[target]以及nums[target + 1]都取反。若遍历过程中出现了操作次数不够用，或者遍历完成后nums[n - 1]不等于target，那么就说明无法将nums都变为target。

另外，对于nums中某个不等于targer的下标nums[index]，若修改了nums[index]，说明也修改了nums[index + 1]。若nums[index + 1]一开始等于target，那么在这次修改之后其就不等于target了，需要对index + 1再执行一次操作，而这次操作在将nums[index + 1]修正为target之后还会修改nums[index + 2]，也就是说在这里通过两次操作修改了nums[index]以及nums[index + 2]。更进一步的，这个操作可以继续向后推，即使用t次操作修改nums[index]以及nums[index + t]。

基于这一点，遍历时就无需真的修改nums中的元素值，而是使用两个指针p和q从左向右遍历。先找出最左侧的不等于target的元素nums[p]，然后q从p + 1开始向后遍历找出第二个不等于target的元素nums[q]，然后使用q - p的代价将这两个元素反转，再将p迭代到q + 1继续向后寻找，重复此过程直到找不到对应的p。若过程中q - p大于剩下的操作次数，或者只能找到p却找不到q，那么就说明无法将nums都变为target。

最后附上python代码：

```python
class Solution(object):
    def canMakeEqual(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: bool
        """
        
        def check(target):
            p = 0
            need = 0
            while p < len(nums):
                while p < len(nums) and nums[p] != target:
                    p += 1
                if p == len(nums):
                    return True
                
                q = p + 1
                while q < len(nums) and nums[q] != target:
                    q += 1
                
                if q == len(nums):
                    return False
                
                need += q - p
                if need > k:
                    return False
                p = q + 1

            return True
    
        return check(1) or check(-1)
```

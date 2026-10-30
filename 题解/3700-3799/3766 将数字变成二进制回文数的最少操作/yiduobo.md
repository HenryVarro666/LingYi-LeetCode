---
title: "3766. 将数字变成二进制回文数的最少操作"
aliases: ["yiduobo的每日leetcode 3766.将数字变成二进制回文数的最少操作"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/math", "leetcode/binary-search", "题单/位运算", "题单/数学算法", "题单/位运算/九-其他", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1981117321054540862"
zhihu_id: "1981117321054540862"
zhihu_title: "yiduobo的每日leetcode 3766.将数字变成二进制回文数的最少操作"
question_id: "3766"
question: "将数字变成二进制回文数的最少操作"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-binary-palindrome/"
difficulty: "Medium"
created: "2025-12-08T22:38:40+08:00"
updated: "2025-12-08T22:38:45+08:00"
upvotes: 1
comments: 0
---

# 3766. 将数字变成二进制回文数的最少操作

> **[yiduobo的每日leetcode 3766.将数字变成二进制回文数的最少操作](https://zhuanlan.zhihu.com/p/1981117321054540862) · 知乎 · 2025-12-08 · 赞同 1**
> 力扣：[3766. 将数字变成二进制回文数的最少操作](https://leetcode.cn/problems/minimum-operations-to-make-binary-palindrome/) · Medium · 灵茶山艾府：[两种非暴力做法：预处理 / O(1) 位运算（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3766.将数字变成二进制回文数的最少操作

[3766. 将数字变成二进制回文数的最少操作 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-operations-to-make-binary-palindrome/)

题目给出一个整数数组nums，其长度以及其中元素的大小都在1到5000之间。

对于其中每个元素nums[index]，可以将其加上1或者减去1任意次（也可以不执行任何操作）。

若一个元素的二进制表示中是回文串，那么就称这个数为二进制回文数。

现在要求计算对于nums中的每个元素nums[index]，将其变为二进制回文数所需的最少操作次数。

由于nums中元素的大小都不超过5000，那么可以先从1枚举到5000，检测其中的所有元素是否为二进制回文数，并将这些数记录下来，得到数组pali。

值得一提的是，在这里可以额外考虑一下5000往上得到的回文数。5000的二进制表示为1001110001000，那么往上的话需要变成1001110111001，也就是5049，可以将其添加到pali的末尾。

实际上，如果将5000向下，可以变成1001101011001，也就是4953，相比之下比5049是更好的，也就是说5049是无需考虑的。

接下来对于nums中的每个元素nums[index]，若其小于pali[0]，那么其对应的操作次数就是pali[0] - nums[index]，否则就可以在pali中二分，找到最大的，满足pali[p] \<\= nums[index]的下标p，那么其对应的操作次数就是nums[index] - pali[p]以及pali[p + 1] - nums[index]之间的较小值。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        
        pali = []
        for v in range(1, 5001):
            digits = []
            x = v
            while x:
                digits.append(x % 2)
                x //= 2
            
            left, right = 0, len(digits) - 1
            flag = True
            while left < right:
                if digits[left] != digits[right]:
                    flag = False
                    break
                left += 1
                right -= 1
            
            if flag:
                pali.append(v)
        
        pali.append(5049)

        res = []
        for v in nums:
            if v < pali[0]:
                res.append(pali[0] - v)
            else:
                left = 0
                right = len(pali) - 1
                while left < right:
                    mid = (left + right + 1) // 2
                    if pali[mid] <= v:
                        left = mid
                    else:
                        right = mid - 1
                
                res.append(min(v - pali[left], pali[left + 1] - v))
        
        return res
```

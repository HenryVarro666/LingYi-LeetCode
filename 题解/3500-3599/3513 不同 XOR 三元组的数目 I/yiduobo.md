---
title: "3513. 不同XOR三元组的数目I"
aliases: ["yiduobo的每日leetcode 3513.不同XOR三元组的数目I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/brainteaser", "题单/贪心算法", "题单/贪心算法/六-构造题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1902521353044751693"
zhihu_id: "1902521353044751693"
zhihu_title: "yiduobo的每日leetcode 3513.不同XOR三元组的数目I"
question_id: "3513"
question: "不同 XOR 三元组的数目 I"
problem_url: "https://leetcode.cn/problems/number-of-unique-xor-triplets-i/"
difficulty: "Medium"
rating: 1663
created: "2025-05-06T00:03:43+08:00"
updated: "2025-05-06T00:03:43+08:00"
upvotes: 1
comments: 0
---

# 3513. 不同XOR三元组的数目I

> **[yiduobo的每日leetcode 3513.不同XOR三元组的数目I](https://zhuanlan.zhihu.com/p/1902521353044751693) · 知乎 · 2025-05-06 · 赞同 1**
> 力扣：[3513. 不同 XOR 三元组的数目 I](https://leetcode.cn/problems/number-of-unique-xor-triplets-i/) · Medium · 灵茶山艾府：[构造题，O(1) 时间做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3513.不同XOR三元组的数目I

[3513. 不同 XOR 三元组的数目 I - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-unique-xor-triplets-i/description/)

题目给出一个长度为n的整数数组nums，其中nums是1到n的一个排列。

XOR三元组的定义为三个元素(nums[i], nums[j], nums[k])的异或值nums[i] XOR nums[j] XOR nums[k]，其中i \<\= j \<\= k。

问所有可能的不同XOR值的数量。

首先可以明确的是，不管怎样异或，且结果都不可能出现最高位之外的1。令p表示最小的大于n的2的幂，那么最终异或的结果必然落在0到p - 1之间。

接下来考察哪些异或值可以达成。

首先二进制表示中具有唯一的1，或者大于等于3个1的数都是很容易达成的。

对于前者，这个具有唯一的1的元素必然小于等于n，于是可以选择这个元素自身，以及两个1，三者异或即可。

对于后者，则可以将最高位的1分配给一个元素，即某个2的幂次，然后将剩下的1分配个两个元素，这三个元素都必然小于等于n。

然后是二进制表示中没有1，即异或结果为0是否可以达成。为了达成0，最简单的自然是一个二进制表示中有两个1的元素，异或两个二进制表示中分别具有一个对应的1的元素，例如(3, 2, 1)。但是当n \<\= 2时，由于数位不足，是无法得到0的。

最后是二进制表示中恰好有两个1的情况。对于这种情况，若这个元素本身小于等于n，那么就可以选择这个元素自身，配合两个1；反之若其大于n，则可以将最高位分配给一个元素，即某个2的幂次，然后将另一个1，以及将某个值为0的位修改为1分配给另一个元素，最后将这个被修改为1的位分配给最后的元素即可。

例如二进制为1001的元素，首先将最高位的1分配出去，得到二进制表示1000的元素。接下来对于另一个1，则可以将倒数第二位上的0修改为1，得到11，另外再来一个10，就可以使用二进制表示为(1000, 11, 10)的三个元素来达成。

需要注意的是，在分配第二个元素时，如果数位的长度不够，也会出现无法分配的情况。更具体的说，当n \<\= 3时，目标值为3时，就会出现位数不够的情况。不过对于n \= 3的情况，可以直接使用前一种方案，即选择(3, 1, 1)来达成3。而对于n >\= 4的情况，若目标值最高位x不是1，则可以采用第一种方案，直接使用(x, 1, 1)；若最高位为1，则可以使用第二种方案，因为此时除了最高位之外的位数至少还有两位，是足够使用的。

综合以上的结论，当n \<\= 2时，答案就是n，否则0到p - 1之间的所有元素都可以达成，答案就是p。

最后附上python代码：

```python
class Solution(object):
    def uniqueXorTriplets(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        if len(nums) <= 2:
            return len(nums)
        
        res = 1
        while res <= len(nums):
            res += res
        return res
```

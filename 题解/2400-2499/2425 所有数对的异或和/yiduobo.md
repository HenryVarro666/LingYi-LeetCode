---
title: "2425. 所有数对的异或和"
aliases: ["yiduobo的每日leetcode 2425.所有数对的异或和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "题单/位运算", "题单/位运算/四-拆位-/-贡献法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/582035598"
zhihu_id: "582035598"
zhihu_title: "yiduobo的每日leetcode 2425.所有数对的异或和"
question_id: "2425"
question: "所有数对的异或和"
problem_url: "https://leetcode.cn/problems/bitwise-xor-of-all-pairings/"
difficulty: "Medium"
rating: 1622
created: "2022-11-10T01:17:36+08:00"
updated: "2022-11-10T01:17:36+08:00"
upvotes: 0
comments: 0
---

# 2425. 所有数对的异或和

> **[yiduobo的每日leetcode 2425.所有数对的异或和](https://zhuanlan.zhihu.com/p/582035598) · 知乎 · 2022-11-10 · 赞同 0**
> 力扣：[2425. 所有数对的异或和](https://leetcode.cn/problems/bitwise-xor-of-all-pairings/) · Medium · 灵茶山艾府：[贡献法：讨论每个元素在答案中的出现次数](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2425.所有数对的异或和

[力扣](https://leetcode.cn/problems/bitwise-xor-of-all-pairings/)

设两个数组的长度分别为m和n，那么这两个数组两两取异或得到的新数组为

nums1[0] ^ nums2[0]，nums1[0] ^ nums2[1]，...，nums1[0] ^ nums2[n - 1]，

nums1[1] ^ nums2[0]，nums1[1] ^ nums2[1]，...，nums1[1] ^ nums2[n - 1]，

...

nums1[m - 1] ^ nums2[0]，nums1[m - 1] ^ nums2[1]，...，nums1[m - 1] ^ nums2[n - 1]

最终结果就是将上面这m \* n个数再异或起来。

观察可以发现，nums1中的数每个都出现了n次，而nums2中的数则出现了m次。由于异或满足交换律，那么在计算最终结果时完全可以先将相同的数放在一起异或，然后这些异或的结果异或起来。

又由于x ^ x \= 0，那么当n为偶数时，nums1中的数各自异或的结果都为0，而当n为奇数时，nums1中的数各自异或的结果则为这个数自身。同样的，当m为偶数时，nums2中的数得到的结果为0，否则就是num2中的数自身。那么只需根据n和m的奇偶性就可以判断最后剩下哪些异或结果将参与参与最终的异或运算，此时只需按部就班将这些数异或起来即可。

最后附上python代码：

```python
class Solution(object):
    def xorAllNums(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """

        m = len(nums1)
        n = len(nums2)

        res = 0
        if n % 2 == 1:
            for num in nums1:
                res ^= num
            
        if m % 2 == 1:
            for num in nums2:
                res ^= num

        return res
```

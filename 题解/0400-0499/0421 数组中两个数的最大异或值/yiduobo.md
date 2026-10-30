---
title: "421. 数组中两个数的最大异或值"
aliases: ["yiduobo的每日leetcode 421.数组中两个数的最大异或值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/bit-manipulation", "leetcode/hash-table", "题单/常用数据结构", "题单/位运算", "题单/常用数据结构/六-字典树-trie", "题单/位运算/五-试填法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/193156822"
zhihu_id: "193156822"
zhihu_title: "yiduobo的每日leetcode 421.数组中两个数的最大异或值"
question_id: "421"
question: "数组中两个数的最大异或值"
problem_url: "https://leetcode.cn/problems/maximum-xor-of-two-numbers-in-an-array/"
difficulty: "Medium"
rating: 2000
created: "2020-08-21T23:54:37+08:00"
updated: "2020-08-21T23:54:37+08:00"
upvotes: 0
comments: 0
---

# 421. 数组中两个数的最大异或值

> **[yiduobo的每日leetcode 421.数组中两个数的最大异或值](https://zhuanlan.zhihu.com/p/193156822) · 知乎 · 2020-08-21 · 赞同 0**
> 力扣：[421. 数组中两个数的最大异或值](https://leetcode.cn/problems/maximum-xor-of-two-numbers-in-an-array/) · Medium · 灵茶山艾府：[【图解】简洁高效，一图秒懂！（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

421.数组中两个数的最大异或值<https://leetcode-cn.com/problems/maximum-xor-of-two-numbers-in-an-array/>

看到异或操作，很自然就想到了位运算。那么要求这个异或的最大值，可以首先计算出各个数在二进制下的位数l，那么最大可能的答案就是1111...111共max(l)个1。

那么我们可以从高位开始向下枚举，首先设答案的最高位为1，那么遍历所有数，取这些数二进制下的最高位，如果存在两个数的最高位异或等于1，说明答案的最高位可能为1，否则答案的最高位必然为0。接下来往后依次处理第二位，第三位等。

对于判断前m位是否能通过异或得到答案，可以通过set在O(n)的时间复杂度内完成。例如对于nums[i]，首先通过右移操作获取到其最高的m位，设为prefix。将这些prefix存在一个set中，那么对于set中的所有prefix，若存在一个prefix，满足prefix ^ now_ans也在set中，那么说明存在两个数的最高m位在异或后可以形成now_ans。

由于每个数满足小于2^31，因此最多计算31轮，每轮的时间复杂度都为O(n)，因此最终的时间复杂度可以认为是O(n)。

最后附上python代码：

```python
class Solution(object):
    def findMaximumXOR(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        max_num = max(nums)
        if max_num == 0:
            return 0

        l = 0
        while max_num:
            l += 1
            max_num >>= 1

        res = 0
        for index in range(l, -1, -1):
            res <<= 1
            now = res | 1
            prefix_set = set()
            for num in nums:
                prefix_set.add(num >> index)
            
            for prefix in prefix_set:
                if now ^ prefix in prefix_set:
                    res = now
                    break

        return res
```

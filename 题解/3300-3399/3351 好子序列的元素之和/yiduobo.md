---
title: "3351. 好子序列的元素之和"
aliases: ["yiduobo的每日leetcode 3351.好子序列的元素之和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/26396797619"
zhihu_id: "26396797619"
zhihu_title: "yiduobo的每日leetcode 3351.好子序列的元素之和"
question_id: "3351"
question: "好子序列的元素之和"
problem_url: "https://leetcode.cn/problems/sum-of-good-subsequences/"
difficulty: "Hard"
rating: 2086
created: "2025-02-26T01:47:57+08:00"
updated: "2025-02-26T01:47:57+08:00"
upvotes: 2
comments: 0
---

# 3351. 好子序列的元素之和

> **[yiduobo的每日leetcode 3351.好子序列的元素之和](https://zhuanlan.zhihu.com/p/26396797619) · 知乎 · 2025-02-26 · 赞同 2**
> 力扣：[3351. 好子序列的元素之和](https://leetcode.cn/problems/sum-of-good-subsequences/) · Hard · 灵茶山艾府：[子序列计数 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3351.好子序列的元素之和

[3351. 好子序列的元素之和 - 力扣（LeetCode）](https://leetcode.cn/problems/sum-of-good-subsequences/)

题目给出一个整数数组nums，定义好子序列为子序列中任意两个连续元素的绝对值之差恰好为1，另外长度为1的子序列也默认为好子序列。现在要求找出nums中所有的好子序列的元素之和。

题目的数据规模比较大，找出所有的好子序列然后求和显然是不行的。对于这类求全体之和的题目，一种常见的思路是共享法。对于本题，就是对于nums中的每个元素nums[index]，可以先想办法计算出包含nums[index]的好子序列的数量，然后二者相乘就是nums[index]对最终答案的贡献，问题就转化成了如何高效计算包含每个nums[index]的好子序列的数量。

---

对于nums[index]，如果将其视为分割点，那么所有包含nums[index]的好子序列就可以切分为以nums[index]结尾的好子序列left，以及以nums[index]开头的好子序列right，在nums[index]这个位置拼接起来，最终可以得到的好子序列数量就是left \* right。而对于left以及right，则可以通过动态规划来求解。

令left[index]表示以nums[index]结尾的好子序列数量，对于left[index]，可以让nums[index]单独形成新的子序列，同时也可以将nums[index]拼在index左侧的所有以nums[index] - 1或者以nums[index] + 1的子序列的末尾，因此在这里还需要使用一个哈希表cnt，其中cnt[v]表示到index - 1为止以v结尾的好子序列的数量。那么对于left[index]，首先可以更新

left[index] \= cnt[nums[index] - 1] + cnt[nums[index] + 1] + 1

其中前两项分别表示将nums[index]拼接在到index - 1为止，以nums[index] - 1和nums[index] + 1为结尾的好子序列的数量，最后这一项1则表示nums[index]单独形成好子序列

在得到left[index]后，则可以利用left[index]更新cnt，即

cnt\[nums\[index\]\] \= cnt\[nums\[index\]\] + left\[index\]

这样一来，一趟遍历就能得到left。

由于right和left是完全对称的，在这里只需从后往前一趟遍历，使用相同的方法就能得到right。

得到left和right后，根据最开始关于贡献法的讨论，只需一趟遍历，将nums[index] \* left[index] \* right[index]累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def sumOfGoodSubsequences(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        mod = 10 ** 9 + 7
        n = len(nums)

        left = [1]
        cnt = {nums[0] : 1}
        for v in nums[1:]:
            left.append((cnt.get(v - 1, 0) + cnt.get(v + 1, 0) + 1) % mod)
            cnt[v] = (cnt.get(v, 0) + left[-1]) % mod
        
        right = [1]
        cnt = {nums[-1] :1}
        for v in nums[-2::-1]:
            right.append((cnt.get(v - 1, 0) + cnt.get(v + 1, 0) + 1) % mod)
            cnt[v] = (cnt.get(v, 0) + right[-1]) % mod
        right.reverse()

        res = 0
        for index, v in enumerate(nums):
            res = (res + left[index] * right[index] % mod * v % mod) % mod
        
        return res
```

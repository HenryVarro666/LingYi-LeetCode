---
title: "41. 缺失的第一个正数"
aliases: ["yiduobo的每日leetcode 41.缺失的第一个正数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/滑动窗口与双指针", "题单/LeetCode-热题-100", "题单/滑动窗口与双指针/三-单序列双指针", "题单/LeetCode-热题-100/普通数组"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/123349136"
zhihu_id: "123349136"
zhihu_title: "yiduobo的每日leetcode 41.缺失的第一个正数"
question_id: "41"
question: "缺失的第一个正数"
problem_url: "https://leetcode.cn/problems/first-missing-positive/"
difficulty: "Hard"
created: "2020-04-02T21:35:13+08:00"
updated: "2020-04-02T21:35:13+08:00"
upvotes: 0
comments: 0
---

# 41. 缺失的第一个正数

> **[yiduobo的每日leetcode 41.缺失的第一个正数](https://zhuanlan.zhihu.com/p/123349136) · 知乎 · 2020-04-02 · 赞同 0**
> 力扣：[41. 缺失的第一个正数](https://leetcode.cn/problems/first-missing-positive/) · Hard · 灵茶山艾府：[O(n) 换座位，通过例子理解算法思想（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

41.缺失的第一个正数<https://leetcode-cn.com/problems/first-missing-positive/>

类似于哈希表思路的题目。这里要找缺失的最小正数，那么对于一个长度为n的数组，假设里面1到n全有了，那么答案就是n + 1。如果1到n不全，那么答案就是其中缺失的最小的数。由此可得答案一定是出现在1到n + 1之间的，且如果长度为n的数组nums里面存在大于n的数，那么由鸽笼原理1到n之间至少有一个缺了，因此我们实际上只要考察nums中的1到n，对于负数或大于n的数都无需考虑。

于是我们可以设计一个哈希数组，其中hash[x] \= x + 1，然后将nums中1到n的数填进去，最后扫描0到n - 1，如果hash[k]不存在，说明nums中不存在k + 1，因此最后的答案就是k + 1，否则的话就是n + 1。

另外，考虑到题目要求常数的空间，意味着我们需要想办法hash覆盖到nums上去，一个可行的思路是从头开始扫描nums，设当前的nums[index] \= p。如果p在1到n之间，且p !\= index + 1，说明p不应该放在当前位置上，于是我们可以交换nums[p - 1]与nums[index]，将p归位。当然，这里有个前提条件是此时的nums[p - 1]不等于p，即如果nums中存在多个p，且其中某个p处在正确的位置上，那么就不应该继续移动p了。

虽然这样看上去是平方的复杂度，但是实际上因为每次交换都能使一个数归位，那么n个数最多执行n - 1次交换后就都归位了，实际上还是O(n)的复杂度。

最后附上python代码：

```python
class Solution(object):
    def firstMissingPositive(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        for index in range(len(nums)):
            while nums[index] > 0 and nums[index] <= len(nums) and nums[index] - 1 != index and nums[nums[index] - 1] != nums[index]:
                tmp = nums[index]
                nums[index] = nums[tmp - 1]
                nums[tmp - 1] = tmp

        for index in range(len(nums)):
            if nums[index] -1 != index:
                return index + 1
        return len(nums) + 1
```

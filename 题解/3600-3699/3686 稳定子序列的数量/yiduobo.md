---
title: "3686. 稳定子序列的数量"
aliases: ["yiduobo的每日leetcode 3686.稳定子序列的数量"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1955317060742678218"
zhihu_id: "1955317060742678218"
zhihu_title: "yiduobo的每日leetcode 3686.稳定子序列的数量"
question_id: "3686"
question: "稳定子序列的数量"
problem_url: "https://leetcode.cn/problems/number-of-stable-subsequences/"
difficulty: "Hard"
rating: 1969
created: "2025-09-27T17:50:40+08:00"
updated: "2025-09-27T17:50:58+08:00"
upvotes: 2
comments: 0
---

# 3686. 稳定子序列的数量

> **[yiduobo的每日leetcode 3686.稳定子序列的数量](https://zhuanlan.zhihu.com/p/1955317060742678218) · 知乎 · 2025-09-27 · 赞同 2**
> 力扣：[3686. 稳定子序列的数量](https://leetcode.cn/problems/number-of-stable-subsequences/) · Hard · 灵茶山艾府：[合法子序列 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3686.稳定子序列的数量

[3686. 稳定子序列的数量 - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-stable-subsequences/description/)

题目给出一个整数数组nums，若一个子序列中不存在连续三个元素奇偶性相同，就称这个子序列为稳定子序列。问非空的稳定子序列数目。

题目要求生成的子序列中不存在奇偶性相同的三个连续元素，也就是说在考虑往子序列中添加新的元素时，只需要考虑添加的元素的奇偶性，以及子序列中最后两个元素的奇偶性，就能判断能否将这个元素加入到子序列中。于是可以用odd_odd[index]、odd_even[index]、even_odd[index]以及even_even[index]来分别表示nums[0]到nums[index]中：

odd_odd[index]：以两个奇数结尾的稳定子序列数目

odd_even[index]：倒数第二个元素是奇数，倒数第一个元素是偶数的稳定子序列数目

even_odd[index]：倒数第二个元素是偶数，倒数第一个元素是奇数的稳定子序列数目

even_even[index]：以两个偶数结尾的稳定子序列数目

当然，长度为2的子序列是不可能凭空出现，再此之前必须有长度为1的子序列，因此还需要使用odd[index]以及even[index]分别表示nums[0]到nums[index]中奇数以及偶数的数目。

接下来对于nums[index]：

1、若nums[index]为奇数：

1-1）首先对于odd和even：

odd[index] \= odd[index - 1] + 1

even[index] \= even[index - 1]

1-2）接下来对于odd_even和even_even：

由于最后一个元素需要为偶数，因此无法将nums[index]加入到这两个子序列中，因此有

odd_even[index] \= odd_even[index - 1]

even_even[index] \= even_even[index - 1]

1-3）对于odd_odd以及even_odd：

此时同样可以选择放弃掉nums[index]，而如果要加入nums[index]：

对于odd_odd，要么从最后一个元素为奇数的子序列转移过来，要么从在单个奇数的基础上，添加nums[index]得到长度为2的子序列。需要特别注意的是，由于题目限制了子序列的最后三个元素不能同为奇数，因此odd_odd只能从even_odd或者odd转移过来，如果在odd_odd的基础上再添加nums[index]，最后三个元素就同为奇数了。于是有：

odd_odd[index] \= odd_odd[index - 1] + (even_odd[index - 1] + odd[index - 1])

对于even_odd，则没有最后三个元素奇偶性的限制，因为even_odd自身就意味着最后三个元素不可能同奇偶，因此even_odd可以从所有以even结尾的子序列转移过来，也可以在单个偶数的基础上添加nums[index]得到长度为2的子序列。于是有：

even_odd[index] \= even_odd[index - 1] + (even_even[index - 1] + odd_even[index - 1] + even[index - 1])

2、若nums[index]为偶数：

此时各种情况与nums[index]为奇数时完全对称，有

odd[index] \= odd[index - 1]

even[index] \= even[index - 1] + 1

odd_odd[index] \= odd_odd[index - 1]

even_odd[index] \= even_odd[index - 1]

even_even[index] \= even_even[index - 1] + (odd_even[index - 1] + even[index - 1])

odd_even[index] \= odd_even[index - 1] + (odd_odd[index - 1] + even_odd[index - 1] + odd[index - 1])

全部计算完成后，所有长度大于等于2的稳定子序列数目就是odd_odd[-1]、odd_even[-1]、even_even[-1]、even_odd[-1]之和，而所有长度为1的子序列都是平衡子序列，因此在这个基础上再加上nums的长度即为最终答案。

注意到上面的状态转移方程都只与上一轮的状态有关，因此可以使用变量迭代省去所有的数组开销。需要特别注意的是，使用变量迭代时需要先更新依赖别人的项，再更新被依赖的项。在本题中，需要先更新odd_odd或者even_even，然后再更新其他两项。

最后附上python代码：

```python
class Solution(object):
    def countStableSubsequences(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        odd = 0
        even = 0
        odd_odd = 0
        odd_even = 0
        even_odd = 0
        even_even = 0
        mod = 10 ** 9 + 7

        for v in nums:
            if v % 2 == 0:
                even_even = (even_even + even + odd_even) % mod
                odd_even = (odd_even + odd + even_odd + odd_odd) % mod
                even += 1
            else:
                odd_odd = (odd_odd + odd + even_odd) % mod
                even_odd = (even_odd + even + odd_even + even_even) % mod
                odd += 1

        return (len(nums) + odd_odd + odd_even + even_odd + even_even) % mod
```

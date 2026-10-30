---
title: "3868. 通过交换使数组相等的最小花费"
aliases: ["yiduobo的每日leetcode 3868.通过交换使数组相等的最小花费"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/hash-table", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2017789464152417542"
zhihu_id: "2017789464152417542"
zhihu_title: "yiduobo的每日leetcode 3868.通过交换使数组相等的最小花费"
question_id: "3868"
question: "通过交换使数组相等的最小花费"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-equalize-arrays-using-swaps/"
difficulty: "Medium"
rating: 1579
created: "2026-03-19T02:44:15+08:00"
updated: "2026-03-19T02:44:18+08:00"
upvotes: 1
comments: 1
---

# 3868. 通过交换使数组相等的最小花费

> **[yiduobo的每日leetcode 3868.通过交换使数组相等的最小花费](https://zhuanlan.zhihu.com/p/2017789464152417542) · 知乎 · 2026-03-19 · 赞同 1**
> 力扣：[3868. 通过交换使数组相等的最小花费](https://leetcode.cn/problems/minimum-cost-to-equalize-arrays-using-swaps/) · Medium · 灵茶山艾府：[等价转化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3868.通过交换使数组相等的最小花费

<https://leetcode.cn/problems/minimum-cost-to-equalize-arrays-using-swaps/description/>

题目给出两个大小为n的整数数组nums1和nums2。

现在可以对这两个数组进行任意次操作，每次操作中：

- 可以在同一个数组中选择两个下标i和j，然后交换nums1[i]和nums1[j]，或者交换nums2[i]和nums[j]。这个操作是免费的。
- 可以在两个数组之间进行交换，选择下标i，交换nums1[i]和nums2[i]。这个操作的花费为1。

问最少需要多少花费，才能使得nums1和num2变得相同。若做不到，则返回-1。

首先，由于同组交换是免费的，因此在这里无需关心组内元素的相对顺序，而只需要关心两个数组中每种元素出现的次数就行了。

接下来，若某个元素在两个数组中出现次数之和为奇数，那么答案必然为-1，因为不可能使得两个数组中该元素出现的次数相同。

若每个元素在两个数组中出现次数之和为偶数，那么在抵消掉nums1和nums2中相同的元素后，对于nums1和nums2中剩下的元素，这些元素出现的次数必然都是偶数次。另一方面，由于nums1和nums2长度相同，因此剩下的元素的数量也必然相同，此时只需将nums1中每种剩余元素的一半，与nums2中每种剩余元素的一半进行交换就行了，总的花费恰好是剩余数组长度的一半。

基于上面的结论，就可以使用一个哈希表cnt记录每种元素在nums1中出现次数与nums2中出现次数之差，然后分别遍历nums1和nums2。对于nums1中的每个元素v，将cnt[v]加上1，而对于nums2中的每个元素v，将cnt[v]减去1。

遍历完成后，再遍历cnt中所有的v，若cnt[v]是奇数，那么直接返回-1，否则若cnt[v]大于0，则将cnt[v] // 2累加到答案中，表示将nums1中剩余的v的一半交换到nums2中。在这里无需考虑与剩余nums2的哪些元素进行交换，因为若所有的cnt[v]都为偶数，那么根据上面的结论，必然有对应的元素可以进行交换。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """
        
        cnt = {}
        for v in nums1:
            cnt[v] = cnt.get(v, 0) + 1
        for v in nums2:
            cnt[v] = cnt.get(v, 0) - 1
        
        res = 0
        for v in cnt:
            if cnt[v] % 2 == 1:
                return -1
            if cnt[v] > 0:
                res += cnt[v] // 2

        return res
```

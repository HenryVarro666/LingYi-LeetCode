---
title: "3859. 统计包含K个不同整数的子数组"
aliases: ["yiduobo的每日leetcode 3859.统计包含K个不同整数的子数组"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2013781247449641398"
zhihu_id: "2013781247449641398"
zhihu_title: "yiduobo的每日leetcode 3859.统计包含K个不同整数的子数组"
question_id: "3859"
question: "统计包含 K 个不同整数的子数组"
problem_url: "https://leetcode.cn/problems/count-subarrays-with-k-distinct-integers/"
difficulty: "Hard"
rating: 2302
created: "2026-03-08T23:35:30+08:00"
updated: "2026-03-08T23:35:35+08:00"
upvotes: 0
comments: 0
---

# 3859. 统计包含K个不同整数的子数组

> **[yiduobo的每日leetcode 3859.统计包含K个不同整数的子数组](https://zhuanlan.zhihu.com/p/2013781247449641398) · 知乎 · 2026-03-08 · 赞同 0**
> 力扣：[3859. 统计包含 K 个不同整数的子数组](https://leetcode.cn/problems/count-subarrays-with-k-distinct-integers/) · Hard · 灵茶山艾府：[恰好型滑动窗口（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3859.统计包含K个不同整数的子数组

<https://leetcode.cn/problems/count-subarrays-with-k-distinct-integers/description/>

题目给出一个整数数组nums以及两个整数k和m。

现在要求返回一个整数，表示满足一下条件的子数组的数量：

- 子数组中恰好包含k个不同的整数
- 子数组中每个不同的整数都出现至少m次

题目要求计算满足条件的子数组数目，在这里可以将这个计算拆分成两个部分。对于每个左边界index：

1、首先找出最大的右边界p1，满足index到p1 - 1这一段中恰好出现了k个不同的整数

2、接下来在index到p1之间，找出最小的右边界p2，满足index到p2 - 1这一段中出现至少m次的整数有k个

3、若存在合法的p1和p2，那么所有左边界为index，右边界在p2 - 1到p1 - 1之间的子数组都是符合题目要求的子数组。理由是由于计算p1的限制，从index到p2 - 1这一段中最多只会出现k个元素，由于计算p2的限制，恰好就是这k个元素都出现了至少m次，因此从index到p2 - 1这一段是一个合法的子数组。对于p2到p1 - 1这一段中的所有元素，由于计算p1的限制，这些元素都是之前的k种元素之一，因此将这些元素添加到子数组后，子数组依然是合法的。这些子数组一共有p2 - p1 + 1个，需要将p2 - p1 + 1累加到答案中。

对于第一个部分，使用哈希表配合变长滑动窗口就能很容易求解。具体来说，使用一个哈希表freq1记录从index到p1 - 1的窗口中每种元素出现的次数，那么对于当前的nums\[p1\]，若其出现在哈希表中，或者当前哈希表的长度小于k，就可以将nums\[p1\]加入到当前窗口中。此时需要更新freq1\[nums\[p1\]\]，并将p1向后移动。

重复此过程直到p1来到数组末尾，或者freq1中有k个元素，且nums[p1]没在freq1中出现过位置。

接下来对于第二个部分，同样是使用哈希表配合变长滑动窗口求解。具体来说，使用另一个哈希表freq2记录从index到p2 - 1的窗口中每种元素出现的次数，同时使用一个变量cnt记录当前窗口中出现次数至少为m次的元素数量，那么对于当前的nums\[p2\]，若cnt \< k，那么就将其加入到窗口中，此时需要更新freq2\[nums\[p2\]\]，并将p2向后移动。若freq2\[nums\[p2\]\]在本次操作后恰好等于m，就说明在本次扩展后，nums\[p2\]在窗口中出现的次数达到了m次，此时应该将cnt也加上1。

重复此过程直到p2来到p1，或者cnt等于k为止。

接下来，若cnt等于k，说明存在合法的p1和p2，此时将p1 - p2 + 1累加到答案中。

处理完右边界后，还需要将左边界index向后移动。此时需要将freq1\[nums\[index\]\]和freq2\[nums\[index\]\]都减去1。若此次操作后freq1\[nums\[index\]\]变为0，说明窗口中没有nums\[index\]了，此时应该将其从freq1中弹出；若此次操作后freq2\[nums\[index\]\]等于m - 1，说明窗口中nums\[index\]的出现次数从m次变成了m - 1次，此时应该将cnt减去1。

最后附上python代码：

```python
class Solution(object):
    def countSubarrays(self, nums, k, m):
        """
        :type nums: List[int]
        :type k: int
        :type m: int
        :rtype: int
        """
        
        freq1 = {}
        freq2 = {}
        cnt = 0
        p1 = 0
        p2 = 0
        res = 0

        n = len(nums)
        for index, v in enumerate(nums):
            while p1 < n and (len(freq1) < k or (len(freq1) == k and nums[p1] in freq1)):
                freq1[nums[p1]] = freq1.get(nums[p1], 0) + 1
                p1 += 1
            
            while p2 < p1 and cnt < k:
                freq2[nums[p2]] = freq2.get(nums[p2], 0) + 1
                if freq2[nums[p2]] == m:
                    cnt += 1
                p2 += 1
            
            if cnt == k:
                res += p1 - p2 + 1

            freq1[v] -= 1
            if freq1[v] == 0:
                freq1.pop(v)
            
            freq2[v] -= 1
            if freq2[v] == m - 1:
                cnt -= 1
            
        return res
```

---
title: "3934. 最短唯一子数组"
aliases: ["yiduobo的每日leetcode 3934.最短唯一子数组"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/suffix-array", "题单/字符串", "题单/字符串/四-字符串哈希", "题单/字符串/八-后缀数组/后缀自动机"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2042067184655000118"
zhihu_id: "2042067184655000118"
zhihu_title: "yiduobo的每日leetcode 3934.最短唯一子数组"
question_id: "3934"
question: "最短唯一子数组"
problem_url: "https://leetcode.cn/problems/smallest-unique-subarray/"
difficulty: "Hard"
rating: 2163
created: "2026-05-26T21:43:20+08:00"
updated: "2026-05-26T21:43:24+08:00"
upvotes: 1
comments: 0
---

# 3934. 最短唯一子数组

> **[yiduobo的每日leetcode 3934.最短唯一子数组](https://zhuanlan.zhihu.com/p/2042067184655000118) · 知乎 · 2026-05-26 · 赞同 1**
> 力扣：[3934. 最短唯一子数组](https://leetcode.cn/problems/smallest-unique-subarray/) · Hard · 灵茶山艾府：[O(n) 后缀数组](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3934.最短唯一子数组

<https://leetcode.cn/problems/smallest-unique-subarray/description/>

题目给出一个整数数组nums，其长度以及其中元素的大小都不超过10^5。

现在要求找出nums中，与其他任何子数组均不相同的子数组的最小长度。

如果将nums视为一个字符串而不是数组，那么问题实际上就是要找出其中独一无二的最短子串。对于这类重复子串相关的问题，可以直接使用后缀数组进行求解。

不过相对的，后缀数组写起来比较复杂，因此我在这里采用的是二分加字符串哈希的做法。

具体来说，首先可以确定这个长度是满足二分条件的，也就是说若存在一个小于nums的长度n的最小长度length，那么在这个length对应的字符串的基础上，在其左侧或者右侧添加一个字符，得到的新字符串必然也是独一无二的。

更一般的说，若对于某个较短的长度存在独一无二的字符串，那么对于较长的长度必然也存在独一无二的字符串，因此在这里可以二分这个长度length，然后检测nums中是否存在这么一个长度为length且独一无二的字符串。

确定了二分的长度length后，就可以一趟遍历，利用滑动窗口计算出nums中所有长度为length的子串的哈希值。具体来说，就是将其中所有的子串都视为一个长度为length的，base为10^5 + 3的base进制数，计算其十进制下对应的值，然后将这个值进行哈希。

不妨设当前窗口的右边界从index - 1移动到index，其中元素的哈希值为v，那么实际上这个v在未哈希的情况下，就相当于

nums[index - length] \* base^(length - 1) + nums[index - length + 1] \* base^(length - 2) + ... + nums[index - 1]

此时只需将其乘以base，再计算nums[index]，然后再减去nums[index - length] \* base^length，就变成了

nums[index - length + 1] \* base^(length - 1) + ... + nums[index - 1] \* base + nums[index]

也就是以index为右边界的长度为length的窗口对应的元素值，接下来对其进行哈希，然后记录哈希值即可

遍历完成后，若存在至少一个哈希值仅出现一次，那么说明存在独一无二的子串，此时调整二分的上界为length，否则调整二分的下界为length + 1。

另外，为了避免哈希表冲突，在这里也可以选择多个哈希函数来降低冲突的概率。

最后附上python代码：

```python
class Solution(object):
    def smallestUniqueSubarray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        base = 100003
        m1 = 10 ** 9 + 7
        m2 = 2147483647

        def check(length):
            cnt = {}
            v1 = 0
            v2 = 0
            p1 = 1
            p2 = 1
            for index in range(length):
                v1 = (v1 * base + nums[index]) % m1
                v2 = (v2 * base + nums[index]) % m2
                p1 = p1 * base % m1
                p2 = p2 * base % m2

            cnt[(v1, v2)] = 1
            for index in range(length, len(nums)):
                v1 = (v1 * base + nums[index]) % m1
                v1 = (v1 - p1 * nums[index - length] % m1 + m1) % m1
                
                v2 = (v2 * base + nums[index]) % m2
                v2 = (v2 - p2 * nums[index - length] % m2 + m2) % m2
                
                key = (v1, v2)
                cnt[key] = cnt.get(key, 0) + 1
            
            for key in cnt:
                if cnt[key] == 1:
                    return True

            return False

        left = 1
        right = len(nums)
        while left < right:
            mid = (left + right) // 2
            if check(mid):
                right = mid
            else:
                left = mid + 1
        
        return left
```

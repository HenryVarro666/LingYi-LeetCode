---
title: "3113. 边界元素是最大值的子数组数目"
aliases: ["yiduobo的每日leetcode 3113.边界元素是最大值的子数组数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/monotonic-stack", "题单/单调栈", "题单/单调栈/一-单调栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/701026463"
zhihu_id: "701026463"
zhihu_title: "yiduobo的每日leetcode 3113.边界元素是最大值的子数组数目"
question_id: "3113"
question: "边界元素是最大值的子数组数目"
problem_url: "https://leetcode.cn/problems/find-the-number-of-subarrays-where-boundary-elements-are-maximum/"
difficulty: "Hard"
rating: 2046
created: "2024-06-01T01:57:55+08:00"
updated: "2024-06-01T01:57:55+08:00"
upvotes: 0
comments: 0
---

# 3113. 边界元素是最大值的子数组数目

> **[yiduobo的每日leetcode 3113.边界元素是最大值的子数组数目](https://zhuanlan.zhihu.com/p/701026463) · 知乎 · 2024-06-01 · 赞同 0**
> 力扣：[3113. 边界元素是最大值的子数组数目](https://leetcode.cn/problems/find-the-number-of-subarrays-where-boundary-elements-are-maximum/) · Hard · 灵茶山艾府：[O(n) 单调栈（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3113.边界元素是最大值的子数组数目

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-number-of-subarrays-where-boundary-elements-are-maximum/description/)

题目给出一个正整数数组，要求找出其中所有满足左右边界都是子数组中最大值的子数组的数目。

对于一个子数组，如果其左右边界的元素相等，且这两个元素的下一个更大的元素是同一个，那么就说明子数组内部的所有元素都小于等于左右边界的元素，即这是一个合法的子数组。

而对于下一个更大元素的问题，则可以利用单调栈一趟遍历求解。使用一个栈stack来储存所有还没有找到下一个更大元素的数组下标，接下来一趟遍历，对于当前遍历到的nums\[index\]，若其大于栈顶元素对应的nums\[stack\[-1\]\]，那么说明stack\[-1\]对应的元素的下一个更大元素就是nums\[index\]，此时将其从栈中弹出并更新其对应的下一个更大元素，重复此过程直到stack为空或者nums\[index\]小于等于nums\[stack\[-1\]\]为止。接下来只需将index加入到栈中，然后继续向后遍历即可。由于栈中的下标对应的元素是单调不增的，因此不会出现nums\[index\]小于等于nums\[stack\[-1\]\]，但栈中还有其他元素小于nums\[index\]的情况，保证了正确性。

得到了数组中每个元素的下一个更大元素下标后，不妨记为f数组，那么只需统计数组中存在多少下标对(i, j)满足nums[i]等于nums[j]同时f[i]等于f[j]，于是可以将(nums[i], f[i])作为key，一趟遍历使用哈希表统计每种key出现的次数。接下来再遍历哈希表中的key，若某个key出现了cnt次，那么就一共可以形成(cnt + 1) \* cnt // 2种合法的pair对，将其累加到答案即可。

最后附上python代码：

```python
class Solution(object):
    def numberOfSubarrays(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        stack = []
        n = len(nums)
        f = [-1] * n
        for index, v in enumerate(nums):
            while stack and nums[stack[-1]] < v:
                f[stack[-1]] = index
                stack.pop()
            stack.append(index)
        
        counter = Counter()
        for index in range(n):
            key = (nums[index], f[index])
            counter[key] += 1
        
        res = 0
        for cnt in counter.values():
            res += (cnt + 1) * cnt // 2
        
        return res
```

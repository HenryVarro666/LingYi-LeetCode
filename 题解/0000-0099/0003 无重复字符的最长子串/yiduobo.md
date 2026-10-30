---
title: "3. 无重复字符的最长子串"
aliases: ["yiduobo的每日leetcode 3.无重复字符的最长子串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/滑动窗口与双指针/二-不定长滑动窗口", "题单/LeetCode-热题-100/滑动窗口", "题单/面试经典-150-题/滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/112545613"
zhihu_id: "112545613"
zhihu_title: "yiduobo的每日leetcode 3.无重复字符的最长子串"
question_id: "3"
question: "无重复字符的最长子串"
problem_url: "https://leetcode.cn/problems/longest-substring-without-repeating-characters/"
difficulty: "Medium"
created: "2020-03-11T22:37:43+08:00"
updated: "2020-03-11T22:38:24+08:00"
upvotes: 1
comments: 2
---

# 3. 无重复字符的最长子串

> **[yiduobo的每日leetcode 3.无重复字符的最长子串](https://zhuanlan.zhihu.com/p/112545613) · 知乎 · 2020-03-11 · 赞同 1**
> 力扣：[3. 无重复字符的最长子串](https://leetcode.cn/problems/longest-substring-without-repeating-characters/) · Medium · 灵茶山艾府：[【视频】一个视频讲透滑动窗口！附题单！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

3.无重复字符的最长子串<https://leetcode-cn.com/problems/longest-substring-without-repeating-characters/>

**O(n^3)的做法**

直接暴力枚举子串的头和尾，然后遍历子串统计是否有重复字符即可。

**O(n)的做法**

动态规划的做法，f[i]表示以原字符串s中，以位置i的字符s[i]为右边界时的最优左边界。

例如样例 a b c a b c b b

对应的f数组为：

f[0] \= 0，左边界为第一个a，对应子串为a

f[1] \= 0，左边界为第一个a，对应子串为ab

f[2] \= 0，左边界为第一个a，对应子串为abc

f[3] \= 1，左边界为第一个b，对应子串为bca

f[4] \= 2，左边界为第一个c，对应子串为cab

f[5] \= 3，左边界为第二个a，对应子串为abc

f[6] \= 5，左边界为第二个c，对应子串为cb

f[7] \= 7，左边界为最后一个b，对应子串为b

对于f[0]，显然就有f[0]\=0。

对于f[i]，其中i>0，那么只需要考察在f[i - 1]到i - 1这个区间中是否已经出现过s[i]。

如果未出现过，那么有f[i] \= f[i - 1]。

如果出现过，那么必然只出现了一次，因为f[i - 1]到i - 1这个区间中是必然不存在重复字符的，于是可以设s[i]出现的位置为pos，那么此时有f[i] \= pos + 1。

例如样例当中的f[5]，考虑f[4]到4之间是否出现过s[5]。具体为f[4] \= 2到4，即c a b中是否出现过c。

出现的位置pos \= 2，那么左边界需要从pos往右移动一位，即f[5] \= pos + 1 \= 3。

可以发现，左边界的更新是单调递增的，因此s中每个字符最多也只会遍历一次。因此最终的时间复杂度为O(n)。

另外，注意到f[i]的更新只于f[i - 1]有关，因此不需要维护整个 f 数组，只需要滚动维护一个当前右边界的最优左边界即可。

最后附上python的代码，其中left表示滚动维护的最优左边界：

```python
class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        left = 0
        res = 0
        for right, char in enumerate(s):
            pos = s.find(char, left, right)
            if pos >= 0:
                left = pos + 1
            if right - left + 1 > res:
                res = right - left + 1
        return res
```

---
title: "1960. 两个回文子字符串长度的最大乘积"
aliases: ["yiduobo的每日leetcode 1960.两个回文子字符串长度的最大乘积"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/string", "leetcode/ma-la-che", "leetcode/manacher", "题单/字符串", "题单/字符串/三-Manacher-算法-回文串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/493381402"
zhihu_id: "493381402"
zhihu_title: "yiduobo的每日leetcode 1960.两个回文子字符串长度的最大乘积"
question_id: "1960"
question: "两个回文子字符串长度的最大乘积"
problem_url: "https://leetcode.cn/problems/maximum-product-of-the-length-of-two-palindromic-substrings/"
difficulty: "Hard"
rating: 2691
created: "2022-04-05T17:19:38+08:00"
updated: "2022-04-05T17:19:38+08:00"
upvotes: 0
comments: 0
---

# 1960. 两个回文子字符串长度的最大乘积

> **[yiduobo的每日leetcode 1960.两个回文子字符串长度的最大乘积](https://zhuanlan.zhihu.com/p/493381402) · 知乎 · 2022-04-05 · 赞同 0**
> 力扣：[1960. 两个回文子字符串长度的最大乘积](https://leetcode.cn/problems/maximum-product-of-the-length-of-two-palindromic-substrings/) · Hard · 灵茶山艾府：[Go 马拉车算法，附详细注释](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1960.两个回文子字符串长度的最大乘积

[力扣](https://leetcode-cn.com/problems/maximum-product-of-the-length-of-two-palindromic-substrings/)

题目要找出两个不重叠回文子串，使得这两个子串长度的乘积最大，那么一般做法就是枚举中间的分割线，在分割线的左侧和右侧分别找出最长的回文子串，然后使用这两个串长度的乘积来更新答案。

由于题目中n个规模比较大，因此有必要预处理出所有位置左侧和右侧最长回文子串的长度，分别记为l_max和r_max。注意到题目中的回文子字符串必须是奇数串，因此可以直接使用马拉车算法求出以每个位置为中心点的最长回文串长度。马拉车具体的细节可以参考之前第5题的题解。

[yiduobo：yiduobo的每日leetcode 5.最长回文子串](https://zhuanlan.zhihu.com/p/113060786)

执行完马拉车算法之后，就得到了以每个字符为中心的最长回文子串的长度，记为f。

对于位置p，以s[p]为中心的最长回文子字符串长度为f[p]，那么对于任意满足p \<\= q \<\= p + f[p] - 1的q而言，s[q]，s[q - 1]，...，s[p + 1]，s[p]，s[p - 1]，...，s[p \* 2 - q]一定是一个回文子字符串，也就是说，对于满足条件的q而言，其必然是一个长度为(q - p) \* 2 + 1的回文子字符串的右边界，因此可以使用这个长度来更新左侧回文子串长度的最大值l_max[q]。

当然，在这里如果对每个满足条件的q都去更新l_max，时间复杂度就太高了。不妨设对于p和p \<\= q \<\= p + f[p] - 1，还存在一个r，满足r \<\= q \<\= r + f[r] - 1，且p \< r。此时可以发现，s[q]到s[p \* 2 - q]是一个回文子字符串，s[q]到s[p \* 2 - r]也是一个回文子字符，但前者的长度为(q - p) \* 2 + 1，后者的长度为(q - r) \* 2 +1。因为p \< r，所以前者的长度显然大于后者的长度，这就说明在这里没有必要考虑q和r带来的回文子字符串。

更进一步的，对于p \< r而言，只需要考虑所有满足r \<\= q \<\= r + f[r] - 1，且p + f[p] - 1 \< q的q就行了。这样一来就可以从头开始向后一趟遍历，使用一个pos来记录当前最大的p + f[p] - 1。若当前的f[index] + index - 1小于等于pos，那么就没有必要使用index中的q来更新l_max了，否则使用pos + 1 \<\= q \<\= f[index] + index - 1直接的q来更新l_max，并将pos更新为f[index] + index - 1。

同样的，从右向左一趟遍历，按相同的方法更新得到r_max即可。

最后附上python代码：

```python
class Solution(object):
    def maxProduct(self, s):
        """
        :type s: str
        :rtype: int
        """

        s = '$' + s + '#'
        mid = 0
        right = 0
        f = [0]
        for index in range(1, len(s) - 1):
            if index <= right:
                f.append(min(right - index, f[mid + mid - index]))
            else:
                f.append(1)
            
            while s[index + f[index]] == s[index - f[index]]:
                f[index] += 1
            
            if right < f[index] + index:
                right = f[index] + index
                mid = index
        
        l_max = [0]
        pos = 0
        for index in range(1, len(s) - 1):
            while pos < index + f[index] - 1:
                pos += 1
                l_max.append(max(l_max[-1], (pos - index) * 2 + 1))
        
        r_max = [0]
        pos = len(s) - 1
        for index in range(len(s) - 2, 0, -1):
            while pos > index - f[index] + 1:
                pos -= 1
                r_max.append(max(r_max[-1], (index - pos) * 2 + 1))
        r_max.append(0)
        r_max.reverse()

        res = l_max[1] * r_max[2]
        for index in range(2, len(s) - 1):
            res = max(res, l_max[index - 1] * r_max[index])

        return res
```

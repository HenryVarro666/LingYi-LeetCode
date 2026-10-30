---
title: "3649. 完美对的数目"
aliases: ["yiduobo的每日leetcode 3649.完美对的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/geometry", "leetcode/math", "leetcode/two-pointers", "leetcode/sorting", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/数学算法", "题单/滑动窗口与双指针/三-单序列双指针", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1948181732454020050"
zhihu_id: "1948181732454020050"
zhihu_title: "yiduobo的每日leetcode 3649.完美对的数目"
question_id: "3649"
question: "完美对的数目"
problem_url: "https://leetcode.cn/problems/number-of-perfect-pairs/"
difficulty: "Medium"
rating: 1716
created: "2025-09-10T22:25:10+08:00"
updated: "2025-09-10T22:25:10+08:00"
upvotes: 0
comments: 0
---

# 3649. 完美对的数目

> **[yiduobo的每日leetcode 3649.完美对的数目](https://zhuanlan.zhihu.com/p/1948181732454020050) · 知乎 · 2025-09-10 · 赞同 0**
> 力扣：[3649. 完美对的数目](https://leetcode.cn/problems/number-of-perfect-pairs/) · Medium · 灵茶山艾府：[用绝对值的几何意义化简式子（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3649.完美对的数目

<https://leetcode.cn/problems/number-of-perfect-pairs/description/>

题目给出一个整数数组nums。对于其中的一个下标对(i, j)，记a \= nums[i], b \= nums[j]，那么当i \< j，且

min(|a - b|, |a + b|) \<\= min(|a|, |b|)

max(|a - b|, |a + b|) >\= max(|a|, |b|)

那么就称(i, j)是完美的。

问完美对的数目。

对于这类绝对值有关的问题，一种自然的想法就是拆开绝对值符号分情况讨论：

1、若a >\= 0且b >\= 0：

此时第二个式子恒成立

对于第一个式子，则只需要考虑|a - b|这个部分。若a >\= b，那么就必须满足a - b \<\= b，也就是a\<\= b \* 2；反之，若a \< b，那么就必须满足b - a \<\= a，也就是b \<\= a \* 2

总的来说，就是较小的那一项的两倍必须大于等于较大的那一项

2、若a >\= 0且b \< 0：

此时第二个式子依然恒成立，在这里可以从数轴上的点的角度来看问题。a和b分别位于原点的两侧，那么|a - b|，也就是a到b的距离，显然大于a到原点的距离以及b到原点的距离。

对于第一个式子，显然有|a + b|小于等于|a - b|，在这里依然可以用数轴上的点的角度来看问题。|a + b|可以认为是a关于原点的对称点-a，与b的距离，而|a - b|则是完整的a到b的距离，相比之下多出了max(-a, b)到min(a, -b)这一段。

接下来，考察什么情况下有|a + b| \<\= min(|a|, |b|)。若|a| >\= |b|，那么就有a + b \<\= -b，即a \<\= -b \* 2；反之，若|a| \< |b|，那么就有-a - b \<\= a，即-b \<\= a \* 2

总的来说，就是绝对值较小的那一项的绝对值的两倍，必须大于等于绝对值较大的那一项的绝对值。

综合情况1，也可以将情况1的结论修正为相同的结论。接下来对于剩下的情况，也可以有意识地往这上面去靠。

3、若a \< 0且b >\= 0：

此时第二个式子依然恒成立，理由与情况2相同。

对于第一个式子，同样有|a + b|小于等于|a - b|，理由也与情况2相同。

接下来，还是考察什么情况下有|a + b| \<\= min(|a|, |b|)。若|a| >\= |b|，那么就有-a - b \<\= b，即-a \<\= b \* 2；反之，若|a| \< |b|，那么就有a + b \<\= -b，即a \<\= -b \* 2。

可以发现，此时符合绝对值较小的那一项的绝对值的两倍，必须大于等于绝对值较大的那一项的绝对值。

4、若a \< 0且b \< 0：

此时第二个式子依然恒成立，理由是|a + b| \= -a - b，相当于两个正数相加，必然大于其中一个单独的正数。

对于第一个式子，也只需要考虑|a - b|这个部分。若|a| >\= |b|，那么就有-a + b \<\= -b，即-a \<\= -b \* 2；反之，若|a| \< |b|，那么就有a - b \<\= -a，即-b \<\= -a \* 2。

可以发现，此时依然符合上面得出的结论。

基于这一点，对于nums中的任意元素v，所有绝对值在(|v| + 1) // 2到|v| \* 2之间的元素都可以与v形成完美对。因为还有i \< j的这个条件，因此一组下标对(i, j)只能计算一次。为了避免重复计算，在这里可以只计算绝对值小于等于|v|的元素与v形成的元素对，那么在这里可以将nums按照绝对值从小到大进行排序，这样一来，随着v的向后遍历，可以与v形成完美对的最小的下标也必然跟着向后移动。

对nums一趟遍历，同时使用一个变量p记录这个最小的下标。对于当前遍历到的index，若当前的|nums[p]| \< (|nums[index]| + 1) // 2，那么就将p向后移动。移动完成后，p到index - 1这一段的元素都可以与nums[index]形成完美对，一共有index - p组，将其累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def perfectPairs(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        nums.sort(key=lambda d:abs(d))
        p = 0
        res = 0
        for index, v in enumerate(nums[1:], 1):
            while abs(nums[p]) < (abs(v) + 1) // 2:
                p += 1
            
            res += index - p

        return res
```

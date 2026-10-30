---
title: "2745. 构造最长的新字符串"
aliases: ["yiduobo的每日leetcode 2745.构造最长的新字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/653847877"
zhihu_id: "653847877"
zhihu_title: "yiduobo的每日leetcode 2745.构造最长的新字符串"
question_id: "2745"
question: "构造最长的新字符串"
problem_url: "https://leetcode.cn/problems/construct-the-longest-new-string/"
difficulty: "Medium"
rating: 1607
created: "2023-09-02T03:44:17+08:00"
updated: "2023-09-02T03:44:17+08:00"
upvotes: 0
comments: 0
---

# 2745. 构造最长的新字符串

> **[yiduobo的每日leetcode 2745.构造最长的新字符串](https://zhuanlan.zhihu.com/p/653847877) · 知乎 · 2023-09-02 · 赞同 0**
> 力扣：[2745. 构造最长的新字符串](https://leetcode.cn/problems/construct-the-longest-new-string/) · Medium · 灵茶山艾府：[两种方法：O(1) 公式 / 记忆化搜索（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2745.构造最长的新字符串

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/construct-the-longest-new-string/)

观察题目给出的三种字符串，可以发现AB是较为特殊的一种，因为对于AB而言，其需要一个前导的B，但是其自身又可以提供一个B，因此AB的存在对另外两种字符串的接法不会产生任何影响，那么在这里就只需要考虑AA和BB的数量，也就是x和y的大小。

另一方面，由于BB只能接在AA的后方，因此当BB的数量y大于AA的数量x时，最多也只能选择x + 1个BB通过x个AA隔开，那么对于这种情况，最终答案就是x + x + 1 + z，一种可行的构造方式为先构造BBAABB...BBAABB，然后将ABABAB...AB接在后面。

对于x和y相同的情况，当然是全都要，一种可行的构造方法相比之前只需去掉最开始的BB就行了。

最后对于x > y的情况，由于AA必须接在BB或者AB的后面，而AB不会改变可用的前导B的数量，因此在这里最多只能选择y + 1个AA，也就是y个BB提供的前导B加上最终答案以A开头的可用A，那么最终答案就是y + y + 1 + z，一种可行的构造方式为先构造ABABAB...AB，然后将AABBAABB...AABBAA接在后面。

最后附上python代码：

```python
class Solution(object):
    def longestString(self, x, y, z):
        """
        :type x: int
        :type y: int
        :type z: int
        :rtype: int
        """

        if x > y:
            return (y + y + 1 + z) * 2
        elif x == y:
            return (x + y + z) * 2
        else:
            return (x + x + 1 + z) * 2
```

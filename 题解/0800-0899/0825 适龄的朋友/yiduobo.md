---
title: "825. 适龄的朋友"
aliases: ["yiduobo的每日leetcode 825.适龄的朋友"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/counting", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/344806379"
zhihu_id: "344806379"
zhihu_title: "yiduobo的每日leetcode 825.适龄的朋友"
question_id: "825"
question: "适龄的朋友"
problem_url: "https://leetcode.cn/problems/friends-of-appropriate-ages/"
difficulty: "Medium"
rating: 1697
created: "2021-01-19T23:13:10+08:00"
updated: "2021-01-19T23:13:10+08:00"
upvotes: 0
comments: 0
---

# 825. 适龄的朋友

> **[yiduobo的每日leetcode 825.适龄的朋友](https://zhuanlan.zhihu.com/p/344806379) · 知乎 · 2021-01-19 · 赞同 0**
> 力扣：[825. 适龄的朋友](https://leetcode.cn/problems/friends-of-appropriate-ages/) · Medium · 灵茶山艾府：[计数+滑动窗口（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

825.适龄的朋友

[力扣](https://leetcode-cn.com/problems/friends-of-appropriate-ages/)

首先，题目给出的三个条件中，条件三是多余的，因为当age[B] > 100 > age[A]时，也必然有age[B] > age[A]。

那么根据剩下的两个条件，A可以对B发送好友请求则需要满足

age[B] \<\= age[A]

age[B] > age[A] \* 0. 5 + 7

即对于age\[A\]而言，age\[B\]年龄的上下限为前开后闭区间(age\[A\] \* 0. 5 + 7，age\[A\]\]

可以发现随着age[A]的增大，这个区间也是在逐渐往坐标轴右侧移动的，因此可以将所有人的年龄从小到大进行排序，然后使用一组left和right维护这个区间的左右边界。当然，这里的右边界就是其自身，因此实际上只需要维护左边界即可。假设这个区间内一共有k人，那么除开此人本身之外，一共可以发出k - 1份好友请求。

另外，注意到可能有重合的年龄，因此也可以先按年龄统计人数，然后在计算时使用乘法一次处理完同一年龄的所有人。例如当前年龄的人数有cnt人，而合法区间内一共有k人，那么可以发出的好友请求就有cnt \* (k - 1)份，即这cnt人对除自己外的所有人都可以发送好友请求。

最后，在计算cnt时，可以利用前缀和的思路来进行优化。

最后附上python代码：

```python
class Solution(object):
    def numFriendRequests(self, ages):
        """
        :type ages: List[int]
        :rtype: int
        """

        age_dict = {}
        for age in ages:
            age_dict[age] = age_dict.get(age, 0) + 1

        age_info = sorted(age_dict.items(), key=lambda d:d[0])
        s = [age_info[0][1]]
        for index in range(1, len(age_info)):
            s.append(s[-1] + age_info[index][1])

        min_pos = 0
        res = 0
        for index in range(len(age_info)):
            now, cnt = age_info[index]
            while min_pos <= index and (age_info[min_pos][0] - 7) * 2 <= now:
                min_pos += 1
            
            if min_pos == 0:
                res += cnt * (s[index] - 1)
            elif min_pos <= index:
                res += cnt * (s[index] - s[min_pos - 1] - 1)

        return res
```

---
title: "3922. 使二进制字符串连贯的最少翻转次数"
aliases: ["yiduobo的每日leetcode 3922.使二进制字符串连贯的最少翻转次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2037308436384310236"
zhihu_id: "2037308436384310236"
zhihu_title: "yiduobo的每日leetcode 3922.使二进制字符串连贯的最少翻转次数"
question_id: "3922"
question: "使二进制字符串连贯的最少翻转次数"
problem_url: "https://leetcode.cn/problems/minimum-flips-to-make-binary-string-coherent/"
difficulty: "Medium"
rating: 1759
created: "2026-05-11T23:23:15+08:00"
updated: "2026-05-11T23:23:35+08:00"
upvotes: 1
comments: 0
---

# 3922. 使二进制字符串连贯的最少翻转次数

> **[yiduobo的每日leetcode 3922.使二进制字符串连贯的最少翻转次数](https://zhuanlan.zhihu.com/p/2037308436384310236) · 知乎 · 2026-05-11 · 赞同 1**
> 力扣：[3922. 使二进制字符串连贯的最少翻转次数](https://leetcode.cn/problems/minimum-flips-to-make-binary-string-coherent/) · Medium · 灵茶山艾府：[从一个更简单的问题开始思考（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3922.使二进制字符串连贯的最少翻转次数

<https://leetcode.cn/problems/minimum-flips-to-make-binary-string-coherent/description/>

题目给出一个二进制字符串s。

若一个字符串不包含子序列"011"或者"110"，那么就认为这个字符串是连贯的。

现在可以翻转s中的任意字符，将0变为1，或者将1变为0。

问使得s连贯所需的最少操作次数。

题目要求让s中不再具备011或者110这样的子序列，直观来看这个条件其实还是很严格的。更具体的说，如果最终的s中存在0，那么这个0的左侧和右侧至多只能有一个1，那么这样就可以推导出一个条件：s中如果有0，那么其中1的数量不能大于等于3个，因为此时将这3个1排开，那么0无论放在哪里，其左侧或右侧中的一边都至少有两个0。基于这一点，就可以想办法分情况讨论了：

1、s中没有0：

这种情况相当于要将s中所有的0翻转掉，操作次数就是s中0的数量

2、s中存在0，但是没有1：

这种情况相当于要将s中所有的1翻转掉，操作次数就是s中1的数量

3、s中存在0，且只有唯一1个1：

此时可以留下任意一个1，将其他的1都变为0，操作次数就是s中1的数量减去1。值得一提的是，如果s中本来就没有1，那么直接走情况2就行了，对应的答案为0

4、s中存在0，且存在两个1：

此时所有的0都必须在这两个1之间，这也就意味着这两个1必须分别处于s的两端。也就是说只有当s的两侧都为1时，才有必要考虑这种情况，所需的操作次数为s中1的数量减去2

以上4种情况就涵盖了所有合法的s，那么基于上面的讨论，只需一趟遍历，计算s中1的数量，不妨记为one，那么：

- 若one等于len(s)，即s一开始就是全1，那么答案为0
- 若one小于等于1，即s一开始就是全0，或者仅有一个1，那么答案为0
- 否则初始化答案为len(s) - one，表示考虑变为全1所需的代价。接下来，若s两端都为1，那么就是用one - 2更新答案，表示变为1000...0001的代价，否则只能使用one - 1更新答案，表示将s变为仅有一个1所需的代价。注意这里不需要考虑将s变为全0的代价，因为相比1000..0001或者仅有一个1，变为全0的操作次数显然更多。

最后附上python代码：

```python
class Solution(object):
    def minFlips(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        one = 0
        for c in s:
            if c == '1':
                one += 1
        
        if one == len(s) or one <= 1:
            return 0
        
        res = len(s) - one
        if s[0] == '1' and s[-1] == '1':
            res = min(res, one - 2)
        else:
            res = min(res, one - 1)
        
        return res
```

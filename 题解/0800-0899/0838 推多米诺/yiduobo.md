---
title: "838. 推多米诺"
aliases: ["yiduobo的每日leetcode 838.推多米诺"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/滑动窗口与双指针", "题单/贪心算法", "题单/滑动窗口与双指针/六-分组循环", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/346550405"
zhihu_id: "346550405"
zhihu_title: "yiduobo的每日leetcode 838.推多米诺"
question_id: "838"
question: "推多米诺"
problem_url: "https://leetcode.cn/problems/push-dominoes/"
difficulty: "Medium"
rating: 1638
created: "2021-01-26T12:07:12+08:00"
updated: "2021-01-26T12:07:12+08:00"
upvotes: 0
comments: 0
---

# 838. 推多米诺

> **[yiduobo的每日leetcode 838.推多米诺](https://zhuanlan.zhihu.com/p/346550405) · 知乎 · 2021-01-26 · 赞同 0**
> 力扣：[838. 推多米诺](https://leetcode.cn/problems/push-dominoes/) · Medium · 灵茶山艾府：[分类讨论，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

838.推多米诺

[力扣](https://leetcode-cn.com/problems/push-dominoes/)

由于这里不需要考虑骨牌的数量而只需要考虑方向，那么对于一块骨牌，如果其向右倾斜，那么这块骨牌**之前所有骨牌的结算**就与**这块骨牌以及之后的骨牌**无关了。同样对于向左倾斜的骨牌，这块骨牌**之后的所有骨牌**的结算就与**这块骨牌以及之前的骨牌**无关了。换言之，通过向左或向右倾斜的骨牌，我们可以将整个序列划分成若干个互不干涉的部分分别求解。基于这一点，我们需要维护一个start_pos，表示当前处理部分的起始位置。

另外，若一块骨牌向右倾斜，那么其后续的骨牌的态势无法断定，但一块骨牌若向左倾斜，那么这块骨牌之前的骨牌，包括这块骨牌在内，就可以得到明确的方向信息了。因此对于向右倾斜的骨牌，我们需要通过维护一个右斜标记right_flag来表示之前有向右倾斜的骨牌，然后当遇到一块向左倾斜的骨牌时，就可以确定骨牌的最终形态了。

接下来从左向右遍历整个序列，对于当前骨牌，设其位于第index位：

1、若当前骨牌为R，那么说明start_pos到index - 1这一段的骨牌方向已经可以确定。此时若right_flag为true，那么这一段将全部向右倾斜，于是在答案中加入index - start_pos个R，否则这一段全部竖直不动，在答案中加入index - start_pos个L。

最后，由于当前是一块R，说明新开启了一个区间，因此要将start_pos置为index，同时置right_flag为true。

2、若当前骨牌为L，那么说明start_pos到index这一段我的骨牌方向已经可以确定。

2-1）此时若right_flag为true，说明这一段将呈现L和R向中间倒的情况，因此最终必然是LLL...RRR的形式。不过需要注意的是，若这一段的长度为奇数，那么正中间的骨牌应该是竖直不动的，因此需要根据start_pos - index + 1的奇偶性判断是否存在竖直不动的正中间骨牌。于是设delta \= start_pos - index + 1，首先在答案中加入delta/2个L，然后若delta为奇数，则需要再加上一个"."，最后再在答案中加入delta/2个R。完成后，需要置right_flag为false。

2-2）此时若right_flag为false，那么这一段将全部向左倾斜，因此在答案中加入start_pos - index + 1个L

无论是哪种情况，当前区间已经处理完毕，新区间的起始位置start_pos应该置为index + 1。

3、若当前骨牌为"."，那么此时还无法做出有效的判断，需要继续向后遍历。

当遍历完成之后，最后这个部分可能还未进行处理，于是还需要根据当前个right_flag决定应该加入len - start_pos个R还是相同数量的"."。

值得一提的是，上面对于L和R的区间长度，一个是index - start_pos，另一个是index - start_pos + 1，造成这种差异的是最上面黑体字的描述：R与当前区间无关，但L被包含在当前区间之内。

最后附上python代码：

```python
class Solution(object):
    def pushDominoes(self, dominoes):
        """
        :type dominoes: str
        :rtype: str
        """

        start_pos = 0
        right_flag = False

        res = ''
        for index, char in enumerate(dominoes):
            if char == 'R':
                if right_flag:
                    res += 'R' * (index - start_pos)
                else:
                    res += '.' * (index - start_pos)
                start_pos = index
                right_flag = True
            elif char == 'L':
                if right_flag:
                    delta = index - start_pos
                    res += 'R' * ((delta + 1) / 2)
                    if delta % 2 == 0:
                        res += '.'
                    res += 'L' * ((delta + 1) / 2)
                    right_flag = False
                else:
                    res += 'L' * (index - start_pos + 1)
                start_pos = index + 1

        if right_flag:
            res += 'R' * (len(dominoes) - start_pos)
        else:
            res += '.' * (len(dominoes) - start_pos)
        return res
```

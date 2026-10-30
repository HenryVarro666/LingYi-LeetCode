---
title: "670. 最大交换"
aliases: ["yiduobo的每日leetcode 670.最大交换"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/三-字符串贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/293106558"
zhihu_id: "293106558"
zhihu_title: "yiduobo的每日leetcode 670.最大交换"
question_id: "670"
question: "最大交换"
problem_url: "https://leetcode.cn/problems/maximum-swap/"
difficulty: "Medium"
created: "2020-11-14T13:15:22+08:00"
updated: "2020-11-14T13:15:22+08:00"
upvotes: 0
comments: 0
---

# 670. 最大交换

> **[yiduobo的每日leetcode 670.最大交换](https://zhuanlan.zhihu.com/p/293106558) · 知乎 · 2020-11-14 · 赞同 0**
> 力扣：[670. 最大交换](https://leetcode.cn/problems/maximum-swap/) · Medium · 灵茶山艾府：[一次遍历，简洁写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

670.最大交换

[力扣](https://leetcode-cn.com/problems/maximum-swap/)

题目保证num的位数最多只有9位，因此这里怎么做其实都可以。

我在这里使用的是贪心法，总的思路就是若高位上的数比后面的数要小，那么交换二者就能得到更大的数。

具体实现起来就是从高位往低位扫描，若当前num[index]小于num[index + 1]，说明在index +1到末尾这些数中至少有一个数比num[index]大。此时扫描index + 1到末尾，找出其中最大的数，相同大小的话就取位置更靠后的那一个，设为num[p]。接下来扫描0到index，若当前数小于num[p]，那么交换二者就是最终答案。

若始终没有nums[index]小于nums[index + 1]，说明此时的num已经是完全的倒序排列，是最大的情况了。

最后附上python代码：

```python
class Solution(object):
    def maximumSwap(self, num):
        """
        :type num: int
        :rtype: int
        """

        char_list = list(str(num))
        swap_pos = 0
        for index in range(len(char_list) - 1):
            if char_list[index] < char_list[index + 1]:
                max_pos = index + 1
                for pos in range(index + 2, len(char_list)):
                    if char_list[pos] >= char_list[max_pos]:
                        max_pos = pos

                for pos in range(0, index + 1):
                    if char_list[pos] < char_list[max_pos]:
                        char_list[pos], char_list[max_pos] = char_list[max_pos], char_list[pos]
                        break

                return int(''.join(char_list))
                  
        return num
```

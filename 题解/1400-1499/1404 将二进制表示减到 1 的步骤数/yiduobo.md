---
title: "1404. 将二进制表示减到1的步骤数"
aliases: ["yiduobo的每日leetcode 1404.将二进制表示减到1的步骤数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/405565866"
zhihu_id: "405565866"
zhihu_title: "yiduobo的每日leetcode 1404.将二进制表示减到1的步骤数"
question_id: "1404"
question: "将二进制表示减到 1 的步骤数"
problem_url: "https://leetcode.cn/problems/number-of-steps-to-reduce-a-number-in-binary-representation-to-one/"
difficulty: "Medium"
created: "2021-08-31T23:19:21+08:00"
updated: "2021-08-31T23:19:21+08:00"
upvotes: 2
comments: 0
---

# 1404. 将二进制表示减到1的步骤数

> **[yiduobo的每日leetcode 1404.将二进制表示减到1的步骤数](https://zhuanlan.zhihu.com/p/405565866) · 知乎 · 2021-08-31 · 赞同 2**
> 力扣：[1404. 将二进制表示减到 1 的步骤数](https://leetcode.cn/problems/number-of-steps-to-reduce-a-number-in-binary-representation-to-one/) · Medium · 灵茶山艾府：[两种方法：模拟 / 简洁公式（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1404.将二进制表示减到1的步骤数

[力扣](https://leetcode-cn.com/problems/number-of-steps-to-reduce-a-number-in-binary-representation-to-one/)

没有什么特别好的思路，于是按照题目的规则进行模拟。方便起见，可以想将字符串转化成数组，然后倒过来，这样一来，从前向后的顺序就是从低位向高位了。

从头开始向后进行遍历，对于当前的位置now：

1、若当前位上的数字为1，且now以及处于数组的末尾，说明此时的数字已经为1，可以退出循环了

2、若当前位上的数字为1，且now还未到达数组的末尾，说明此时的数字是一个大于1的奇数，那么应该将其加上1。加上1之后，这个数字变成了一个偶数，那么此时应该将其除以2。两步操作组合起来，就是将now的下一位加上1，然后跳过now这一位，视为除以2。于是此时应该将答案加上2，将now的下一位加上1，然后将now向后移动一位。

3、若当前位上的数字为2，说明该位接受到了上一位的进位，那么应该先处理当前位的进位。此时需要考察now是否处于数组的末尾，若处于，那么应该将数组末尾新增一个1，否则直接将now的下一位加上1即可。处理完进位之后，当前位就变成了0，那么此时应该将答案加上1，并将now向后移动一位，表示除以2。

4、若当前位上的数字为0，与上面相同，也是将答案加上1，并将now向后移动一位。

最后附上python代码：

```python
class Solution(object):
    def numSteps(self, s):
        """
        :type s: str
        :rtype: int
        """

        num_list = [int(char) for char in s][::-1]
        n = len(num_list)
        now = 0
        res = 0
        while now < n:
            if num_list[now] == 1:
                if now == n - 1:
                    break
                else:
                    num_list[now + 1] += 1
                    res += 2
                    now += 1
            else:
                if num_list[now] == 2:
                    if now == n - 1:
                        num_list.append(1)
                        n += 1
                    else:
                        num_list[now + 1] += 1
                res += 1
                now += 1
        
        return res
```

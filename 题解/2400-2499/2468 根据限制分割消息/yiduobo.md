---
title: "2468. 根据限制分割消息"
aliases: ["yiduobo的每日leetcode 2468.根据限制分割消息"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/587557006"
zhihu_id: "587557006"
zhihu_title: "yiduobo的每日leetcode 2468.根据限制分割消息"
question_id: "2468"
question: "根据限制分割消息"
problem_url: "https://leetcode.cn/problems/split-message-based-on-limit/"
difficulty: "Hard"
rating: 2382
created: "2022-11-28T23:58:54+08:00"
updated: "2022-11-28T23:58:54+08:00"
upvotes: 1
comments: 0
---

# 2468. 根据限制分割消息

> **[yiduobo的每日leetcode 2468.根据限制分割消息](https://zhuanlan.zhihu.com/p/587557006) · 知乎 · 2022-11-28 · 赞同 1**
> 力扣：[2468. 根据限制分割消息](https://leetcode.cn/problems/split-message-based-on-limit/) · Hard · 灵茶山艾府：[枚举+视频讲解（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2468.根据限制分割消息

[力扣](https://leetcode.cn/problems/split-message-based-on-limit/)

令message的长度为n，那么有一点可以明确的是，b必然小于等于n。若b大于n，必然存在某些空的组，去除掉这些组只会让答案数组更短而不影响分割的正确性，这也就说明b的取值可以更小。

由于题目要求数组越短越小，那么也就是要求b越小越好。对于一个给定的b，其尖括号里的内容，即字符串\<a/b>的长度是可以提前预处理出来的。这里b的取值范围在1到n之间。

1、当1 \<\= b \<\= 9时：

此时a只能是一位数，因此尖括号字符串的长度必然为5，总长度就是5 \* b

2、当10 \<\= b \<\= 99时：

此时a的取值可以分割成两个部分，分别为1到9以及10到b。

当a取值范围在1到9时，\<a/b>的长度由左尖括号的1，a的1，斜线的1，b的2以及右尖括号的1组成，长度为6，一共有9组。

当a取值范围在10到b时，\<a/b>的长度则为7，一共有b - 10 + 1组。

综合起来，总长度就是7 \* (b - 10 + 1) + 6 \* 9

3、当100 \<\= b \<\= 999时：

此时a的取值可以分割成1到9、10到99以及100到b这三个部分。

当a取值范围在1到9时，长度为7，一共9组。

当a取值范围在10到99时，长度为8，一共90组。

当a取值范围在100到b时，长度为9，一共b - 100 + 1组。

综合起来，总长度就是9 \* (b - 100 + 1) + 8 \* 90 + 7 \* 9

4、当1000 \<\= b \<\= 9999时：

按照上面类似的方法，将a分割成四个部分，长度分别为8、9、10、11，组数则为9、90、900以及b - 1000 + 1，综合起来，总长度就是11 \* (b - 1000 + 1) + 10 \* 900 + 9 \* 90 + 8 \* 9

5、当b \= 10000时：

按照相同的计算方式，总长度为13 + 12 \* 9000 + 11 \* 900 + 10 \* 90 + 9 \* 9

记上面计算的尖括号内容的总长度为suffix_len，那么在这里就需要找出最小的b，满足

n + suffix_len \<\= limit \* b

即使用b组长度不超过limit的数组可以涵盖住原字符串中的所有字符以及额外的尖括号中的字符。

我在这里额外添加了一个条件。记\<b/b>为max_suffix，那么max_suffix的长度必须小于limit，否则就会出现空的或者长度超出limit的分组。

接下来只需要从1到n开始遍历，找出最小的满足条件的b。

找到b之后，再从1到b枚举a，构造出最终的答案数组就行了。

最后附上python代码：

```python
class Solution(object):
    def splitMessage(self, message, limit):
        """
        :type message: str
        :type limit: int
        :rtype: List[str]
        """

        res = []
        for b in range(1, len(message) + 1):
            if b < 10:
                suffix_len = 5 * b
            elif b < 100:
                suffix_len = 7 * (b - 10 + 1) + 6 * 9
            elif b < 1000:
                suffix_len = 9 * (b - 100 + 1) + 8 * 90 + 7 * 9
            elif b < 10000:
                suffix_len = 11 * (b - 1000 + 1) + 10 * 900 + 9 * 90 + 8 * 9
            else:
                suffix_len = 13 + 12 * 9000 + 11 * 900 + 10 * 90 + 9 * 9

            if len(message) + suffix_len <= limit * b:
                max_suffix = '<%d/%d>' % (b, b)
                if len(max_suffix) >= limit:
                    break

                a = 1
                suffix = '<%d/%d>' % (a, b)
                cnt = 0
                for char in message:
                    if cnt == 0:
                        res.append('')
                    res[-1] += char
                    cnt += 1
                    if cnt + len(suffix) == limit:
                        res[-1] += suffix
                        a += 1
                        suffix = '<%d/%d>' % (a, b)
                        cnt = 0
                
                if cnt > 0:
                    res[-1] += suffix
                break
        
        return res
```

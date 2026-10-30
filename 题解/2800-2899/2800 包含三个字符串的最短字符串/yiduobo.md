---
title: "2800. 包含三个字符串的最短字符串"
aliases: ["yiduobo的每日leetcode 2800.包含三个字符串的最短字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/字符串", "题单/字符串/一-KMP-前缀的后缀"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/657277710"
zhihu_id: "657277710"
zhihu_title: "yiduobo的每日leetcode 2800.包含三个字符串的最短字符串"
question_id: "2800"
question: "包含三个字符串的最短字符串"
problem_url: "https://leetcode.cn/problems/shortest-string-that-contains-three-strings/"
difficulty: "Medium"
created: "2023-09-20T04:58:05+08:00"
updated: "2023-09-20T04:58:05+08:00"
upvotes: 0
comments: 0
---

# 2800. 包含三个字符串的最短字符串

> **[yiduobo的每日leetcode 2800.包含三个字符串的最短字符串](https://zhuanlan.zhihu.com/p/657277710) · 知乎 · 2023-09-20 · 赞同 0**
> 力扣：[2800. 包含三个字符串的最短字符串](https://leetcode.cn/problems/shortest-string-that-contains-three-strings/) · Medium · 灵茶山艾府：[枚举](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2800.包含三个字符串的最短字符串

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/shortest-string-that-contains-three-strings/)

两个字符串的情况比较直观。对于包含a和b的最短字符串s，若a出现在左侧，那么s的组成一定是a的前缀，加上a的后缀与b的前缀的最大重叠部分，再加上b的后缀；反过来，若b出现在左侧情况也是一样。

由于本题的数据规模较小，因此可以直接枚举左侧字符串的后缀与右侧字符串前缀的最大重叠长度并进行检测，然后按照上面的方法构造出最短的包含两个字符串的字符串。

对于本题三个字符串的情况，则只需枚举出三个字符串的排列顺序，一共是6种。接下来对于每种排列方案，就只需优先合并前两个字符串，然后将合并结果再与第三个字符串合并就行了。合并完成后得到6个备选答案，从中选出最短且字典序最小的即可。

最后附上python代码：

```python
class Solution(object):
    def minimumString(self, a, b, c):
        """
        :type a: str
        :type b: str
        :type c: str
        :rtype: str
        """

        def merge(x, y, z):
            xy = ''
            for index in range(len(x)):
                compare_len = min(len(x) - index, len(y))
                if x[index: index + compare_len] == y[:compare_len]:
                    if compare_len < len(y):
                        xy = x[:index] + y
                    else:
                        xy = x
                    break
            
            if xy == '':
                xy = x + y

            for index in range(len(xy)):
                compare_len = min(len(xy) - index, len(z))
                if xy[index: index + compare_len] == z[:compare_len]:
                    if compare_len < len(z):
                        return xy[:index] + z
                    else:
                        return xy

            return xy + z

        candidate = [merge(a, b, c), merge(a, c, b), merge(b, a, c), merge(b, c, a), merge(c, a, b), merge(c, b, a)]
        return sorted(candidate, key=lambda d:(len(d), d))[0]
```

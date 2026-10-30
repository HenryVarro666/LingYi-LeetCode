---
title: "2266. 统计打字方案数"
aliases: ["yiduobo的每日leetcode 2266.统计打字方案数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/dynamic-programming", "leetcode/counting", "题单/动态规划", "题单/动态规划/一-入门-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/549203972"
zhihu_id: "549203972"
zhihu_title: "yiduobo的每日leetcode 2266.统计打字方案数"
question_id: "2266"
question: "统计打字方案数"
problem_url: "https://leetcode.cn/problems/count-number-of-texts/"
difficulty: "Medium"
rating: 1857
created: "2022-08-03T00:36:50+08:00"
updated: "2022-08-03T00:36:50+08:00"
upvotes: 0
comments: 0
---

# 2266. 统计打字方案数

> **[yiduobo的每日leetcode 2266.统计打字方案数](https://zhuanlan.zhihu.com/p/549203972) · 知乎 · 2022-08-03 · 赞同 0**
> 力扣：[2266. 统计打字方案数](https://leetcode.cn/problems/count-number-of-texts/) · Medium · 灵茶山艾府：[分组 + 爬楼梯（Python/Go/C++/Java）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2266.统计打字方案数

[力扣](https://leetcode.cn/problems/count-number-of-texts/)

经典的动态规划问题。令f[i]表示按键字符串pressedKeys中第0到第i个字符可以解码的方案数，那么对于f[i]：

1、直接将pressedKeys[i]解码成一个字符总是可行的，那么可以初始化f[i] \= f[i - 1]

2、如果pressedKeys[i]与pressedKeys[i - 1]相同，那么将最后这两个数字解码成一个字符也是可以的，于是就有f[i] +\= f[i - 2]

3、与情况2类似，如果pressedKeys[i]与pressedKeys[i - 1]以及pressedKeys[i - 2]相同，那么就可以将最后这三个数字解码成一个字符，于是有f[i] +\= f[i - 3]

4、最后，如果pressedKeys[i]开始往前的4个字符都相同，且输入的数字是7或者9，那么也可以将最后这四个数字解码成一个字符，于是有f[i] +\= f[i - 4]

于是只需一趟遍历，求解出f数组，f[-1]就是最终答案。

注意到这里f数组的更新依赖于往前推4位的状态，于是可以使用四个变量滚动储存最后4个f值来节省空间。

最后附上python代码：

```python
class Solution(object):
    def countTexts(self, pressedKeys):
        """
        :type pressedKeys: str
        :rtype: int
        """

        mod = 10 ** 9 + 7
        a = b = c = d = 1
        for index in range(1, len(pressedKeys)):
            now = 0
            if pressedKeys[index] == pressedKeys[index - 1]:
                if index >= 2 and pressedKeys[index] == pressedKeys[index - 2]:
                    if index >= 3 and pressedKeys[index] == pressedKeys[index - 3] and (pressedKeys[index] == '7' or pressedKeys[index] == '9'):
                        now += a
                        if now >= mod:
                            now -= mod
                    
                    now += b
                    if now >= mod:
                        now -= mod
                
                now += c
                if now >= mod:
                    now -= mod
            
            now += d
            if now >= mod:
                now -= mod

            a, b, c, d = b, c, d, now
        
        return d
```

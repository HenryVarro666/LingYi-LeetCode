---
title: "3941. 密码强度"
aliases: ["yiduobo的每日leetcode 3941.密码强度"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2043458581501104261"
zhihu_id: "2043458581501104261"
zhihu_title: "yiduobo的每日leetcode 3941.密码强度"
question_id: "3941"
question: "密码强度"
problem_url: "https://leetcode.cn/problems/password-strength/"
difficulty: "Medium"
created: "2026-05-30T02:09:14+08:00"
updated: "2026-05-30T02:09:18+08:00"
upvotes: 2
comments: 0
---

# 3941. 密码强度

> **[yiduobo的每日leetcode 3941.密码强度](https://zhuanlan.zhihu.com/p/2043458581501104261) · 知乎 · 2026-05-30 · 赞同 2**
> 力扣：[3941. 密码强度](https://leetcode.cn/problems/password-strength/) · Medium · 灵茶山艾府：[库函数写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3941.密码强度

<https://leetcode.cn/problems/password-strength/>

题目给出一个字符串password。

密码的强度按照以下规则计算：

- 每个不同的小写字母('a'到'z')计1分
- 每个不同的大写字母('A'到'Z')记2分
- 每个不同的数字('0'到'9')计3分
- 每个来自集合"!@\#\$"的不同特殊字符计5分

每个字符最多只贡献一次分数，且password仅由以上字符组成，问密码的强度是多少。

由于每个字符只贡献一次分数，因此可以先将password转化为集合来去重，接下来遍历其中的每种字符，根据字符类型更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def passwordStrength(self, password):
        """
        :type password: str
        :rtype: int
        """
        
        res = 0
        for c in set(password):
            if 'a' <= c <= 'z':
                res += 1
            elif 'A' <= c <= 'Z':
                res += 2
            elif '0' <= c <= '9':
                res += 3
            else:
                res += 5
        
        return res
```

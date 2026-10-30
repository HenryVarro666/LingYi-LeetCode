---
title: "1807. 替换字符串中的括号内容"
aliases: ["yiduobo的每日leetcode 1807.替换字符串中的括号内容"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/464303606"
zhihu_id: "464303606"
zhihu_title: "yiduobo的每日leetcode 1807.替换字符串中的括号内容"
question_id: "1807"
question: "替换字符串中的括号内容"
problem_url: "https://leetcode.cn/problems/evaluate-the-bracket-pairs-of-a-string/"
difficulty: "Medium"
created: "2022-02-06T14:54:22+08:00"
updated: "2022-02-06T14:54:23+08:00"
upvotes: 0
comments: 0
---

# 1807. 替换字符串中的括号内容

> **[yiduobo的每日leetcode 1807.替换字符串中的括号内容](https://zhuanlan.zhihu.com/p/464303606) · 知乎 · 2022-02-06 · 赞同 0**
> 力扣：[1807. 替换字符串中的括号内容](https://leetcode.cn/problems/evaluate-the-bracket-pairs-of-a-string/) · Medium · 灵茶山艾府：[记录左括号的位置，模拟（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1807.替换字符串中的括号内容

[力扣](https://leetcode-cn.com/problems/evaluate-the-bracket-pairs-of-a-string/)

由于题目保证了括号不嵌套且一定匹配，那么就可以直接一趟遍历，当碰到左括号时开始记录括号内的key，当碰到右括号时则去knowledge中查找这个key，若存在那么将对应的value加入到答案中，否则将问号加入到答案中。对于其他不在括号内的字符，则直接加入到答案中。

关于key的查找，我在这里偷懒直接用了python的dict，但是实际上更普适的做法是用knowledge中的key做一颗trie树。

最后附上python代码：

```python
class Solution(object):
    def evaluate(self, s, knowledge):
        """
        :type s: str
        :type knowledge: List[List[str]]
        :rtype: str
        """

        knowledge_dict = {}
        for key, value in knowledge:
            knowledge_dict[key] = value
        
        res = []
        flag = False
        for char in s:
            if char == '(':
                key = []
                flag = True
            elif char == ')':
                flag = False
                res.append(knowledge_dict.get(''.join(key), '?'))
            elif flag:
                key.append(char)
            else:
                res.append(char)
        
        return ''.join(res)
```

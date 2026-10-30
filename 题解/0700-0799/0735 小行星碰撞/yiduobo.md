---
title: "735. 行星碰撞"
aliases: ["yiduobo的每日leetcode 735.行星碰撞"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/simulation", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/336467038"
zhihu_id: "336467038"
zhihu_title: "yiduobo的每日leetcode 735.行星碰撞"
question_id: "735"
question: "小行星碰撞"
problem_url: "https://leetcode.cn/problems/asteroid-collision/"
difficulty: "Medium"
created: "2020-12-12T18:38:40+08:00"
updated: "2020-12-12T18:38:40+08:00"
upvotes: 2
comments: 0
---

# 735. 行星碰撞

> **[yiduobo的每日leetcode 735.行星碰撞](https://zhuanlan.zhihu.com/p/336467038) · 知乎 · 2020-12-12 · 赞同 2**
> 力扣：[735. 小行星碰撞](https://leetcode.cn/problems/asteroid-collision/) · Medium · 灵茶山艾府：[用栈维护小行星（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

735.行星碰撞

[力扣](https://leetcode-cn.com/problems/asteroid-collision/)

对于同向的行星，不论其大小多少，永远都不可能发生碰撞，而对于反向的行星，则必然会发生碰撞，因此最终答案必然是m个负数，然后n个正数这种形式，这里的m和n都可以为0。

对于一颗行星，若其为正数，那么我们需要考察其右侧幸存的负数行星，若其为负数，那么我们需要考察其左侧幸存的正数行星。方便起见，我们选择从左往右一趟扫描的方式，此时对于每颗行星，若其为正数，则将其大小记录下来，然后考察后续的行星；若其为负数，则需要考察其左侧最近的且幸存的正数行星。需要储存，且需要最近的信息，因此这里很自然想到使用栈来做，那么现在的做法为：

1、若当前行星大小为正数，那么将其压入栈中，继续考察下一颗行星

2、若当前行星大小为负数，且当前栈不为空，栈顶元素为正数：

2-1、当前行星大小的绝对值大于栈顶元素：此时栈顶元素代表的行星将被撞毁，因此弹出栈顶元素，重复步骤2

2-2、当前行星大小的绝对值等于栈顶元素：此时栈顶元素代表的行星以及当前行星都会撞毁，因此弹出栈顶元素之后继续往后考察下一颗行星

2-3、当前行星大小的绝对值大于栈顶元素：此时当前行星将被撞毁，那么不需要对栈进行操作，直接往后考察下一颗行星

遍历完成后，栈即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def asteroidCollision(self, asteroids):
        """
        :type asteroids: List[int]
        :rtype: List[int]
        """

        stack = []
        for r in asteroids:
            if r > 0:
                stack.append(r)
            else:
                while stack and stack[-1] > 0 and stack[-1] < -r:
                    stack.pop()
                if stack and stack[-1] > 0:
                    if stack[-1] == -r:
                        stack.pop()
                else:
                    stack.append(r)

        return stack
```

---
title: "71. 简化路径"
aliases: ["yiduobo的每日leetcode 71.简化路径"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/simulation", "题单/常用数据结构", "题单/面试经典-150-题", "题单/常用数据结构/三-栈", "题单/面试经典-150-题/栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/131662648"
zhihu_id: "131662648"
zhihu_title: "yiduobo的每日leetcode 71.简化路径"
question_id: "71"
question: "简化路径"
problem_url: "https://leetcode.cn/problems/simplify-path/"
difficulty: "Medium"
created: "2020-04-16T23:27:04+08:00"
updated: "2020-04-16T23:27:04+08:00"
upvotes: 0
comments: 0
---

# 71. 简化路径

> **[yiduobo的每日leetcode 71.简化路径](https://zhuanlan.zhihu.com/p/131662648) · 知乎 · 2020-04-16 · 赞同 0**
> 力扣：[71. 简化路径](https://leetcode.cn/problems/simplify-path/) · Medium · 灵茶山艾府：[栈模拟，简洁写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

71.简化路径<https://leetcode-cn.com/problems/simplify-path/>

字符串处理的题目。上学的时候学习linux操作系统的时候还处理过更复杂的情况，具体就是是带\~、pwd之类的问题。

这里可以先split('/')，然后对于/之间的字符串，可能有以下几种情况：

1、什么都没有，例如样例中的/home//foo/中的第2、3个/，那么此时无事发生。

2、只有一个点，表示留在当前目录，也是无事发生。

3、两个点，说明跳转到上级目录（如果存在）。

4、其他，说明来到了一个新的子目录。

由于每次往上跳转时都是去掉了当前路径中的最后一个子目录，因此可以用栈来维护整个路径，当出现新的子目录时，将其压入栈顶。当需要往上及目录跳转时，则弹出栈顶即可。

最后将栈中的目录名称用/进行join，然后加上最高级目录的/即可。

最后附上python代码：

```python
class Solution(object):
    def simplifyPath(self, path):
        """
        :type path: str
        :rtype: str
        """

        path_list = path.split('/')
        now = []
        for path_part in path_list:
            if not path_part:
                continue
            elif path_part == '.':
                continue
            elif path_part == '..':
                if len(now) > 0:
                    now.pop()
            else:
                now.append(path_part)
        
        res = '/' + '/'.join(now)
        return res
```

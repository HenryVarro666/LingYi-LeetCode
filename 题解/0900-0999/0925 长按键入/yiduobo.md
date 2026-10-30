---
title: "925. 长按键入"
aliases: ["yiduobo的每日leetcode 925.长按键入"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/356457684"
zhihu_id: "356457684"
zhihu_title: "yiduobo的每日leetcode 925.长按键入"
question_id: "925"
question: "长按键入"
problem_url: "https://leetcode.cn/problems/long-pressed-name/"
created: "2021-03-11T23:37:28+08:00"
updated: "2021-03-11T23:37:28+08:00"
upvotes: 0
comments: 0
---

# 925. 长按键入

> **[yiduobo的每日leetcode 925.长按键入](https://zhuanlan.zhihu.com/p/356457684) · 知乎 · 2021-03-11 · 赞同 0**
> 力扣：[925. 长按键入](https://leetcode.cn/problems/long-pressed-name/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

925.长按键入

[力扣](https://leetcode-cn.com/problems/long-pressed-name/)

我们可以将name和typed的连续重复字符进行收缩，并统计其出现的次数。

那么如果typed可以与name对应，那么二者收缩后的字符串必然完全一致，同时对于每个字符而言，typed中的出现次数必然要大于等于name中出现的次数。

根据上面两个条件，收缩之后一趟遍历进行判断即可。

最后附上python代码：

```python
class Solution(object):
    def isLongPressedName(self, name, typed):
        """
        :type name: str
        :type typed: str
        :rtype: bool
        """

        now_char = None
        now_cnt = 0
        name_list = []
        for char in name:
            if char == now_char:
                now_cnt += 1
            else:
                if now_char is not None:
                    name_list.append([now_char, now_cnt])
                now_char = char
                now_cnt = 1

        name_list.append([now_char, now_cnt])

        now_char = None
        now_cnt = 0
        typed_list = []
        for char in typed:
            if char == now_char:
                now_cnt += 1
            else:
                if now_char is not None:
                    typed_list.append([now_char, now_cnt])
                now_char = char
                now_cnt = 1
        
        typed_list.append([now_char, now_cnt])

        if len(name_list) != len(typed_list):
            return False

        for index in range(len(name_list)):
            if name_list[index][0] != typed_list[index][0]:
                return False
            if name_list[index][1] > typed_list[index][1]:
                return False
        
        return True
```

---
title: "520. 检测大写字母"
aliases: ["yiduobo的每日leetcode 520.检测大写字母"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/260819030"
zhihu_id: "260819030"
zhihu_title: "yiduobo的每日leetcode 520.检测大写字母"
question_id: "520"
question: "检测大写字母"
problem_url: "https://leetcode.cn/problems/detect-capital/"
difficulty: "Easy"
created: "2020-09-30T21:02:00+08:00"
updated: "2020-09-30T21:02:00+08:00"
upvotes: 0
comments: 0
---

# 520. 检测大写字母

> **[yiduobo的每日leetcode 520.检测大写字母](https://zhuanlan.zhihu.com/p/260819030) · 知乎 · 2020-09-30 · 赞同 0**
> 力扣：[520. 检测大写字母](https://leetcode.cn/problems/detect-capital/) · Easy · 灵茶山艾府：[简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

520.检测大写字母<https://leetcode-cn.com/problems/detect-capital/>

比较基础的题目，按题目要求进行判断即可：

1、若单词首字母为小写字母，那么判断其后续字母中是否有大写字母。如果有，那么就不合法，否则合法。

2、若单词首字母为大写字母，且长度为1，那么合法。

3、若单词首字母为大写字母，第二个字母为小写字母，那么判断后续字母中是否有大写字母。如果有，那么就不合法，否则合法。

4、若单词首字母为大写字母，第二个字母也是大写字母，那么判断后续字母中是否有小写字母。如果有，那么就不合法，否则合法。

最后附上python代码：

```python
class Solution(object):
    def detectCapitalUse(self, word):
        """
        :type word: str
        :rtype: bool
        """

        if word[0] >= 'a':
            for char in word[1:]:
                if char < 'a':
                    return False
            return True

        if len(word) == 1:
            return True

        if word[1] >= 'a':
            for char in word[2:]:
                if char < 'a':
                    return False
            return True
        
        for char in word[2:]:
            if char >= 'a':
                return False
        return True
```

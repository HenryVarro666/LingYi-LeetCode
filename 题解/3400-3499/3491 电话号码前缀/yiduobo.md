---
title: "3491. 电话号码前缀"
aliases: ["yiduobo的每日leetcode 3491.电话号码前缀"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1899506862589730816"
zhihu_id: "1899506862589730816"
zhihu_title: "yiduobo的每日leetcode 3491.电话号码前缀"
question_id: "3491"
question: "电话号码前缀"
problem_url: "https://leetcode.cn/problems/phone-number-prefix/"
created: "2025-04-26T16:58:16+08:00"
updated: "2025-04-26T16:58:16+08:00"
upvotes: 1
comments: 0
---

# 3491. 电话号码前缀

> **[yiduobo的每日leetcode 3491.电话号码前缀](https://zhuanlan.zhihu.com/p/1899506862589730816) · 知乎 · 2025-04-26 · 赞同 1**
> 力扣：[3491. 电话号码前缀](https://leetcode.cn/problems/phone-number-prefix/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3491.电话号码前缀

[3491. 电话号码前缀 - 力扣（LeetCode）](https://leetcode.cn/problems/phone-number-prefix/description/)

题目给出一个字符串数组numbers，表示电话号码。问是否有电话号码是任何其他电话号码的前缀。

对于这类前缀匹配的问题，使用trie树是比较合适的方案。不过本题的数据规模较小，直接暴力计算也是没问题的。将所有字符串按长度从小到大进行排序，然后一趟遍历，对于当前遍历到的电话号码numbers[index]，从0到index - 1之间枚举较短的电话号码shorter，检测numbers[index]是否以shorter开头即可。

最后附上python代码：

```python
class Solution(object):
    def phonePrefix(self, numbers):
        """
        :type numbers: List[str]
        :rtype: bool
        """
        
        numbers.sort(key=lambda d:len(d))
        for index, now in enumerate(numbers):
            for shorter in numbers[:index]:
                if now.startswith(shorter):
                    return False
        
        return True
```

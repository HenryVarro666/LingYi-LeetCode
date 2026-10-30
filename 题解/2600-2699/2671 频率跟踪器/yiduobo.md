---
title: "2671. 频率跟踪器"
aliases: ["yiduobo的每日leetcode 2671.频率跟踪器"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/design", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/648847732"
zhihu_id: "648847732"
zhihu_title: "yiduobo的每日leetcode 2671.频率跟踪器"
question_id: "2671"
question: "频率跟踪器"
problem_url: "https://leetcode.cn/problems/frequency-tracker/"
difficulty: "Medium"
created: "2023-08-09T01:35:12+08:00"
updated: "2023-08-09T01:35:12+08:00"
upvotes: 1
comments: 0
---

# 2671. 频率跟踪器

> **[yiduobo的每日leetcode 2671.频率跟踪器](https://zhuanlan.zhihu.com/p/648847732) · 知乎 · 2023-08-09 · 赞同 1**
> 力扣：[2671. 频率跟踪器](https://leetcode.cn/problems/frequency-tracker/) · Medium · 灵茶山艾府：[双哈希表，简洁写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2671.频率跟踪器

[力扣](https://leetcode.cn/problems/frequency-tracker/description/)

使用两个哈希表，分别记录每种数次出现的频率，以及每种频率出现的次数。对于每次增加或者删除操作，都先更新对应数出现的频率，然后根据频率的变化更新每种频率出现的次数。对于询问操作，则只需判断询问的频率出现次数是否大于0。

最后附上python代码：

```python
class FrequencyTracker(object):

    def __init__(self):
        self.num_dict = {}
        self.freq_dict = {}

    def add(self, number):
        """
        :type number: int
        :rtype: None
        """
        freq = self.num_dict.get(number, 0)
        self.num_dict[number] = freq + 1
        self.freq_dict[freq] = self.freq_dict.get(freq, 0) - 1
        self.freq_dict[freq + 1] = self.freq_dict.get(freq + 1, 0) + 1

    def deleteOne(self, number):
        """
        :type number: int
        :rtype: None
        """
        if self.num_dict.get(number, 0) > 0:
            freq = self.num_dict[number]
            self.num_dict[number] -= 1
            self.freq_dict[freq] -= 1
            self.freq_dict[freq - 1] = self.freq_dict.get(freq - 1, 0) + 1

    def hasFrequency(self, frequency):
        """
        :type frequency: int
        :rtype: bool
        """
        return self.freq_dict.get(frequency, 0) > 0

# Your FrequencyTracker object will be instantiated and called as such:
# obj = FrequencyTracker()
# obj.add(number)
# obj.deleteOne(number)
# param_3 = obj.hasFrequency(frequency)
```

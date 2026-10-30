---
title: "2284. 最多单词数的发件人"
aliases: ["yiduobo的每日leetcode 2284.最多单词数的发件人"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/551830832"
zhihu_id: "551830832"
zhihu_title: "yiduobo的每日leetcode 2284.最多单词数的发件人"
question_id: "2284"
question: "最多单词数的发件人"
problem_url: "https://leetcode.cn/problems/sender-with-largest-word-count/"
difficulty: "Medium"
created: "2022-08-09T22:10:07+08:00"
updated: "2022-08-09T22:10:07+08:00"
upvotes: 0
comments: 0
---

# 2284. 最多单词数的发件人

> **[yiduobo的每日leetcode 2284.最多单词数的发件人](https://zhuanlan.zhihu.com/p/551830832) · 知乎 · 2022-08-09 · 赞同 0**
> 力扣：[2284. 最多单词数的发件人](https://leetcode.cn/problems/sender-with-largest-word-count/) · Medium · 灵茶山艾府：[统计空格个数 + 模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2284.最多单词数的发件人

[力扣](https://leetcode.cn/problems/sender-with-largest-word-count/)

首先可以对messages进行一趟遍历，对每条message以第一个空格为间隔符执行一次split，就可以分离出message的发件人和具体的消息内容。接下来对消息内容再执行一次split，得到的结果数组长度就是消息中单词的数量。此时就可以使用哈希表统计每个发件人发送的单词数了。

得到哈希表后，对哈希表中的发件人和消息数目进行一趟遍历，按题目要求找出最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def largestWordCount(self, messages, senders):
        """
        :type messages: List[str]
        :type senders: List[str]
        :rtype: str
        """

        cnt_dict = {}
        for index in range(len(messages)):
            cnt_dict[senders[index]] = cnt_dict.get(senders[index], 0) + len(messages[index].split(' '))

        res = None
        max_cnt = 0
        for user, cnt in cnt_dict.items():
            if cnt > max_cnt or (cnt == max_cnt and user > res):
                max_cnt, res = cnt, user
        
        return res
```

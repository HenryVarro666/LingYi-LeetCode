---
title: "937. 重新排列日志文件"
aliases: ["yiduobo的每日leetcode 937.重新排列日志文件"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/357919494"
zhihu_id: "357919494"
zhihu_title: "yiduobo的每日leetcode 937.重新排列日志文件"
question_id: "937"
question: "重新排列日志文件"
problem_url: "https://leetcode.cn/problems/reorder-data-in-log-files/"
created: "2021-03-17T22:44:41+08:00"
updated: "2021-03-17T22:44:41+08:00"
upvotes: 0
comments: 0
---

# 937. 重新排列日志文件

> **[yiduobo的每日leetcode 937.重新排列日志文件](https://zhuanlan.zhihu.com/p/357919494) · 知乎 · 2021-03-17 · 赞同 0**
> 力扣：[937. 重新排列日志文件](https://leetcode.cn/problems/reorder-data-in-log-files/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

937.重新排列日志文件

[力扣](https://leetcode-cn.com/problems/reorder-data-in-log-files/)

比较基础的题目。只需要将log通过第一个空格进行分割，然后判断分割出来的第二部分的首字符是数字还是字母，然后将其加入到字符list或者数字list的末尾。

最后，对于字符list进行排序后，合并上数字list即可。

最后附上python代码：

```python
class Solution(object):
    def reorderLogFiles(self, logs):
        """
        :type logs: List[str]
        :rtype: List[str]
        """

        letters = []
        digits = []
        for log in logs:
            tmp = log.split(' ', 1)
            if tmp[1][0] >= '0' and tmp[1][0] <= '9':
                digits.append(log)
            else:
                letters.append([tmp[0], tmp[1]])
        
        return [x[0] + ' ' + x[1] for x in sorted(letters, key=lambda d:(d[1], d[0]))] + digits
```

---
title: "165. 比较版本号"
aliases: ["yiduobo的每日leetcode 165.比较版本号"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/144363173"
zhihu_id: "144363173"
zhihu_title: "yiduobo的每日leetcode 165.比较版本号"
question_id: "165"
question: "比较版本号"
problem_url: "https://leetcode.cn/problems/compare-version-numbers/"
difficulty: "Medium"
created: "2020-05-28T23:20:15+08:00"
updated: "2020-05-28T23:20:15+08:00"
upvotes: 1
comments: 0
---

# 165. 比较版本号

> **[yiduobo的每日leetcode 165.比较版本号](https://zhuanlan.zhihu.com/p/144363173) · 知乎 · 2020-05-28 · 赞同 1**
> 力扣：[165. 比较版本号](https://leetcode.cn/problems/compare-version-numbers/) · Medium · 灵茶山艾府：[库函数写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

165.比较版本号<https://leetcode-cn.com/problems/compare-version-numbers/>

字符串处理的题目，python写起来也很简单。使用split分离字符串之后逐个比较即可，需要注意当某个版本号的某一位缺失时应该当做0来计算，即样例5中的情况。

最后附上python代码：

```python
class Solution(object):
    def compareVersion(self, version1, version2):
        """
        :type version1: str
        :type version2: str
        :rtype: int
        """

        v1 = version1.split('.')
        v2 = version2.split('.')

        now = 0
        while now < len(v1) or now < len(v2):
            v1_number = int(v1[now]) if now < len(v1) else 0
            v2_number = int(v2[now]) if now < len(v2) else 0
            if v1_number < v2_number:
                return -1
            elif v1_number > v2_number:
                return 1
            else:
                now += 1
                
        return 0
```

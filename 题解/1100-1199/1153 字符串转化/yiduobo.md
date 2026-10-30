---
title: "1153. 字符串转化"
aliases: ["yiduobo的每日leetcode 1153.字符串转化"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/611167811"
zhihu_id: "611167811"
zhihu_title: "yiduobo的每日leetcode 1153.字符串转化"
question_id: "1153"
question: "字符串转化"
problem_url: "https://leetcode.cn/problems/string-transforms-into-another-string/"
created: "2023-03-04T00:05:55+08:00"
updated: "2023-03-04T00:05:55+08:00"
upvotes: 0
comments: 0
---

# 1153. 字符串转化

> **[yiduobo的每日leetcode 1153.字符串转化](https://zhuanlan.zhihu.com/p/611167811) · 知乎 · 2023-03-04 · 赞同 0**
> 力扣：[1153. 字符串转化](https://leetcode.cn/problems/string-transforms-into-another-string/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1153.字符串转化

[力扣](https://leetcode.cn/problems/string-transforms-into-another-string/)

首先，如果某个字符需要变换成多个不同的字符，那么答案显示是false，而对于其他的情况，可能出现冲突的就是互相变换，例如a要变成b，b要变成c，那么在这里就必须先执行b变成c，再执行a变成b。

更进一步的，按照上面的说法似乎涉及到拓扑排序，那么不妨考虑如果出现了变换的环应该怎么处理。从最简单的环入手，即a变成b，b变成a，那么在这里相当于交换a和b。对于这个问题，最经典的做法自然是搞一个中间字符c来辅助变换。也就是说，只要存在空闲的中间字符就可以解决掉变换的环，也就是说在这里不考虑具体的变换方式，只要存在空闲的字符且没有单个字符变成多个字符的变换，那么就一定可以完成所有的变换。

到了这里，就可以一趟遍历，使用哈希表记录字符的变换规则，使用集合记录使用过的目标字符。若过程中出现某个字符当前的变换目标与哈希表中记录的不一致，那么说明该字符需要变换成多个不同的字符，此时直接返回false。遍历完成后，若当前的目标字符集合大小小于26，说明存在空闲字符，那么返回true。而对于目标字符集合等于26的情况，还存在一种可能的变换方式就是原字符串与目标字符串完全一致，这种情况下也应该返回true，否则就会出现因为变换的路径上有环，且没有空闲的中间字符导致无法变换的情况，此时应该返回false。

值得一提的是，在目标字符数组等于26时是一定可以确定变换规则中存在环的，因为此时相当于构造出了一个26个节点，26条边的有向图，而26个节点组成的树中恰好是25条边，多出的这条边必然会在树中形成环。

最后附上python代码：

```python
class Solution(object):
    def canConvert(self, str1, str2):
        """
        :type str1: str
        :type str2: str
        :rtype: bool
        """

        mapping = {}
        used = set()
        for char1, char2 in zip(str1, str2):
            if char1 not in mapping:
                mapping[char1] = char2
            elif mapping[char1] != char2:
                return False
            
            used.add(char2)
        
        return str1 == str2 or len(used) < 26
```

---
title: "1366. 通过投票对团队排名"
aliases: ["yiduobo的每日leetcode 1366.通过投票对团队排名"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/array", "leetcode/hash-table", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/400037197"
zhihu_id: "400037197"
zhihu_title: "yiduobo的每日leetcode 1366.通过投票对团队排名"
question_id: "1366"
question: "通过投票对团队排名"
problem_url: "https://leetcode.cn/problems/rank-teams-by-votes/"
difficulty: "Medium"
created: "2021-08-15T18:23:41+08:00"
updated: "2021-08-15T18:23:41+08:00"
upvotes: 0
comments: 0
---

# 1366. 通过投票对团队排名

> **[yiduobo的每日leetcode 1366.通过投票对团队排名](https://zhuanlan.zhihu.com/p/400037197) · 知乎 · 2021-08-15 · 赞同 0**
> 力扣：[1366. 通过投票对团队排名](https://leetcode.cn/problems/rank-teams-by-votes/) · Medium · 灵茶山艾府：[自定义排序，简洁写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1366.通过投票对团队排名

[力扣](https://leetcode-cn.com/problems/rank-teams-by-votes/)

有一种经典的排序方式，名称为基数排序。其做法是先将要排序的数补充到同样的长度，然后从低位开始向高位遍历，逐位进行排序。

例如133、123、223以及321。首先排最低位，那么得到的结果是

321、133、123、223

接下来排十位，那么得到的结果是

321、123、223、133

最后再排百位，那么最终结果为

123、133、223、321

在这里我们同样可以从低位开始向高位遍历，按每一位上字符出现的次数来进行排序即可。

另外，一般来说对于每一位的排序，由于数字的范围较小，因此都会使用桶排序。我在这里偷懒，直接使用了sort。

最后附上python代码：

```python
class Solution(object):
    def rankTeams(self, votes):
        """
        :type votes: List[str]
        :rtype: str
        """

        n = len(votes)
        l = len(votes[0])
        char_set = set(list(votes[0]))
        cnt_list = [{} for _ in range(l)]
        for vote in votes:
            for index, char in enumerate(vote):
                if char not in cnt_list[index]:
                    cnt_list[index][char] = 0
                cnt_list[index][char] += 1
        
        order = {}
        cnt = 0
        for asc in range(26):
            char = chr(asc + 65)
            if char in char_set:
                order[char] = cnt
                cnt += 1

        for index in range(l - 1, -1, -1):
            order = {x: index for index, x in enumerate(sorted(order.keys(), key=lambda d:(-cnt_list[index].get(d, 0), order[d])))}

        return ''.join([x[0] for x in sorted(order.items(), key=lambda d:d[1])])
```

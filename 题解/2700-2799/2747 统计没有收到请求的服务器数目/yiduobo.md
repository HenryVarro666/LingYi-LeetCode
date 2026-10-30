---
title: "2747. 统计没有收到请求的服务器数目"
aliases: ["yiduobo的每日leetcode 2747.统计没有收到请求的服务器数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/常用数据结构", "题单/常用数据结构/专题-离线算法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/653980161"
zhihu_id: "653980161"
zhihu_title: "yiduobo的每日leetcode 2747.统计没有收到请求的服务器数目"
question_id: "2747"
question: "统计没有收到请求的服务器数目"
problem_url: "https://leetcode.cn/problems/count-zero-request-servers/"
difficulty: "Medium"
rating: 2405
created: "2023-09-03T02:46:07+08:00"
updated: "2023-09-03T02:46:07+08:00"
upvotes: 0
comments: 0
---

# 2747. 统计没有收到请求的服务器数目

> **[yiduobo的每日leetcode 2747.统计没有收到请求的服务器数目](https://zhuanlan.zhihu.com/p/653980161) · 知乎 · 2023-09-03 · 赞同 0**
> 力扣：[2747. 统计没有收到请求的服务器数目](https://leetcode.cn/problems/count-zero-request-servers/) · Medium · 灵茶山艾府：[离线+滑动窗口（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2747.统计没有收到请求的服务器数目

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/count-zero-request-servers/)

题目中的询问区间长度固定，那么很自然想到使用滑动窗口来求解。具体来说，就是使用一个长度为x的滑动窗口，让窗口的右边界从询问中的最小值开始向右滑动，直到来到询问中的最大值，那么在这里就需要先将询问从小到大进行排序。

另一方面，窗口内部统计的信息应该是在窗口内每个服务器收到消息的次数，那么当窗口滑动时，首先将右边界时间点收到消息的服务器对应的次数加上1，然后将老的左边界时间点收到消息的服务器对应的次数减去1，因此在这里就需要预先得到每个时间点有哪些服务器收到了消息，因此需要遍历logs，使用哈希表储存每个时间点收到消息的服务器列表。

接下来，使用排序后询问的最小时间点减去x到最小时间点这一段来初始化窗口并更新答案，接下来每一轮，窗口右边界将滑过上一个询问的时间点加1，到这一个询问的时间点，期间更新窗口内每个服务器收到请求的数目，然后更新答案即可。

这种实现看上去复杂度很高，但是实际上每个时间点只会进出窗口一次，同时每个请求也只会被加减一次，因此滑动过程的时间复杂度就是询问的时间跨度，最大不超过10^6。

最后附上python代码：

```python
class Solution(object):
    def countServers(self, n, logs, x, queries):
        """
        :type n: int
        :type logs: List[List[int]]
        :type x: int
        :type queries: List[int]
        :rtype: List[int]
        """

        log_info = {}
        for sid, t in logs:
            if t not in log_info:
                log_info[t] = set()
            log_info[t].add(sid)
        
        cnt = {}
        q_info = sorted(enumerate(queries), key=lambda d:d[1])

        res = [None] * len(q_info)
        for t in range(q_info[0][1] - x, q_info[0][1] + 1):
            if t in log_info:
                for sid in log_info[t]:
                    cnt[sid] = cnt.get(sid, 0) + 1
        res[q_info[0][0]] = n - len(cnt)

        for index in range(1, len(q_info)):
            for t in range(q_info[index - 1][1] + 1, q_info[index][1] + 1):
                if t in log_info:
                    for sid in log_info[t]:
                        cnt[sid] = cnt.get(sid, 0) + 1
            
                if t - x - 1 in log_info:
                    for sid in log_info[t - x - 1]:
                        cnt[sid] -= 1
                        if cnt[sid] == 0:
                            cnt.pop(sid)
            
            res[q_info[index][0]] = n - len(cnt)

        return res
```

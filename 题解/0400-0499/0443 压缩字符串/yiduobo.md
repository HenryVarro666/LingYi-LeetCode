---
title: "443. 压缩字符串"
aliases: ["yiduobo的每日leetcode 443.压缩字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/205567882"
zhihu_id: "205567882"
zhihu_title: "yiduobo的每日leetcode 443.压缩字符串"
question_id: "443"
question: "压缩字符串"
problem_url: "https://leetcode.cn/problems/string-compression/"
created: "2020-08-29T21:42:42+08:00"
updated: "2020-08-29T21:42:42+08:00"
upvotes: 0
comments: 0
---

# 443. 压缩字符串

> **[yiduobo的每日leetcode 443.压缩字符串](https://zhuanlan.zhihu.com/p/205567882) · 知乎 · 2020-08-29 · 赞同 0**
> 力扣：[443. 压缩字符串](https://leetcode.cn/problems/string-compression/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

443.压缩字符串<https://leetcode-cn.com/problems/string-compression/>

比较基础的题目。一趟扫描统计每个字符连续出现的次数，若cnt大于1，那么就需要进行压缩。需要注意的是，在将cnt放入chars数组中时，如果使用mod 10取余的做法逐位放进去，那么需要将高位放在左边低位放在右边。

最后附上python代码：

```python
class Solution(object):
    def compress(self, chars):
        """
        :type chars: List[str]
        :rtype: int
        """
        
        res_len = 0
        now = None
        cnt = 0
        for char in chars:
            if now == char:
                cnt += 1
            else:
                if now is not None:
                    chars[res_len] = now
                    res_len += 1
                    if cnt > 1:
                        cnt_len = 0
                        tmp = cnt
                        while tmp:
                            tmp /= 10
                            cnt_len += 1
                        tmp_len = cnt_len
                        while cnt:
                            chars[res_len + tmp_len - 1] = chr(cnt % 10 + 48)
                            tmp_len -= 1
                            cnt /= 10
                        res_len += cnt_len

                now = char
                cnt = 1

        if now:
            chars[res_len] = now
            res_len += 1
            if cnt > 1:
                cnt_len = 0
                tmp = cnt
                while tmp:
                    tmp /= 10
                    cnt_len += 1
                tmp_len = cnt_len
                while cnt:
                    chars[res_len + tmp_len - 1] = chr(cnt % 10 + 48)
                    tmp_len -= 1
                    cnt /= 10
                res_len += cnt_len

        return res_len
```

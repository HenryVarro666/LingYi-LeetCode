---
title: "1864. 构成交替字符串需要的最小交换次数"
aliases: ["yiduobo的每日leetcode 1864.构成交替字符串需要的最小交换次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string", "题单/贪心算法", "题单/贪心算法/八-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/473858538"
zhihu_id: "473858538"
zhihu_title: "yiduobo的每日leetcode 1864.构成交替字符串需要的最小交换次数"
question_id: "1864"
question: "构成交替字符串需要的最小交换次数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-swaps-to-make-the-binary-string-alternating/"
difficulty: "Medium"
rating: 1601
created: "2022-02-28T23:22:31+08:00"
updated: "2022-02-28T23:22:31+08:00"
upvotes: 1
comments: 0
---

# 1864. 构成交替字符串需要的最小交换次数

> **[yiduobo的每日leetcode 1864.构成交替字符串需要的最小交换次数](https://zhuanlan.zhihu.com/p/473858538) · 知乎 · 2022-02-28 · 赞同 1**
> 力扣：[1864. 构成交替字符串需要的最小交换次数](https://leetcode.cn/problems/minimum-number-of-swaps-to-make-the-binary-string-alternating/) · Medium · 灵茶山艾府：[比较 1010... 或 0101... 的最小不同值](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1864.构成交替字符串需要的最小交换次数

[力扣](https://leetcode-cn.com/problems/minimum-number-of-swaps-to-make-the-binary-string-alternating/)

好像之前有一道一模一样的题目，但是记不清楚题号了。

首先，合法的交替字符串只有奇数位都是1，偶数位都是0，以及奇数位都是0，偶数位都是1这两种情况。无论是哪种情况，0和1的个数之差至多为1。具体的，设字符串长度为n，若n为奇数，那么0和1这两种字符，出现在偶数位的需要有n / 2 + 1个，出现在奇数位则需要n / 2个；相对的，若n为偶数，不论奇偶都需要n / 2个。

也就是说，首先可以统计0和1出现的次数。若二者出现的次数相差超过一个，那么返回false。否则的话，在这里可以将n的长度是奇数和偶数的情况统一起来考虑。若1的个数大于等于0的个数，那么可以尝试将1放在偶数位上；同样的，若0的个数大于等于1的个数，则可以尝试将0放在偶数位上。

由于题目可以自由交换各个位置上的字符，因此若需要将1放在偶数位上，那么交换的次数就是不在偶数位上的1的个数，而如果要将0放在偶数位上，那么交换的次数就是在偶数位上的1的个数，因此只需要在统计1和0的个数时顺便统计偶数位上1的个数。另外，由于0的个数就等于字符串长度减去1的个数，因此实际上只需要统计1的个数，以及偶数位上1的个数就行了。

最后附上python代码：

```python
class Solution(object):
    def minSwaps(self, s):
        """
        :type s: str
        :rtype: int
        """

        cnt_one = 0
        even_one = 0
        for index, char in enumerate(s):
            if char == '1':
                cnt_one += 1
                if index % 2 == 0:
                    even_one += 1

        if abs(cnt_one - (len(s) - cnt_one)) >= 2:
            return -1
        
        res = cnt_one

        if cnt_one >= len(s) - cnt_one:
            res = min(res, cnt_one - even_one)
        
        if cnt_one <= len(s) - cnt_one:
            res = min(res, even_one)
        
        return res
```

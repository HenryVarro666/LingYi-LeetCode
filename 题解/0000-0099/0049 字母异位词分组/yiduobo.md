---
title: "49. 字母异位词分组"
aliases: ["yiduobo的每日leetcode 49.字母异位词分组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/string", "leetcode/sorting", "题单/贪心算法", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/贪心算法/五-思维题", "题单/LeetCode-热题-100/哈希", "题单/面试经典-150-题/哈希表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/126357843"
zhihu_id: "126357843"
zhihu_title: "yiduobo的每日leetcode 49.字母异位词分组"
question_id: "49"
question: "字母异位词分组"
problem_url: "https://leetcode.cn/problems/group-anagrams/"
difficulty: "Medium"
created: "2020-04-06T22:59:43+08:00"
updated: "2020-04-06T22:59:43+08:00"
upvotes: 0
comments: 0
---

# 49. 字母异位词分组

> **[yiduobo的每日leetcode 49.字母异位词分组](https://zhuanlan.zhihu.com/p/126357843) · 知乎 · 2020-04-06 · 赞同 0**
> 力扣：[49. 字母异位词分组](https://leetcode.cn/problems/group-anagrams/) · Medium · 灵茶山艾府：[哈希表分组，简洁写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

49.字母异位词分组<https://leetcode-cn.com/problems/group-anagrams/>

简单的字符串处理题。

由于题目描述只包含小写字母，那么对于strs中的每个字符串，可以先统计出当前字符串中每个字母出现的次数，然后用这个次数作为dict的key来将异位词加入到key所对应的list当中，最后按key输出对应的list即可。

最后附上python代码，其中97位小写字母a的ascii码，作用是将a-z映射到0-25：

```python
class Solution(object):
    def groupAnagrams(self, strs):
        """
        :type strs: List[str]
        :rtype: List[List[str]]
        """

        res_dict = {}

        for string in strs:
            str_list = [0] * 26
            for char in string:
                str_list[ord(char) - 97] += 1
            key = ''
            for index, count in enumerate(str_list):
                if count > 0:
                    key = key + chr(index + 97) + str(count)
            if key not in res_dict:
                res_dict[key] = []
            res_dict[key].append(string)

        return res_dict.values()
```

---
title: "1487. 保证文件名唯一"
aliases: ["yiduobo的每日leetcode 1487.保证文件名唯一"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/416460573"
zhihu_id: "416460573"
zhihu_title: "yiduobo的每日leetcode 1487.保证文件名唯一"
question_id: "1487"
question: "保证文件名唯一"
problem_url: "https://leetcode.cn/problems/making-file-names-unique/"
created: "2021-10-02T23:38:59+08:00"
updated: "2021-10-02T23:38:59+08:00"
upvotes: 0
comments: 0
---

# 1487. 保证文件名唯一

> **[yiduobo的每日leetcode 1487.保证文件名唯一](https://zhuanlan.zhihu.com/p/416460573) · 知乎 · 2021-10-02 · 赞同 0**
> 力扣：[1487. 保证文件名唯一](https://leetcode.cn/problems/making-file-names-unique/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1487.保证文件名唯一

[力扣](https://leetcode-cn.com/problems/making-file-names-unique/)

题目并不难，但是有些奇怪的case，例如最后一个样例中的kaido(1)最终被变成了kaido(1)(1)，也就是说这里不能将kaido(1)拆分成kaido和序号1之后，由于1和2被使用过，然后得出答案为kaido(3)，而是应该直接将kaido(1)视为一个字符串，在后面添加上额外的1，得到kaido(1)(1)。

那么此时只需要保存每个字符串已经使用过的序号，然后每次检测当前的字符串是否被使用过。若被使用过，那么在该字符串后面加上对应的序号，然后再进行检测，直到没有出现过位置。为了保存这个序号，就需要使用一个dict保存当前所有字符串已经用到了哪个序号。接下来只需遍历names中的所有字符串，对于当前字符串name：

1、若其没有在dict中出现过，说明该字符串还没有被使用过，那么将其加入到dict以及答案中，同时将该字符使用的序号置为1

2、若其在dict中出现过，设当前已经使用的序号dict[name]为x，那么就应该将其改写成name(x)的形式。接下来还需要检测name(x)是否在dict中出现过，若出现过，则重复此过程，不断在其后面添加序号，直到其没有在dict中出现过为止。对于最终得到的字符串，同样是将其加入到dict和答案中，并将该字符串使用的序号置为1

最后附上python代码：

```python
class Solution(object):
    def getFolderNames(self, names):
        """
        :type names: List[str]
        :rtype: List[str]
        """

        name_dict = {}
        res = []
        for name in names:
            tmp = name
            while tmp in name_dict:
                tmp = name + '(' + str(name_dict[name]) + ')'
                name_dict[name] += 1
                
            name = tmp
            name_dict[name] = 1
            res.append(name)
        
        return res
```

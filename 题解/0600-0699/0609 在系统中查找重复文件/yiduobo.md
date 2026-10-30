---
title: "609. 在系统中查找重复文件"
aliases: ["yiduobo的每日leetcode 609.在系统中查找重复文件"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/268910089"
zhihu_id: "268910089"
zhihu_title: "yiduobo的每日leetcode 609.在系统中查找重复文件"
question_id: "609"
question: "在系统中查找重复文件"
problem_url: "https://leetcode.cn/problems/find-duplicate-file-in-system/"
created: "2020-10-26T22:35:08+08:00"
updated: "2020-10-26T22:35:08+08:00"
upvotes: 0
comments: 0
---

# 609. 在系统中查找重复文件

> **[yiduobo的每日leetcode 609.在系统中查找重复文件](https://zhuanlan.zhihu.com/p/268910089) · 知乎 · 2020-10-26 · 赞同 0**
> 力扣：[609. 在系统中查找重复文件](https://leetcode.cn/problems/find-duplicate-file-in-system/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

609.在系统中查找重复文件<https://leetcode-cn.com/problems/find-duplicate-file-in-system/>

由于题目保证文件数量不超过20000，且内容长度不超过50，那么就可以当做简单的字符串处理问题来做。

具体来说就是遍历每一个目录，然后遍历其中的文件，将文件内容作为key，目录名称加文件名作为value储存到dict当中。处理完毕后，若dict中某个key对应的value中包含多个文件名，说明该文件重复，将value对应的文件名加入到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def findDuplicate(self, paths):
        """
        :type paths: List[str]
        :rtype: List[List[str]]
        """

        file_dict = {}
        for path in paths:
            tmp = path.split(' ')
            file_dir = tmp[0]
            for index in range(1, len(tmp)):
                file_name, file_content = tmp[index][:-1].split('(')
                if file_content not in file_dict:
                    file_dict[file_content] = []
                file_dict[file_content].append(file_dir + '/' + file_name)
        
        res = []
        for file_content in file_dict:
            if len(file_dict[file_content]) > 1:
                res.append(file_dict[file_content])

        return res
```

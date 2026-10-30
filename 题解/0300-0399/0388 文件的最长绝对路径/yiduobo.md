---
title: "388. 文件的最长绝对路径"
aliases: ["yiduobo的每日leetcode 388.文件的最长绝对路径"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/170584393"
zhihu_id: "170584393"
zhihu_title: "yiduobo的每日leetcode 388.文件的最长绝对路径"
question_id: "388"
question: "文件的最长绝对路径"
problem_url: "https://leetcode.cn/problems/longest-absolute-file-path/"
created: "2020-08-06T21:15:58+08:00"
updated: "2020-08-06T21:15:58+08:00"
upvotes: 0
comments: 0
---

# 388. 文件的最长绝对路径

> **[yiduobo的每日leetcode 388.文件的最长绝对路径](https://zhuanlan.zhihu.com/p/170584393) · 知乎 · 2020-08-06 · 赞同 0**
> 力扣：[388. 文件的最长绝对路径](https://leetcode.cn/problems/longest-absolute-file-path/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

388.文件的最长绝对路径<https://leetcode-cn.com/problems/longest-absolute-file-path/submissions/>

通过换行将每个文件或者文件夹名称分离出来，然后通过统计tab的个数，将每个文件或文件夹的名称填到数组对应的位置上。

例如样例二的

dir\\n\\tsubdir1\\n\\t\\tfile1.ext\\n\\t\\tsubsubdir1\\n\\tsubdir2\\n\\t\\tsubsubdir2\\n\\t\\t\\tfile2.ext

按照换行分离后分别是

dir

[\\t]subdir1

[\\t\\t]file1.ext

[\\t\\t]subsubdir1

[\\t]subdir2

[\\t\\t]subsubdir2

[\\t\\t\\t]file2.ext

由于题目需要统计的是文件的路径长度，因此对于带有'.'符号的字符串，我们只需要求出文件长度，对于没有带'.'的字符串，我们则需要将其储存起来方便后续计算文件夹长度。

设f[i]表示第i层文件夹的长度，那么对于上面的样例就有：

1、首先f[0] \= 0，表示处于根目录中

2、对于dir1，长度为3，带上后续的'\\'就是4，于是有f[1] \= 4

3、对于[\\t]subdir1，长度为7，有一个tab符号，于是有f[2] \= 8

4、对于[\\t\\t]file1.ext，长度为9，字符串中有'.'，需要求总长度。注意到有两个tab符号，于是其总长度为f[1] + f[2] + 9 \= 21

5、对于[\\t\\t]subsubdir1，长度为10，有两个tab符号，于是有f[3] \= 11

6、对于[\\t]subdir2，长度为7，只有一个tab符号，此时之前[\\t]subdir1中的内容已经处理完毕了，因此可以直接覆盖掉f[2]，于是有f[2] \= 8

7、对于[\\t\\t]subsubdir2，长度为10，有两个tab符号，同样是覆盖掉f[3]，即f[3] \= 11

8、对于[\\t\\t\\t]file2.ext，字符串中有'.'，需要求总长度，为f[1] + f[2] + f[3] + 9 \= 32

因此最终答案为32。

注意到对于文件夹来说，需要关注的是f的前缀和，而对于f本身的值并不关心，于是可以直接维护前缀和数组来提高效率。

最后附上代码，其中prefix为前缀和数组：

```python
class Solution(object):
    def lengthLongestPath(self, input):
        """
        :type input: str
        :rtype: int
        """

        res = 0

        prefix = [0]
        for part in split(input, '\n'):
            pos = 0
            while part[pos] == '\t':
                pos += 1
            l = len(part) - pos + prefix[pos]

            if part.find('.') != -1:
                res = max(res, l)
            else:
                if len(prefix) < pos + 2:
                    prefix.append(l + 1)
                else:
                    prefix[pos + 1] = l + 1

        return res
```

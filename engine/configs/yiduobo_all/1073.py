CONFIG = dict(
    num=1073, title='负二进制数相加', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='逐位相加 + 负二进制进位', tags=[],
    code='''
class Solution(object):
    def addNegabinary(self, arr1, arr2):

        m = len(arr1)
        n = len(arr2)
        res = [0] * max(m, n)
        for index in range(m):
            res[m - index - 1] += arr1[index]
        for index in range(n):
            res[n - index - 1] += arr2[index]
        
        p = 0
        while p < len(res):
            if res[p] > 1:
                if p + 1 < len(res) and res[p + 1] > 0:
                    res[p + 1] -= 1
                else:
                    if p + 1 < len(res):
                        res[p + 1] += 1
                    else:
                        res.append(1)
                    if p + 2 < len(res):
                        res[p + 2] += 1
                    else:
                        res.append(1)

                res[p] -= 2
            
            p += 1

        
        while len(res) > 1 and res[-1] == 0:
            res.pop()
        res.reverse()
        return res
''',
    call='Solution().addNegabinary([1,1,1], [1,1,1])',
    expect=[1, 1, 0, 1, 0],
    views=[
        dict(type='array', var='arr1', h=150, label='arr1（高位在前）', cell=90),
        dict(type='array', var='arr2', h=150, label='arr2（高位在前）', cell=90),
        dict(type='array', var='res', h=200, label='res：逐位和（低位在前，> 1 要进位）', pointers={'p': 'pink'}, cell=90,
             color=lambda S, i, v: 'red' if v > 1 else None),
    ],
    watch=['m', 'n', 'p', ('res', 'res', 'green')],
    captions={
        'res = [0]': '`res` 按较长的那个数开空间，低位在前：长度 `{len(res)}`',
        'res[m - index - 1] += arr1[index]': '`arr1` 第 `{index}` 个数放到 `res[{m-index-1}]`（翻成低位在前）：`{res}`',
        'res[n - index - 1] += arr2[index]': '`arr2` 第 `{index}` 个数放到 `res[{n-index-1}]`：`{res}`',
        'p = 0': '从最低位开始处理进位',
        'while p < len(res)': '检查第 `{p}` 位：=={"系数 > 1，需要进位" if p < len(res) and res[p] > 1 else "无需处理"}==',
        'if res[p] > 1': '`res[{p}] = {res[p]}`：=={"大于 1，进位" if res[p] > 1 else "不大于 1，跳过"}==。`2·(−2)^k = −(−2)^(k+1)`',
        'if p + 1 < len(res) and res[p + 1] > 0': '高一位系数 `{res[p+1] if p+1 < len(res) else 0}`：=={"有 → 减 1 抵消" if p+1 < len(res) and res[p+1] > 0 else "没有 → 高一位和高两位都加 1"}==',
        'res[p + 1] -= 1': '抵消：高一位减 1 → `{res}`',
        'res[p + 1] += 1': '高一位加 1：`{res}`',
        'res[p + 2] += 1': '高两位也加 1：`{res}`',
        'res.append(1)': '长度不够，补一位 `1`：`{res}`',
        'res[p] -= 2': '这一位减 2：`{res}`',
        'p += 1': '看下一位，`p` → {p}',
        'while len(res) > 1': '去掉高位多余的 0：=={"末尾是 0，弹出" if len(res) > 1 and res[-1] == 0 else "没有前导 0 了"}==',
        'res.pop()': '弹出前导 0：`{res}`',
        'res.reverse()': '翻转成高位在前',
        'return res': '结果 `{ret}`',
    },
    cards=dict(
        one_liner='先逐位相加，再用负二进制进位规则一趟清理',
        complexity='时间 `O(max(m, n))`，空间 `O(max(m, n))`',
        problem=['给两个以 `−2` 为基的数（数组，高位在前）',
                 '返回它们的和，同样是 `−2` 进制数组，不含前导 0',
                 '示例：`[1,1,1,1,1] + [1,0,1]` → `[1,0,0,0,0]`',
                 '本视频：`[1,1,1] + [1,1,1]`（3+3）→ `[1,1,0,1,0]`（6）'],
        quote='对于某一位需要进位的p，若第p + 1位上不等于0，那么就将第p + 1位减去1，同时将第p位减去2；若第p + 1位上等于0，那么需要将第p + 1位以及第p + 2位都加上1，同时将第p位减去2。',
        quote_src='—— yiduobo 题解原文',
        idea=['沿用 1017 题的结论：这一位 ≥ 2，就要进位',
              '高一位非 0：减 1 抵消；高一位为 0：高一位、高两位都加 1',
              '先对齐相加，再从低位到高位一趟清理，最后去前导 0'],
        summary=['时间 `O(max(m, n))`，空间 `O(max(m, n))`',
                 '原文已是 Python 3 可运行写法，未作修改',
                 '易错：高位补 1 时可能要新增两位；最后要去掉前导 0 但至少留一位',
                 '同类题：1017 负二进制转换'],
    ),
)

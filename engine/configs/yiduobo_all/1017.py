CONFIG = dict(
    num=1017, title='负二进制转换', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='二进制转负二进制 + 进位', tags=[],
    code='''
class Solution(object):
    def baseNeg2(self, N):

        if N == 0:
            return "0"

        x = N
        origin = []
        while x:
            origin.append(x % 2)
            x //= 2
        
        p = 0
        res = []
        for index, num in enumerate(origin):
            if index < len(res):
                res[index] += num
            else:
                res.append(num)

            if index % 2 == 1 and num == 1:
                if index + 1 < len(res):
                    res[index + 1] += num
                else:
                    res.append(num)

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

        res.reverse()
        return ''.join(str(x) for x in res)
''',
    call='Solution().baseNeg2(6)',
    expect='11010',
    views=[
        dict(type='array', var='origin', h=170, label='origin：N 的二进制（低位在前）', pointers={'index': 'blue'}, cell=100),
        dict(type='array', var='res', h=200, label='res：每位的系数（低位在前，> 1 要进位）', pointers={'p': 'pink'}, cell=100,
             color=lambda S, i, v: 'red' if v > 1 else None),
        dict(type='text', size=32, fn=lambda S: '`(−2)^k`：k 偶数 = `2^k`，k 奇数 = `−2^k`'),
    ],
    watch=['x', 'index', 'p', ('N', 'N', 'green')],
    captions={
        'if N == 0': '`N = {N}`：0 的负二进制就是 `"0"`，这里不是 0，继续',
        'x = N': '先把 `N = {N}` 转成普通二进制',
        'origin.append': '`x % 2 = {x % 2}`：二进制的一位放进 `origin`（低位在前）',
        'x //= 2': '`x` → {x}',
        'for index, num': '第 `{index}` 位，二进制值 `{num}`',
        'res[index] += num': '偶数位 `2^k = (−2)^k`，直接加到 `res[{index}]`：`{res}`',
        'if index % 2 == 1': lambda S, B, r: ('第 `%d` 位是奇数位且为 1：`2^k = (−2)^(k+1) + (−2)^k`，要在高一位再补一个 1' % S.index) if S.index % 2 == 1 and S.num == 1 else ('第 `%d` 位是偶数位或为 0：`2^k = (−2)^k`，不用补位' % S.index),
        'res[index + 1] += num': '奇数位的 1 向高一位补 1：`res = {res}`',
        'res.append(num)': '`res` 还没有这一位，新增系数 `{num}`：`{res}`',
        'while p < len(res)': '检查第 `{p}` 位：=={"系数 > 1，需要进位" if p < len(res) and res[p] > 1 else "无需处理"}==',
        'if res[p] > 1': '`res[{p}] = {res[p]}`：=={"大于 1，进位" if res[p] > 1 else "不大于 1，跳过"}==。`2·(−2)^k = −(−2)^(k+1)`',
        'if p + 1 < len(res) and res[p + 1] > 0': '高一位已有系数 `{res[p+1] if p+1 < len(res) else 0}`：=={"有 → 两个 (−2)^k 把它抵消掉 1" if p+1 < len(res) and res[p+1] > 0 else "没有 → 要变形"}==',
        'res[p + 1] -= 1': '抵消：`res[p+1]` 减 1 → `{res}`',
        'res[p + 1] += 1': '`−(−2)^(k+1) = (−2)^(k+2) + (−2)^(k+1)`：先把第 `{p+1}` 位置 1',
        'res.append(1)': '补出新的一位 `1`：`{res}`',
        'res[p + 2] += 1': '同时第 `{p+2}` 位也加 1：`{res}`',
        'res[p] -= 2': '这一位减 2：`res = {res}`',
        'p += 1': '看下一位，`p` → {p}',
        'res.reverse()': '翻转成高位在前',
        'return': '负二进制表示：`{ret}`',
    },
    cards=dict(
        one_liner='先转二进制，再按奇偶位修正，最后处理进位',
        complexity='时间 `O(log N)`，空间 `O(log N)`',
        problem=['把非负整数 `N` 转成以 `−2` 为基的二进制字符串',
                 '例如 `2 → "110"`，`3 → "111"`，`4 → "100"`',
                 '本视频：`N = 6` → `"11010"`'],
        quote='(-2)^k + (-2)^k = 2 * (-2)^k = -1 * -2 * (-2)^k = -(-2)^(k + 1)',
        quote_src='—— yiduobo 题解原文',
        idea=['`(−2)^k` 偶数次方等于 `2^k`，奇数次方是 `−2^k`',
              '奇数位上的 `2^k = (−2)^(k+1) + (−2)^k`：额外补一个高位 1',
              '某位出现两个 → 与高一位抵消，高一位没有就向上变形并继续进位'],
        summary=['时间 `O(log N)`，空间 `O(log N)`',
                 '原文为 Python 2 写法，整数除法 `/=` 已改为 `//=`',
                 '易错：进位会连锁到 k+2 位，要边走边检查长度',
                 '同类题：1073 负二进制数相加，用同一套进位规则'],
    ),
)

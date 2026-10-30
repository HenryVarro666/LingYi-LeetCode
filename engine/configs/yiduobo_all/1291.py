def _text(S):
    if 'q' not in S:
        return '合法的数只有 8+7+…+1 = 36 个，先按顺序生成，再按 `low` 截取'
    if S.get('now') is None:
        return '`q[l:r]` 是已生成的顺次数；`l` 是待扩展的下标'
    return f'`now = {S["now"]}`：末位 `{S["now"] % 10}`，末位再加 1 接到后面得到下一个顺次数'


def _col(S, i, v):
    ln = S.get('_line')
    if 'now' in S and 'l' in S and i == S['l'] - 1 and ln in (8, 9, 10, 11, 12, 13, 14, 15, 16):
        return 'blue'
    if ln == 22 and 'l' in S and 'r' in S and S['l'] <= i < S['r']:
        return 'green'
    return None


CONFIG = dict(
    num=1291, title='顺次数', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='按位生成 + 队列扩展',
    code='''
class Solution(object):
    def sequentialDigits(self, low, high):
        
        q = list(range(1, 9))
        l = 0
        r = len(q)
        while l < r:
            now = q[l]
            l += 1
            last = now % 10
            if last != 9:
                next = now * 10 + last + 1
                if next > high:
                    break
                q.append(next)
                r += 1
        
        l = 0
        while l < r and q[l] < low:
            l += 1

        return q[l : r]
''',
    call='Solution().sequentialDigits(12, 100)',
    expect=[12, 23, 34, 45, 56, 67, 78, 89],
    views=[
        dict(type='text', fn=_text, h=80),
        dict(type='array', var='q', pointers={'l': 'blue', 'r - 1': 'pink'}, color=_col, dim=lambda S, i, v: S.get('_line') in (19, 22) and i < S['l'], cell=70, label='q（队列：按长度从小到大生成）', h=330),
    ],
    watch=['l', 'r', 'now', 'last', 'next', 'high'],
    max_steps=90,
    skip=['l += 1', 'last = now % 10', 'r += 1'],
    captions={
        4: '先放入所有 1 位数 `1..8`（9 不能再往后接）',
        5: '`l` 指向队首，从最小的数开始扩展',
        6: '`r = {r}`：`q[l:r]` 是目前生成好、不超过 `high` 的数',
        7: lambda S, B, r: (f'`l = {S.l}` < `r = {S.r}`：队里还有数没扩展' if S.l < S.r else f'`l = {S.l}` ≥ `r = {S.r}`：全部扩展完'),
        8: lambda S, B, r: f'取出队首 `now = q[{S.l}] = {S.now}`，`l` 随即后移，末位是 `{S.now % 10}`',
        11: lambda S, B, r: f'末位是 `{S.last}`：' + ('还能接 `' + str(S.last + 1) + '`' if S.last != 9 else '已经是 9，没法再接'),
        12: '在 `{now}` 后接 `{last}+1`：`next = {next}`',
        13: lambda S, B, r: f'`next = {S.next}` ' + (f'> `high = {S.high}` → 后面生成的只会更大，停止' if S.next > S.high else f'≤ `high = {S.high}` → 合法，继续'),
        14: '`break`：后面的数都比 `high` 大，不用再生成',
        15: '`{next}` 入队：`q` 里共 `{len(q)}` 个数，`r` 随之 +1',
        18: '`l` 归零：从最小的数开始，跳过比 `low` 小的',
        19: lambda S, B, r: ((f'`q[{S.l}] = {S.q[S.l]}` < `low = {S.low}` → 太小，`l` 右移到 {S.l + 1}' if S.q[S.l] < S.low else f'`q[{S.l}] = {S.q[S.l]}` ≥ `low = {S.low}` → 起点找到') if S.l < S.r else '`l` 走到头了'),
        22: '答案是 `q[{l}:{r}]` = `{ret}`',
    },
    cards=dict(
        one_liner='合法顺次数只有 36 个，按顺序生成再截取',
        complexity='时间 `O(log² high)`，空间 `O(log² high)`',
        problem=['顺次数：每一位都比前一位大 `1` 的整数',
                 '返回 `[low, high]` 内所有顺次数，从小到大',
                 '示例：`low=100, high=300` → `[123,234]`；本视频用 `[12,100]` → `[12,23,…,89]`'],
        quote='实际上，最多也就只有8 + 7 + ... + 1一共是36个可能的解，于是我们可以先将这些数按顺序生成出来，然后根据给出的low和high找出合法的最小解和最大解即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['两位数 12、23、…、89；三位数就是把两位数末位复制再加 1：12→123',
              '用队列 `q` 按长度从小到大生成：取队首，末位不是 9 就在后面接 `末位+1`',
              '生成超过 `high` 就停；再从左边跳过小于 `low` 的，剩下 `q[l:r]` 就是答案'],
        summary=['时间 `O(log² high)`，最多 36 个数',
                 '队列天然有序：短的在前，同长度里高位小的在前',
                 '`last != 9` 才能继续接数；`next > high` 可直接 `break`',
                 '原文为 Python 2 写法，`q = range(1, 9)` 已改为 `q = list(range(1, 9))`（Python 3 的 range 不能 append）',
                 '对比灵神：灵神把答案看成 `123456789` 的子串，用滑动窗口 O(1) 算下一个'],
    ),
)

def _text(S):
    if 'char' not in S:
        return '扫一遍：`flag` 记「是否见过 0」，`cnt` 统计第一个 0 之后的 1'
    if 'n' in S:
        n, cnt, flag = S['n'], S['cnt'], S['flag']
        if cnt == 0:
            return '`cnt = 0`：' + ('有 0 但后面没有 1 → `1...10`' if flag else '没有 0 → 原样返回')
        return f'`cnt = {cnt}`：前缀 `{n - cnt - 1}` 个 1，一个 0，后缀 `{cnt}` 个 1'
    return f'`char = {S["char"]!r}`，`flag = {S["flag"]}`，`cnt = {S["cnt"]}`'


def _col(S, i, v):
    if not S.get('flag'):
        return None
    b = S['binary']
    z = b.find('0')
    if i == z:
        return 'yellow'
    if v == '1' and i > z and b[z + 1:i + 1].count('1') <= S['cnt']:
        return 'green'
    return None


CONFIG = dict(
    num=1702, title='修改后的最大二进制字符串', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='一趟扫描 · 数第一个 0 之后的 1',
    tags=['灵神题单', '难度分 1825'],
    code='''
class Solution(object):
    def maximumBinaryString(self, binary):

        cnt = 0
        flag = False
        for char in binary:
            if char == '0':
                flag = True
            elif flag:
                cnt += 1
        
        n = len(binary)

        if cnt == 0:
            if flag:
                return '1' * (n - 1) + '0'
            else:
                return binary
        else:
            return '1' * (n - cnt - 1) + '0' + '1' * cnt
''',
    call="Solution().maximumBinaryString('101010')",
    expect='111011',
    views=[
        dict(type='text', fn=_text, h=80),
        dict(type='string', var='binary', h=240, color=_col),
    ],
    watch=[('char', 'char', 'blue'), ('flag', 'flag', 'yellow'), ('cnt', 'cnt', 'green'), 'n'],
    captions={
        'cnt = 0': '`cnt` 统计「第一个 0 之后」出现的 1 的个数',
        'flag = False': '`flag` 表示是否已经见过 0',
        'for char in binary': '看下一个字符 `{char}`',
        "if char == '0'": lambda S, B, r: (f'`char = {S.char!r}`：是 0 → 见到 0 了' if S.char == '0' else f'`char = {S.char!r}`：不是 0'),
        'flag = True': lambda S, B, r: ('`flag = True`：第一个 0 出现，从这里开始后面的 1 才要计数' if not B.flag else '又是 0：`flag` 早已是 True，只有后面的 1 才会让 `cnt` 增加'),
        'elif flag': lambda S, B, r: (f'`flag = {S.flag}`：已见过 0，这个 1 要数' if S.flag else '`flag = False`：还没遇到 0，前面的 1 是高位前缀，不用数'),
        'cnt += 1': '第一个 0 之后又一个 1：`cnt` → {cnt}',
        'n = len': '`n = {n}`',
        'if cnt == 0': lambda S, B, r: ('`cnt = 0`：0 后面没有 1（或没有 0），情况 1、2' if S.cnt == 0 else f'`cnt = {S.cnt} > 0`：第一个 0 之后还有 1 → 情况 3'),
        'if flag': '`flag = {flag}`',
        "return '1' * (n - 1) + '0'": '后面全是 0：两两用 `00 → 10`，最后得到 `1...10`',
        'return binary': '全是 1，原样返回',
        "return '1' * (n - cnt - 1)": '`{n - cnt - 1}` 个 1 + 一个 0 + `{cnt}` 个 1 → `{ret}`',
    },
    cards=dict(
        one_liner='把第一个 0 后面的 1 全部挤到末尾，剩一个 0',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['操作 1：`00 → 10`；操作 2：`10 → 01`，任意次',
                 '求能得到的最大二进制串',
                 '示例：`000110` → `111011`；本视频：`101010` → `111011`'],
        quote='对于011...10这种形式的字符串，需要从低位开始两位两位执行10 -> 01的操作，最后将会得到0011...111。可以发现，实际上就相当于是将连续1后面的那个0移动到了高位。',
        quote_src='—— yiduobo 题解原文',
        idea=['先看特例：全 1 原样；`11..100..0` 用 `00 → 10` 变成 `1..10`',
              '一般情形：用 `10 → 01` 把后面的 0 一路移到第一个 0 旁边，再 `00 → 10`',
              '结果是 `n-cnt-1` 个 1、一个 0、`cnt` 个 1，`cnt` 为第一个 0 后 1 的个数'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`flag` 控制只数第一个 0 之后的 1',
                 '`cnt = 0` 要分「没有 0」和「有 0 但后面全是 0」两种',
                 '原文无 Python 2 专有写法，未做修改'],
    ),
)

def _text(S):
    b = S['binary']
    n = len(b)
    if 'cnt1' in S and 'i' in S and S['i'] >= 0:
        c = S['cnt1']
        res = '1' * (n - 1 - c) + '0' + '1' * c
        if S.get('_line') == 7:
            return f'结果 = `{n - 1 - c}` 个 1 + 一个 0 + `{c}` 个 1 = ==​{res}=='
        return f'`binary[{S["i"]}:]` 里有 ==​{c}== 个 1，它们会被「挤」到末尾'
    if 'i' in S and S['i'] >= 0:
        return f'第一个 `0` 在下标 =={S["i"]}==：它前面的 1 已经是最优，不用动'
    if 'i' in S:
        return '没有 0：全是 1，已经最大'
    return '答案里至多只有一个 0，位置由「后面有多少个 1」决定'


def _col(S, i, v):
    if 'i' not in S or S['i'] < 0:
        return None
    if i == S['i']:
        return 'yellow'
    if i > S['i'] and v == '1':
        return 'green'
    return None


CONFIG = dict(
    num=1702, title='修改后的最大二进制字符串', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='分类证明 · 只剩一个 0',
    tags=['灵神题单', '难度分 1825'],
    code='''
class Solution:
    def maximumBinaryString(self, binary: str) -> str:
        i = binary.find('0')
        if i < 0:  # binary 全是 '1'
            return binary
        cnt1 = binary.count('1', i)  # 统计 binary[i:] 中 '1' 的个数
        return '1' * (len(binary) - 1 - cnt1) + '0' + '1' * cnt1
''',
    call="Solution().maximumBinaryString('101010')",
    expect='111011',
    views=[
        dict(type='text', fn=_text, h=80),
        dict(type='string', var='binary', color=_col, h=240),
    ],
    watch=[('i', 'i', 'yellow'), ('cnt1', 'cnt1', 'green'), ('n', 'len(binary)')],
    captions={
        'i = binary.find': lambda S, B, r: (f'`find(\'0\')` 找最高位的第一个 0：下标 `{S.i}`；它前面全是 1，不用动' if S.i >= 0
                                             else '`find` 返回 -1：没有 0'),
        'if i < 0': lambda S, B, r: ('`i = -1`：全是 1，已经最大' if S.i < 0 else f'`i = {S.i} ≥ 0`：有 0，继续'),
        'return binary': '没有 0，直接返回原串',
        'cnt1 = ': '`binary[{i}:]` 里的 1 有 `{cnt1}` 个：0 每左移一步就把一个 1 挤到末尾',
        'return \'1\'': '`{len(binary) - 1 - cnt1}` 个 1 + 唯一的 0 + `{cnt1}` 个 1 → `{ret}`',
    },
    cards=dict(
        after=[dict(heading='0 是怎么左移的', lines=[
            '`101010 → 100110`：操作 2，把右边的 0 往左挪一格',
            '`100110 → 110110`：出现 `00`，操作 1 把高位的 0 变成 1',
            '重复下去：`110110 → 110011 → 111011`',
            '1 被挤到末尾，最后只剩一个 0'])],
        one_liner='答案至多一个 0：其余 0 都能被操作 1、2 变成 1',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['操作 1：`00 → 10`；操作 2：`10 → 01`，可做任意次',
                 '返回能得到的最大二进制串',
                 '示例：`000110` → `111011`；本视频：`101010` → `111011`'],
        quote='答案至多包含一个 0。反证法：有多个 0，总是可以通过操作 2 让最高位的 0 的右侧也是 0，然后通过操作 1 让最高位的 0 变成 1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['有 `00` 就能换成 `10`，所以答案没有 `00`，进一步至多一个 0',
              '全是 1 → 原样返回；否则恰好剩一个 0',
              '0 左移时把 `[i, n-1]` 里的 1 挤到末尾：`n-1-cnt1` 个 1、一个 0、`cnt1` 个 1'],
        summary=['时间 `O(n)`，空间 `O(n)`（拼接新串）',
                 '`cnt1` 只统计第一个 0 之后的 1；它前面的 1 属于前缀',
                 '易错：别忘了全是 1 的特判（`find` 返回 -1）',
                 '末尾那个 0 不会右移，因此无法把所有 0 都变成 1'],
    ),
)

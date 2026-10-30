_P = 'sum(cnt.values()) - (_line == 12) if _line != 14 else None'


def _letters(m):
    return ''.join(chr(97 + i) for i in range(26) if m >> i & 1) or '空'


def _txt(S):
    if 'state' not in S or S.get('_line') in (6, 14):
        return '每个字符串 → 一个 ==26 位二进制==：字符存在则该位为 1'
    m = S['state']
    bits = format(m, '04b')
    return f"`state = {m}`，低位 `…{bits}`（右起 a,b,c,d），含字母 =={_letters(m)}=="


CONFIG = dict(
    num=2506, title='统计相似字符串对的数目', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='26 位二进制状态 · 哈希计数',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def similarPairs(self, words):

        cnt = {}
        res = 0
        for w in words:
            state = 0
            for char in w:
                state |= (1 << (ord(char) - 97))

            res += cnt.get(state, 0)
            cnt[state] = cnt.get(state, 0) + 1

        return res
''',
    call='Solution().similarPairs(["aabb","ab","ba","ca","ac"])',
    expect=4,
    views=[
        dict(type='array', var='words', label='words（w = 当前字符串）', pointers={_P: 'blue'}, pointer_labels={_P: 'w'}, h=210,
             cell=110, dim=lambda S, i, v: 'cnt' in S and S.get('_line') != 14 and i > sum(S['cnt'].values()) - (S.get('_line') == 12)),
        dict(type='text', fn=_txt, h=100, size=30),
        dict(type='map', var='cnt', label='cnt：state（整数）→ 之前出现的次数', fmt=lambda k, v: f'{k}({_letters(k)}): {v}', h=170, font=34),
    ],
    watch=[('w', 'w', 'blue'), 'char', ('state', 'state', 'orange'), ('res', 'res', 'green')],
    skip=['for char in w'],
    captions={
        'cnt = {}': '`cnt`：每个整数（字符串状态）之前出现的次数',
        'res = 0': '`res` 统计相似对',
        'for w in words': lambda S, B, r: (f'处理字符串 `w = {S.w!r}`' if sum(S.cnt.values()) < len(S.words) else '遍历结束'),
        'state = 0': '`state = 0`：还没有任何字符',
        'state |= (1 <<': lambda S, B, r: (f"`{S.char!r}` 是第 `ord({S.char!r}) − 97 = {ord(S.char) - 97}` 位 → `state = {S.state}`" if S.state != B.state
                                           else f"`{S.char!r}` 对应的位已经是 1，`state` 仍为 `{S.state}`"),
        'res += cnt.get': lambda S, B, r: (f'状态 `{S.state}` 之前出现过 `{S.cnt.get(S.state, 0)}` 次 → 能配 `{S.cnt.get(S.state, 0)}` 对，`res = {S.res}`'
                                           if S.cnt.get(S.state, 0) else f'状态 `{S.state}` 之前没出现过，`res` 不变'),
        'cnt[state] = ': '再更新当前整数出现的次数：`cnt[{state}] = {cnt[state]}`',
        'return res': '一共 `{res}` 对',
    },
    cards=dict(
        one_liner='字符串 → 26 位二进制整数，相似就是整数相等',
        complexity='时间 `O(L)`，空间 `O(n)`，`L` 为总长度',
        problem=['两个字符串由相同的字符组成就算==相似==（不管次数与顺序）',
                 '求满足 `i < j` 且相似的下标对数目',
                 '本视频：`["aabb","ab","ba","ca","ac"]` → `4`'],
        quote='对于每个字符串，都可以使用一个26位的二进制来表示，其中每一位都对应字符串中的某个字符，若某个字符存在，其对应的位置就是1，否则就为0。',
        quote_src='—— yiduobo 题解原文',
        idea=['这样一来，就==将字符串都转化成了一个整数==',
              '先用哈希表查当前整数之前出现的次数，累加到答案',
              '再把当前整数的出现次数加 1'],
        summary=['时间 `O(L)`，空间 `O(n)`',
                 '`ord(char) - 97` 即字母序号，`97` 是 `\'a\'` 的 ASCII 码',
                 '`cnt.get(state, 0)`：没出现过的状态当作 0 次',
                 '原文代码在 Python 3 下可直接运行，未做修改'],
    ),
)

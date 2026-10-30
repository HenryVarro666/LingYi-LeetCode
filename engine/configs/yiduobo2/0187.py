S0 = 'CGTACGTACGTACG'
VAL = {'A': 0, 'C': 1, 'G': 2, 'T': 3}


def _code(t):
    v = 0
    for c in t:
        v = v * 4 + VAL[c]
    return v


def _decode(x):
    return ''.join('ACGT'[x // 4 ** k % 4] for k in range(9, -1, -1))


def _b4(x):
    return ''.join(str(x // 4 ** k % 4) for k in range(9, -1, -1))


def _k(S):
    """第一个循环里：已经编码进 now 的字符个数（S0 以 C 开头，前缀编码互不相同）"""
    if 'now' not in S or 'index' in S:
        return None
    for k in range(11):
        if _code(S['s'][:k]) == S['now']:
            return k
    return None


def _ptr(S):
    """当前要加入的字符下标"""
    if 'index' in S:
        return S['index'] + 10
    if 'char' in S and 'now' in S:
        k = _k(S)
        if k is None:
            return None
        return k - 1 if S.get('_line') == 9 else (k if k < 10 else None)
    return None


def _win(S):
    if 'index' in S:
        st = S['index'] + (1 if S.get('_line') != 16 else 0)
        return st, st + 9
    k = _k(S)
    if k:
        return 0, k - 1
    return None


def _color(S, i, v):
    w = _win(S)
    if w and w[0] <= i <= w[1]:
        return 'blue'
    if 'index' in S and S.get('_line') == 17 and i == S['index']:
        return 'red'               # 刚被移出窗口的头部字符
    return None


def _dim(S, i, v):
    w = _win(S)
    p = _ptr(S)
    hi = max(w[1] if w else -1, p if p is not None else -1)
    return 'now' in S and i > hi


def _info(S):
    if 'now' not in S:
        return '编码：`A=0  C=1  G=2  T=3`，长度 10 的子串 = 一个 10 位的 4 进制数'
    return f'`now = {S["now"]}` = 4 进制 `{_b4(S["now"])}`'


def _roll(S, B, r):
    i, c = S.index, S.char
    rest = B.now % 262144
    return (f'`{B.now} % 4^9` 去掉最高位（移出 `s[{i}] = {S.s[i]}`）= `{rest}`，'
            f'`×4` 整体左移一位，`+{VAL[c]}` 加入 `{c}` → `now = {S.now}`（窗口 `{S.s[i + 1:i + 11]}`）')


def _hit(S, B, r):
    w = S.s[S.index + 1:S.index + 11]
    if S.now in S.check_set:
        return f'`{S.now}` ==已在 set 中== → 子串 `{w}` 重复出现了！'
    return f'`{S.now}` 不在 set 中 → `{w}` 第一次出现'


CONFIG = dict(
    num=187, title='重复的DNA序列', difficulty='Medium', category='哈希',
    author='yiduobo', technique='4 进制编码 · 滚动哈希（RK）',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def findRepeatedDnaSequences(self, s):
        if len(s) <= 10:
            return []

        val_dict = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
        now = 0
        for char in s[:10]:
            now = now * 4 + val_dict[char]

        check_set = set()
        check_set.add(now)

        res_dict = {}

        for index, char in enumerate(s[10:]):
            now = now % 262144 * 4 + val_dict[char]
            if now in check_set:
                res_dict[now] = s[index + 1 : index + 11]
            else:
                check_set.add(now)

        return list(res_dict.values())
''',
    call=f'Solution().findRepeatedDnaSequences({S0!r})',
    expect=['CGTACGTACG'],
    result_fn=lambda v: sorted(v),
    views=[
        dict(type='text', fn=_info, size=30, h=80),
        dict(type='string', var='s', label='s（蓝 = 当前编码的 10 个字符，红 = 刚移出）', cell=64, h=230,
             pointers={_ptr: 'yellow'}, pointer_labels={_ptr: 'char'}, color=_color, dim=_dim),
        dict(type='set', var='check_set', label='check_set（出现过的编码值）', fmt=lambda x: f'{x}', h=150),
        dict(type='map', var='res_dict', label='res_dict（编码值 → 重复子串）', fmt=lambda k, v: f'{k}: {v}', h=130),
    ],
    watch=['char', ('index', 'index', 'cyan'), ('now', 'now', 'yellow')],
    captions={
        'if len(s) <= 10': '长度 `{len(s)}`：不超过 10 就不可能有重复的长 10 子串',
        'val_dict = ': '`A=0, C=1, G=2, T=3`：只有四种字符 → ==用 4 进制编码==代替字符串哈希',
        'now = 0': '`now`：当前 10 个字符的 4 进制编码',
        'for char in s[:10]': lambda S, B, r: ('前十个字符编码完毕' if _k(S) == 10 else f'先编码前十个字符：取 `{S.char}`'),
        'now = now * 4': '`now = {B.now} × 4 + {val_dict[char]}` = `{now}`（4 进制末尾添一位 `{val_dict[char]}`）',
        'check_set = set()': '`check_set` 记录出现过的编码值',
        'check_set.add(now)': lambda S, B, r: (f'第一个窗口 `{S.s[:10]}` 的编码 `{S.now}` 放进 set' if 'index' not in S
                                               else f'记下 `{S.now}`'),
        'res_dict = {}': '`res_dict`：编码值 → 重复子串（用 dict 去重，同一子串只记一次）',
        'for index, char in enumerate': lambda S, B, r: ('所有字符都滑过了，遍历结束' if 'index' in B and B.index == S.index
                                                         else f'第 `{S.index + 11}` 个字符 `{S.char}` 加入窗口'),
        'now = now % 262144': _roll,
        'if now in check_set': _hit,
        'res_dict[now] = ': '加入答案：`res_dict[{now}] = {res_dict[now]!r}`',
        'return list(res_dict.values())': '返回所有重复的子串：`{list(res_dict.values())}`',
    },
    cards=dict(
        one_liner='把长 10 的 DNA 子串编码成 4 进制数，滑动时 O(1) 更新',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['DNA 串 `s` 只含 `A C G T`，找出所有==出现不止一次==的长度为 10 的子串',
                 '示例：`"AAAAAAAAAAAAA"` → `["AAAAAAAAAA"]`',
                 f'本视频：`"{S0}"` → `["CGTACGTACG"]`'],
        quote='从第十一个字符开始，每次加入一个字符，同时将头部的字符移除。这个过程相当于将之前的编码模上4的9次方，然后往左移一位，即乘上4，最后加上新加入字符的编码值。',
        quote_src='—— yiduobo 题解原文',
        idea=['`A=0 C=1 G=2 T=3`，`s[0:10]` 编码为 `s[0]·4^9 + … + s[9]·4^0`',
              '滑一格：`% 4^9` 去掉 `s[0]` 那一项，`×4` 让其余各项升一位，`+ s[10]`',
              '编码值进 set 判重；这就是字符串匹配里的 ==RK 算法=='],
        summary=['时间 `O(n)`，空间 `O(n)`；4^10 ≈ 10^6，编码不会溢出也不会冲突',
                 '`262144 = 4^9`：先取模去掉最高位，==再==乘 4，顺序不能反',
                 '新字符是 `s[index + 10]`，所以当前窗口是 `s[index + 1 : index + 11]`',
                 '原文为 Python 2 写法：删去类型说明文档字符串，`return res_dict.values()` 改为 `list(...)`（Py3 中 values() 不是列表）',
                 '若字符集是 26 个字母，编码太大，需取模哈希（RK 字符串匹配）'],
    ),
)

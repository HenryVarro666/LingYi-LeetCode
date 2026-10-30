_src = lambda S: S['f'][S['index'] - 2] if 'index' in S and 'f' in S and S['index'] >= 2 else None


def _formula(S):
    if 'index' not in S or 's' not in S or S['_line'] not in (8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18):
        return ''
    s = S['s']
    return f"里层 `'{s}'` 的头尾套数对：`0{s}0`  `1{s}1`  `6{s}9`  `8{s}8`  `9{s}6`"


CONFIG = dict(
    num=247, title='中心对称数 II', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='按长度递推构造（头尾加数对）',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def findStrobogrammatic(self, n):

        f = []
        f.append([''])
        f.append(['0', '1', '8'])

        for index in range(2, n + 1):
            f.append([])
            for s in f[index - 2]:
                f[-1].append('0' + s + '0')
                f[-1].append('1' + s + '1')
                f[-1].append('6' + s + '9')
                f[-1].append('8' + s + '8')
                f[-1].append('9' + s + '6')
        
        res = []
        for s in f[n]:
            if n == 1 or s[0] != '0':
                res.append(s)

        return res
''',
    call='Solution().findStrobogrammatic(3)',
    expect=['101', '609', '808', '906', '111', '619', '818', '916', '181', '689', '888', '986'],
    skip=['f.append([])', "f[-1].append('1'", "f[-1].append('6'", "f[-1].append('8'", "f[-1].append('9'"],
    max_steps=80,
    views=[
        dict(type='text', fn=_formula, size=28, h=70),
        dict(type='array', var=_src, label='里层 f[index-2]（黄 = 当前的 s，它去头去尾前的样子）', cell=96, h=150,
             color=lambda S, i, v: 'yellow' if v == S.get('s') and S['_line'] in (9, 10, 11, 12, 13, 14) else None),
        dict(type='queue', var=lambda S: S['f'][-1] if 'f' in S else None, label='f[-1]（最新一层，绿 = 刚加入）', font=19, h=120),
        dict(type='queue', var='res', label='res（去掉前导 0 的结果）', font=19, h=120),
    ],
    watch=[('index', 'index', 'blue'), ('s', 's', 'yellow'), ('len(f[-1])', lambda S: len(S['f'][-1]) if 'f' in S else None, 'green'), ('len(res)', lambda S: len(S['res']) if 'res' in S else None)],
    captions={
        'f = []': '`f[len]` 保存==所有长度为 len 的中心对称数==',
        "f.append([''])": '长度 0：只有空串（它是长度 2 的“里层”）',
        "f.append(['0', '1', '8'])": '长度 1：只有 `0`、`1`、`8` 自己旋转后不变',
        'for index in range(2, n + 1)': lambda S, B, r: ('长度 `2..n` 都构造完了' if S.index == B.get('index') else f'开始构造长度 `{S.index}` 的：去头去尾后必是长度 `{S.index - 2}` 的中心对称数'),
        'for s in f[index - 2]': lambda S, B, r: ('长度 `{}` 的里层都用完了，这一层构造完毕'.format(S.index - 2) if 's' in B and B.s == S.s and B.get('index') == S.index else f'取一个长度 `{S.index - 2}` 的里层 `s = {S.s!r}`，准备在头尾加数对'),
        "f[-1].append('0' + s + '0')": '头尾加 `0…0`、`1…1`、`6…9`、`8…8`、`9…6` 五种数对：旋转后头尾互相对应。先加 `0{s}0`，后四种同理',
        'res = []': '直接构造会带前导 0（如 `0 … 0`），要在最后去掉',
        'for s in f[n]': lambda S, B, r: ('长度 `n` 的候选都检查完了' if 's' in B and B.s == S.s and len(S.res) == len(B.res) and S.res and B.s == S.res[-1] else f'检查候选 `{S.s}`'),
        'if n == 1 or s[0]': lambda S, B, r: (f'`{S.s}` 首位是 `0` 且 `n > 1` → ==前导 0，丢弃=='
                                                if not (S.n == 1 or S.s[0] != '0') else f'`{S.s}` 没有前导 0 → 保留'),
        'res.append(s)': '`{s}` 加入答案',
        'return res': '共 `{len(res)}` 个长度为 `{n}` 的中心对称数',
    },
    cards=dict(
        one_liner='像造回文数一样：往里层的头尾套数对',
        complexity='时间 `O(5^(n/2))`，空间同阶',
        problem=['中心对称数：旋转 180° 后和原来一样（`0 1 8` 不变，`6 ↔ 9`）',
                 '返回所有长度为 `n` 的中心对称数，顺序不限，不能有前导 0',
                 '本视频：`n = 3` → `101, 111, 181, 609, ...` 共 12 个'],
        quote='对于长度大于等于2的中心对称数，不妨设其长度为len，那么其去头去尾的部分就必然是一个长度为len - 2的中心对称数。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[len]` 由 `f[len-2]` 的每个数在头尾加 5 种数对得到',
              '长度 0 是空串，长度 1 是 `0 1 8`，作为递推起点',
              '这样会产生前导 0 的数，最后过滤掉（`n = 1` 的 `0` 保留）'],
        summary=['时间/空间都是 `O(5^(n/2))`，即答案规模',
                 '易错：数对里的 `0…0` 只能用在里层，最外层不能有前导 0',
                 '易错：`n == 1` 时 `0` 是合法答案，要单独放行',
                 '原文为 Python 2 风格，代码未改'],
    ),
)

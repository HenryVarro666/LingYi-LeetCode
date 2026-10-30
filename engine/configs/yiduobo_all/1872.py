A = [5, 9, 1, -4, -5, -4, -2]

def _idx(S):
    """下标 i：当前正在算 f(i)（p = s[i]）"""
    if 'f' not in S or 'p' not in S:
        return None
    n = len(S['stones'])
    if len(S['f']) >= n:
        return None if S.get('_line') == 9 else n - len(S['f'])
    return n - len(S['f']) - 1 if S.get('_line') == 9 else n - len(S['f'])


_P_BUILD = lambda S: (len(S['s']) - 1) if 'f' not in S and 's' in S else None
_P_SCAN = _idx


def _formula(S):
    if 'f' not in S:
        if 's' in S:
            return '先算前缀和 `s`：`s[k]` = 前 `k+1` 个石子的和（= 拿到 k 为止的得分）'
        return '玩家每次拿走一段前缀，得分 = 前缀和'
    i = _idx(S)
    if i is None or 'p' not in S:
        if 'p' in S:
            return f'`f` 全部算完：`f[-2]` 就是 `f(1)` = {S["f"][-2]}'
        return f'`f(n-1) = s[n-1] = {S["f"][0]}`：只剩最后一步，一次全拿光'
    n = len(S['stones'])
    fv = S['f'][-2] if S.get('_line') != 9 else S['f'][-1]
    return f'`i = {i}`：拿到 i → `s[i] − f(i+1)` = `{S["p"]} − {fv}` = {S["p"] - fv}；不拿 → `{fv}`'


def _scolor(S, k, v):
    i = _idx(S)
    return 'yellow' if i is not None and k == i else None


CONFIG = dict(
    num=1872, title='石子游戏 VIII', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='前缀和 + 倒推 f[i]',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 2440'],
    code='''
class Solution(object):
    def stoneGameVIII(self, stones):

        s = [stones[0]]
        for stone in stones[1:]:
            s.append(s[-1] + stone)

        f = [s[-1]]
        for p in s[-2::-1]:
            f.append(f[-1])
            f[-1] = max(f[-1], p - f[-1])
        
        return f[-2]
''',
    call=f'Solution().stoneGameVIII({A!r})',
    expect=8,
    views=[
        dict(type='text', fn=_formula, size=24, h=70),
        dict(type='array', var='stones', label='stones', h=170, cell=90),
        dict(type='array', var='s', label='s：前缀和（黄 = 当前的 p）', h=190, cell=90,
             pointers={_P_BUILD: 'blue', _P_SCAN: 'yellow'}, pointer_labels={_P_BUILD: 'new', _P_SCAN: 'p'},
             color=_scolor),
        dict(type='array', var='f', label='f：先扫到的在前（f[0] 对应最后一个位置，f[-1] 是当前）', h=190, cell=90,
             pointers={'len(f) - 1': 'green'}, pointer_labels={'len(f) - 1': 'f[-1]'},
             color=lambda S, k, v: 'green' if k == len(S['f']) - 1 else None),
    ],
    watch=[('p', 'p', 'yellow'), ('f[-1]', 'f[-1]', 'green')],
    captions={
        's = [stones[0]]': '`s[0] = {s[0]}`：前缀和从第一个石子开始累加',
        'for stone in stones[1:]': lambda S, B, r: (f'取下一个石子 `stone = {S.stone}`' if S.get('stone') != B.get('stone') or S.get('stone') is None else '前缀和 `s` 算完：' + str(S.get('s'))),
        's.append(s[-1] + stone)': '`s` 末尾加入 `{s[-2]} + {stone}` = =={s[-1]}==',
        'f = [s[-1]]': '边界：先手一次拿光所有石子，`f[n-1] = s[n-1] = {f[0]}`',
        'for p in s[-2::-1]': lambda S, B, r: (f'`p = s[{_idx(S)}] = {S.p}`：从后往前，现在算 `f({_idx(S)})`' if _idx(S) is not None else '`s` 扫完了，`f` 全部算好'),
        'f.append(f[-1])': lambda S, B, r: f'先假设==不拿到 i==：直接继承后面的 `f({_idx(S)+1}) = {S.f[-1]}`',
        'f[-1] = max': '再考虑==拿到 i==：得分 `p = {p}`，后手还能多拿 `{f[-2]}` → `{p} − {f[-2]}` = {p - f[-2]}；取大 `f[-1] = {f[-1]}`',
        'return f[-2]': '`f[-1]` 对应 `f[0]`（不合法，不能只拿一个），答案是倒数第二个 `f[-2]` = =={ret}==',
    },
    cards=dict(
        one_liner='先手要么拿到 i（得 s[i]，再减后手的最优），要么把机会留给 i+1',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每回合拿走最左边至少 2 个石子，得分加上它们的和，再放回一个值为这个和的新石子',
                 '只剩一个石子时结束；Alice 想最大化分差，Bob 想最小化',
                 '本视频：`[5,9,1,-4,-5,-4,-2]` → `8`'],
        quote='玩家每次都是拿走了石子的某个前缀……令f[i]表示当前必须从第i个石子开始拿时先手与后手的最大分差……f[i] = max(f[i + 1], s[i] - f[i + 1])',
        quote_src='—— yiduobo 题解原文',
        idea=['每次拿的都是前缀，所以先求前缀和 `s`',
              '`f[i]`：必须从第 i 个开始拿时，先手比后手多多少',
              '拿到 i：得 `s[i]`，后手之后多得 `f[i+1]` → `s[i] − f[i+1]`；不拿到 i：等于 `f[i+1]`',
              '边界 `f[n-1] = s[n-1]`：一次拿光'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '答案是 `f[1]` 而不是 `f[0]`：先手不能只拿最前面一个石子',
                 '代码把 f 倒着存：`f[-2]` 就是 `f[1]`，`f[-1]` 是多算的 `f[0]`',
                 '对比灵神：灵神把 f 压缩成一个变量，yiduobo 保留整个数组'],
    ),
)

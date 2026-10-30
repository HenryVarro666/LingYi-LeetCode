STATE = '++++-++'


def _text(S):
    if 'res' not in S:
        return '把连续的 `+` 分成若干段：每段是一个独立的小游戏，SG 值异或起来看胜负'
    cnt, res = S.get('cnt', 0), S['res']
    x = S.get('_inner', {}).get('x')
    if x is not None:
        return f'正在算长度 `{x}` 的一段的 SG 值：翻转一对 `++` 后分成长度 `y` 和 `{x}-2-y` 两段'
    return f'当前连续 `+` 长度 `cnt = {cnt}`；已完成各段 SG 值的异或 `res = {res}`'


def _calls_hide():
    return ()


CONFIG = dict(
    num=294, title='翻转游戏 II', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='SG 函数 · 分段异或',
    tags=['灵神题单·动态规划', '灵神题单·数学算法'],
    code='''
class Solution(object):
    def canWin(self, currentState):

        f = {0: 0, 1: 0}

        def calc(x):
            if x in f:
                return f[x]
            
            mex = set()
            for y in range(x - 1):
                mex.add(calc(y) ^ (calc(x - 2 - y)))
            
            f[x] = 0
            while f[x] in mex:
                f[x] += 1
            return f[x]

        cnt = 0
        res = 0
        for char in currentState:
            if char == '+':
                cnt += 1
            else:
                if cnt > 0:
                    res ^= calc(cnt)
                cnt = 0
        
        if cnt > 0:
            res ^= calc(cnt)

        return res != 0
''',
    call=f'Solution().canWin({STATE!r})',
    expect=True,
    max_steps=110,
    views=[
        dict(type='text', fn=_text, size=24, h=70),
        dict(type='string', var='currentState', label='currentState（连续的 + 才能翻转）', h=150, cell=70,
             color=lambda S, i, v: 'green' if v == '+' else None),
        dict(type='map', var='f', label='f[长度] = 这一段的 SG 值', h=190, fmt=lambda k, v: f'{k} → {v}'),
        dict(type='set', var='mex', label='mex：所有后继状态的 SG 值（最小没出现的自然数 = f[x]）', h=160, fmt=lambda x: str(x)),
        dict(type='calls', h=200),
    ],
    watch=[('char', 'char', 'yellow'), ('cnt', 'cnt', 'blue'), ('res', 'res', 'green'), ('x', "_inner.get('x')", 'pink')],
    captions={
        'f = {0: 0, 1: 0}': '`f[x]` 是长度 `x` 的一段 `+` 的 SG 值。长度 0、1 一步都走不了，必败态 → SG 为 `0`',
        'if x in f': lambda S, B, r: (f'`calc({S.x})`：已经算过，直接用 `f[{S.x}] = {S.f[S.x]}`' if S.x in S.f else f'`calc({S.x})`：第一次遇到，要自己算'),
        'return f[x]': lambda S, B, r: f'长度 `{B.x}` 的 SG 值就是 =={r}==',
        'mex = set()': '准备收集 `x = {x}` 所有后继状态的 SG 值',
        'for y in range(x - 1)': lambda S, B, r: (f'翻转第 `{S._inner["y"]}`、`{S._inner["y"] + 1}` 位的 `++`，这一段被分成长度 `{S._inner["y"]}` 和 `{S._inner["x"] - 2 - S._inner["y"]}` 的两段' if S._inner.get('y') is not None and S._inner.get('y') != B._inner.get('y') else f'所有翻法都试完了，`mex = {sorted(S._inner["mex"])}`'),
        'mex.add(': lambda S, B, r: f'后继状态 = 左右两段：SG 值 `calc({B._inner["y"]}) ^ calc({B._inner["x"] - 2 - B._inner["y"]})`（异或）加入 `mex`',
        'f[x] = 0': '从 `0` 开始，找 `mex` 中没出现的最小自然数',
        'while f[x] in mex': lambda S, B, r: (f'`{S.f[S.x]}` 在 `mex = {sorted(S.mex)}` 里 → 试下一个' if S.f[S.x] in S.mex else f'`{S.f[S.x]}` 不在 `mex` 里 → 这就是 SG 值'),
        'f[x] += 1': '`f[{x}]` 加 1，变成 `{f[x]}`',
        'for char in currentState': '逐个字符扫描，当前 `char = {char}`；扫完就退出循环',
        "if char == '+'": lambda S, B, r: ('`+`：属于当前这一段' if S.char == '+' else '`-`：当前这一段到此结束'),
        'cnt += 1': '这一段长度 `cnt` = =={cnt}==',
        'if cnt > 0': lambda S, B, r: (f'这一段长度是 `{S.cnt}`，要算它的 SG 值' if S.cnt > 0 else '连着的 `-`，没有段，跳过'),
        'res ^= calc(cnt)': '各段是互不影响的小游戏：总 SG 值 = 各段 SG 值的==异或==',
        'cnt = 0': lambda S, B, r: ('`cnt` 记录当前连续 `+` 的长度' if 'res' not in B else '重新开始统计下一段'),
        'res = 0': '`res` 累计各段 SG 值的异或',
        'return res != 0': lambda S, B, r: ('`res = %d ≠ 0`：先手必胜' % S.res if S.res != 0 else '`res = 0`：先手必败'),
    },
    cards=dict(
        one_liner='把连续的 + 拆成独立小游戏，用 SG 函数（mex）求每段，再异或',
        complexity='时间 `O(n^2)`（记忆化后每个长度只算一次），空间 `O(n)`',
        problem=['字符串由 `+` 和 `-` 组成，两人轮流把相邻的 `++` 翻成 `--`，不能操作的人输',
                 '先手能否保证获胜？返回 `true` / `false`',
                 '本视频：`"++++-++"` → `true`'],
        quote='非常典型的nim游戏问题，最常规的做法就是利用sg函数来进行求解……集合中未出现的最小自然数就是其对应的sg值。而对于多个平等的状态，最终结果则是这些状态各自的sg值取异或。',
        quote_src='—— yiduobo 题解原文',
        idea=['翻转 `++` 后，一段 `+` 会被切成左右两段，彼此独立',
              '某段的 SG 值 = 所有后继状态 SG 值集合里没出现的最小自然数（mex）',
              '后继状态由两段组成 → 两段 SG 值异或',
              '整个字符串各段 SG 异或不为 0，先手必胜'],
        summary=['时间 `O(n^2)`，空间 `O(n)`：每个长度只算一次，每次枚举 `O(n)` 种翻法',
                 '长度 0、1 的 SG 值初始化为 0（没法操作 = 必败）',
                 '最后一段 `+` 要在循环外再处理一次',
                 '同样的 nim 思路也能解决后续类似的取石子博弈'],
    ),
)

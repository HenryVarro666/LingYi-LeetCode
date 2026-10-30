_L = lambda S: S['_inner'].get('level') if 'level' in S['_inner'] and 's' in S['_inner'] else None


def _state(S):
    I = S['_inner']
    mod = S.get('mod')
    if 'level' in I and 's' in I and mod is not None:
        fl = I['flag']
        parts = []
        if 'rest' in I:
            parts.append('前导零' if fl & 4 else '已有非零数位')
        parts.append('贴 left' if fl & 2 else '不贴 left')
        parts.append('贴 right' if fl & 1 else '不贴 right')
        kind = f"乘积余数 `rest = {I['rest']}`" if 'rest' in I else ('已出现非前导 0' if fl & 8 else '尚无非前导 0')
        return f"枚举目标数位和 `mod = {mod}`：`level={I['level']}`，已填数位和 `s = {I['s']}`，{kind}，{'、'.join(parts)}"
    if mod is not None:
        return f"枚举最终的数位和 `mod = {mod}`（1 到 9n），数位和 == mod 的数里，数美丽整数"
    return '枚举最终数位和 mod；对每个 mod 数「乘积能被 mod 整除」的数'


CONFIG = dict(
    num=3490, title='统计美丽整数的数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='枚举数位和 mod + 数位 DP（有 0 / 无 0 分开算）',
    tags=['灵神题单', '动态规划', '难度分 2502'],
    code='''
class Solution(object):
    def beautifulNumbers(self, l, r):
        
        left = [int(x) for x in str(l)]
        right = [int(x) for x in str(r)]
        left = [0] * (len(right) - len(left)) + left

        n = len(right)

        def calc_with_zero(level, s, flag, f):
            if f[level][s][flag] is None:
                f[level][s][flag] = 0
                if level == n:
                    if flag & 8:
                        f[level][s][flag] = 1
                    return f[level][s][flag]
                
                start, end = 0, 9
                if flag & 2:
                    start = left[level]
                
                if flag & 1:
                    end = right[level]

                for v in range(start, end + 1):
                    nxt_s = s + v

                    if nxt_s + (n - level - 1) * 9 < mod:
                        continue

                    if nxt_s > mod:
                        break
                    
                    nxt_flag = (flag & 8)
                    if v == 0:
                        if flag & 4:
                            nxt_flag |= 4
                        else:
                            nxt_flag |= 8
                    
                    if v == left[level]:
                        nxt_flag |= (flag & 2)
                    
                    if v == right[level]:
                        nxt_flag |= (flag & 1)

                    f[level][s][flag] += calc_with_zero(level + 1, nxt_s, nxt_flag, f)
            
            return f[level][s][flag]

        def calc_without_zero(level, s, rest, flag, f):
            if f[level][s][rest][flag] is None:
                f[level][s][rest][flag] = 0
                if level == n:
                    if rest == 0 and s == mod:
                        f[level][s][rest][flag] = 1
                    return f[level][s][rest][flag]
                
                start, end = 1, 9
                if flag & 4:
                    start = 0

                if flag & 2:
                    start = max(start, left[level])
                
                if flag & 1:
                    end = right[level]

                for v in range(start, end + 1):
                    nxt_s = s + v

                    if nxt_s + (n - level - 1) * 9 < mod:
                        continue

                    if nxt_s > mod:
                        break

                    nxt_flag = 0
                    if flag & 4:
                        if v == 0:
                            nxt_flag |= 4
                            nxt_rest = 0
                        else:
                            nxt_rest = v % mod
                    else:
                        nxt_rest = rest * v % mod
                    
                    if v == left[level]:
                        nxt_flag |= (flag & 2)
                    
                    if v == right[level]:
                        nxt_flag |= (flag & 1)

                    f[level][s][rest][flag] += calc_without_zero(level + 1, nxt_s, nxt_rest, nxt_flag, f)
            
            return f[level][s][rest][flag]

        res = 0
        for mod in range(1, 9 * n + 1):
            tmp = mod
            for v in [2, 3, 5, 7]:
                while tmp % v == 0:
                    tmp //= v
            
            if tmp == 1:
                f = [[[[None] * 8 for _ in range(mod)] for _ in range(mod + 1)] for _ in range(n + 1)]
                res += calc_without_zero(0, 0, 0, 7, f)

            f = [[[None] * 16 for _ in range(mod + 1)] for _ in range(n + 1)]
            res += calc_with_zero(0, 0, 7, f)
        
        return res
''',
    call='Solution().beautifulNumbers(8, 12)',
    expect=3,
    skip=['left = [int', 'right = [int', 'left = [0]', 'n = len(right)', 'f[level][s][flag] = 0', 'f[level][s][rest][flag] = 0',
          'start, end =', 'start = ', 'end = ', 'nxt_s = s + v', 'nxt_flag = ', 'nxt_flag |=', 'nxt_rest = ', 'tmp = mod', 'for v in', 'while tmp',
          'tmp //= v', 'else:', 'if v == left', 'if v == right', 'if flag & 4', 'if flag & 2', 'if flag & 1', 'if v == 0',
          'res = 0', 'f = [[[', 'continue', 'break', 'if flag & 8', 'if rest == 0'],
    views=[
        dict(type='array', var='right', label='right = r 的数位（蓝箭头 = 正在填第 level 位）', cell=70, h=170,
             pointers={_L: 'blue'}, pointer_labels={_L: 'level'},
             color=lambda S, i, v: 'blue' if i == _L(S) else None),
        dict(type='array', var='left', label='left = l 的数位（补前导零对齐）', cell=70, h=170,
             pointers={_L: 'blue'}, pointer_labels={_L: 'level'},
             color=lambda S, i, v: 'blue' if i == _L(S) else None),
        dict(type='text', fn=_state, size=22, h=90),
        dict(type='calls', h=190, hide=('f',)),
    ],
    watch=[('mod', lambda S: S.get('mod', '-'), 'cyan'),
           ('level', lambda S: S['_inner'].get('level', '-'), 'blue'),
           ('s', lambda S: S['_inner'].get('s', '-'), 'yellow'),
           ('flag', lambda S: S['_inner'].get('flag', '-'), 'pink'),
           ('res', lambda S: S.get('res', '-'), 'green')],
    captions={
        'for mod in range': lambda S, B, r: f"枚举数位和 `mod = {S['mod']}`：不能直接对「变化的数位和」取模，所以==先固定最终数位和==" if 'mod' in S else '开始',
        'if tmp == 1': lambda S, B, r: (f"`mod = {S.mod}` 的质因子只有 2、3、5、7 → 「没有 0」的数也可能整除，要算「无 0」的部分"
                                        if S.tmp == 1 else f"`mod = {S.mod}` 含其他质因子 → 数位乘积（没有 0 时）不可能被它整除，跳过「无 0」部分"),
        'res += calc_without_zero': '「无 0」：数位里没有非前导 0，乘积的余数 `rest` 要变成 0，且数位和恰好 `mod`',
        'res += calc_with_zero': '「有 0」：只要出现非前导 0，乘积就是 0，必能整除 → 只需记数位和恰好 `mod`（`flag & 8` 表示出现过 0）',
        'if f[level][s][flag] is None': '备忘录：没算过才往下算',
        'if f[level][s][rest][flag] is None': '备忘录：没算过才往下算',
        'if level == n': lambda S, B, r: (f"填满 {S.n} 位：" + ('数位和恰好 `mod`，且 ' + ('出现过非前导 0 → ==算 1 种==' if S['_inner']['flag'] & 8 else '没出现非前导 0 → 算 0 种')
                                                                 if 'rest' not in S['_inner'] else '数位和是否恰好 `mod`、乘积余数 `rest` 是否为 0 → 满足才算 1 种'))
                                         if S['_inner']['level'] == S.n else f"`level = {S['_inner']['level']}`，还没填满 {S.n} 位",
        'if nxt_s + (n - level - 1) * 9 < mod': lambda S, B, r: (
            f"填 `v = {S['_inner']['v']}` 后数位和 `{S['_inner']['nxt_s']}`，后面最多再补 `{(S.n - S['_inner']['level'] - 1) * 9}` → 最多 {S['_inner']['nxt_s'] + (S.n - S['_inner']['level'] - 1) * 9} < `mod = {S.mod}`，凑不到 → ==剪枝，换下一个 v=="
            if S['_inner']['nxt_s'] + (S.n - S['_inner']['level'] - 1) * 9 < S.mod else
            f"填 `v = {S['_inner']['v']}`，数位和 `{S['_inner']['nxt_s']}`，后面还有机会凑到 `mod = {S.mod}` → 继续"),
        'if nxt_s > mod': lambda S, B, r: (
            f"数位和 `{S['_inner']['nxt_s']}` 已超过 `mod = {S.mod}`，更大的 v 只会更大 → ==结束这层循环=="
            if S['_inner']['nxt_s'] > S.mod else f"数位和 `{S['_inner']['nxt_s']}` ≤ `mod = {S.mod}`，可以往下填"),
        'f[level][s][flag] += calc_with_zero': '这一位填 `v`，交给下一位：`flag` 的各位表示「有 0 / 前导零 / 贴 left / 贴 right」',
        'f[level][s][rest][flag] += calc_without_zero': '这一位填 `v`：乘积余数 `rest × v % mod`，交给下一位',
        'return f[level][s][flag]': '这个状态的方案数 ==`{ret}`==',
        'return f[level][s][rest][flag]': '这个状态的方案数 ==`{ret}`==',
        'return res': '答案 ==`{res}`==',
    },
    max_steps=48,
    max_events=60000,
    cards=dict(
        one_liner='先固定最终数位和 mod，再用数位 DP 数乘积能被 mod 整除的数',
        complexity='状态多、常数大，靠枚举 mod 和剪枝过题',
        problem=['数位乘积能被数位之和整除的正整数是==美丽整数==',
                 '数出 `[l, r]` 里有多少个美丽整数，`r < 10^9`',
                 '本视频：`l=8, r=12` → `3`（8、9、10）'],
        quote='数位之和可能随着数位的填充不断变化，在这个过程中无法通过上一轮的余数计算出新的余数。……在这里可以枚举最后的数位和mod，接下来对于当前的mod，就可以使用f[level][s][rest][flag]',
        quote_src='—— yiduobo 题解原文',
        idea=['数位和 ≤ 72：枚举最终的数位和 `mod`，乘积就能对固定的 `mod` 取余',
              '数位里有非前导 0：乘积为 0，必能整除，不用记 `rest`',
              '无 0：乘积只含质因子 2、3、5、7，`mod` 含别的质因子就不用算'],
        summary=['时间复杂度高，靠可行性剪枝和质因子判断才能通过',
                 '`flag` 是位掩码：4 前导零，2 贴 left，1 贴 right，8 出现过非前导 0（有 0 版本）',
                 '「有 0」「无 0」两部分分别累计，互不重复',
                 '原文已是 Python 3 可运行的写法，代码未做修改',
                 '对比灵神：灵神直接把乘积 `m` 和数位和 `s` 都当状态（乘积只有 3026 种）；yiduobo 枚举数位和以固定模数'],
    ),
)

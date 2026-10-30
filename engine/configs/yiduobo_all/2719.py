def _L(S):
    return S['_inner'].get('level')


def _txt(S):
    I = S['_inner']
    if 'level' not in I or 'flag' not in I:
        return '`flag` 两位：低位 = 仍贴着 `num1`，高位 = 仍贴着 `num2`'
    f = I['flag']
    lo = '贴 num1' if f & 1 else '不限下界'
    hi = '贴 num2' if f & 2 else '不限上界'
    return f"`dfs(level={I['level']}, rest_s={I['rest_s']}, flag={f})`：=={lo}==，=={hi}==，还剩数位和额度 `{I['rest_s']}`"


CONFIG = dict(
    num=2719, title='统计整数数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='数位 DP · 上限相减',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def count(self, num1, num2, min_sum, max_sum):

        mod = 10 ** 9 + 7
        n = len(num2)

        global f
        f = [[[None] * 4 for j in range(max_sum + 1)] for i in range(n + 1)]

        def dfs(level, rest_s, flag):
            global f

            if level == len(num2):
                return 1
            
            if f[level][rest_s][flag] is not None:
                return f[level][rest_s][flag]
            
            f[level][rest_s][flag] = 0

            for digit in range(10):
                if digit > rest_s:
                    break
                
                next_flag = 0

                if flag & 1:
                    if digit < int(num1[level]):
                        continue
                    elif digit == int(num1[level]):
                        next_flag |= 1
                
                if flag & 2:
                    if digit > int(num2[level]):
                        continue
                    elif digit == int(num2[level]):
                        next_flag |= 2
                
                f[level][rest_s][flag] += dfs(level + 1, rest_s - digit, next_flag)
                if f[level][rest_s][flag] >= mod:
                    f[level][rest_s][flag] -= mod
            
            return f[level][rest_s][flag]
                

        num1 = '0' * (n - len(num1)) + num1
        res = dfs(0, max_sum, 3) - dfs(0, min_sum - 1, 3)
        if res < 0:
            res += mod
        return res
''',
    call='Solution().count("1", "12", 1, 5)',
    expect=8,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='string', var='num1', label='num1（补前导零后）', cell=64, h=130, pointers={_L: 'blue'}, pointer_labels={_L: 'level'}),
        dict(type='string', var='num2', label='num2', cell=64, h=130, pointers={_L: 'pink'}, pointer_labels={_L: 'level'}),
        dict(type='calls', h=300),
    ],
    watch=[('level', lambda S: S['_inner'].get('level'), 'blue'), ('rest_s', lambda S: S['_inner'].get('rest_s'), 'yellow'),
           ('flag', lambda S: S['_inner'].get('flag'), 'purple'), ('digit', lambda S: S['_inner'].get('digit'), 'orange'),
           ('res', lambda S: S.get('res'), 'green')],
    skip=['next_flag = 0', 'mod = ', 'n = len', 'global f', 'f[level][rest_s][flag] = 0'],
    max_steps=50,
    captions={
        'f = [[[None]': '`f[level][rest_s][flag]` 记忆化表，`None` 表示还没算过',
        'if level == len(num2)': lambda S, B, r: ('`level == len(num2)`：每一位都填完了 → 得到一个数，返回 ==1==' if S.level == len(S.num2)
                                                 else f'`level = {S.level} < {len(S.num2)}`：还有数位要填'),
        'if f[level][rest_s][flag] is not None': lambda S, B, r: ('这个状态算过了，直接取表里的值' if S.f[S.level][S.rest_s][S.flag] is not None else '这个状态还没算过，往下枚举'),
        'for digit in range(10)': '枚举这一位填 `digit`：`{digit}`',
        'if digit > rest_s': lambda S, B, r: (f'`{S.digit} > rest_s = {S.rest_s}`：数位和额度不够，后面更大的 `digit` 也不行 → ==break==' if S.digit > S.rest_s
                                              else f'`{S.digit} ≤ rest_s = {S.rest_s}`：额度够，继续'),
        'if flag & 1': '`flag & 1`：是否还贴着下界 `num1` → {flag & 1 == 1}',
        'if digit < int(num1[level])': lambda S, B, r: (f'`{S.digit} < num1[{S.level}] = {S.num1[S.level]}`：比下界还小，这个数不合法 → ==continue=='
                                                        if S.digit < int(S.num1[S.level]) else f'`{S.digit} ≥ num1[{S.level}] = {S.num1[S.level]}`：没低于下界，继续'),
        'elif digit == int(num1[level])': lambda S, B, r: (f'`{S.digit} == num1[{S.level}]`：恰好贴着下界，下一位还要受 `num1` 约束 → `next_flag |= 1`'
                                                           if S.digit == int(S.num1[S.level]) else f'`{S.digit} > num1[{S.level}]`：已高于下界，之后不再受 `num1` 约束'),
        'if flag & 2': '`flag & 2`：是否还贴着上界 `num2` → {flag & 2 == 2}',
        'if digit > int(num2[level])': lambda S, B, r: (f'`{S.digit} > num2[{S.level}] = {S.num2[S.level]}`：超过上界，这个数不合法 → ==continue=='
                                                        if S.digit > int(S.num2[S.level]) else f'`{S.digit} ≤ num2[{S.level}] = {S.num2[S.level]}`：没超过上界，继续'),
        'elif digit == int(num2[level])': lambda S, B, r: (f'`{S.digit} == num2[{S.level}]`：恰好贴着上界，下一位还要受 `num2` 约束 → `next_flag |= 2`'
                                                           if S.digit == int(S.num2[S.level]) else f'`{S.digit} < num2[{S.level}]`：已低于上界，之后不再受 `num2` 约束'),
        'f[level][rest_s][flag] += dfs': '填 `digit = {B.digit}`：额度剩 `{B.rest_s - B.digit}`，新 `flag = {B.next_flag}`，累加子问题的方案数',
        'if f[level][rest_s][flag] >= mod': '累计值若 `≥ mod` 就减一个 `mod`，保持取余',
        'return f[level][rest_s][flag]': '`f[{level}][{rest_s}][{flag}]` = ==`{ret}`== 个方案',
        'num1 = ': '`num1` 左边补 0 到和 `num2` 一样长：`num1 = {num1!r}`',
        'res = dfs': '`res = dfs(0, max_sum, 3) − dfs(0, min_sum−1, 3)`：数位和 `≤ 5` 的个数 − 数位和 `≤ 0` 的个数 = ==`{res}`==',
        'if res < 0': '相减可能为负，取余前先判断：`res = {res}`',
        'res += mod': '`res` 为负，加回 `mod`',
        'return res': '好整数共 ==`{res}`== 个',
    },
    cards=dict(
        result='返回 `8`：数位和 ≤ 5 的 9 个数 − 数位和 ≤ 0 的 1 个数（即 0）',
        one_liner='数位和下限用「上限相减」，flag 两位记录贴不贴上下界',
        complexity='时间 `O(n·max_sum·4·10)`，空间 `O(n·max_sum·4)`',
        problem=['给数字字符串 `num1`、`num2` 和数位和范围 `[min_sum, max_sum]`',
                 '数 `num1 ≤ x ≤ num2` 且数位和在范围内的整数个数（取余 `10^9+7`）',
                 '本视频：`"1"~"12"`，数位和 `1..5` → `8`'],
        quote='数位和的上下界不方便直接放进状态表示中，那么在这里可以采用类似前缀差求解区间问题的方法。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[level][rest_s][flag]`：从第 `level` 位起，数位和额度还剩 `rest_s`，`flag` 记录与两个边界的关系',
              '答案 = 数位和 `≤ max_sum` 的个数 − 数位和 `≤ min_sum−1` 的个数',
              '`digit` 超过额度就 `break`；贴边界时才用 `num1/num2` 限制 `digit`'],
        summary=['时间 `O(n·S·4·10)`，`S = max_sum`',
                 '`flag` 低位贴 `num1`、高位贴 `num2`，初始 `3` 表示两个都贴着',
                 '易错：`num1` 要先补前导零；相减后为负要加回 `mod`',
                 '对比灵神：他把数位和放进状态并在填完时判 `≥ min_sum`；这里改成额度递减，用两次搜索相减'],
    ),
)

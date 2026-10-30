def _txt(S):
    if 'x7' not in S:
        return '`s9`、`pre7`：前缀数位和模 9、前缀数值模 7；`x7 = pre7 × inv7[index % 6] % 7`'
    return f"`s9` = {S['s9']}，`pre7` = {S['pre7']}，`x7` = {S['pre7']}×{S['inv7'][S['index'] % 6]} % 7 = =={S['x7']}=="


CONFIG = dict(
    num=3448, title='统计可以被最后一个数位整除的子字符串数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='按末位分类讨论 · 前缀和计数',
    tags=['灵神题单', '动态规划', '难度分 2387'],
    code='''
class Solution(object):
    def countSubstrings(self, s):
        
        res = 0
        cnt7 = [0] * 7
        cnt9 = [0] * 9
        cnt7[0] = 1
        cnt9[0] = 1
        s9 = 0
        pre7 = 0

        inv7 = [1, 5, 4, 6, 2, 3]

        for index, char in enumerate(s):
            v = int(char)
            s9 += v
            s9 %= 9
            pre7 = (pre7 * 10 + v) % 7
            x7 = pre7 * inv7[index % 6] % 7

            if v == 0:
                pass
            elif v == 1 or v == 2 or v == 5:
                res += index + 1
            elif v == 3 or v == 6:
                x = s9 % 3
                res += cnt9[x] + cnt9[(x + 3) % 9] + cnt9[(x + 6) % 9]
            elif v == 4:
                res += 1
                if index > 0 and int(s[index - 1]) % 2 == 0:
                    res += index
            elif v == 7:
                res += cnt7[x7]
            elif v == 8:
                res += 1
                if index > 0 and int(s[index - 1]) % 4 == 0:
                    res += 1
                if index > 1 and (int(s[index - 2]) * 10 + int(s[index - 1])) % 4 == 0:
                    res += index - 1
            elif v == 9:
                res += cnt9[s9]
            
            cnt9[s9] += 1
            cnt7[x7] += 1

        return res
''',
    call='Solution().countSubstrings("7839")',
    expect=6,
    skip=['cnt7[0] = 1', 'cnt9[0] = 1', 's9 = 0', 'pre7 = 0', 'inv7 = ', 'v = int(char)', 's9 += v', 's9 %= 9',
          'pre7 = (pre7', 'cnt7 = [0] * 7', 'cnt9 = [0] * 9'],
    max_steps=90,
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前末位 s[index]）', h=140, cell=80,
             color=lambda S, i, x: 'blue' if i == S.get('index') else None,
             dim=lambda S, i, x: 'index' in S and i > S['index']),
        dict(type='text', size=26, h=60, fn=_txt),
        dict(type='array', var='cnt9', label='cnt9[r]：前缀数位和模 9 余 r 的前缀个数（黄 = 当前 s9）', h=150, cell=70,
             color=lambda S, i, x: 'yellow' if 's9' in S and i == S['s9'] and S.get('_line', 0) >= 20 else None),
        dict(type='array', var='cnt7', label='cnt7[r]：x7 = r 的前缀个数（黄 = 当前 x7）', h=150, cell=70,
             color=lambda S, i, x: 'yellow' if 'x7' in S and i == S['x7'] and S.get('_line', 0) >= 20 else None),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v', 'pink'), ('s9', 's9', 'cyan'), ('x7', 'x7', 'orange'), ('res', 'res', 'green')],
    captions={
        'for index, char': lambda S, B, r: (f"看以 `s[{S.index}]` 结尾的所有子串：末位 `{S.char}` 决定怎么判断整除" if S.get('index') != B.get('index') else '所有末位都处理完了'),
        'x7 = ': _txt,
        'if v == 0': lambda S, B, r: '末位 `0`：题目不统计末位为 0 的子串，直接跳过' if S.v == 0 else '末位是 `%d`，不是 0，继续分类' % S.v,
        'elif v == 1': lambda S, B, r: ('末位 `%d` 是 1/2/5：能被自己末位整除的子串==全部==满足（任何整数被 1 整除；末位 2、5 同理）' % S.v) if S.v in (1, 2, 5) else '`%d` 不是 1/2/5，继续' % S.v,
        'res += index + 1': '以 `s[{index}]` 结尾的 `{index} + 1` 个子串全部满足：`res` = =={res}==',
        'elif v == 3': lambda S, B, r: ('末位 `%d` 是 3/6：整除 3 只看数位和（6 末位已保证偶数），转成前缀和模 9 计数' % S.v) if S.v in (3, 6) else '`%d` 不是 3/6，继续' % S.v,
        'x = s9 % 3': '数位和要是 3 的倍数：前缀和模 9 与当前相差 0/3/6 的前缀都行，`x = {x}`',
        'res += cnt9[x]': '`cnt9[{x}] + cnt9[{(x + 3) % 9}] + cnt9[{(x + 6) % 9}]`：共 {cnt9[x] + cnt9[(x + 3) % 9] + cnt9[(x + 6) % 9]} 个满足 → `res` = =={res}==',
        'elif v == 4': lambda S, B, r: '末位 `4`：100 = 4×25，只看末两位是否被 4 整除' if S.v == 4 else '`%d` 不是 4，继续' % S.v,
        29: '`s[{index}]` 单独成串就是 4，必然整除',
        30: '倒数第二位是偶数 → 末两位能被 4 整除 → 所有更长的子串都满足，再加 `index` 个',
        31: '再加 `{index}` 个：`res` = =={res}==',
        'elif v == 7': lambda S, B, r: '末位 `7`：没有简单规律，改用同余：子串 = 前缀 − 前缀×10 的幂' if S.v == 7 else '`%d` 不是 7，继续' % S.v,
        'res += cnt7[x7]': '`s[:index+1]×inv ≡ s[:p]×inv (mod 7)` 的前缀 p 共 `cnt7[{x7}]` = {cnt7[x7]} 个 → `res` = =={res}==',
        'elif v == 8': lambda S, B, r: '末位 `8`：1000 = 8×125，看末三位；长度 1、2、≥3 分别判断' if S.v == 8 else '`%d` 不是 8，继续' % S.v,
        35: '`s[{index}]` 单独成串就是 8，必然整除',
        36: lambda S, B, r: ('倒数第二位 %d 能被 4 整除 → 末两位（长度 2 的子串）能被 8 整除，再加 1' % int(S.s[S.index - 1])) if S.index > 0 and int(S.s[S.index - 1]) % 4 == 0 else '长度 2 的子串（末两位）不能被 8 整除，不加',
        37: '长度为 2 的子串满足：`res` = =={res}==',
        38: lambda S, B, r: ('长度 ≥ 3 的子串：看末三位的前两位能否被 4 整除（1000 = 8×125）' ),
        39: '长度 ≥ 3 的 `{index} - 1` 个子串都满足：`res` = =={res}==',
        'elif v == 9': lambda S, B, r: '末位 `9`：整除 9 只看数位和，找前缀和模 9 相同的前缀' if S.v == 9 else '`%d` 不是 9' % S.v,
        'res += cnt9[s9]': '`cnt9[{s9}]` = {cnt9[s9]} 个前缀与当前同余，子串数位和是 9 的倍数 → `res` = =={res}==',
        'cnt9[s9] += 1': '记下这个前缀：`cnt9[{s9}]` 加 1',
        'cnt7[x7] += 1': '记下这个前缀：`cnt7[{x7}]` 加 1',
        'return res': '全部扫完，答案 =={ret}==',
    },
    cards=dict(
        one_liner='按末位 0~9 逐类讨论：1/2/5 全中，3/6/9 用前缀和，7 用逆元',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['数字串 `s`，统计末位不是 0、且能被自己末位整除的子串个数（可有前导 0）',
                 '示例：`s = "12936"` → `11`；`s = "5701283"` → `18`',
                 '视频里用 `s = "7839"` 演示，答案 6'],
        quote='若某个整数可以被3整除，那么其数位之和也一定可以被3整除。……而子串的数位和问题可以认为是某种区间和问题，于是可以想办法转化为前缀和问题进行求解。',
        quote_src='—— yiduobo 题解',
        idea=['一趟遍历，看以 `s[index]` 结尾的子串，末位只有 10 种情况，逐个找整除规律',
              '1、2、5 全满足；4、8 看末 2、3 位；3、6、9 看数位和 → 前缀和模 9 计数 `cnt9`',
              '7 没有好规律：子串值 = 前缀 − 前缀×10 的幂，转成模 7 同余，用逆元 `inv7` 和 `cnt7` 计数'],
        summary=['时间 `O(n)`，空间 `O(1)`（`cnt7`、`cnt9` 是定长数组）',
                 '`cnt7[0] = cnt9[0] = 1` 对应空前缀，别漏',
                 '`x7` 与 `cnt7[x7]` 要先用后更新：先累加答案，再 `+= 1`',
                 '10 的幂模 7 循环节为 6，所以 `inv7` 是 `[1,5,4,6,2,3]`'],
    ),
)

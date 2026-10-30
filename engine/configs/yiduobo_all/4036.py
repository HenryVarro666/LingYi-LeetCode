def _vbits(S):
    v = S.get('v')
    return bin(v)[2:] if v else '0'


def _s_text(S):
    s = S.get('s')
    if s is None:
        return ''
    return f's（先收集，低位 → 高位）= ==`{"".join(s) or "空"}`=='


def _res_text(S):
    r = S.get('res')
    if not r:
        return ''
    return '已得答案：' + ' , '.join(f'`{x}`' for x in r)


def _if_cap(S, B, ret):
    # 执行前的 v（B.v）的最低位
    v = B['v']
    idx = S.index
    if v & 1:
        return f'第 `{idx}` 位：`v & 1 = 1` → 有 `2^{idx}` 个 a 合成的字母 ==`{chr(idx + 97)}`==，收进 s'
    return f'第 `{idx}` 位：`v & 1 = 0` → 没有字母 `{chr(idx + 97)}`，跳过'


CONFIG = dict(
    num=4036, title='字符对转换后字典序最大的字符串', difficulty='Medium', category='位运算',
    author='yiduobo', technique='x 看成二进制数 · 低位收集再翻转',
    tags=[],
    code='''
class Solution(object):
    def largestString(self, nums):
        
        
        res = []
        for v in nums:
            s = []
            for index in range(25):
                if v & 1:
                    s.append(chr(index + 97))
                v >>= 1
            
            s.extend(['z'] * v)
            res.append(''.join(s[::-1]))
        
        return res
''',
    call='Solution().largestString([13])',
    expect=['dca'],
    skip=['res = []', 's = []', 'v >>= 1', 'for index in range'],
    max_steps=80,
    views=[
        dict(type='array', var='nums', label='nums', h=150, cell=90,
             color=lambda S, k, v: 'blue' if S.get('res') is not None and k == len(S['res']) else None,
             dim=lambda S, k, v: S.get('res') is not None and k < len(S['res'])),
        dict(type='string', var=_vbits, label='当前 v 的二进制（每轮右移一位，最右边是最低位）', h=210, cell=70,
             pointers={'低位': 'pink'}, color=lambda S, k, v: 'pink' if k == len(_vbits(S)) - 1 else None),
        dict(type='text', fn=_s_text, size=26, h=60),
        dict(type='text', fn=_res_text, size=26, h=60),
    ],
    watch=['v', ('index', 'index', 'pink'), ('s', lambda S: ''.join(S['s']) if 's' in S else '', 'green')],
    captions={
        'for v in nums': lambda S, B, r: ('nums 都处理完了' if 'v' in B and S.res and len(S.res) == len(S.nums) else f'处理 `v = {S.v}`，二进制 `{bin(S.v)[2:]}`；下面扫 25 位，每轮看最低位再右移'),
        'if v & 1': _if_cap,
        's.append(chr': '`chr({index} + 97)` = ==`{s[-1]}`== 接到 s 末尾：`s` = `{"".join(s)}`',
        's.extend': '右移 25 位后 `v = {v}` 就是 `a[25]`：补 ==`{v}`== 个 `z` → s = `{"".join(s)}`',
        'res.append': '`s` 是低位在前，翻转让大字母在前：==`{res[-1]}`==',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='x 当二进制数拆开：每一位是 1 就有对应字母',
        complexity='时间 `O(n·(25 + U/2^25))`，空间 `O(1)`',
        problem=['`x` 个 `a`，每次把相邻相同的两个字母合成下一个字母（`zz` 除外）',
                 '对每个 `x` 求字典序最大的字符串',
                 '示例：`[2,5,7]` → `["b","ca","cba"]`；本视频：`[13]` → `["dca"]`'],
        quote='可以将x视为一个超长的2进制数，那么其可以写成 a[0] * 2^0 + a[1] * 2^1 + ... + a[25] * 2^25，其中a[0]到a[24]只能是0或者1，而a[25]则可以大于1。',
        quote_src='—— yiduobo 题解原文',
        idea=['先尽量合出 `z`：用 `2^25` 个 a 一组，之后再考虑 `y`、`x`……',
              '`a` 数组恰好是每种字符在答案中的个数，大字符放前面即可',
              '从低位到高位提取 25 位，位移后剩下的 `v` 就是 `z` 的个数，最后整体翻转'],
        summary=['时间 `O(n·(25 + U/2^25))`，空间 `O(1)`',
                 '低位到高位是 a → y，所以最后要 `s[::-1]`；`z` 先 extend 再翻转，自然排在最前面',
                 '位移 25 次之后的 `v` 可以大于 1，用 `[\'z\'] * v` 补上',
                 '对比灵神：灵神直接倒着从高位枚举，不用翻转；本文从低位收集再翻转'],
    ),
)

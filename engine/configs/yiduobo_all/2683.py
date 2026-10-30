def _recon(S):
    d = S['derived']
    o = [0]
    for v in d[:-1]:
        o.append(o[-1] ^ v)
    return f"令 original[0]=0 反推：`{o}`；回环 `{o[-1]} ⊕ {o[0]} = {o[-1]^o[0]}`，需等于 derived[-1] = `{d[-1]}`"

CONFIG = dict(
    num=2683, title='相邻值的按位异或', difficulty='Medium', category='位运算',
    author='yiduobo', technique='固定首位反推 / 异或和',
    tags=['灵神题单', '位运算', '难度分 1518'],
    code='''
class Solution:
    def doesValidArrayExist(self, derived):

        xor = 0
        for v in derived:
            xor ^= v
        
        return xor == 0
''',
    call='Solution().doesValidArrayExist([1,1,0,1,1])',
    expect=True,
    views=[
        dict(type='array', var='derived', pointers={'v': 'blue'}, label='derived', h=170),
        dict(type='text', fn=_recon, size=26, h=100),
        dict(type='text', fn=lambda S: f"累积异或 xor = `{S['xor']}`" if 'xor' in S else '', size=34, h=80),
    ],
    watch=['v', ('xor', 'xor', 'green')],
    captions={
        'xor = 0': '异或的单位元是 0，从 0 开始累积',
        'for v in': '取出 `derived` 的下一个数 `v = {v}`',
        'xor ^= v': '`{B.xor} ^ {v} = {xor}`：把 `v` 并入累积异或',
        'return xor': '`derived` 全部异或 = `{xor}`，`== 0` → =={ret}==；等于 0 说明反推出的 original[n-1]^original[0] 恰好等于 derived[n-1]',
    },
    cards=dict(
        one_liner='首位固定为 0 反推，回环条件化成全体异或为 0',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`derived[i]` 是 `original` 相邻两数的异或，末尾与首位回环',
                 '判断是否存在满足的 0/1 数组 `original`',
                 '示例：`[1,1,0]` → `true`；`[1,0]` → `false`'],
        quote='若其以1开头，那么就可以将数组中的每个数v都变为1 - v，此时相邻元素间的异或结果不会发生变化。',
        quote_src='—— yiduobo 题解',
        idea=['有解就一定有以 0 开头的解：整体取反，相邻异或不变',
              '令 `original[0]=0`，逐个推出 `original[i]=original[i-1]^derived[i-1]`',
              '代入得 `original[n-1]` = 前 n-1 个 derived 的异或，回环要求再异或 derived[n-1] 为 0'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '关键是“可调整为 0 开头”这一步，把存在性问题变成确定性反推',
                 '最终只需检查 derived 全体异或是否为 0',
                 '易错：循环要包含最后一个元素'],
    ),
)

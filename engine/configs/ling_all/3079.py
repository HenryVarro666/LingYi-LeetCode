CONFIG = dict(
    num=3079, title='求出加密整数的和', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='逐位拆数 · 同时造 111…',
    tags=[],
    code='''
class Solution:
    def sumOfEncryptedInt(self, nums: List[int]) -> int:
        ans = 0
        for x in nums:
            mx = base = 0
            while x:
                x, d = divmod(x, 10)
                mx = max(mx, d)
                base = base * 10 + 1
            ans += mx * base
        return ans
''',
    call='Solution().sumOfEncryptedInt([523, 10, 21, 7])',
    expect=595,
    views=[
        dict(type='array', var='nums', h=200, color=lambda S, i, v: 'green' if 'ans' in S and v == 0 else None),
        dict(type='text', h=120, size=40, fn=lambda S: (f"当前数位 `d = {S['d']}`，最大数位 `mx = {S['mx']}`，`base = {S['base']}`" if 'd' in S and 'mx' in S else '')),
        dict(type='text', h=120, size=40, fn=lambda S: (f"加密值 = `mx × base` = `{S['mx']} × {S['base']}` = =={S['mx']*S['base']}==" if 'base' in S and 'mx' in S and S['base'] > 0 else '')),
    ],
    watch=['x', 'd', ('mx', 'mx', 'pink'), ('base', 'base', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'mx = base = 0': '新的一个数：最大数位 `mx` 和 `base` 都从 0 开始',
        'divmod': '`divmod(x, 10)`：把最低位 ==`d = {d}`== 拆出来，`x` 剩下 `{x}`',
        'mx = max': '`mx = max({B.mx}, {d}) = {mx}`：记下目前见过的最大数位',
        'base = base': '每拆一位，`base` 多一个 1：`{B.base}` → =={base}==（位数和原数相同）',
        'ans += ': '加密后的数 = 每一位都是 `mx` = `{mx} × {base}` = =={mx*base}==，累加得 `ans = {ans}`',
    },
    cards=dict(
        one_liner='拆数位时顺手造出 111…，乘以最大数位',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['加密：把整数每一位都换成其中最大的数位，如 `523 → 555`',
                 '求数组里所有元素加密后的和',
                 '示例：`[10,21,31]` → `11+22+33 = 66`'],
        quote='遍历 x 的每个数位，计算其最大数位 mx。遍历的同时，计算出一个等于 111⋯ 的值 base。那么加密后的结果就是 mx·base。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`divmod(x, 10)` 一次拿到「剩余部分」和「最低位」',
              '数位个数 = 循环次数，所以 `base` 每轮 `*10+1` 就得到 111…',
              '加密结果 `mx * base`，不用真的拼字符串'],
        summary=['时间 `O(n log U)`：每个数有 `log U` 位',
                 '==`base` 的位数要和原数相同==：每拆一位才加一个 1',
                 '题目保证正整数，`x = 0` 时不会进入 while，也不会出现']),
)

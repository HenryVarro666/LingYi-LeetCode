def _chain(S):
    d = S['derived']
    acc = 0
    parts = []
    for v in d:
        acc ^= v
        parts.append(str(v))
    return f"`{' ⊕ '.join(parts)}` = ==%d==" % acc

def _orig(S):
    d = S['derived']
    o = [0]
    for v in d[:-1]:
        o.append(o[-1] ^ v)
    o2 = [1 - x for x in o]
    return f"original 取 `{o}` 或 `{o2}`，首尾回环：`{o[-1]} ⊕ {o[0]} = {o[-1]^o[0]}` = derived[-1]"

CONFIG = dict(
    num=2683, title='相邻值的按位异或', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='全体异或和为 0',
    tags=['灵神题单', '位运算', '难度分 1518'],
    code='''
class Solution:
    def doesValidArrayExist(self, derived: List[int]) -> bool:
        return reduce(xor, derived) == 0
''',
    call='Solution().doesValidArrayExist([1,1,0,1,1])',
    expect=True,
    views=[
        dict(type='array', var='derived', label='derived', h=170),
        dict(type='text', fn=_chain, size=34, h=90),
        dict(type='text', fn=_orig, size=28, h=110),
    ],
    watch=[('derived 异或和', 'reduce(xor, derived)', 'green')],
    captions={
        'return reduce': lambda S, B, ret: f"derived 全部异或 = =={reduce(xor, S['derived'])}==。右边每个 `original[i]` 出现两次，异或抵消成 0，所以必须等于 0 → `== 0` → =={ret}==",
    },
    cards=dict(
        one_liner='列出所有式子，两边同时异或：右边全部抵消',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`derived[i] = original[i] ⊕ original[i+1]`，最后一个与 `original[0]` 回环',
                 '问是否存在 0/1 数组 `original` 能派生出给定的 `derived`',
                 '示例：`[1,1,0]` → `true`；`[1,0]` → `false`'],
        quote='右边中的每个 original[i] 都出现了两次（original[0] 首尾各出现一次），由于一个数异或两次等于 0，所以右边所有数的异或和为 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把 n 个式子列出来，左右两边同时求异或和',
              '右边每个 `original[i]` 出现两次，抵消为 `0`',
              '所以有解的必要条件是 derived 异或和为 0，而且恰有两个解（original[0] 取 0 或 1）'],
        after=[dict(heading='为什么恰有两个解', lines=['异或和为 0 时有解，且 `original[0]` 取 0 或 1 各一个解',
                                          '`original[0]` 定了，后面 `original[i]=original[i-1]⊕derived[i-1]` 全被确定',
                                          '两个解互为按位取反，相邻异或不变'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '一行搞定：`reduce(xor, derived) == 0`',
                 '写法二：`sum(derived) % 2 == 0`，因为异或和就是 1 的个数的奇偶性',
                 '易错：回环那一项也算进异或和里，别漏掉最后一个'],
    ),
)

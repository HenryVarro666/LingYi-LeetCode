S0, K0 = '0001011100', 3


def _wl(S):
    if 'i' not in S:
        return None
    return max(0, S['i'] - S['k'] + 1)


def _txt(S, B):
    if 'x' not in S:
        return f'`MASK = (1 << k) − 1`：低 `k` 位全是 1，用来==去掉超出 k 的比特位=='
    if 'i' not in S:
        return f"`x = {S['x']}`"
    k = S['k']
    old = B.get('x', 0) if B.get('x') is not None else 0
    if S['_line'] != 9:
        return f"`x` = =={S['x']:0{k}b}==（十进制 {S['x']}）　已收集 `{len(S['st'])}` / `{1 << k}` 种"
    return (f"`x = ({old:0{k}b} << 1 & {S['MASK']:0{k}b}) | {S['ch']}` = =={S['x']:0{k}b}==（十进制 {S['x']}）"
            f"　已收集 `{len(S['st'])}` / `{1 << k}` 种")


CONFIG = dict(
    num=1461, title='检查一个字符串是否包含所有长度为 K 的二进制子串', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='位运算滑窗 + 哈希集合',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution:
    def hasAllCodes(self, s: str, k: int) -> bool:
        MASK = (1 << k) - 1
        st = set()  # 更快的写法见另一份代码【Python3 列表】
        x = 0
        for i, ch in enumerate(s):
            # 把 ch 加到 x 的末尾：x 整体左移一位，然后或上 ch
            # &MASK 目的是去掉超出 k 的比特位
            x = (x << 1 & MASK) | int(ch)
            if i >= k - 1:
                st.add(x)
        return len(st) == 1 << k
''',
    call=f'Solution().hasAllCodes({S0!r}, {K0})',
    expect=True,
    views=[
        dict(type='string', var='s', label=f's（框 = 长为 k = {K0} 的窗口）', h=230, cell=96,
             pointers={'i': 'blue'}, window=(_wl, 'i')),
        dict(type='text', h=90, size=28, fn=_txt),
        dict(type='set', var='st', label='st（窗口对应的二进制数）', h=170, font=34,
             fmt=lambda v: f'{v:0{K0}b} ({v})'),
    ],
    watch=[('i', 'i', 'blue'), ('ch', 'ch'), ('x', 'x', 'orange'), ('MASK', 'MASK'), ('len(st)', 'len(st)', 'green')],
    captions={
        'MASK = (1 << k) - 1': '`MASK = {MASK}`（二进制 `{MASK:b}`）',
        'st = set()': '`st` 存所有出现过的长为 k 的子串（转成整数）',
        'x = 0': '`x`：窗口里的子串对应的二进制数',
        'for i, ch in': lambda S, B, r: ('遍历结束' if B.get('i') == S.i else f'`s[{S.i}] = {S.ch!r}` 进入窗口'),
        'x = (x << 1': lambda S, B, r: (f'左移一位、去掉第 k+1 位、末尾补 `{S.ch}`：`x` = `{S.x:0{S.k}b}`'
                                        if S.i >= S.k - 1 else f'窗口还没满，`x` = `{S.x:0{S.k}b}`'),
        'if i >= k - 1': lambda S, B, r: (f'`i = {S.i} ≥ k − 1`：窗口 `{S.s[S.i - S.k + 1:S.i + 1]!r}` 长度够 k' if S.i >= S.k - 1
                                          else f'`i = {S.i} < k − 1`：窗口还不满 k 个字符'),
        'st.add(x)': lambda S, B, r: (f'`{S.x:0{S.k}b}` 是==新的==子串，加入集合（共 {len(S.st)} 种）' if len(S.st) > len(B.st)
                                      else f'`{S.x:0{S.k}b}` 已经出现过，集合不变'),
        'return len(st)': '`len(st) = {len(st)}`，长为 k 的二进制串共 `2^k = {1 << k}` 种 → `{ret}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='把长为 k 的窗口看成一个 k 位二进制数，滑动只需移位',
        complexity='时间 `O(n)`，空间 `O(n − k)`（或布尔数组 `O(2^k)`）',
        problem=['二进制串 `s`，判断==所有==长为 `k` 的二进制串是否都是 `s` 的子串',
                 '示例：`s = "00110110", k = 2` → `true`（00、01、10、11 都出现了）',
                 '`s = "0110", k = 2` → `false`（没有 00）',
                 '本视频：`s = "0001011100", k = 3` → `true`（8 个窗口恰好是 8 种）'],
        quote='把子串转成整数，保存到哈希集合或者布尔数组中。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['入：`x << 1 | ch`，把新字符接到末尾',
              '出：`& MASK` 去掉超出 k 位的最高位 → 窗口最左边的字符离开',
              '集合大小恰好是 `2^k` ⇔ 所有串都出现了'],
        summary=['时间 `O(n)`，不用每次切片拷贝长为 k 的子串',
                 '易错：`i ≥ k − 1` 时窗口才满，之前不能加入集合',
                 '方法一：直接把切片 `s[i−k:i]` 放进集合，时间 `O((n−k)k)`',
                 '更快：布尔数组 `has` + 计数，凑满 `2^k` 种就提前返回 True'],
    ),
)

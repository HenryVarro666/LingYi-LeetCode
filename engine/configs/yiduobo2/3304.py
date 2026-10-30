K = 10


def _info(S):
    if 'chars' not in S:
        return f'k 最大只有 500 → ==直接暴力模拟==，直到长度 ≥ k'
    n = len(S['chars'])
    if S.get('_line') == 8 or (S.get('_line') == 4 and n >= K):
        return f"长度 `{n}` ≥ `k = {K}`：第 k 个字符就是 `chars[{K - 1}]`"
    if S.get('_line') == 6:
        L = n - 1 - S['index']
        return f"本轮：把前 `{L}` 个字母各自的==下一个字母==依次接到后面（长度 `{L}` → `{2 * L}`）"
    return f"当前长度 `{n}` < `k = {K}`：再操作一轮"


def _color(S, i, v):
    if 'index' in S and S.get('_line') == 6:
        L = len(S['chars']) - 1 - S['index']  # 本轮开始时的长度
        if i == S['index']:
            return 'blue'
        if i == len(S['chars']) - 1:
            return 'green'
        if i >= L:
            return 'cyan'
    if S.get('_line') in (4, 8) and len(S['chars']) >= K and i == K - 1:
        return 'yellow'
    return None


def _cap_while(S, B, ret):
    n = len(B.chars)
    if n < K:
        return f'`len(chars) = {n} < k = {K}` → 再操作一轮：长度会翻倍到 `{2 * n}`'
    return f'`len(chars) = {n} ≥ k = {K}` → 够长了，停止模拟'


def _cap_append(S, B, ret):
    i = S.index
    c = S.chars[i]
    nc = S.chars[-1]
    tip = '（z 的下一个是 a，所以 `% 26`）' if c == 'z' else ''
    return f'`chars[{i}] = {c}` 的下一个字母 `{nc}` 接到末尾{tip}'


CONFIG = dict(
    num=3304, title='找出第 K 个字符 I', difficulty='Easy', category='技巧',
    author='yiduobo', technique='k 很小 → 直接暴力模拟',
    tags=['字节30天'],
    code='''
class Solution(object):
    def kthCharacter(self, k):
        chars = ['a']
        while len(chars) < k:
            for index in range(len(chars)):
                chars.append(chr((ord(chars[index]) - 97 + 1) % 26 + 97))

        return chars[k - 1]
''',
    call=f'Solution().kthCharacter({K})',
    expect='c',
    views=[
        dict(type='text', fn=_info, size=26, h=70),
        dict(type='array', var='chars', label='chars（蓝 = 正在读的字母，青 = 本轮新接上的，绿 = 刚接上）', cell=60, h=200,
             color=_color, pointers={'index': 'blue', 'k - 1': 'pink'}, min_slots=16),
        dict(type='text', fn=lambda S: (f"`ord('{S['chars'][S['index']]}') - 97 + 1` → 再 `% 26 + 97` → `'{S['chars'][-1]}'`"
                                        if S.get('_line') == 6 else ''), size=26, h=70),
    ],
    watch=[('k', 'k', 'pink'), ('len(chars)', lambda S: len(S['chars']) if 'chars' in S else None, 'green'),
           ('index', 'index', 'blue')],
    captions={
        "chars = ['a']": '初始 `word = "a"`，用列表 `chars` 存每个字母',
        'while len(chars) < k': _cap_while,
        'chars.append': _cap_append,
        'return chars[k - 1]': '第 `k = {k}` 个字符是 `chars[{k - 1}]` = =={ret}==',
    },
    skip=['for index in range'],
    cards=dict(
        one_liner='k ≤ 500，直接按题意模拟到长度 ≥ k',
        complexity='时间 `O(k)`，空间 `O(k)`',
        problem=['一开始 `word = "a"`；每次操作把 word 的==每个字母换成下一个字母==，再接到 word 后面',
                 '例如 `"c"` → `"cd"`，`"zb"` → `"zbac"`（z 的下一个是 a）',
                 '操作足够多次后，返回 word 的第 `k` 个字符（`1 <= k <= 500`）',
                 '示例：`k = 5` → `"b"`；`k = 10` → `"c"`（本视频）'],
        quote='题目中k的范围较小，那么就可以==直接暴力模拟整个操作的过程直到字符串的长度大于等于k==，然后返回其中第k个字符即可。',
        quote_src='—— yiduobo 知乎题解',
        idea=['每一轮：遍历当前的每个字母，把它的下一个字母追加到末尾',
              '`chr((ord(c) - 97 + 1) % 26 + 97)`：`% 26` 处理 z → a',
              '长度每轮翻倍，至多 `log k` 轮；最后返回 `chars[k - 1]`'],
        result='返回 `"c"`：`"abbcbccdbc…"` 的第 10 个字符 ✓',
        summary=['时间 `O(k)`：最终长度不超过 `2k`；空间 `O(k)`',
                 '易错：`range(len(chars))` 在循环开始时就固定了，所以本轮只复制旧的部分',
                 '易错：返回 `chars[k - 1]`，下标从 0 开始',
                 '对比灵神 `O(1)`：答案就是 `a` + `k-1` 的二进制中 1 的个数',
                 '原文为 Python 2 风格：删去了文档字符串，代码未改'],
    ),
)

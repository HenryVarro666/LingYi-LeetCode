def _txt(S):
    if 's' not in S:
        return ''
    mx = S.get('mx'); mn = S.get('mn')
    a = f'最大 `mx` = =={mx}==' if mx is not None else ''
    b = f'最小 `mn` = =={mn}==' if mn is not None else ''
    return '　　'.join(x for x in (a, b) if x) or f'`num = {S["num"]}`，转成字符串 `s`'


CONFIG = dict(
    num=2566, title='替换一个数字后的最大差值', difficulty='Easy', category='贪心与思维',
    author='灵茶山艾府', technique='字符串贪心 · 最高位替换',
    tags=['灵神题单', '字符串贪心'],
    code='''
class Solution:
    def minMaxDifference(self, num: int) -> int:
        s = str(num)
        mx = num
        for c in s:
            if c != '9':  # 第一个不等于 9 的字符
                mx = int(s.replace(c, '9'))  # 替换成 9
                break
        mn = int(s.replace(s[0], '0'))  # 第一个不等于 0 的字符，替换成 0
        return mx - mn
''',
    call='Solution().minMaxDifference(11891)',
    expect=99009,
    views=[
        dict(type='text', fn=_txt, size=28),
        dict(type='string', var='s', label='s（黄 = 当前要整体替换的字符）', cell=90, h=200,
             color=lambda S, i, v: 'yellow' if 'c' in S and v == S['c'] else None),
    ],
    watch=['c', ('mx', 'mx', 'green'), ('mn', 'mn', 'pink')],
    captions={
        's = str': '`num = {num}` 转成字符串 `s = "{s}"`，方便按字符替换',
        'mx = num': '`mx` 先设为 `num`：万一全是 9，一个都不用换',
        'for c in s': '从左往右看字符 `c = {c}`',
        "if c != '9'": lambda S, B, r: (f"`c = '{S.c}'` ≠ `'9'` → ==第一个不是 9 的字符==，换成 9 最划算" if S.c != '9'
                                       else "`c` 已经是 `'9'`，换它没有收益，看下一个"),
        "mx = int": '把 `s` 里==所有== `{c}` 都换成 9 → `mx = {mx}`（前面的位变大，赢得最多）',
        'break': '最高的非 9 位已经处理，后面不必再看，退出循环',
        'mn = int': '`s[0]` 一定不是 0，把所有 `{s[0]}` 换成 0 → `mn = {mn}`',
        'return': '差值 `{mx} − {mn}` = =={ret}==',
    },
    cards=dict(
        one_liner='最大：第一个非 9 换成 9；最小：首位换成 0',
        complexity='时间 `O(log num)`，空间 `O(log num)`',
        problem=['把 `num` 的某个数字 `d1` 整体替换成 `d2`（所有 `d1` 一起换）',
                 '分别取替换后的最大值和最小值，求差',
                 '示例：`11891` → 最大 `99899`，最小 `890`，差 `99009`'],
        quote='从左到右找第一个不等于 9 的字符 c，把 s 中的 c 都替换成 9，得到最大数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['位越靠前权重越大，所以要把==最靠前的非 9 位==变成 9',
              '例：换后面的 `8` 只得到 `11991`，前面的 `1` 没变大，不如换 `1`',
              '最小同理，但首位非 0，直接把 `s[0]` 全换成 0 即可'],
        summary=['时间 `O(log num)`，空间 `O(log num)`',
                 '`replace` 会==替换所有==相同字符，符合题意',
                 '全是 9 时循环不触发，`mx` 保持 `num`，所以要先 `mx = num`',
                 '最小值允许前导 0，`int` 自动去掉'],
    ),
)

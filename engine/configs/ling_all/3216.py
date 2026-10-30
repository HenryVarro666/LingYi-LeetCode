def _txt(S):
    if 't' not in S:
        return '至多交换一次：交换的位置越靠左越好，且左边数字必须更大'
    if 'i' not in S:
        return '把字符串拆成列表 `t`，才能原地交换'
    return f"看相邻两位 `t[{S['i'] - 1}] = {S['t'][S['i'] - 1]}`、`t[{S['i']}] = {S['t'][S['i']]}`"


CONFIG = dict(
    num=3216, title='交换后字典序最小的字符串', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='从左到右找第一个逆序且同奇偶的相邻对',
    tags=['灵神题单', '难度分 1243'],
    code='''
class Solution:
    def getSmallestString(self, s: str) -> str:
        t = list(s)
        for i in range(1, len(t)):
            x, y = t[i - 1], t[i]
            if x > y and ord(x) % 2 == ord(y) % 2:
                t[i - 1], t[i] = y, x
                break
        return ''.join(t)
''',
    call='Solution().getSmallestString("2457320")',
    expect='2453720',
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='string', var='t', pointers={'i-1': 'blue', 'i': 'pink'}, window=('i-1', 'i'), label='t（蓝 = x，粉 = y）', h=240),
    ],
    watch=[('i', 'i', 'cyan'), ('x', 'x', 'blue'), ('y', 'y', 'pink')],
    captions={
        't = list(s)': '字符串不能原地改，先转成列表 `t`',
        'for i in range': '`i = {i}`：检查相邻的一对 `t[{i-1}]`、`t[{i}]`',
        'x, y = ': '`x = {x}`（左），`y = {y}`（右）',
        'if x > y': lambda S, B, r: (
            f'`{S["x"]} > {S["y"]}` 且奇偶相同 → ==换了字典序变小==，而且这是最靠左的一对' if S['x'] > S['y'] and ord(S['x']) % 2 == ord(S['y']) % 2
            else (f'`{S["x"]} <= {S["y"]}`：左边不更大，交换不会变小，跳过' if not S['x'] > S['y']
                  else f'`{S["x"]} > {S["y"]}` 但奇偶不同：不允许交换，跳过')),
        't[i - 1], t[i] = y, x': '交换：`t` 变成 `{"".join(t)}`',
        'break': '只能交换一次，而且越靠左收益越大：==立刻停止==',
        'return': '拼回字符串 `{"".join(t)}`',
    },
    cards=dict(
        one_liner='最靠左的「大换小」，且奇偶相同',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数字字符串 `s`，至多交换一次==相邻且奇偶相同==的两位',
                 '返回字典序最小的结果',
                 '本视频：`"2457320"` → `"2453720"`'],
        quote='交换的两个数字，左边必须大于右边，否则交换不会使字典序变小。交换的位置越靠左越好。',
        quote_src='—— 灵茶山艾府题解',
        idea=['字典序由左往右比：越靠左的位置变小，收益越大',
              '所以从左往右扫，第一对「左 > 右 且奇偶相同」就交换，然后 `break`',
              '字符的奇偶性 = ASCII 码的奇偶性，用 `ord(x) % 2` 判断'],
        summary=['时间 `O(n)`，空间 `O(n)`（列表 `t`）',
                 '易错点：要同时满足「左 > 右」和「奇偶相同」；交换后必须 `break`',
                 '没有可交换的对时原样返回',
                 '思考题：交换任意两位见 670. 最大交换'],
    ),
)

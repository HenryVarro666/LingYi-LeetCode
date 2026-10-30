S0 = 'dbaab*c*a*'


def _stacks(S):
    st = S.get('stacks')
    if st is None:
        return None
    return {chr(97 + k): v for k, v in enumerate(st) if v}


def _scolor(S, k, v):
    if S0[k] != '*' and v == '*':
        return 'red'
    if S0[k] == '*':
        return 'yellow' if S.get('i') == k else None
    if S.get('i') == k:
        return 'blue'
    return None


def _txt(S):
    mask = S.get('mask')
    if mask is None:
        return '`mask` 的第 c 位是 1 ⇔ 第 c 个栈非空；最低位的 1 对应==最小的字母=='
    low = (mask & -mask).bit_length() - 1 if mask else None
    m = format(mask, '08b')[-8:]
    return f'`mask` = `...{m}`（右起第 0 位是 a）' + (f'，最小的非空栈是 `{chr(97 + low)}`' if low is not None else '，所有栈都空')


CONFIG = dict(
    num=3170, title='删除星号以后字典序最小的字符串', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='26 个栈 + 位运算找最小字母',
    tags=['常用数据结构', '贪心与思维', '难度分 1772'],
    code='''
class Solution:
    def clearStars(self, s: str) -> str:
        s = list(s)
        stacks = [[] for _ in range(26)]
        mask = 0
        for i, c in enumerate(s):
            if c != '*':
                c = ord(c) - ord('a')
                stacks[c].append(i)
                mask |= 1 << c  # 标记第 c 个栈为非空
            else:
                lb = mask & -mask
                st = stacks[lb.bit_length() - 1]
                s[st.pop()] = '*'
                if not st:
                    mask ^= lb  # 标记栈为空
        return ''.join(c for c in s if c != '*')
''',
    call=f'Solution().clearStars({S0!r})',
    expect='dbbc',
    skip=['stacks = [[]', 'c = ord(c)'],
    max_steps=90,
    views=[
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='array', var='s', label='s（红 = 已被某个 * 删掉的字母；黄 = 当前的 *）', cell=70, h=190,
             pointers={'i': 'blue'}, color=_scolor, dim=lambda S, k, v: S0[k] == '*' and S.get('i', -1) != k),
        dict(type='map', var=_stacks, label='stacks（只显示非空的栈：字母 → 下标栈，栈顶在右）', h=330,
             fmt=lambda k, v: f"{k}: [{', '.join(map(str, v))}]"),
    ],
    watch=['i', ('c', 'c', 'blue'), ('mask', 'mask', 'cyan'), ('lb', 'lb', 'pink')],
    captions={
        's = list(s)': '把 `s` 变成列表：要删的字母不真删，而是==标记成 `*`==，避免最后排序',
        'mask = 0': '`mask` 用二进制记录哪些栈非空，开始全空 = 0',
        7: lambda S, B, r: (f'`{S.c}` 是字母：记下它的下标 `{S.i}`' if S.c != '*' else '遇到 `*`：要删掉左边==最小的字母=='),
        'stacks[c].append(i)': '字母编号 `c = {c}`（`a`=0 … `z`=25）；下标 `{i}` 入栈 `{chr(97+c)}`：同字母里==越靠右的越在栈顶==',
        'mask |= 1 << c': '`mask |= 1 << {c}`：第 {c} 位置 1，标记栈 `{chr(97+c)}` 非空 → `mask = {mask}`',
        'lb = mask & -mask': lambda S, B, r: f'`mask & -mask` 取最低位的 1 → `lb = {S.lb}`，它是第 `{S.lb.bit_length()-1}` 位 → 最小字母 ==`{chr(97 + S.lb.bit_length() - 1)}`==',
        'st = stacks': lambda S, B, r: f'取出字母 `{chr(97 + S.lb.bit_length() - 1)}` 的栈 `{S.st}`',
        "s[st.pop()] = '*'": lambda S, B, r: (f'弹出栈顶 `{B.st[-1]}`：同样是最小字母，==删最靠右的==，这样前面更多的小字母保留，字典序更小；`s[{B.st[-1]}]` 标记为 `*`'),
        'if not st': lambda S, B, r: ('这个栈空了' if not S.st else f'栈里还剩 `{S.st}`，还非空'),
        'mask ^= lb': '栈空了：`mask ^= lb` 把这一位清 0 → `mask = {mask}`',
        17: '去掉所有 `*`，剩下的字母连起来 = =={ret}==',
    },
    cards=dict(
        one_liner='最小字母有多个就删最靠右的，用 26 个栈 + mask 找最小',
        complexity='时间 `O(n + |Σ|)`，空间 `O(n + |Σ|)`',
        problem=['字符串 `s` 含小写字母和 `*`',
                 '每次删掉最左边的 `*` 和它左边==字典序最小==的一个字母（有多个可任选）',
                 '求删完所有 `*` 后字典序最小的字符串',
                 '本视频：`"dbaab*c*a*"` → `"dbbc"`'],
        quote='可以发现，如果去掉的字母靠左，那么会让更大的字母往左移，字典序更大；如果去掉的字母靠右，那么前面会保留更多更小的字母，字典序更小。核心思路：每次操作应当去掉最小字母中靠后的字母。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从左到右遍历，用 26 个栈记录每种字母出现过的下标，栈顶就是最靠右的',
              '遇到 `*`：弹最小字母那个栈的栈顶，把 `s` 里这个位置标成 `*`',
              '`mask` 记录哪些栈非空，`mask & -mask` 在 `O(1)` 内找到最小字母'],
        summary=['时间 `O(n + |Σ|)`，`|Σ| = 26`；写法一二逐个扫 26 个栈，是 `O(n|Σ|)`',
                 '写法一最后按下标排序（`O(n log n)`），写法二、三用 `*` 标记，省掉排序',
                 '易错：同一个字母删==靠右==的，删靠左会让更大的字母前移',
                 '易错：弹栈后栈变空要把 `mask` 对应位清 0',
                 '思考题：改成每次删最大字母，把 `mask & -mask` 换成取最高位即可'],
    ),
)

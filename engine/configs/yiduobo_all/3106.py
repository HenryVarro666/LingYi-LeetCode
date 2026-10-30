def _txt(S):
    if 'k' not in S:
        return ''
    base = f"剩余代价 `k = {S['k']}`"
    if 'dis' in S and 'char' in S and S['char'] != 'a':
        base += f"　　`{S['char']}` 到 `a` 的距离 `dis` = =={S['dis']}=="
    return base


CONFIG = dict(
    num=3106, title='满足距离约束且字典序最小的字符串', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='贪心 · 一趟遍历变 a',
    tags=['灵神题单', '贪心与思维', '难度分 1515'],
    code='''
class Solution(object):
    def getSmallestString(self, s, k):

        res = list(s)
        for index, char in enumerate(res):
            if char == 'a':
                continue
            
            dis = min(ord(char) - 97, 123 - ord(char))
            if dis <= k:
                k -= dis
                res[index] = 'a'
            else:
                res[index] = chr(ord(char) - k)
                break
        
        return ''.join(res)
''',
    call='Solution().getSmallestString("zbbz", 3)',
    expect='aaaz',
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='array', var='res', label='res（粉 = 当前字符 index）', cell=90, h=200,
             pointers={'index': 'pink'},
             color=lambda S, i, v: 'green' if v == 'a' and i < S.get('index', 0) else None),
    ],
    watch=['index', 'char', 'dis', ('k', 'k', 'green')],
    captions={
        'res = list': '复制成列表 `res`，边遍历边修改',
        'for index, char': '遍历到 `index = {index}`，字符 `{char}`',
        "if char == 'a'": lambda S, B, r: ("已经是 `a`，不用花代价，跳过" if S.char == 'a' else f"`{S.char}` 不是 `a`，需要计算代价"),
        'continue': '跳过这一位',
        'dis = min': '往回走 `{ord(char) - 97}`，或绕过 `z` 走 `{123 - ord(char)}` → 取小 `dis = {dis}`',
        'if dis <= k': lambda S, B, r: (f'`dis = {S.dis}` ≤ `k = {S.k}`：代价够，可以变成 `a`' if S.dis <= S.k
                                       else f'`dis = {S.dis}` > `k = {S.k}`：代价不够变成 `a`'),
        'k -= dis': '`k` 减去 `dis` → {k}',
        "res[index] = 'a'": '`res[{index}]` 变成 `a`',
        'chr(ord(char) - k)': '变不成 `a`，就尽量往前移 `k` 位：`{char}` → `{res[index]}`',
        'break': '`k` 已经消耗完，退出循环',
        'return': '拼成字符串 =={ret}==',
    },
    cards=dict(
        one_liner='让字符串的头部尽量向 a 靠拢，剩余代价耗在第一个变不成 a 的位置',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['花代价 `x` 可把字符改成字母表上距离为 `x` 的字符（`a` `z` 相邻）',
                 '总代价不超过 `k`，求字典序最小的结果',
                 '示例：`s = "zbbz"`，`k = 3` → `"aaaz"`'],
        quote='为了使得答案的字典序尽量小，那么就应该让字符串的头部尽量向字符\'a\'靠拢，于是可以一趟遍历，计算当前字符char与\'a\'的距离dis。',
        quote_src='—— yiduobo 题解原文',
        idea=['`dis` 取「往回走」和「绕 z 走」的较小者',
              '`dis <= k`：变成 `a`，并从 `k` 里扣掉 `dis`',
              '`dis > k`：变不成 `a`，就往前移 `k` 个字符；此时 `k` 耗尽，直接退出'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '字符 `a` 直接跳过，否则 `dis = 0` 也能走但多一步',
                 '`123 - ord(char)` 就是绕过 z 的距离（`z` 到 `a` 加一步）',
                 '对比灵神：灵神用 `map(ord, s)` 直接拿 ASCII，yiduobo 用 `ord(char)` 多算几次'],
    ),
)

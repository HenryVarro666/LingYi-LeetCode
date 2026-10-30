CONFIG = dict(
    num=2546, title='执行逐位运算使字符串相等', difficulty='Medium', category='位运算',
    author='yiduobo', technique='枚举操作结果 · 分别判断是否含 1',
    tags=['灵神题单·位运算', '灵神题单·贪心与思维', '难度分 1605'],
    code='''
class Solution(object):
    def makeStringsEqual(self, s, target):

        flag_s = False
        for char in s:
            if char == '1':
                flag_s = True
                break
        
        flag_target = False
        for char in target:
            if char == '1':
                flag_target = True
                break
        
        return flag_s == flag_target
''',
    call="Solution().makeStringsEqual('0110', '0001')",
    expect=True,
    views=[
        dict(type='string', var='s', label='s（绿 = 1）', h=190,
             color=lambda S, i, v: 'green' if v == '1' else None),
        dict(type='string', var='target', label='target（绿 = 1）', h=190,
             color=lambda S, i, v: 'green' if v == '1' else None),
        dict(type='text', size=32, h=110,
             fn=lambda S: f"flag_s = ==`{S['flag_s']}`==" + (f"　flag_target = ==`{S['flag_target']}`==" if 'flag_target' in S else '')),
        dict(type='text', size=26, h=130,
             fn=lambda S: '两个 0 → 还是 0、0；0 和 1 → 变成 1、1；两个 1 → 变成 1、0'),
    ],
    watch=[('flag_s', 'flag_s', 'blue'), ('flag_target', 'flag_target', 'pink'), ('char', 'char', 'yellow')],
    captions={
        "if char == '1'": lambda S, B, r: (f"`char = '{S.char}'` 是 1 → ==这个串里有 1=="
                                           if S.char == '1' else f"`char = '{S.char}'` 是 0 → 继续看下一位"),
        'for char in': '扫描下一个字符（循环到头就结束）',
        'flag_s = True': '`s` 里找到了 1：`flag_s = True`，不用再找了 → `break`',
        'flag_target = True': '`target` 里找到了 1：`flag_target = True`，不用再找了 → `break`',
        'flag_s = False': '先假设 `s` 里没有 1：`flag_s = False`',
        'flag_target = False': '先假设 `target` 里没有 1：`flag_target = False`',
        'return': '`flag_s = {flag_s}`，`flag_target = {flag_target}`：两边==同有 1 或同无 1== → 返回 {ret}',
    },
    cards=dict(
        one_liner='s 里有 1 就能变成任意含 1 的串，全 0 只能还是全 0',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二元串 `s` 每次选两个下标，`s[i]` 变成 `s[i] OR s[j]`，`s[j]` 变成 `s[i] XOR s[j]`',
                 '能否把 `s` 变成 `target`',
                 '本视频：`s = "0110"`，`target = "0001"` → `true`'],
        quote='只要s中存在1，那么就可以将s变为任意包含至少一个1的字符串，但无法变为全0的字符串。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把三种运算结果列出来：`00→00`，`01→11`，`11→10`',
              '有 1 就能扩散出更多 1，也能把 1 消到只剩一个；永远不能全消掉',
              '所以分别扫 `s` 和 `target`，记录各自有没有 1，再比较'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '用两个布尔变量分别记录，找到第一个 1 就 `break`',
                 '易错点：全 0 与含 1 的串之间不可互相转换',
                 '对比灵神：他一行 `\'1\' in s` 完成，yiduobo 手写两遍扫描'],
    ),
)

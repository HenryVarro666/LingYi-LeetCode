CONFIG = dict(
    num=3849, title='重新排列后的最大按位异或值', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='计数 + 高位优先填反值',
    tags=['灵神题单', '贪心与思维', '难度分 1556'],
    code='''
class Solution(object):
    def maximumXor(self, s, t):
        
        cnt = [0] * 2
        for c in t:
            cnt[int(c)] += 1
        
        res = []
        for c in s:
            c = int(c)
            target = int(c) ^ 1
            if cnt[target] > 0:
                cnt[target] -= 1
                res.append('1')
            else:
                cnt[c] -= 1
                res.append('0')
        
        return ''.join(res)
''',
    call="Solution().maximumXor('0110', '1110')",
    expect='1101',
    views=[
        dict(type='string', var='t', h=170, label='t（只统计 0/1 个数，顺序随便）',
             pointers={}),
        dict(type='array', var='cnt', h=170, label='cnt：t 里 [0 的个数, 1 的个数]（还没用掉的）',
             color=lambda S, i, v: ('yellow' if 'target' in S and i == S['target'] and S['_line'] >= 12 else None)),
        dict(type='string', var='s', h=170, label='s', pointers={}),
        dict(type='array', var='res', h=170, label='res：已确定的结果位',
             color=lambda S, i, v: 'green' if v == '1' else None),
    ],
    watch=[('c', 'c', 'cyan'), ('target', 'target', 'pink'), ('cnt', 'cnt', 'orange'), ('res', "''.join(res)", 'green')],
    captions={
        'cnt = [0] * 2': '`cnt[0]`、`cnt[1]`：t 里 0 和 1 各有多少',
        'for c in t': '取 t 的下一个字符去统计',
        'cnt[int(c)] += 1': '统计 t 的字符 `{c}`：`cnt = {cnt}`',
        'res = []': '`res` 按位收集结果，从高位开始',
        'for c in s': '取 s 的下一位（从高位开始，取完则结束）',
        'c = int(c)': '看 s 的这一位 `{c}`',
        'target = int(c) ^ 1': '想异或出 1，t 就得放和它不同的 `{target}`',
        'if cnt[target] > 0': lambda S, B, r: (f'还有 `{S.cnt[S.target]}` 个 `{S.target}` → 这位能得到 `1`'
                                                if S.cnt[S.target] > 0 else f'`{S.target}` 用完了 → 只能放相同的 `{S.c}`'),
        'cnt[target] -= 1': '放一个 `{target}`：`cnt = {cnt}`',
        "res.append('1')": '不同异或 → `1`：`res = {"".join(res)}`',
        'cnt[c] -= 1': '没得选，放一个相同的 `{c}`：`cnt = {cnt}`',
        "res.append('0')": '相同异或 → `0`：`res = {"".join(res)}`',
        'return': '得到最大异或值 `{"".join(res)}`',
    },
    cards=dict(
        one_liner='先数 t 里的 0 和 1，再从高位逐位填反值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给两个等长二进制串 `s`、`t`，`t` 可以任意重排',
                 '求 `s` 与重排后 `t` 异或的最大值',
                 '示例：`s="0110"`，`t="1110"` → `"1101"`'],
        quote='应该尽量让t在高位上的数字与s在高位上的数字不同。',
        quote_src='—— yiduobo 题解原文',
        idea=['结果要大，高位必须尽量是 `1`，也就是 t 与 s 这一位不同',
              '先扫 t 得到 0、1 的数目，重排就变成“从库存里取”',
              '扫 s：库存里有 `s[i]^1` 就取它，否则只能取相同的，结果位为 0'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '`target = c ^ 1` 即“需要的反值”，没有时退而取 `c`',
                 '易错点：取不到反值时也要扣 `cnt[c]`',
                 '对比灵神：灵神把 ans 原地覆盖在 s 的拷贝上；yiduobo 另开 res 列表追加'],
    ),
)

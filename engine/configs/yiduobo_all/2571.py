def _fn(S):
    if 'binary' not in S:
        return ''
    s = ''.join(map(str, S['binary']))
    return f"binary（低位在左）= `{s}`　　已操作 `res` = =={S.get('res', 0)}=="


CONFIG = dict(
    num=2571, title='将整数减少到零需要的最少操作数', difficulty='Medium', category='位运算',
    author='yiduobo', technique='低位到高位扫描二进制：落单减、连续加',
    tags=['灵神题单·位运算', '灵神题单·贪心与思维', '难度分 1649'],
    code='''
class Solution(object):
    def minOperations(self, n):

        binary = []
        while n:
            binary.append(n % 2)
            n //= 2
        
        p = 0
        res = 0
        while p < len(binary):
            while binary[p] == 0:
                p += 1
            
            if p + 1 < len(binary) and binary[p + 1] == 1:
                res += 1
                while p < len(binary) and binary[p] == 1:
                    p += 1
                
                if p == len(binary):
                    return res + 1
                else:
                    binary[p] = 1
            
            else:
                res += 1
                p += 1
        
        return res
''',
    call='Solution().minOperations(39)',
    expect=3,
    views=[
        dict(type='text', fn=_fn, size=30, h=80),
        dict(type='array', var='binary', pointers={'p': 'blue'}, label='binary（下标 = 二进制位，0 是最低位）', h=240,
             color=lambda S, i, v: 'green' if v == 1 else None),
    ],
    watch=[('p', "S.get('p')", 'blue'), ('res', "S.get('res')", 'green'), ('n', 'n', 'cyan')],
    captions={
        'binary.append': '把 `n` 的二进制从低位到高位存进 `binary`：末位 `{n % 2}`',
        'n //= 2': '右移一位：`n` = {n}',
        'p = 0': '`p` 从最低位开始向高位扫',
        'res = 0': '`res` 记录操作次数',
        'while p < len(binary):': lambda S, B, r: (f'`p = {S.p}` 还没扫完（共 {len(S.binary)} 位）' if S.p < len(S.binary) else '全部位扫完'),
        'while binary[p] == 0': lambda S, B, r: (f'`binary[{S.p}] = 0`：这一位是 0，不用管，跳到下一位' if S.binary[S.p] == 0 else f'`binary[{S.p}] = 1`：碰到一个 1，停下来看它的相邻位'),
        'p += 1': lambda S, B, r: (f'`p` → {S.p}（跳过 0 位）' if S['_line'] == 13 else f'连续的 1 往高位走，`p` → {S.p}' if S['_line'] == 18 else f'这个落单的 1 已减掉，`p` → {S.p}'),
        'if p + 1 < len': lambda S, B, r: (f'`binary[{S.p+1}] = 1`：相邻位也是 1，是连续的 1 → 在这里 ==加 1== 一次进位' if S.p + 1 < len(S.binary) and S.binary[S.p + 1] == 1
                                        else '相邻位是 0（或到头了）：落单的 1 → ==减 1== 最划算'),
        'res += 1': '做一次操作：`res` = =={res}==',
        'while p < len(binary) and binary[p] == 1': lambda S, B, r: (f'`binary[{S.p}] = 1`，还在这一段连续的 1 里' if S.p < len(S.binary) and S.binary[S.p] == 1 else '这一段连续的 1 因进位全部变 0，扫到段尾之后'),
        'if p == len': lambda S, B, r: ('进位出了最高位：新产生的 1 还要消一次' if S.p == len(S.binary) else f'进位落在第 {S.p} 位（原为 0）'),
        'return res + 1': '最后进位产生的那个 1 再减一次：`res + 1` = =={res + 1}==',
        'binary[p] = 1': '进位后这一位变成 1，下一轮循环会继续处理它：`binary[{p}] = 1`',
        'return res': '全部消完，共 =={res}== 次操作',
    },
    cards=dict(
        one_liner='落单的 1 减掉，连续的 1 在最低位加 1 一起进位',
        complexity='时间 `O(log n)`，空间 `O(log n)`',
        problem=['正整数 `n`，每次可以 ==加上或减去一个 2 的幂==',
                 '求把 `n` 变成 0 的最少操作数',
                 '示例：`39` → `3`'],
        quote='对于落单的1而言，如果选择减去1，只需1个操作就能将其消除，而如果选择加上1，其进位后又产生了新的1需要消除，这样是不划算的。',
        quote_src='—— yiduobo 题解原文',
        idea=['把 `n` 当成二进制位序列，每次操作 = 某一位 ±1',
              '为 0 的位不用动；落单的 1 减一次就没了',
              '连续的 1 在最低位加 1：一次进位全清零，只留下更高位的一个 1'],
        summary=['时间 `O(log n)`，空间 `O(log n)`（存二进制数组）',
                 '进位后把 `binary[p]` 置 1，后面的循环会接着处理它',
                 '连续 1 一直到最高位时，进位产生新的最高位，要 `return res + 1`',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`，并删去类型说明'],
    ),
)

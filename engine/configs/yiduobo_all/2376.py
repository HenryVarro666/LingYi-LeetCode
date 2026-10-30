CONFIG = dict(
    num=2376, title='统计特殊整数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='组合数学 · 逐位统计',
    tags=['灵神题单', '数位 DP', '难度分 2120'],
    code='''
class Solution(object):
    def countSpecialNumbers(self, n):

        l = 0
        tmp = n
        num_list = []
        while tmp:
            num_list.append(tmp % 10)
            tmp //= 10
            l += 1
        
        num_list.reverse()

        f = [0, 9]
        for index in range(2, l + 1):
            f.append(f[-1] * (11 - index))
        
        res = 0
        for index in range(l):
            res += f[index]
        
        used = set()
        possible = f[l] // 9
        for index, now in enumerate(num_list):
            if index == 0:
                res += (now - 1) * possible
            else:
                for num in range(now):
                    if num not in used:
                        res += possible
            
            if now in used:
                break
            
            used.add(now)
            possible //= (10 - index - 1)
            if index == l - 1:
                res += 1
        
        return res
''',
    call='Solution().countSpecialNumbers(135)',
    expect=110,
    views=[
        dict(type='array', var='num_list', label='num_list = n 的各位（高位在前）', cell=64, h=170,
             pointers={'index': 'blue'}, pointer_labels={'index': 'index'}),
        dict(type='array', var='f', label='f[i]：恰好 i 位的特殊整数个数', cell=84, h=160),
        dict(type='set', var='used', label='used：n 的前缀已经用过的数字', h=80),
        dict(type='text', h=50, fn=lambda S: f"`res` = =={S['res']}==" + (f"，`possible` = =={S['possible']}==" if 'possible' in S else '') if 'res' in S else ''),
    ],
    skip=['l = 0', 'tmp = n', 'num_list = []', 'l += 1', 'res = 0', 'used = set()'],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green'), ('possible', 'possible', 'yellow')],
    captions={
        'num_list.append': '取出个位，`num_list = {num_list}`',
        'tmp //= 10': '去掉最后一位 → `tmp = {tmp}`，位数 `l = {l}`',
        'num_list.reverse': '翻转成高位在前：`{num_list}`',
        'f = [0, 9]': '`f[1] = 9`：一位数 1~9 共 9 个（不含 0）',
        'f.append': '`f[{len(f)-1}] = f[{len(f)-2}] × (11 − {len(f)-1}) = {f[-1]}`：首位 9 种，之后每多一位少一种选择',
        'res += f[index]': '位数不足 `{l}` 位的特殊整数都小于 n：加上 `f[{index}] = {f[index]}`，`res = {res}`',
        'possible = f[l]': '`possible = f[{l}] // 9 = {possible}`：首位取 1~9 中任何一个，后面的方案数都相同',
        'for index, now': '处理第 `{index}` 位，`now = {now}`，已用 `{used}`',
        'if index == 0': lambda S, B, r: ('最高位：不能填 0，比 now 小的首位有 `now − 1` 个' if S.index == 0
                                          else f'非最高位：枚举比 `now = {S.now}` 小、且没用过的数字'),
        'res += (now - 1)': '首位比 `{now}` 小且 ≥ 1 的取法有 `{now-1}` 种，每种 `possible = {possible}` 个 → `res = {res}`',
        'for num in range(now)': '逐个检查比 `now = {now}` 小的数字',
        'if num not in used': lambda S, B, r: (f'`num = {S.num}` 没用过 → 可以填，后面随便填合法的' if S.num not in S.used
                                               else f'`num = {S.num}` 已在 used 里 → 重复，跳过'),
        'res += possible': '加上 `possible = {possible}` → `res = {res}`',
        'if now in used': lambda S, B, r: (f'`now = {S.now}` 已经出现过 → 以这个前缀开头的数都重复，==后面不用再看了== → break' if S.now in S.used
                                           else f'`now = {S.now}` 没出现过，n 的这个前缀还是合法的，继续'),
        'used.add': '`{now}` 记入 used',
        'possible //=': '确定一位后，后面少一位：`possible` → `{possible}`',
        'if index == l - 1': lambda S, B, r: ('走到最后一位都没重复 → n 本身也是特殊整数，`res += 1`' if S.index == S.l - 1
                                              else '还没到最后一位，继续'),
        'return res': '一共 `{res}` 个特殊整数',
    },
    cards=dict(
        one_liner='先加上位数更少的，再沿着 n 的前缀逐位数「比它小」的方案',
        complexity='时间 `O(log n)`，空间 `O(log n)`',
        problem=['每一位数字都互不相同的正整数叫特殊整数',
                 '求 `[1, n]` 中特殊整数个数',
                 '示例：`n = 20` → `19`；本视频：`n = 135` → `110`'],
        quote='对于本题，则可以基于简单的组合数学，用简单点的做法来做。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]` = 恰好 `i` 位的特殊整数个数，即 `9 × 9 × 8 × …`（先做 357 题）',
              '位数不足的全加上；同位数的，从最高位起逐位数出「这一位比 n 小」的方案',
              '前缀一旦出现重复数字就停；走到最后没重复则 n 自己也算一个'],
        summary=['时间 `O(log n)`，空间 `O(log n)`',
                 '易错点：最高位要从 1 开始，所以是 `(now − 1) × possible`',
                 '`possible` 每确定一位就除以剩余选择数，别忘了更新',
                 '原文为 Python 2 写法，`/` 做整数除法的 3 处已改为 `//`',
                 '对比灵神：他用 dfs + mask 记忆化，这里直接用排列数公式'],
    ),
)

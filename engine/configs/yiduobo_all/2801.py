def _lv(S):
    v = S['_inner'].get('level')
    if isinstance(v, int):
        return v if v < len(S['high']) else None
    return 0 if 'first' in S['_inner'] else None


def _info(S):
    I = S['_inner']
    names = ((4, '前导0'), (2, '贴上界'), (1, '贴下界'))
    if 'flag' in I and 'level' in I:
        fl = I['flag']
        on = ' '.join(n for b, n in names if fl & b) or '无'
        return f"level=`{I['level']}`  last=`{I['last']}`  flag=`{fl:03b}`（=={on}==）"
    if 'flag' in I:
        fl = I['flag']
        on = ' '.join(n for b, n in names if fl & b) or '无'
        return f"最高位 `first={I['first']}`  flag=`{fl:03b}`（=={on}==）"
    return 'flag 三位：4 前导 0 · 2 贴上界 high · 1 贴下界 low'


CONFIG = dict(
    num=2801, title='统计范围内的步进数字数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='数位 DP · 前导 0 + 上下界 flag',
    tags=['灵神题单', '数位 DP', '难度分 2367'],
    code='''
class Solution(object):
    def countSteppingNumbers(self, low, high):

        mod = 10 ** 9 + 7

        max_level = len(high)
        low = '0' * (max_level - len(low)) + low

        f = [[[None] * 8 for j in range(10)] for i in range(max_level)]
        res = 0

        def dfs(level, last, flag):
            if level == max_level:
                return 1
            
            if f[level][last][flag] is None:
                f[level][last][flag] = 0
                if flag & 4 == 4:
                    candidate = range(10)
                else:
                    candidate = []
                    if last > 0:
                        candidate.append(last - 1)
                    if last < 9:
                        candidate.append(last + 1)

                if flag & 1 == 1:
                    bottom = int(low[level])
                else:
                    bottom = 0
                    
                if flag & 2 == 2:
                    top = int(high[level])
                else:
                    top = 9

                for digit in candidate:
                    if digit < bottom or digit > top:
                        continue
                    new_flag = 0
                    if digit == bottom and (flag & 1 == 1):
                        new_flag |= 1
                    if digit == top and (flag & 2 == 2):
                        new_flag |= 2
                    if digit == 0 and (flag & 4 == 4):
                        new_flag |= 4
                    
                    f[level][last][flag] += dfs(level + 1, digit, new_flag)
                    if f[level][last][flag] >= mod:
                        f[level][last][flag] -= mod
            
            return f[level][last][flag]

        for first in range(int(low[0]), int(high[0]) + 1):
            flag = 0
            if first == int(low[0]):
                flag |= 1
            if first == int(high[0]):
                flag |= 2
            if first == 0:
                flag |= 4

            res += dfs(1, first, flag)
            if res >= mod:
                res -= mod
        
        return res
''',
    call='Solution().countSteppingNumbers("1", "11")',
    expect=10,
    views=[
        dict(type='text', fn=_info, h=80),
        dict(type='string', var='high', label='high = "11"（蓝箭头 = 当前位）', pointers={_lv: 'blue'},
             pointer_labels={_lv: 'level'}, cell=70, h=190),
        dict(type='string', var='low', label='low = "1"，补前导 0', pointers={_lv: 'pink'},
             pointer_labels={_lv: 'level'}, cell=70, h=190),
        dict(type='calls', hide=('f',), h=230),
    ],
    watch=[('level', "_inner.get('level')", 'blue'), ('last', "_inner.get('last')", 'pink'),
           ('flag', "_inner.get('flag')", 'purple'), ('bottom', "_inner.get('bottom')", 'cyan'),
           ('top', "_inner.get('top')", 'cyan'), ('res', 'res', 'green')],
    skip=[4, 10, 14, 17, 39, 40, 49, 50, 64, 65],
    max_steps=60,
    captions={
        'max_level = len': '要填的位数 = `high` 的长度 = `{max_level}`',
        "low = '0'": '`low` 补前导 0 成 `{low!r}`：这样每个位置上下界都能直接比',
        'f = [[[None]': '记忆化表 `f[level][last][flag]`，`None` = 还没算',
        'if level == max_level': lambda S, B, r: ('填满 `max_level` 位 → ==这是一个合法的步进数，返回 1==（不合法的路径早被剪掉了）'
                                                 if S['_inner']['level'] == S.max_level else '还有数位要填'),
        'is None': '这个状态没算过 → 现在算',
        'if flag & 4 == 4': lambda S, B, r: ('前导 0 状态：相邻差 1 的限制不生效，可以填 0~9' if S.flag & 4
                                             else f'非前导 0：这一位只能是 `last-1` 或 `last+1`（`last = {S.last}`）'),
        'candidate = range(10)': '候选数字 = 0~9',
        'candidate = []': '候选数字从空开始，按 `last ± 1` 添加',
        'candidate.append(last - 1)': '`last > 0` → 可以填 `last - 1 = {last - 1}`',
        'candidate.append(last + 1)': '`last < 9` → 可以填 `last + 1 = {last + 1}`',
        'bottom = int(low': '贴着下界：这一位不能小于 `low[level]` → `bottom = {bottom}`',
        'bottom = 0': '没贴下界：这一位从 0 起 → `bottom = 0`',
        'top = int(high': '贴着上界：这一位不能大于 `high[level]` → `top = {top}`',
        'top = 9': '没贴上界：这一位至多 9 → `top = 9`',
        'for digit in candidate': '候选集 `{candidate}`，当前 `digit = {digit}`',
        'if digit < bottom or digit > top': lambda S, B, r: (f'`digit = {S.digit}` 不在 `[{S.bottom}, {S.top}]` 里 → ==跳过==' if S.digit < S.bottom or S.digit > S.top
                                                              else f'`digit = {S.digit}` 在 `[{S.bottom}, {S.top}]` 里 → 可以填'),
        'new_flag |= 1': '`digit` 恰好等于下界这一位 → 下一位仍贴下界',
        'new_flag |= 2': '`digit` 恰好等于上界这一位 → 下一位仍贴上界',
        'new_flag |= 4': '前导 0 状态下又填了 0 → 仍是前导 0',
        'f[level][last][flag] += dfs': '填 `digit = {digit}`：递归算下一位（`last` 变成 `digit`），结果累加',
        'return f[level][last][flag]': '这个状态的方案数 `{ret}`，缓存后返回',
        'for first in range': '最高位不受「差 1」约束，单独枚举：`first` 从 `low[0]` 到 `high[0]`，当前 `first = {first}`',
        55: '每个最高位 `first` 重新算 `flag`',
        'if first == int(low': '`first` 等于 `low[0]`？{first == int(low[0])}',
        'if first == int(high': '`first` 等于 `high[0]`？{first == int(high[0])}',
        'if first == 0': '`first = 0` 说明最高位仍是前导 0（数比 `high` 短）',
        'res += dfs(1, first': '从第 1 位往下填：`dfs(1, first, flag)`，累加到 `res`',
        'return res': '步进数字一共 `{res}` 个',
    },
    cards=dict(
        one_liner='low 补前导 0 对齐 high，用 flag 三位记录前导 0 和上下界',
        complexity='时间 `O(n · 10 · 8 · 10)`，空间 `O(n · 10 · 8)`',
        problem=['相邻数位差的绝对值恰好是 1 的数叫步进数字，不能有前导 0',
                 '求 `[low, high]` 内步进数字的个数（字符串很长），结果模 `10^9+7`',
                 '示例：`low="1", high="11"` → `10`（1~9 和 10）'],
        quote='flag 在这里是一个 3 位的二进制数，其中最高位用来储存前导 0 的标记，而中间和最低位则分别表示当前构造的数是否与上界 high 以及下界 low 的前缀相同。',
        quote_src='—— yiduobo 题解原文',
        idea=['统一填成 `len(high)` 位：`low` 补前导 0，位数少的数靠「前导 0」标记表示',
              '前导 0 时无视差 1 限制，候选 0~9；否则候选只有 `last ± 1`',
              '最高位不受差 1 约束，所以单独枚举 `first`，再从第 1 位开始 `dfs`'],
        summary=['时间 `O(n · D² · 8)`，`n` 是 `high` 的长度',
                 '每次加法后立刻减 `mod`，避免溢出',
                 '易错点：`last = 0` 时只能填 1，`last = 9` 时只能填 8',
                 '对比灵神：灵神用 `is_num` 表示是否已填数字，yiduobo 把前导 0 塞进 flag'],
    ),
)

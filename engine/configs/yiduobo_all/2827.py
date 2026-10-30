def _lv(S):
    v = S['_inner'].get('level')
    return v if isinstance(v, int) and v < len(S['str_high']) else None


def _info(S):
    I = S['_inner']
    if 'flag' not in I:
        return '`f[level][diff][r][flag]`：diff 带偏移，max_level 表示差为 0'
    fl = I['flag']
    on = ' '.join(n for b, n in ((4, '前导0'), (2, '贴上界'), (1, '贴下界')) if fl & b) or '无'
    return (f"level=`{I['level']}`  diff=`{I['diff']}`（偏移后，=={S['max_level']}== 表示相等）  r=`{I['r']}`\n"
            f"flag=`{fl:03b}`（=={on}==）")


CONFIG = dict(
    num=2827, title='范围中美丽整数的数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='数位 DP · 3 位 flag + 预处理 10 的幂',
    tags=['灵神题单', '数位 DP', '难度分 2324'],
    code='''
class Solution(object):
    def numberOfBeautifulIntegers(self, low, high, k):

        str_high = str(high)
        max_level = len(str_high)
        str_low = str(low)
        str_low = '0' * (max_level - len(str_low)) + str_low

        now = 1
        r_list = []
        for index in range(max_level):
            r_list.append(now)
            now = now * 10 % k
        r_list.reverse()

        f = [[[[None] * 8 for _ in range(k)] for _ in range(max_level * 2 + 1)] for _ in range(max_level)]

        def dfs(level, diff, r, flag):
            if level == max_level:
                if diff == max_level and r == 0:
                    return 1
                else:
                    return 0

            if f[level][diff][r][flag] is None:
                f[level][diff][r][flag] = 0
                
                for digit in range(10):
                    if (flag & 2 == 2) and digit > int(str_high[level]):
                        continue
                    if (flag & 1 == 1) and digit < int(str_low[level]):
                        continue
                    
                    if digit == 0 and (flag & 4 == 4):
                        f[level][diff][r][flag] += dfs(level + 1, diff, r, 5)
                    else:
                        new_flag = 0
                        if (flag & 2 == 2) and digit == int(str_high[level]):
                            new_flag |= 2
                        if (flag & 1 == 1) and digit == int(str_low[level]):
                            new_flag |= 1
                        
                        new_diff = diff
                        if digit % 2 == 0:
                            new_diff += 1
                        else:
                            new_diff -= 1
                        
                        new_r = (r + r_list[level] * digit) % k

                        f[level][diff][r][flag] += dfs(level + 1, new_diff, new_r, new_flag)
                    
            
            return f[level][diff][r][flag]
        

        return dfs(0, max_level, 0, 7)
''',
    call='Solution().numberOfBeautifulIntegers(1, 10, 1)',
    expect=1,
    views=[
        dict(type='text', fn=_info, h=80),
        dict(type='string', var='str_high', label='high = 10（蓝箭头 = level）', pointers={_lv: 'blue'},
             pointer_labels={_lv: 'level'}, cell=70, h=190),
        dict(type='string', var='str_low', label='low = 1（补前导 0 对齐）', pointers={_lv: 'pink'},
             pointer_labels={_lv: 'level'}, cell=70, h=190),
        dict(type='calls', h=230),
    ],
    watch=[('level', "_inner.get('level')", 'blue'), ('diff', "_inner.get('diff')", 'pink'),
           ('r', "_inner.get('r')", 'orange'), ('flag', "_inner.get('flag')", 'purple'),
           ('digit', "_inner.get('digit')", 'cyan')],
    skip=[5, 6, 9, 10, 26, 28, 30, 32, 37, 43],
    max_steps=54,
    captions={
        'str_high = str': '`high` 转成字符串，长度 `max_level` 就是要填的位数',
        'str_low = ': '`low` 左边补 0，和 `high` 一样长（`{str_low}`）：补出来的 0 要靠前导 0 标记区分',
        'now = now * 10 % k': '`r_list` 存 `10^p % k`：第 `level` 位填 `digit` 实际贡献 `digit × 10^(后面位数)`',
        'r_list.reverse()': '反转后 `r_list[level]` 就是第 `level` 位的权重取模 = {r_list}',
        'f = [[[[None]': '记忆化表 `f[level][diff][r][flag]`，`None` = 还没算',
        'if level == max_level': lambda S, B, r: ('`level = max_level`：填完了，检查两个条件' if S['_inner']['level'] == S.max_level else '还有数位要填'),
        'if diff == max_level and r == 0': lambda S, B, r: (
            f"`diff={S.diff}`（偏移后{'等于' if S.diff == S.max_level else '不等于'} `max_level={S.max_level}`），`r={S.r}`："
            + ('奇偶数位一样多且被 `k` 整除 → ==返回 1==' if S.diff == S.max_level and S.r == 0
               else ('奇偶数位个数不等 → 返回 0' if S.diff != S.max_level else '余数不是 0，不能被 `k` 整除 → 返回 0'))),
        'is None': '这个状态还没算过 → 现在枚举这一位 `digit` 去算',
        'for digit in range': '枚举这一位填 `digit`（0~9）',
        'digit > int(str_high': lambda S, B, r: (
            f"枚举 `digit={S.digit}`：" + ('没贴上界，上界不限制' if not S.flag & 2 else
            ('贴着上界，超过 `high` 的这一位 → ==跳过==' if S.digit > int(S.str_high[S._inner['level']]) else '贴着上界，但没超过'))),
        'digit < int(str_low': lambda S, B, r: (
            f"`digit={S.digit}`：" + ('没贴下界，下界不限制' if not S.flag & 1 else
            ('贴着下界，比 `low` 的这一位小 → ==跳过==' if S.digit < int(S.str_low[S._inner['level']]) else '贴着下界，但没小于，可以填'))),
        'dfs(level + 1, diff, r, 5)': '前导 0 状态下填 0：不算数位，`diff`、`r` 都不变；`flag` 固定为 5（前导 0 + 贴下界）',
        'new_flag |= 2': '`digit` 恰好等于 `high` 这一位 → 仍贴上界',
        'new_flag |= 1': '`digit` 恰好等于 `low` 这一位 → 仍贴下界',
        'new_diff += 1': '偶数位：`diff` 加 1 → {new_diff}',
        'new_diff -= 1': '奇数位：`diff` 减 1 → {new_diff}',
        'new_r = ': '余数更新：`(r + r_list[level] × digit) % k` = =={new_r}==',
        'f[level][diff][r][flag] += dfs(level + 1, new_diff': '递归算下一位，结果累加到当前状态',
        'return f[level][diff][r][flag]': '这个状态的方案数 `{ret}`，缓存后返回',
        'return dfs(0': '入口：`diff = max_level`（偏移后表示差 0），`flag = 7` = 前导 0 + 贴上界 + 贴下界',
    },
    cards=dict(
        one_liner='把前导 0 做成状态位，10 的幂次预处理成取模权重',
        complexity='时间约 `O(n · n · k · 8 · 10)`，空间 `O(n² k · 8)`',
        problem=['奇数位与偶数位个数相同，且能被 `k` 整除的数是美丽整数',
                 '求 `[low, high]` 内美丽整数的个数',
                 '示例：`low=1, high=10, k=1` → `1`（只有 10）'],
        quote='前导0在本题中既不应该参与奇偶位数的计算，也不应该参与对k取模的计算，因此在这里需要一个标记来区分当前是否依然处于前导0的情况。',
        quote_src='—— yiduobo 题解原文',
        idea=['`low` 补前导 0 到和 `high` 一样长，一次填满 `max_level` 位',
              '`flag` 三位：前导 0、贴上界、贴下界；`diff` 加偏移避免负下标',
              '第 `level` 位填 `digit` 的余数贡献是 `digit × 10^p`，提前算好 `r_list`'],
        summary=['时间约 `O(n² k · 8 · 10)`，`n` 是 `high` 的位数',
                 '易错点：前导 0 不能算偶数位，所以单独走 `flag = 5` 的分支',
                 '`diff` 初值是 `max_level`，终点判断 `diff == max_level`',
                 '对比灵神：灵神拆成 `calc(high) - calc(low-1)`，yiduobo 同时贴上下界一次算完'],
    ),
)

CONFIG = dict(
    num=2147, title='分隔长廊的方案数', difficulty='Hard', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='乘法原理 · 相邻座位的空隙数',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·数学算法', '难度分 1915'],
    code='''
class Solution:
    def numberOfWays(self, corridor: str) -> int:
        MOD = 1_000_000_007
        ans = 1
        cnt_s = last_s = 0

        for i, ch in enumerate(corridor):
            if ch == 'S':
                cnt_s += 1
                # 对于第 3,5,7,... 个座位，可以在其到其左侧最近座位之间的任意空隙放置屏风
                if cnt_s >= 3 and cnt_s % 2:
                    ans = ans * (i - last_s) % MOD
                last_s = i  # 记录上一个座位的位置
 
        if cnt_s == 0 or cnt_s % 2:  # 座位个数不能为 0 或奇数
            return 0
        return ans
''',
    call='Solution().numberOfWays("SSPPSSPPPSS")',
    expect=12,
    views=[
        dict(type='string', var='corridor', pointers={'i': 'blue', 'last_s': 'pink'}, h=260, cell=70,
             color=lambda S, i, v: ('yellow' if i == S['i'] and v == 'S' else 'green' if v == 'S' and i <= S.get('i', -1) else None) if 'i' in S else None,
             dim=lambda S, i, v: v == 'P'),
        dict(type='text', h=90, size=34, fn=lambda S: (f"已见座位 `cnt_s` = =={S['cnt_s']}==，方案数 `ans` = =={S['ans']}==" if 'cnt_s' in S else '')),
    ],
    watch=['i', 'ch', ('cnt_s', 'cnt_s', 'blue'), ('last_s', 'last_s', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = 1': '`ans = 1`：方案数是各个屏风放法的乘积，先从 1 开始',
        'cnt_s = last_s = 0': '`cnt_s` 数座位，`last_s` 记上一个座位的下标',
        'if ch ==': lambda S, B, r: (f"`corridor[{S.i}] = 'S'` → 是座位" if S.ch == 'S' else f"`corridor[{S.i}] = 'P'` → 是植物，不影响方案，跳过"),
        'cnt_s += 1': '座位数 `cnt_s` → {cnt_s}',
        'if cnt_s >= 3': lambda S, B, r: (f"`cnt_s = {S.cnt_s}`：第 {S.cnt_s} 个座位是新一段的开头 → 前面一段已满，可以在它和上个座位之间放屏风" if S.cnt_s >= 3 and S.cnt_s % 2 else f"`cnt_s = {S.cnt_s}`：{'前两个座位必然在第一段里' if S.cnt_s < 3 else '偶数个座位：它是一段的第二个座位，段内不能放屏风'} → 不乘"),
        'ans = ans * (i - last_s)': '空隙数 = 下标差 `{i} - {last_s}` = =={i-last_s}==，屏风放法互相独立 → `ans = {B.ans} × {i-last_s}` = =={ans}==',
        'last_s = i': '记录这个座位的位置：`last_s = {i}`',
        'if cnt_s == 0 or': lambda S, B, r: (f"`cnt_s = {S.cnt_s}`：座位数为 {'0' if S.cnt_s == 0 else '奇数'} → 必有一段座位数不对，返回 0" if S.cnt_s == 0 or S.cnt_s % 2 else f"`cnt_s = {S.cnt_s}`：偶数个座位，可以两两分段"),
        'return ans': '方案数 `{ans}`（已对 `10^9+7` 取模）',
    },
    cards=dict(
        one_liner='相邻两段之间的屏风，可以放在两座位之间任一空隙，各段独立相乘',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`corridor` 由座位 `S` 和植物 `P` 组成，用屏风把走廊分段',
                 '每一段恰好有 ==2 个座位==，植物数不限；求划分方案数（模 `10^9+7`）',
                 '示例：`SSPPSPS` → `3`；本视频：`SSPPSSPPPSS` → `12`'],
        quote='对于第 3,5,7,… 个座位，可以在其到其左侧最近座位之间的任意空隙放置一个屏风，空隙个数为两个座位的下标之差。总的方案数为每个屏风的放法之积。',
        quote_src='—— 灵茶山艾府题解',
        idea=['座位按 2 个一组，第 2、3 个座位之间必须恰有一个屏风',
              '这个屏风有 `下标差` 种放法（挨着前面放 … 挨着后面放）',
              '各屏风互不影响，由==乘法原理==把放法数连乘；中途取模'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '座位数为 0 或奇数：直接返回 0',
                 '第 1、2 个座位之间不乘；只在 `cnt_s >= 3` 且为奇数时乘',
                 '取模放在每次乘法之后，`ans * (i - last_s) % MOD`',
                 '同类题：组合数学 · 乘法原理题单'],
    ),
)

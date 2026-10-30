CONFIG = dict(
    num=3541, title='找到频率最高的元音和辅音', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='元音位掩码 · 一遍统计',
    code='''
class Solution:
    def maxFreqSum(self, s: str) -> int:
        VOWEL_MASK = 0x104111
        cnt = [0] * 26
        max_cnt = [0] * 2
        for ch in s:
            ch = ord(ch) - ord('a')
            bit = VOWEL_MASK >> ch & 1
            cnt[ch] += 1
            max_cnt[bit] = max(max_cnt[bit], cnt[ch])
        return sum(max_cnt)
''',
    call="Solution().maxFreqSum('successes')",
    expect=6,
    views=[
        dict(type='string', var='s', label='s', cell=80, h=150, pointers={'sum(cnt) - (0 if _line <= 8 else 1)': 'blue'},
             pointer_labels={'sum(cnt) - (0 if _line <= 8 else 1)': 'ch'}),
        dict(type='array', var='cnt', label='cnt[0..25]：a 到 z 的出现次数', cell=36, h=170,
             pointers={'ch': 'pink'},
             color=lambda S, i, v: 'yellow' if v and i == S.get('ch') else None, dim=lambda S, i, v: v == 0),
        dict(type='array', var='max_cnt', label='max_cnt：[0] 辅音最大频率，[1] 元音最大频率', cell=110, h=170,
             pointers={'bit': 'orange'}),
    ],
    watch=['VOWEL_MASK', 'ch', 'bit', ('max_cnt', 'max_cnt', 'green')],
    captions={
        'VOWEL_MASK = ': '元音集合 `{{a,e,i,o,u}}` 压成整数：第 0、4、8、14、20 位为 1 → `0x104111`',
        'cnt = [0] * 26': '`cnt` 记录 26 个字母各出现几次',
        'max_cnt = [0] * 2': '`max_cnt[0]` 存辅音最大频率，`max_cnt[1]` 存元音最大频率',
        'for ch in s': lambda S, B, r: ('逐个字符处理' if 'ch' in S and isinstance(S.ch, str) else '遍历结束'),
        'ch = ord': '字母转成下标：`ch = {ch}`',
        'bit = ': lambda S, B, r: f'`VOWEL_MASK` 右移 `{S.ch}` 位取最低位：`bit = {S.bit}` → =={"元音" if S.bit else "辅音"}==',
        'cnt[ch] += 1': '这个字母出现次数 +1 → `cnt[{ch}] = {cnt[ch]}`',
        'max_cnt[bit] = max': '`max_cnt[{bit}] = max({B.max_cnt[bit]}, {cnt[ch]}) = {max_cnt[bit]}`：只在同类（元音/辅音）里比较',
        'return sum': '元音最大 + 辅音最大：`{max_cnt[1]} + {max_cnt[0]}` = =={sum(max_cnt)}==',
    },
    cards=dict(
        one_liner='一遍扫描：用位掩码判元音，元音辅音各自维护最大次数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['小写字符串 `s`，找出现次数最多的==元音==和最多的==辅音==',
                 '返回这两个频率之和；没有元音或辅音时该频率记 0',
                 '示例：`"successes"` → 元音 `e` 2 次 + 辅音 `s` 4 次 = `6`'],
        quote='可以用位运算快速判断字母是否在元音集合中。',
        quote_src='—— 灵茶山艾府题解（写法二）',
        idea=['元音集合 `{a,e,i,o,u}` 视作整数 `0x104111`，第 `c` 位为 1 表示字母 c 是元音',
              '`VOWEL_MASK >> ch & 1` 得到 `bit`，同时当作 `max_cnt` 的下标',
              '每统计一个字母，就更新所属类别的最大频率'],
        summary=['时间 `O(n)`，空间 `O(|Σ|)`，`|Σ| = 26`',
                 '易错：`ch` 先被重新赋值成下标，后面都按下标用',
                 '`max_cnt` 下标 0 是辅音、1 是元音，别记反',
                 '写法一用 `ch in "aeiou"` 判元音，思路相同；写法二先 `Counter` 再删掉元音，视频选掩码写法'],
    ),
)

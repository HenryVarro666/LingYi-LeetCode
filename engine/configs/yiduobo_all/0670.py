def _txt(S):
    if 'char_list' not in S:
        return ''
    if 'max_pos' in S:
        return f"`index = {S['index']}`：`{S['char_list'][S['index']]}` < `{S['char_list'][S['index']+1]}`，右边最大 `max_pos = {S['max_pos']}`（=={S['char_list'][S['max_pos']]}==）"
    return f"从高位往低位扫，找第一个比后一位小的位置"


CONFIG = dict(
    num=670, title='最大交换', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='贪心 · 先找升序处再找最大数',
    tags=['灵神题单', '贪心与思维'],
    code='''
class Solution(object):
    def maximumSwap(self, num):

        char_list = list(str(num))
        swap_pos = 0
        for index in range(len(char_list) - 1):
            if char_list[index] < char_list[index + 1]:
                max_pos = index + 1
                for pos in range(index + 2, len(char_list)):
                    if char_list[pos] >= char_list[max_pos]:
                        max_pos = pos

                for pos in range(0, index + 1):
                    if char_list[pos] < char_list[max_pos]:
                        char_list[pos], char_list[max_pos] = char_list[max_pos], char_list[pos]
                        break

                return int(''.join(char_list))
                  
        return num
''',
    call='Solution().maximumSwap(1993)',
    expect=9913,
    skip=['swap_pos = 0'],
    views=[
        dict(type='text', fn=_txt, size=26),
        dict(type='array', var='char_list', label='char_list（蓝 = max_pos，粉 = index，黄 = pos）', cell=90, h=230,
             pointers={'index': 'pink', 'max_pos': 'blue', 'pos': 'yellow'}),
    ],
    watch=[('index', 'index', 'pink'), ('max_pos', 'max_pos', 'blue'), ('pos', 'pos', 'yellow')],
    captions={
        'char_list = list': '把 `num` 拆成字符列表 `{char_list}`',
        'for index in range': '从高位往低位看 `index = {index}`',
        'if char_list[index] < char_list[index + 1]': lambda S, B, r: (
            f"`{S.char_list[S.index]}` < `{S.char_list[S.index+1]}`：高位比低位小 → 后面一定有更大的数可以换上来" if S.char_list[S.index] < S.char_list[S.index+1]
            else f"`{S.char_list[S.index]}` ≥ `{S.char_list[S.index+1]}`：目前还是降序，继续往后"),
        'max_pos = index + 1': '先假设 `index + 1` 是最大的：`max_pos = {max_pos}`',
        'for pos in range(index + 2': lambda S, B, r: ('后面的数扫完了，最大数在 `max_pos = %d`' % S.max_pos if B.get('pos') == S.get('pos') else f'继续扫后面的数 `pos = {S.pos}`'),
        'if char_list[pos] >= char_list[max_pos]': lambda S, B, r: (
            f"`{S.char_list[S.pos]}` ≥ `{S.char_list[S.max_pos]}` → 更新（==相等也更新==，取靠后的）" if S.char_list[S.pos] >= S.char_list[S.max_pos]
            else f"`{S.char_list[S.pos]}` < `{S.char_list[S.max_pos]}`，不更新"),
        'max_pos = pos': '`max_pos` → {max_pos}',
        'for pos in range(0, index + 1)': '从最高位起，找第一个比最大数小的位置 `pos = {pos}`',
        'if char_list[pos] < char_list[max_pos]': lambda S, B, r: (
            f"`{S.char_list[S.pos]}` < `{S.char_list[S.max_pos]}` → 就是它，换成最大数" if S.char_list[S.pos] < S.char_list[S.max_pos]
            else f"`{S.char_list[S.pos]}` 不比最大数小，换了没用，看下一位"),
        'char_list[pos], char_list[max_pos] =': '交换 `pos = {pos}` 和 `max_pos = {max_pos}` → `{"".join(char_list)}`',
        'break': '换完一次就够了',
        'return int': '拼回数字 =={ret}==',
        'return num': '整个数字是降序，已经最大，直接返回 `num`',
    },
    cards=dict(
        one_liner='找到第一处「前小后大」，再把高位最小的换成后面的最大数',
        complexity='时间 `O(log^2 num)`，空间 `O(log num)`',
        problem=['最多交换一次数字的任意两位，求最大值',
                 '示例：`2736` → `7236`；`9973` → `9973`',
                 '本视频：`1993` → `9913`'],
        quote='若高位上的数比后面的数要小，那么交换二者就能得到更大的数。相同大小的话就取位置更靠后的那一个。',
        quote_src='—— yiduobo 题解原文',
        idea=['从高位扫，遇到 `num[index] < num[index+1]`，说明后面有数比它大',
              '在 `index+1` 之后找最大数，并列取==最靠后==的，记为 `max_pos`',
              '再从最高位往后找第一个比它小的位置，交换即答案；一直降序则不用换'],
        summary=['最多 `O(n^2)`，位数只有 9 位，足够',
                 '找最大数用 `>=`，保证并列时取最后一个：`1993` 换成 `9913` 而非 `9193`',
                 '交换位置要从==最高位==开始找，而不是只换 `index`',
                 '对比灵神：灵神倒序一遍扫完，yiduobo 分三步找，更直观'],
    ),
)

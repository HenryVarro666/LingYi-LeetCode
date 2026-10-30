CONFIG = dict(
    num=869, title='重新排序得到 2 的幂', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='枚举同位数的 2 的幂，比较数位计数', tags=['难度分 1505'],
    code='''
class Solution(object):
    def reorderedPowerOf2(self, N):

        now = 1
        cnt_dict = {}
        length = 0
        while N:
            num = N % 10
            N //= 10
            length += 1
            cnt_dict[num] = cnt_dict.get(num, 0) + 1

        while len(str(now)) <= length:
            if len(str(now)) == length:
                tmp_cnt_dict = {}
                tmp = now
                while tmp:
                    num = tmp % 10
                    tmp //= 10
                    tmp_cnt_dict[num] = tmp_cnt_dict.get(num, 0) + 1
                if cnt_dict == tmp_cnt_dict:
                    return True

            now += now

        return False
''',
    call='Solution().reorderedPowerOf2(46)',
    expect=True,
    views=[
        dict(type='text', fn=lambda S: f"位数 `length` = =={S.get('length', 0)}==；当前枚举的 2 的幂 `now` = =={S.get('now', '')}==", h=60),
        dict(type='map', var='cnt_dict', fmt=lambda k, v: f'数字 {k} 出现 {v} 次', h=200, label='cnt_dict：N 的数位计数'),
        dict(type='map', var='tmp_cnt_dict', fmt=lambda k, v: f'数字 {k} 出现 {v} 次', h=200, label='tmp_cnt_dict：now 的数位计数'),
    ],
    watch=['length', 'now', ('same', "'tmp_cnt_dict' in dir() and tmp_cnt_dict == cnt_dict", 'green')],
    captions={
        'num = N % 10': '取出 N 的最低位 `{num}`',
        'cnt_dict[num] = cnt_dict.get(num, 0) + 1': '数字 `{num}` 的计数 → `{cnt_dict[num]}`',
        'while len(str(now)) <= length': lambda S, B, r: f'`now = {S.now}` 有 {len(str(S.now))} 位，{"不超过" if len(str(S.now)) <= S.length else "超过了"} `length = {S.length}` → {"继续枚举" if len(str(S.now)) <= S.length else "枚举完毕，没有找到"}',
        'if len(str(now)) == length': lambda S, B, r: f'`now = {S.now}` 的位数 {"等于" if len(str(S.now)) == S.length else "不等于"} `{S.length}`' + ('，值得比较' if len(str(S.now)) == S.length else '，位数不同直接跳过'),
        'tmp_cnt_dict[num] = ': '`now` 的数字 `{num}` 计数 → `{tmp_cnt_dict[num]}`',
        'if cnt_dict == tmp_cnt_dict': lambda S, B, r: '两个数位构成完全一致 → ==能重排成 now==' if S.cnt_dict == S.tmp_cnt_dict else f'`{S.now}` 的数位构成和 N 不同',
        'now += now': '`now` 翻倍：`{B.now}` → `{now}`（下一个 2 的幂）',
        'return True': '`{now}` 的数位构成与 N 一致 → ==返回 True==',
    },
    cards=dict(
        one_liner='只看数位构成：枚举同位数的 2 的幂，逐个比对',
        complexity='时间 `O(log N)` 量级（同位数的 2 的幂至多 4 个），空间 `O(1)`',
        problem=['把正整数 `N` 的数位任意重排（不能有前导零），能否得到 2 的幂',
                 '示例：`N = 1` → `true`；`N = 10` → `false`',
                 '本视频：`N = 46`，重排为 `64` → `true`'],
        quote='由于在这里可以任意交换N中各位数字，因此我们只需要判断是否存在2的幂，其各个位置上的数字构成与N的各位数字一致。',
        quote_src='—— yiduobo 题解原文',
        idea=['先数出 N 的位数 `L` 和每个数字出现的次数',
              '从 1 开始不断翻倍，只看位数恰为 `L` 的 2 的幂',
              '数位计数字典相等就说明能重排得到；位数超过 L 就停'],
        summary=['时间约 `O(log N)`，空间 `O(1)`',
                 '位数相同才比较，相同位数的 2 的幂至多 4 个',
                 '字典比较与数位顺序无关，所以等价于“能否重排”',
                 '原文为 Python 2 写法，整数除法 `N /= 10`、`tmp /= 10` 已改为 `//=`',
                 '对比灵神：灵神预处理排序后的字符串集合；yiduobo 现场枚举并比较数位计数'],
    ),
)

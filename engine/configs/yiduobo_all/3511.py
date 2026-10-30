CONFIG = dict(
    num=3511, title='构造正数组', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀和 · 截断重算',
    code='''
class Solution(object):
    def makeArrayPositive(self, nums):
        
        s = [0]
        left = 0
        res = 0
        ma = 0
        for index, v in enumerate(nums):
            s.append(s[-1] + v)
            if index - left + 1>= 3 and ma >= s[-1]:
                res += 1
                ma = 0
                s[-1] = 0
                left = index + 1
            elif index >= left + 1:
                ma = max(ma, s[-3])

        return res
''',
    call='Solution().makeArrayPositive([1,-2,-3,4,1,-5,2,-6])',
    expect=2,
    views=[
        dict(type='array', var='nums', pointers={'left': 'blue', 'index': 'pink'}, window=('left', 'index'), h=230,
             label='nums（蓝框 = 当前段 left..index）',
             dim=lambda S, i, v: 'left' in S and i < S['left']),
        dict(type='array', var='s', pointers={}, h=200, label='s（前缀和；被截断的位置重置为 0）',
             color=lambda S, i, v: 'green' if i == len(S['s']) - 1 else None),
        dict(type='text', h=90, fn=lambda S: (f"最大的候选前缀 `ma` = =={S['ma']}==，当前前缀 `s[-1]` = =={S['s'][-1]}==" if 's' in S else '')),
    ],
    watch=[('left', 'left', 'blue'), ('index', 'index', 'pink'), ('ma', 'ma', 'cyan'), ('res', 'res', 'green')],
    captions={
        's = [0]': '前缀和数组，开头放 `0` 表示空前缀',
        'left = 0': '`left`：当前这一段的起点，截断之后会往后挪',
        'res = 0': '`res` 统计需要改几个元素',
        7: '`ma`：能和当前位置组成长度 ≥ 3 子数组的前缀里，最大的那个',
        's.append': '前缀和：`s[-1] = {s[-2]} + {v} = {s[-1]}`',
        'if index - left': lambda S, B, r: (f"段长 `{S.index - S.left + 1}`，`ma = {S.ma}` {'≥' if S.ma >= S.s[-1] else '<'} `s[-1] = {S.s[-1]}`"
                                            + ('：最大前缀不小于当前前缀 → 某个长度 ≥ 3 的子数组和 ≤ 0，==必须改一个元素==' if S.index - S.left + 1 >= 3 and S.ma >= S.s[-1]
                                               else '：段还不到 3 个元素，不用判断' if S.index - S.left + 1 < 3 else '：最大前缀比当前前缀小 → 所有长度 ≥ 3 的子数组和都为正，不用改')),
        'res += 1': '改掉当前元素：`res` → {res}（改成 10^18，很大的正数）',
        12: '改成大数后，前面的部分截断，`ma` 清零重新统计',
        's[-1] = 0': '截断后从 0 重新算前缀和：`s[-1] = 0`，不用真的加 10^18',
        'left = index + 1': '新的一段从 `index + 1` 开始：`left` → {left}',
        'elif index >= left + 1': lambda S, B, r: ('段内已有 ≥ 2 个元素，`s[-3]` 是可收录的前缀' if S.index >= S.left + 1 else '段内才 1 个元素，没有 `s[-3]` 可收录，跳过'),
        'ma = max': '`ma = max({B.ma}, s[-3] = {s[-3]}) = {ma}`：只收录和当前下标隔至少 2 位的前缀',
        'return res': '一共需要修改 `{res}` 次',
    },
    cards=dict(
        one_liner='长度 ≥ 3 的子数组和必须为正，等价于“隔 2 位以上的前缀和只能升”',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['数组 `nums`，要求所有长度 ≥ 3 的子数组之和都 `> 0`',
                 '每次操作可把任意一个元素改成 `[-10^18, 10^18]` 内的整数',
                 '求最少操作次数；本视频：`[1,-2,-3,4,1,-5,2,-6]` → `2`'],
        quote='若在s[0]到s[index - 3]之间存在某个前缀和s[p]，其大于s[index]，那么从p + 1到index这一段的子数组和必然小于0，此时就需要将s[index]修改为10^18。',
        quote_src='—— yiduobo 题解原文',
        idea=['子数组和 = 两个前缀和之差，所以只看 `ma` 和 `s[-1]` 的大小',
              '一旦要改，就把当前位置改成极大值，==前面全部截断，从 0 重新算==',
              '用 `left` 记录段起点：段长 ≥ 3 才判断，段内 ≥ 2 个元素才更新 `ma`'],
        summary=['时间 `O(n)`，空间 `O(n)`（`s` 一直在增长）',
                 '易错点：`ma >= s[-1]` 带等号，因为要求和严格 `> 0`',
                 '改完后 `ma`、`s[-1]`、`left` 三个量要一起重置',
                 '原文题面里“超过两个元素”指长度 ≥ 3',
                 '代码原文即为 Python 3 可运行写法，未做修改'],
    ),
)

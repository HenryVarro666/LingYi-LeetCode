def _in_shuffle(S):
    return 'index' in S and 12 <= S.get('_line', 0) <= 14


def _col(S, i, v):
    if not _in_shuffle(S):
        return None
    if i == S.get('pos') and S.get('_line') in (13, 14):
        return 'pink'
    if i < S['index'] or (S.get('_line') == 14 and i == S['index']):
        return 'green'
    return None


def _info(S):
    if not _in_shuffle(S):
        return '洗牌：从左往右，每个位置从「自己 + 右边所有数」里随机选一个换过来'
    n = len(S['self.now'])
    k = S['index']
    return (f"第 `{k}` 轮：从下标 `{k}..{n - 1}` 这 `{n - k}` 个数里等概率选一个放到位置 `{k}`，"
            f"每个数概率 =={'1' if n - k == 1 else f'1/{n - k}'}==")


CONFIG = dict(
    num=384, title='打乱数组', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='Fisher-Yates 洗牌算法',
    tags=['labuladong', '灵神题单·数学算法'],
    code='''
class Solution(object):

    def __init__(self, nums):
        self.original = nums[:]
        self.now = nums[:]

    def reset(self):
        self.now = self.original[:]
        return self.now

    def shuffle(self):
        for index in range(len(self.now) - 1):
            pos = random.randint(index, len(self.now) - 1)
            self.now[index], self.now[pos] = self.now[pos], self.now[index]

        return self.now
''',
    setup='import random\nrandom.seed(0)',
    call='''s = Solution([1, 2, 3, 4, 5])
[list(s.shuffle()), list(s.reset()), list(s.shuffle())]''',
    expect=[[4, 5, 3, 2, 1], [1, 2, 3, 4, 5], [5, 1, 4, 2, 3]],
    views=[
        dict(type='text', fn=_info, size=24, h=110, lines=2),
        dict(type='array', var='self.now', cell=110, h=300,
             label='self.now（绿 = 已经定下来的位置，青框 = 本轮候选范围，粉 = 抽中的 pos）',
             pointers={'index': 'yellow', 'pos': 'pink'}, color=_col,
             window=(lambda S: S['index'] if _in_shuffle(S) else None,
                     lambda S: len(S['self.now']) - 1 if _in_shuffle(S) else None)),
        dict(type='array', var='self.original', cell=80, h=170, label='self.original（原始数组的备份，reset 用）', index=False),
    ],
    watch=[('index', 'index', 'yellow'), ('pos', 'pos', 'pink')],
    captions={
        'self.original = nums[:]': '备份原数组：`original = {self.original}`（==拷贝==，不是引用）',
        'self.now = nums[:]': '`now`：当前被打乱的数组',
        'self.now = self.original[:]': '`reset()`：用备份的拷贝恢复 `now = {self.now}`',
        'return self.now': lambda S, B, r: f'返回 `{r}`',
        'for index in range(len(self.now) - 1)': lambda S, B, r: (
            f'最后一个位置只剩 1 个数可选，不用再换 → 洗牌结束' if 'index' in B and B['index'] == S.index
            else f'第 `{S.index}` 轮：处理位置 `{S.index}`，前 {S.index} 个位置已经定好'),
        'pos = random.randint': '在 `[{index}, {len(self.now) - 1}]` 里随机：`pos = {pos}`（概率 `1/{len(self.now) - index}`）',
        'self.now[index], self.now[pos]': lambda S, B, r: (
            f'`pos = index = {S.pos}`：自己换自己，`{S.self.now[S.index]}` 留在原地' if S.pos == S.index
            else f'交换位置 `{S.index}` 和 `{S.pos}`：`{S.self.now[S.index]}` 定在位置 {S.index}'),
    },
    cards=dict(
        one_liner='每一轮从剩下的数里等概率挑一个放到当前位置',
        complexity='`shuffle`、`reset` 均为 `O(n)`；空间 `O(n)`',
        problem=['给整数数组 `nums`，实现 `shuffle()`：返回随机打乱后的数组，==所有排列等概率==',
                 '`reset()`：把数组恢复成初始状态并返回',
                 '本视频：`[1,2,3,4,5]` 依次 `shuffle` → `reset` → `shuffle`（固定随机种子）'],
        quote='到了这里，就得到了一种做法：==从左往右一趟扫描，每次随机选择当前位置或当前位置右侧的某一个数与当前位置进行交换==即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['剩 `n−k` 个数时，它们前 `k` 轮都没被选中的概率 = `(n−k)/n`',
              '本轮要让每个数以总概率 `1/n` 落到位置 `k`：`(1/n) ÷ ((n−k)/n) = 1/(n−k)`',
              '恰好就是==从剩下的 n−k 个数里等概率随机选一个=='],
        summary=['时间 `O(n)`，空间 `O(n)`（保存原数组）',
                 '易错：随机范围是 `[index, n−1]`，==包含 index 自己==；写成 `[0, n−1]` 会导致排列不等概率',
                 '易错：`original` 要存拷贝 `nums[:]`，否则打乱时原数组也被改掉',
                 '原文为 Python 2 写法：删去了 `:rtype` 文档字符串；演示中补上 `import random` 并固定随机种子'],
    ),
)

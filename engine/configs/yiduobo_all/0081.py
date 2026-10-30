NUMS = [2, 5, 6, 0, 0, 1, 2]


CONFIG = dict(
    num=81, title='搜索旋转排序数组 II', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='有重复就放弃二分 · 线性扫描',
    tags=['labuladong', '灵神题单·二分算法'],
    code='''
class Solution(object):
    def search(self, nums, target):

        for num in nums:
            if num == target:
                return True

        return False
''',
    # 演示用：让 nums 记住 for 循环当前走到的下标（仅用于画图，不影响题解代码）
    setup='''
class Arr(list):
    pos = -1
    frozen = False
    def __iter__(self):
        if self.frozen:
            return list.__iter__(self)
        return self._walk()
    def _walk(self):
        for i in range(len(self)):
            self.pos = i
            yield self[i]
        self.pos = len(self)
    def __deepcopy__(self, memo):
        c = Arr(list.__iter__(self))
        c.pos, c.frozen = self.pos, True
        return c
''',
    call=f'[Solution().search(Arr({NUMS}), 0), Solution().search(Arr({NUMS}), 3)]',
    expect=[True, False],
    views=[
        dict(type='text', size=26, h=80,
             fn=lambda S: f"`target = {S['target']}`：从左到右逐个比较" if 'target' in S else ''),
        dict(type='custom', h=330, draw=lambda cv, S, B, box, T: _draw(cv, S, B, box, T)),
        dict(type='text', size=24, h=150,
             fn=lambda S: '为什么不二分？`[0,0,0,0,0,0,1]` 旋转成 `[0,1,0,0,0,0,0]` 后，'
                          '首、中、尾==全是 0==，判断不出哪一半被旋转过'),
    ],
    watch=[('target', 'target', 'green'), ('num', 'num', 'yellow')],
    captions={
        'for num in nums': lambda S, B, r: ('所有数都比较完了，循环结束' if S.nums.pos >= len(S.nums)
                                         else f'取第 {S.nums.pos} 个数 `num = {S.num}`'),
        'if num == target': lambda S, B, r: (f'`{S.num} == {S.target}` → 找到了！' if S.num == S.target
                                             else f'`{S.num} ≠ {S.target}`，继续往后看'),
        'return True': '数组里有 `{target}` → 返回 ==True==',
        'return False': '整个数组扫完都没有 `{target}` → 返回 ==False==',
    },
    cards=dict(
        one_liner='有了重复数字，二分时分不清哪半边被旋转过 —— 那就老老实实扫一遍',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['非降序数组（==可能有重复==）在某处旋转后得到 `nums`，判断 `target` 是否在其中',
                 '示例：`nums = [2,5,6,0,0,1,2]`，`target = 0` → `true`；`target = 3` → `false`',
                 '本视频依次演示这两个 target'],
        quote='例如[0, 0, 0, 0, 0, 0, 1]这个数组，旋转成[0, 1, 0, 0, 0, 0, 0]之后，此时进行二分会发现==二分的边界全都是0==，根本无从判断那个部分是经历过旋转操作的。',
        quote_src='—— yiduobo 题解原文',
        idea=['33 题（无重复）靠比较边界判断「哪一半有序」来二分',
              '有重复时边界可能全相等，这条路断了 → 最坏情况下==最优就是 O(n)==',
              '既然如此，直接一趟扫描判断即可'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 'yiduobo 的结论：这题考的是==思路的变化==——重复元素让二分最坏退化成线性',
                 '对比灵神：仍然二分，遇到 `nums[mid] == nums[right]` 就 `right -= 1`，平均更快、最坏同为 `O(n)`',
                 '原文为 Python 2 风格，代码无需改动即可在 Python 3 运行'],
    ),
)


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), 'nums（暗 = 已比较过且不相等，黄 = 正在比较，绿 = 找到）', 24, T['muted'], bold=True)
    nums = S.get('nums', NUMS)
    n = len(nums)
    cell = min(100, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    ys = y0 + 70
    ch = cell * 0.9
    # 当前 num 的位置：用这次调用里已经执行的 for 行次数推算（num 没有下标）
    k = getattr(nums, 'pos', -1)
    k = None if k < 0 else k
    for i, v in enumerate(nums):
        X = sx + i * cell
        fill, tc = T['panel2'], T['text']
        if k is not None:
            if i < k or (k == n):
                fill, tc = (40, 45, 53), T['dim']
            elif i == k:
                fill, tc = (T['green'] if v == S.get('target') else T['yellow']), T['bg']
        cv.rect((X + 5, ys, X + cell - 5, ys + ch), fill=fill, r=8, outline=T['border'])
        cv.text((X + cell / 2, ys + ch / 2), v, 34, tc, anchor='mm', bold=True)
        cv.text((X + cell / 2, ys + ch + 6), i, 18, T['dim'], anchor='mt', mono=True)
    if k is not None and k < n:
        X = sx + k * cell + cell / 2
        cv.tri_up(X, ys + ch + 40, 10, T['yellow'])
        cv.text((X, ys + ch + 62), 'num', 22, T['yellow'], anchor='mt', bold=True)

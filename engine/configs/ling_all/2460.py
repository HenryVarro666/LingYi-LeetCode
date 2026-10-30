CONFIG = dict(
    num=2460, title='对数组执行操作', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='原地合并 + 非零前移', tags=['灵神题单'],
    code='''
class Solution:
    def applyOperations(self, a: List[int]) -> List[int]:
        j, n = 0, len(a)
        for i in range(n - 1):
            if a[i]:
                if a[i] == a[i + 1]:
                    a[i] *= 2
                    a[i + 1] = 0
                a[j] = a[i]  # 非零数字排在前面
                j += 1
        if a[-1]:
            a[j] = a[-1]
            j += 1
        for i in range(j, n):
            a[i] = 0
        return a
''',
    call='Solution().applyOperations([1,2,2,1,1,0,3])',
    expect=[1, 4, 2, 3, 0, 0, 0],
    views=[
        dict(type='array', var='a', pointers={'i': 'blue', 'j': 'pink'}, h=300,
             label='a（蓝 i = 正在处理，粉 j = 下一个非零要放的位置）',
             dim=lambda S, k, v: v == 0,
             color=lambda S, k, v: 'green' if ('j' in S and k < S['j'] and v != 0) else None),
        dict(type='text', size=28, fn=lambda S: (f"已经排好的非零数：前 `{S['j']}` 个" if 'j' in S else '')),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink')],
    captions={
        'j, n = 0': '`j` 指向「下一个非零数该放的位置」，一开始是 0',
        'for i in range(n - 1)': lambda S, B, r: (f'处理第 `{S.i}` 步操作，比较 `a[{S.i}]` 和 `a[{S.i + 1}]`' if S.i != B.get('i') else '前 `n-1` 步都做完了，最后一个数单独处理'),
        'if a[i]:': lambda S, B, r: (f'`a[{S.i}] = {S.a[S.i]}` 非零 → 要参与后面的处理' if S.a[S.i] else f'`a[{S.i}] = 0` → 跳过，不占位置'),
        'if a[i] == a[i + 1]': lambda S, B, r: (f'`a[{S.i}] == a[{S.i + 1}]`（都是 {S.a[S.i]}）→ 满足合并条件' if S.a[S.i] == S.a[S.i + 1] else f'`a[{S.i}] = {S.a[S.i]}` 与 `a[{S.i + 1}] = {S.a[S.i + 1]}` 不等 → 不操作'),
        'a[i] *= 2': '`a[{i}]` 翻倍成 =={a[i]}==',
        'a[i + 1] = 0': '后一个变 0；之后轮到它时 `a[i]` 为 0，会被跳过',
        'a[j] = a[i]': '非零数字写到前面：`a[{j}] = {a[j]}`（`j ≤ i`，不会覆盖没读过的数）',
        'j += 1': '`j` → {j}',
        'if a[-1]:': lambda S, B, r: (f'最后一个 `a[-1] = {S.a[-1]}` 非零 → 也要放到前面' if S.a[-1] else '最后一个是 0 → 不用放'),
        'a[j] = a[-1]': '`a[{j}] = {a[-1]}`',
        'for i in range(j, n)': lambda S, B, r: (f'前 `{S.j}` 个是非零数，从下标 `{S.i}` 开始补 0' if S.i != B.get('i') else '补完了，后面全是 0'),
        'a[i] = 0': '`a[{i}] = 0`：后面的位置全部补 0',
        'return a': '非零在前、0 在后：`{a}`',
    },
    cards=dict(
        one_liner='翻倍和挪 0 合成一趟：边合并，边把非零数写到前面',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['依次对每个 `i`：若 `nums[i] == nums[i+1]`，`nums[i]` 翻倍，`nums[i+1]` 置 0',
                 '操作完成后把所有 0 移到末尾',
                 '示例：`[1,2,2,1,1,0]` → `[1,4,2,0,0,0]`'],
        quote='不需要额外创建数组，直接在原数组上操作。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`j` 记录下一个非零数该放的位置，`j ≤ i` 所以不会覆盖没读的数',
              '合并完马上 `a[j] = a[i]`，翻倍和前移一次循环做完',
              '最后一个数没有 `i+1`，循环外单独处理，之后把 `j` 到末尾清零'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '循环只到 `n-2`，最后一个元素要单独判断',
                 '`a[i+1] = 0` 之后下一轮 `a[i]` 为 0，自然被跳过，不会连续合并',
                 '同类题：283 移动零'],
    ),
)

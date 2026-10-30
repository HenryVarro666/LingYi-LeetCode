def _txt(S):
    if 'stack' not in S:
        return ''
    nums = S['nums']
    tops = ' '.join(f'{nums[i]}(下标{i})' for i in S['stack']) or '空'
    return f"栈（下标，递增）：{tops}；`res = {S['res']}`"


CONFIG = dict(
    num=4054, title='统计影子数对 I', difficulty='Medium', category='单调栈',
    author='yiduobo', technique='单调栈 · 出栈时统计 · cnt 去掉相等元素',
    tags=[],
    code='''
class Solution(object):
    def shadowPairs(self, nums):
        
        stack = []
        res = 0
        nums.append(0)

        for index, v in enumerate(nums):
            pre = None
            cnt = 0
            while stack and nums[stack[-1]] > v:
                if pre != nums[stack[-1]]:
                    pre = nums[stack[-1]]
                    cnt = 0
                else:
                    cnt += 1
                
                res += index - stack[-1] - 1 - cnt
                stack.pop()
            
            stack.append(index)

        return res
''',
    call='Solution().shadowPairs([6, 7, 6, 6, 7])',
    expect=4,
    views=[
        dict(type='array', var='nums', label='nums（末尾补了哨兵 0，用来把栈清空）', cell=100, h=200,
             pointers={'index': 'blue'},
             color=lambda S, i, v: 'blue' if 'index' in S and i == S['index'] else ('yellow' if 'stack' in S and i in S['stack'] else None)),
        dict(type='stack', var='stack', label='stack（存下标）', h=170, font=30),
        dict(type='text', fn=_txt, size=26, h=80),
    ],
    watch=[('index', 'index', 'blue'), ('v', 'v', 'cyan'), ('pre', 'pre', 'pink'), ('cnt', 'cnt', 'orange'), ('res', 'res', 'green')],
    skip=[9, 10],
    captions={
        'nums.append(0)': '末尾补一个 0：比所有数都小，最后会把栈里剩下的下标全部弹出，统一结算',
        'for index, v in enumerate(nums)': lambda S, B, r: (f'处理下标 `index = {S.index}`，`v = {S.v}`；`pre` 记上一个出栈的值，`cnt` 记连续相等的个数（每轮重置）'
                                                     if 'index' not in B or B.index != S.index else '哨兵 0 也处理完了，遍历结束'),
        'while stack and': lambda S, B, r: (f'栈顶 `nums[{S.stack[-1]}] = {S.nums[S.stack[-1]]}` > `v = {S.v}`：v 是它的下一个更小元素 → 出栈结算'
                                            if S.stack and S.nums[S.stack[-1]] > S.v else '栈空或栈顶 ≤ v：不再出栈'),
        'if pre != nums[stack[-1]]': lambda S, B, r: (f'栈顶值 `{S.nums[S.stack[-1]]}` 与 `pre = {S.pre}` 不同 → 换了新的值'
                                                      if S.pre != S.nums[S.stack[-1]] else f'栈顶值 `{S.nums[S.stack[-1]]}` 与 `pre` 相同 → 又一个相等元素'),
        'pre = nums[stack[-1]]': '记下 `pre = {pre}`',
        'cnt = 0': '值变了，`cnt` 清零（前面没有出栈的相等元素）',
        'cnt += 1': '相等元素又出栈了，`cnt` → {cnt}（它们在 i 与 p 之间，要剔除）',
        'res += index': lambda S, B, r: (f'`i = {S.stack[-1]}` 的下一个更小在 `{S.index}`：`{S.index} − {S.stack[-1]} − 1 − same({S.cnt})` = '
                                         f'=={S.index - S.stack[-1] - 1 - S.cnt}== → `res = {S.res}`'),
        'stack.pop()': '下标 `{B.stack[-1]}` 出栈',
        'stack.append(index)': '`index = {index}` 入栈',
        'return res': '影子对一共 =={ret}== 个',
    },
    cards=dict(
        one_liner='每个 i 找下一个更小元素 p，p 之前扣掉相等的就是影子对',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`(i, j)` 满足 `i < j`、`nums[i] < nums[j]`，且中间没有 `nums[k] < nums[i]`',
                 '数出所有影子对的个数',
                 '本视频：`[6,7,6,6,7]` → `4`'],
        quote='对于每个下标i，都找出下一个更小元素所在的下标p，那么p右侧的所有下标都无法与i形成影子对，理由是p在这里充当了k的角色。',
        quote_src='—— yiduobo 题解原文',
        idea=['i 的下一个更小元素在 p：`i+1 ~ p-1` 都 ≥ `nums[i]`，只有严格更大的能配对',
              '个数 = `p - 1 - i - same`，same 是这一段里恰好等于 `nums[i]` 的个数',
              '单调栈里 i 出栈时，相等的元素刚好在它之前连续出栈 → 用 `pre` 和 `cnt` 数出 same'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '末尾补 0 当哨兵，让所有下标都在最后出栈结算',
                 '易错：`cnt` 要在值变化时清零，相等才累加',
                 '原文会修改传入的 `nums`（append 0），原文代码未改动',
                 '对比灵神：灵神枚举 j、栈里存 (值, 次数)；yiduobo 在出栈时结算 i'],
    ),
)

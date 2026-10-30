def _bi(S):
    """建 f 阶段：当前 num 在 group 中的下标"""
    if not isinstance(S.get('f'), list) or 'group' not in S or not 8 <= S['_line'] <= 13:
        return None
    i = len(S['f']) - (1 if S['_line'] == 13 else 0)
    return i if i < len(S['group']) else None


def _si(S):
    """匹配阶段：nums 里当前读到的下标"""
    return S.get('index') if S.get('_line', 0) >= 17 else None


def _matched(S, k):
    ln, pos, idx = S.get('_line', 0), S.get('pos', 0), S.get('index')
    if ln < 17 or not pos or idx is None:
        return False
    if ln <= 20:
        return idx - pos <= k <= idx - 1
    return idx - pos + 1 <= k <= idx


def _top(S):
    if 'group' not in S:
        return ''
    g = S['groups'].index(S['group']) + 1
    ln = S['_line']
    if ln <= 13:
        return f"第 {g} 组 `group = {S['group']}`：先给它建 next 数组 `f`"
    return f"第 {g} 组：在 `nums` 里从下标 `p = {S['p']}` 开始找 `{S['group']}`"


CONFIG = dict(
    num=1764, title='通过连接另一个数组的子数组得到一个数组', difficulty='Medium', category='字符串',
    author='yiduobo', technique='依次对每组做 KMP 匹配',
    tags=['灵神题单', '字符串'],
    code='''
class Solution(object):
    def canChoose(self, groups, nums):

        p = 0
        for group in groups:
            f = [0]
            pos = 0
            for num in group[1:]:
                while pos > 0 and num != group[pos]:
                    pos = f[pos - 1]
                if num == group[pos]:
                    pos += 1
                f.append(pos)
            
            pos = 0
            flag = False
            for index in range(p, len(nums)):
                while pos > 0 and nums[index] != group[pos]:
                    pos = f[pos - 1]
                if nums[index] == group[pos]:
                    pos += 1
                if pos == len(group):
                    flag = True
                    p = index + 1
                    break
            
            if not flag:
                return False
        
        return True
''',
    call='Solution().canChoose([[1,2,1],[3,1]], [1,1,2,1,2,3,1])',
    expect=True,
    views=[
        dict(type='text', size=26, h=70, fn=_top),
        dict(type='array', var='nums', label='nums（灰 = 前面的组已经用掉，绿 = 当前匹配上的部分）', cell=80, h=230,
             pointers={'p': 'orange', _si: 'pink'}, pointer_labels={_si: 'index'},
             dim=lambda S, k, v: k < S.get('p', 0), color=lambda S, k, v: 'green' if _matched(S, k) else None),
        dict(type='array', var='group', label='group（蓝箭头 = pos 已匹配长度；粉箭头 = 建表时的 num）', cell=80, h=230,
             pointers={'pos': 'blue', _bi: 'pink'}, pointer_labels={_bi: 'num'},
             color=lambda S, k, v: 'green' if S.get('_line', 0) >= 17 and S.get('pos') and k < S['pos'] else None),
        dict(type='array', var='f', label='f：group 的 next 数组', cell=80, h=170),
    ],
    watch=[('p', 'p', 'orange'), ('pos', 'pos', 'blue'), ('index', 'index', 'pink'), ('flag', 'flag', 'green')],
    captions={
        'p = 0': '`p` 是 nums 里下一组可以开始匹配的位置；组必须按先后顺序、不重叠，所以每组都尽量靠前匹配',
        'for group in groups': lambda S, B, r: (f"取出下一组 `group = {S.group}`" if 'group' in S and S.get('group') != B.get('group') else 'groups 全部处理完'),
        'f = [0]': '给这一组建 kmp 的 next 数组 `f`，`f[0] = 0`',
        'for num in group[1:]': '`num = {num}`：看它能不能接在已匹配的前缀后面',
        'while pos > 0 and num != group[pos]': lambda S, B, r: (
            f"`group[{S.pos}] = {S.group[S.pos]}` ≠ `num = {S.num}`：失配，`pos` 退到 `f[{S.pos-1}] = {S.f[S.pos-1]}`" if S.pos > 0 and S.num != S.group[S.pos]
            else '`pos = 0` 或已经相等，不再回退'),
        'pos = f[pos - 1]': '借助 `f` 回退：`pos` → {pos}',
        'if num == group[pos]': lambda S, B, r: (
            f"`num = {S.num}` == `group[{S.pos}]` → 匹配长度加一" if S.num == S.group[S.pos]
            else f"`num = {S.num}` ≠ `group[{S.pos}] = {S.group[S.pos]}` → 这一位没有匹配"),
        'pos += 1': '`pos` → {pos}',
        'f.append(pos)': '`f` 追加 `{pos}`，现在 `f = {f}`',
        'flag = False': '`flag` 记录这一组有没有在 nums 里找到',
        'for index in range(p, len(nums))': lambda S, B, r: (f"从 `p = {S.p}` 往后扫：`index = {S.index}`，`nums[{S.index}] = {S.nums[S.index]}`" if S.get('index') != B.get('index')
                                                              else f'`nums` 扫完了，这一组没找到'),
        'while pos > 0 and nums[index] != group[pos]': lambda S, B, r: (
            f"`group[{S.pos}] = {S.group[S.pos]}` ≠ `nums[{S.index}] = {S.nums[S.index]}`：失配，`pos` 退到 `f[{S.pos-1}] = {S.f[S.pos-1]}`，不用回头重扫 nums" if S.pos > 0 and S.nums[S.index] != S.group[S.pos]
            else '`pos = 0` 或已经相等，不再回退'),
        'pos = f[pos - 1]': '借助 `f` 回退：`pos` → {pos}',
        'if nums[index] == group[pos]': lambda S, B, r: (
            f"`nums[{S.index}] = {S.nums[S.index]}` == `group[{S.pos}]` → 又匹配一位" if S.nums[S.index] == S.group[S.pos]
            else f"`nums[{S.index}] = {S.nums[S.index]}` ≠ `group[{S.pos}] = {S.group[S.pos]}` → 没匹配上"),
        'if pos == len(group)': lambda S, B, r: (f'`pos = {S.pos} == len(group)`：整组匹配成功' if S.pos == len(S.group)
                                                 else f'`pos = {S.pos} < len(group) = {len(S.group)}`，继续扫'),
        'flag = True': '这一组找到了',
        'p = index + 1': '下一组从 `index + 1 = {p}` 开始找，保证不重叠、顺序靠后',
        'if not flag': lambda S, B, r: ('这一组没找到 → 不可能按序取出所有组' if not S.flag else '这一组找到了，继续下一组'),
        'return False': '有一组在剩余的 nums 里匹配不上 → `False`',
        'return True': '所有组都按顺序、不重叠地匹配上 → `True`',
    },
    cards=dict(
        one_liner='把每个 group 依次当成模式串，用 kmp 在 nums 里靠前匹配',
        complexity='时间 `O(n + Σ|group|)`，空间 `O(max|group|)`',
        problem=['给整数数组 `groups` 的若干组和数组 `nums`，问能否按 groups 的顺序，从 nums 里选出==互不重叠==的子数组，依次等于每个 group',
                 '示例：`groups = [[1,2,1],[3,1]]`，`nums = [1,1,2,1,2,3,1]` → `true`',
                 '子数组必须是 nums 中连续的一段，且按组的先后顺序出现'],
        quote='对于groups中的数组而言，应该尽可能靠前地去匹配nums……将匹配位置的结束位置开始进行下一个字符串的匹配',
        quote_src='—— yiduobo 题解原文',
        idea=['数组匹配可以看成字符串匹配：每个 `group` 是模式串，`nums` 是主串',
              '每组匹配到最靠前的位置，下一组从 `index + 1` 接着找，给后面留最多空间',
              '每组用 kmp：先建 `f`，再扫 `nums`，失配时 `pos = f[pos - 1]`，主串不回退'],
        summary=['时间 `O(len(nums) + Σ|group|)`，空间 `O(max|group|)`',
                 '易错：下一组要从 `index + 1` 开始，不能重叠；有一组找不到就 `return False`',
                 '建 `f` 从 `group[1:]` 开始，`f[0] = 0` 是初始值',
                 '原文没有 Python 2 特有写法，代码未改动'],
    ),
)

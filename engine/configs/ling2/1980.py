NUMS = ["1010", "0110", "1101", "0001"]


def _gcolor(S, i, j, v):
    k = S.get('i')
    if k is None:
        return None
    if i == j and i < k:
        return 'cyan'
    if i == j and i == k:
        return 'yellow' if S.get('_line') == 4 else 'cyan'
    return None


def _acolor(S, i, v):
    if v == '':
        return None
    if S.get('_line') == 5 and i == S.get('i'):
        return 'yellow'
    return 'green'


def _info(S):
    ln = S.get('_line')
    i = S.get('i')
    if ln == 5 and i is not None:
        s = S['s']
        return f"`nums[{i}][{i}] = {s[i]}` → `ans[{i}] = {S['ans'][i]}`：ans 和 `nums[{i}]` ==在第 {i} 位不同=="
    if ln == 6:
        return f"`ans = \"{''.join(S['ans'])}\"` 和每个 `nums[i]` 都至少有一位不同 → 一定不在 nums 里"
    return '只看==对角线==：第 `i` 位取 `nums[i][i]` 的反'


CONFIG = dict(
    num=1980, title='找出不同的二进制字符串', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='构造 · 康托对角线',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def findDifferentBinaryString(self, nums: List[str]) -> str:
        ans = [''] * len(nums)
        for i, s in enumerate(nums):
            ans[i] = '1' if s[i] == '0' else '0'
        return ''.join(ans)
''',
    call=f'Solution().findDifferentBinaryString({NUMS!r})',
    expect='0010',
    views=[
        dict(type='text', fn=_info, size=26, h=70),
        dict(type='grid', var='nums', label='nums（第 i 行 = nums[i]，黄/青 = 对角线 nums[i][i]）', h=360, cell=78,
             rows=lambda S: list(range(len(S['nums']))), cols=lambda S: list(range(len(S['nums']))),
             color=_gcolor, cursors=[('i', 'i', 'yellow', 'i')]),
        dict(type='array', var='ans', label='ans（第 i 位 = nums[i][i] 取反）', cell=78, h=150, color=_acolor),
    ],
    watch=[('i', 'i', 'yellow'), ('s', 's', 'cyan'), ('s[i]', lambda S: S['s'][S['i']] if 's' in S else None, 'yellow')],
    captions={
        "ans = [''] * len(nums)": '`n = {len(nums)}`：答案也是 `{len(nums)}` 位，先开好 `{len(nums)}` 个空位',
        'for i, s in enumerate(nums)': lambda S, B, r: ('所有串都处理完，对角线取反完毕，退出循环' if B.get('i') == S.i else
                                                        f'看第 `{S.i}` 个串 `s = "{S.s}"`，只关心它的第 `{S.i}` 位 `s[{S.i}] = {S.s[S.i]}`'),
        "ans[i] = '1' if s[i] == '0' else '0'": '`s[{i}] = {s[i]}` → 取反填 `ans[{i}] = {ans[i]}`：保证 ans ==不等于== `nums[{i}]`',
        "return ''.join(ans)": '每一位都和对应的 `nums[i]` 错开 → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='第 i 位取 nums[i][i] 的反，答案和每个串都至少差一位',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计）',
        problem=['`nums` 有 `n` 个==互不相同==的二进制串，每个长度都是 `n`',
                 '返回一个长度为 `n` 且==没有出现==在 `nums` 中的二进制串（任意一个即可）',
                 '示例：`nums = ["111","011","001"]` → `"101"`（`"000"` 等也对）',
                 f'本视频：`nums = {NUMS}`'.replace("'", '"')],
        quote='这个方法灵感来自数学家康托关于「实数是不可数无限」的证明。……==一般地，令 ans[i] = nums[i][i] ⊕ 1，即可满足要求。==',
        quote_src='—— 灵茶山艾府题解（方法二：康托对角线）',
        idea=['`ans[i] ≠ nums[i][i]` → `ans` 和 `nums[i]` 在第 `i` 位不同',
              '对每个 `i` 都成立 → `ans` 和每个 `nums[i]` ==都至少有一个字符不同==',
              '只访问了每个串的一个字符，连 `nums` 互不相同都用不上'],
        result='`ans = "0010"`：和 4 个串分别在第 0/1/2/3 位不同 ✓',
        summary=['时间 `O(n)`：每个串只看一个字符；空间 `O(1)`（不计返回值）',
                 '方法一（暴力）：把串转成整数放进集合，`ans` 从 0 往上枚举到不在集合里，再补前导零',
                 '易错：方法一返回时要补齐到 `n` 位：`f"{ans:0{n}b}"`',
                 '对角线法也说明了：方法一的答案==一定存在==（n 个串挡不住 2^n 种可能）'],
    ),
)

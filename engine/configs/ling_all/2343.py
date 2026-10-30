CONFIG = dict(
    num=2343, title='裁剪数字后查询第 K 小的数字', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='离线 + 增量排序',
    tags=['灵神题单·常用数据结构', '难度分 1652'],
    code='''
class Solution:
    def smallestTrimmedNumbers(self, nums: List[str], queries: List[List[int]]) -> List[int]:
        idx = list(range(len(nums)))
        ans, j = [0] * len(queries), 1
        for qi, (k, trim) in sorted(enumerate(queries), key=lambda q: q[1][1]):  # 按 trim 排序
            while j <= trim:
                idx.sort(key=lambda i: nums[i][-j])  # 只比较倒数第 j 个字符的大小
                j += 1
            ans[qi] = idx[k - 1]
        return ans
''',
    call='Solution().smallestTrimmedNumbers(["102","473","251","814"], [[1,1],[2,3],[4,2],[1,2]])',
    expect=[2, 2, 1, 0],
    views=[
        dict(type='array', var='nums', label='nums（要比较的是倒数第 j 位）', cell=130, h=170),
        dict(type='array', var='idx', label='idx：当前按“后 j-1 位”排好的下标（sort 稳定）', cell=100, h=170,
             color=lambda S, i, v: ('green' if 'k' in S and S.get('_line') == 8 and i == S['k'] - 1 else None)),
        dict(type='array', var='queries', label='queries（按 trim 从小到大处理）', cell=130, h=185, color=lambda S, i, v: ('blue' if i == S.get('qi') else None)),
        dict(type='array', var='ans', label='ans（按原询问下标 qi 写入）', cell=100, h=150, color=lambda S, i, v: ('green' if i == S.get('qi') and S.get('_line') == 9 else None)),
    ],
    watch=[('qi', 'qi', 'blue'), 'k', 'trim', ('j', 'j', 'yellow'), ('idx', 'idx', 'cyan')],
    captions={
        'idx = list': '`idx` 是下标数组：排序时只动下标，不动 `nums`',
        'ans, j = ': '`ans` 按原询问顺序存答案；`j` = 下一个要加进来比较的位数（从最后一位开始）',
        'for qi': lambda S, B, r: ('询问都处理完了' if getattr(B, 'qi', None) == S.qi else f'处理询问 `{S.qi}`：第 `{S.k}` 小、裁剪到 `{S.trim}` 位（询问按 `trim` 从小到大）'),
        'while j <= trim': lambda S, B, r: (f'`j = {S.j} ≤ trim = {S.trim}`：还要再加一位进来排' if S.j <= S.trim else f'`j = {S.j} > trim = {S.trim}`：位数够了，直接取答案'),
        'idx.sort': '再加入倒数第 `{j}` 位：只比较这一个字符；`idx` 之前已按更低位排好，==稳定排序==保证相同字符保持旧序 → `idx = {idx}`',
        'j += 1': '`j = {j}`：下一次再多看一位',
        'ans[qi]': '`idx[{k} - 1] = {idx[k-1]}` 就是第 `{k}` 小的下标 → `ans[{qi}] = {ans[qi]}`',
        'return ans': '答案按原询问顺序 `{ans}`',
    },
    max_steps=80,
    cards=dict(
        one_liner='询问按 trim 排序：每多一位，只在上次顺序上再排一次',
        complexity='时间 `O(q log q + mn log n)`，空间 `O(q + n)`',
        problem=['`nums` 是等长数字字符串，每个询问 `[k, trim]`：只留最右 `trim` 位，求第 `k` 小的下标',
                 '相等时下标小的算小',
                 '示例：`["102","473","251","814"]`，4 个询问 → `[2,2,1,0]`'],
        quote='先将询问按照 trim 从小到大排序，并按照这一顺序回答询问。随着 trim 的不断增加，我们可以在排好序的字符串数组的基础上，向每个字符串的前面添加一个对应的字符，只需要比较这个新增的字符的大小。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['后 `trim` 位的顺序 = 先看第 `trim` 位，再看之前已排好的顺序',
              '所以每增加一位，只对 `idx` 按新字符做一次稳定排序',
              '用 `qi` 记住原顺序，答案写回 `ans[qi]`'],
        summary=['时间 `O(q log q + mn log n)`（基数排序可到 `O(q log q + mn)`），空间 `O(q + n)`',
                 '易错：`idx.sort` 必须稳定；`j` 只增不减，不能每个询问重排',
                 '方法一：每个询问直接 `sorted((s[-trim:], i) ...)`，时间 `O(qmn log n)`，写法一行',
                 '同类：离线 + 排序询问，把重复工作摊平'],
    ),
)

class Graph:
    def __init__(self, mat, unconn=0):
        vnum = len(mat)
        for x in mat:
            if len(x) != vnum:
                raise ValueError("参数错误")
        self._mat = [mat[i][:] for i in range(vnum)]  # 做拷贝
        self._unconn = unconn
        self._vnum = vnum

    # 顶点个数
    def vertex_num(self):
        return self._vnum

    # 顶点是否无效
    def _invalid(self, v):
        return v < 0 or v >= self._vnum

    # 添加边
    def add_edge(self, vi, vj, val=1):
        if self._invalid(vi) or self._invalid(vj):
            raise ValueError(str(vi) + " or " + str(vj) + "不是有效的顶点")
        self._mat[vi][vj] = val

    # 获取边的值
    def get_edge(self, vi, vj):
        if self._invalid(vi) or self._invalid(vj):
            raise ValueError(str(vi) + " or " + str(vj) + "不是有效的顶点")
        return self._mat[vi][vj]

    # 获得一个顶点的各条出边
    def out_edges(self, vi):
        if self._invalid(vi):
            raise ValueError(str(vi) + "不是有效的顶点")
        return self._out_edges(self._mat[vi], self._unconn)

    @staticmethod
    def _out_edges(row, unconn):
        edegs = []
        for i in range(len(row)):
            if row[i] != unconn:
                edegs.append((i, row[i]))
        return edegs

    def __str__(self):
        return "[\n" + ",\n".join(map(str, self._mat)) + "\n]" + "\nUnconnected: " + str(self._unconn)
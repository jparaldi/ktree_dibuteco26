from src.models.point import Point

class KdNode:
    def __init__(self, point: Point, axis:int, left=None, right=None):
        self.point = point # ponto armazenado
        self.axis = axis # 0 = latitude, 1 = longitude
        self.left = left # subarvore esquerda
        self.right = right # subarvore direita
    
    def __repr__(self):
        return f"KdNode(point={self.point}, axis={self.axis})"
    
# axis vai ficar guardado no nó para simplificação e evitar bugs na recursão

    def build_kdtree(points, depth=0):
        if not points:
            return None
        
        axis = depth % 2 # alterna entre latitude e longitude

        # ordena os pontos pelo eixo atual e encontra a mediana para dividir o espaço
        points.sort(key=lambda p: p.get_coord(axis))

        median = len(points) // 2 # índice da mediana

        # cria o nó com o ponto da mediana
        node = KdNode(points[median], axis)

        node.left = build_kdtree(points[:median], depth + 1) # constrói a subárvore esquerda
        node.right = build_kdtree(points[median + 1:], depth + 1) # constrói a subárvore direita

        return node


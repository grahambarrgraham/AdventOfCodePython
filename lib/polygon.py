def polygon_area(vertices):  # shoelace formula, vertices must be ordered
    num_vertices = len(vertices)
    sum1 = 0
    sum2 = 0

    for i in range(0, num_vertices - 1):
        sum1 = sum1 + vertices[i][0] * vertices[i + 1][1]
        sum2 = sum2 + vertices[i][1] * vertices[i + 1][0]

    # Add xn.y1
    sum1 = sum1 + vertices[num_vertices - 1][0] * vertices[0][1]
    # Add x1.yn
    sum2 = sum2 + vertices[0][0] * vertices[num_vertices - 1][1]

    area = abs(sum1 - sum2) / 2
    return area

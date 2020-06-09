def calculate_centroids(startX, endX, startY, endY):
    cX = int((startX + endX) / 2.0)
    cY = int((startY + endY) / 2.0)
    return (cX, cY)


def calculate_box_size(startX, endX, startY, endY):
    return (endX - startX) * (endY - startY)


def calculate_box_size_for_swag(swag):
    return calculate_box_size(swag.box[0], swag.box[2], swag.box[1], swag.box[3])

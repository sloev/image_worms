import time

class Path:

    def __init__(self, lifespan, max_width, max_height, source_image):
        self.lifespan = lifespan
        self.max_width = max_width
        self.max_height = max_height
        self.pg = createGraphics(max_width, max_height)
        self.pg.beginDraw()
        self.pg.background(0)
        self.pg.endDraw()
        self.source_image = source_image
        self.last_point = None

    def get_next_point(self, last_point):
        raise NotImplemented()

    def next(self):
        if not self.lifespan:
            return None
        self.last_point = self.get_next_point(self.last_point)
        self.lifespan -= 1
        self.pg.beginDraw()
        self.pg.background(0)
        x, y, angle = self.last_point
        self.pg.stroke(255)
        self.pg.strokeWeight(30)
        self.pg.point(x, y)
        self.pg.endDraw()
        img_tmp = self.source_image.copy()
        img_tmp.mask(self.pg)#, 0, 0, self.max_width, self.max_height,0,0,self.max_width, self.max_height, MULTIPLY)
        return img_tmp

    def __nonzero__(self):
        return 1 if self.lifespan else 0


class NoisyPath(Path):

    def get_next_point(self, last_point):
        if last_point is None:
            p = random(self.max_width), random(self.max_height), random(360)
            return p
        else:
            x, y, angle = last_point
            angle += random(-30, 30)
            next_x = x + (cos(radians(angle)))
            next_y = y + (sin(radians(angle)))
            if next_x > self.max_width or next_x < 0 or next_y > self.max_height or next_y < 0:
                angle -= 180
            x += cos(radians(angle)) * 10
            y += sin(radians(angle)) * 10
            return x, y, angle


def setup():
    global img, running_paths, source_images, path_classes
    source_images = [
        loadImage("1.jpg"),
        loadImage("2.jpg"),
        loadImage("3.jpg"),
        loadImage("4.jpg"),
        loadImage("5.jpg")
    ]
    path_classes = [
        NoisyPath
    ]
    size(1024, 768)
    running_paths = []
    background(0)


def draw():
    global img, running_paths, source_images, path_classes
    running_paths = [path for path in running_paths if path]
    for i in range(2-len(running_paths)):
        path_index = int(random(len(path_classes)-1))
        path_class = path_classes[path_index]
        lifespan = int(random(100, 300))
        img_index = int(random(len(source_images)-1))
        img = source_images[img_index]
        print("added", lifespan, path_index, img_index)
        running_paths.append(path_class(lifespan, width, height, img))
    
    for path in running_paths:
        img = next(path)
        image(img, 0,0)#, 0, 0, width, height,0,0, width,  height, BLEND)

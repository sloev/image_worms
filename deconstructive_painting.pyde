import time

class Path:

    def __init__(self, lifespan, max_width, max_height, source_image, difference):
        self.lifespan = lifespan
        self.max_width = max_width
        self.max_height = max_height
        self.pg = createGraphics(max_width, max_height)
        self.pg.beginDraw()
        self.pg.background(0)
        self.pg.endDraw()
        self.source_image = source_image
        self.last_point = None
        self.it = 0
        self.factor = lifespan/10.0
        self.difference = difference


    def get_next_point(self, last_point):
        raise NotImplemented()

    def render(self):
        if not self.lifespan:
            return None
        self.last_point = self.get_next_point(self.last_point)
        self.lifespan -= 1
        self.pg.beginDraw()
        self.pg.background(0)
        x, y, angle = self.last_point
        add_stroke = min(self.it, self.factor) * (255 / self.factor)
        sub_stroke = (
            self.factor - min(self.lifespan, self.factor)) * (255 / self.factor)
        s = add_stroke - sub_stroke
        self.pg.stroke(s)
        self.pg.strokeWeight(30)
        self.pg.point(x, y)
        self.pg.endDraw()
        img_tmp = self.source_image.copy()
        # , 0, 0, self.max_width, self.max_height,0,0,self.max_width, self.max_height, MULTIPLY)
        img_tmp.mask(self.pg)
        self.it += 1
        if self.difference:
            blend(img_tmp, 0, 0, self.max_width, self.max_height,0,0, self.max_width,  self.max_height, DIFFERENCE)
        else:
            image(img_tmp, 0, 0)

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
            x += cos(radians(angle)) * 5
            y += sin(radians(angle)) * 5
            return x, y, angle


def setup():
    global img, running_paths, source_images, path_classes, delete_all
    frameRate(60)
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
    delete_all = time.time() + 100


def draw():
    global img, running_paths, source_images, path_classes, delete_all
    running_paths = [path for path in running_paths if path]
    for i in range(1 - len(running_paths)):
        path_index = int(random(len(path_classes) - 1))
        path_class = path_classes[path_index]
        lifespan = int(random(100, 500))
        img_index = int(random(len(source_images) - 1))
        img = source_images[img_index]
        #print("added", lifespan, path_index, img_index)
        difference = random(0,10) > 8
        running_paths.append(path_class(lifespan, width, height, img, difference=difference))
    if delete_all < time.time():
        fill(0, 0, 0, 30)
        rect(-2, -2, width + 4, height + 4)
        if delete_all + 5 < time.time():
            delete_all = time.time() + random(50, 400)
    for path in running_paths:
        path.render()

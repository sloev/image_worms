import time
import random

class Path:

    def __init__(self, lifespan=0, max_width=1, max_height=1, source_image=None, difference=None):
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
        self.factor = lifespan/5.0
        self.difference = difference
        self.weight = random.randint(2,120)


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
        add_stroke = min(self.it, self.factor) * (255.0 / self.factor)
        sub_stroke = (
            self.factor - min(self.lifespan, self.factor)) * (255.0 / self.factor)
        s = add_stroke - sub_stroke
        self.pg.stroke(s)
        self.pg.strokeWeight(self.weight-2)
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
    weight = 30

    def get_next_point(self, last_point):
        if last_point is None:
            p = random.randint(0, self.max_width), random.randint(0, self.max_height), random.randint(0, 360)
            return p
        else:
            x, y, angle = last_point
            angle += random.randint(-30, 30)
            next_x = x + (cos(radians(angle)))
            next_y = y + (sin(radians(angle)))
            if next_x + self.weight > self.max_width or next_x - self.weight < 0 or next_y + self.weight> self.max_height or next_y - self.weight < 0:
                angle -= 180
            x += cos(radians(angle)) * 5
            y += sin(radians(angle)) * 5
            return x, y, angle


def setup():
    global img, running_paths, source_images, path_classes, delete_all, back
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

    for i in range(2):
        running_paths.append(path_classes[0]())
    back = get()

black = time.time()+1
def draw():
    global img, running_paths, source_images, path_classes, delete_all, back, black
    if black < time.time():

        back = get()

        blend(back, 0,0,width, height, 1,1,width-2, height-2, BLEND)
       
        
        black = time.time()+1

    for p in running_paths:
        if p:
            continue
        path_index = random.randint(0,len(path_classes) - 1)
        lifespan = random.randint(100, 500)
        img_index = random.randint(0, len(source_images) - 1)
        img = source_images[img_index]
        #print("added", lifespan, path_index, img_index)
        difference = random.randint(0,10) > 8
        p.__init__(lifespan, width, height, img, difference=difference)
    if delete_all < time.time():
        fill(0, 0, 0, 30)
        rect(-2, -2, width + 4, height + 4)
        if delete_all + 5 < time.time():
            delete_all = time.time() + random.randint(100, 500)
    for path in running_paths:
        path.render()
        

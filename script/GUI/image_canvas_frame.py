from tkinter import Canvas, Tk, Frame
from PIL import Image, ImageTk


class ImageCanvas(Canvas):
    def __init__(self, master: Frame, canvas_width: int,
                 canvas_height: int):

        super(ImageCanvas, self) \
            .__init__(master, width=canvas_width, height=canvas_height)

        self.image_id = \
            self.create_image(canvas_width/2, canvas_height/2)
        self.photo_image = None

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

    def update_image(self, image: Image.Image):
        resized_image = image.resize((self.canvas_width, self.canvas_height))
        self.photo_image = ImageTk.PhotoImage(resized_image, master=self)

        self.itemconfigure(self.image_id, image=self.photo_image)


if __name__ == "__main__":
    from tkinter import filedialog
    root = Tk()
    canvas = ImageCanvas(root, 300, 300)
    canvas.update_image(Image.open(filedialog.askopenfilename()))
    canvas.pack()

    root.mainloop()

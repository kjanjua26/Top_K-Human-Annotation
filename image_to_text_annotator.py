'''
	Annotator Software v0.0.1
	Image to Sentence Retrieval Scorer
'''
import tkinter
import os
from PIL import ImageTk, Image 
import glob 
import cv2 
image_folder = 'human-baseline/images-128'
gt_file = 'human-baseline/coco_text_test.txt'
rest_file = 'human-baseline/results-img2sent.txt'
img_array = []
gt_dict = {}
retrived_dict = {}

for i in glob.glob(image_folder+"/*.png"):
	img_array.append(i)
with open(gt_file, 'r+') as gtlabels:
	for label in gtlabels:
		sent_name, sent = label.split('|')
		sent_name = sent_name.replace("#", "_")
		gt_dict[sent_name] = sent
with open(rest_file, 'r+') as rest_file:
	for res in rest_file:
		if 'correct' in res:
			continue
		target = res.split(', Distances:')[0].replace('Target: ', '')
		out = ''.join(res.split(', Distances:')[1:])
		out.replace(' ', '')
		temp_x = ""
		for i in out.split(', '):
			temp_x += i + '|'
		temp_y = []
		for j in temp_x.split('|'):
			j = j.replace("'", '')
			if j.endswith('.png'):
				j = j.replace("[(", "").replace("(", "").replace(" ", "").replace(".png", "")
				temp_y.append(gt_dict[j])
		retrived_dict[target] = temp_y

root = tkinter.Tk()
root.geometry("1200x500")
root.title("Annotator Software 0.0.1")

counter = tkinter.IntVar()
r_k_ = tkinter.IntVar()
imgName = tkinter.StringVar()

def onClick():
	if counter.get() < len(img_array):
		img_label = tkinter.Label(text="Query Image").place(x=10, y=80)
		gt_label = tkinter.Label(text="Gold Labels").place(x=200, y=80)
		ret_label = tkinter.Label(text="Retrieval Result").place(x=580, y=80)
		imgName.set(img_array[counter.get()])
		load = Image.open(imgName.get())
		gt = tkinter.Text(height=10, width=50)
		rt = tkinter.Text(height=10, width=80)
		render = ImageTk.PhotoImage(load)
		img = tkinter.Label(image=render)
		img.image = render
		img.place(x=10, y=100)
		gt.place(x=200, y=100)
		rt.place(x=580, y=100)
		gt_ = img_array[counter.get()].split('/')[-1].replace('.png', '')
		for i in range(5):
			gt_temp = gt_ + "_" + str(i)
			gt.insert('end', gt_dict[gt_temp])
		rt.insert('end', retrived_dict[gt_])
		counter.set(counter.get() + 1)
	else:
		final_ = tkinter.Label(text="Done. Stop Hitting that button now!").place(x=350,y=300)
		print("Final Result: ", str(r_k_.get()-1)+"/"+str(len(img_array)))
		pass_.config(state="disabled")
		corr.config(state="disabled")

def correct():
	pass_.config(state="active")
	corr.config(text="Correct")
	if r_k_.get() < len(img_array):
		r_k_.set(r_k_.get() + 1)
		res = tkinter.Label(text="Result: "+str(r_k_.get()-1)+"/"+str(len(img_array))).place(x=1000, y=30)
		onClick()

tkinter.Label(root, textvariable=imgName).pack()
pass_ = tkinter.Button(root, text="Pass", command=onClick, fg="dark green", bg = "white", state="disabled")
pass_.place(x=250,y=300)
corr = tkinter.Button(root, text="Start", command=correct, fg="dark green", bg = "white")
corr.place(x=1000, y=50)
root.mainloop()

'''
	Annotator Software v0.0.1
	Sentence to Image Retrieval Scorer
'''
import tkinter
import os
from PIL import ImageTk, Image 
import glob 
import cv2
image_folder = 'human-baseline/images-128'
gt_file = 'human-baseline/coco_text_test.txt'
rest_file = 'human-baseline/results-sent2img.txt'
mod_img_array = []
gt_dict = {}
retrived_dict = {}
for i in glob.glob(image_folder+"/*.png"):
	i = i.split('/')[-1].replace('.png','')
	for j in range(5):
			temp = i + "_" + str(j)
			mod_img_array.append(temp)

with open(gt_file, 'r+') as gtlabels:
	for label in gtlabels:
		sent_name, sent = label.split('|')
		sent_name = sent_name.replace("#", "_")
		gt_dict[sent_name] = sent
with open(rest_file, 'r+') as rest_file:
	for res in rest_file:
		if 'correct' in res:
			continue
		target = res.split(', Distances:')[0].replace('Target: ', '').replace(".png","")
		out = ''.join(res.split(', Distances:')[1:])
		temp_x = ""
		for i in out.split(", "):
			temp_x += i + "|"
		temp_y = []
		for j in temp_x.split("|"):
			j = j.replace("'", '')
			if j.endswith(".png"):
				j = j.replace("[(", "").replace("(", "").replace(" ", "").replace(".png", "")
				temp_y.append(j)
		retrived_dict[target] = temp_y
root = tkinter.Tk()
root.geometry("1200x800")
root.title("Annotator Software 0.0.1")

counter = tkinter.IntVar()
r_k_ = tkinter.IntVar()
imgName = tkinter.StringVar()

def onClick():
	if counter.get() < (len(mod_img_array)):
		imgName.set(mod_img_array[counter.get()])
		query_label = tkinter.Label(text="Query Sentence").place(x=10, y=80)
		query_box = tkinter.Text(height=10, width=50)
		query_box.place(x=10,y=100)
		query_box.insert('end', gt_dict[imgName.get()])
		for i in range(len(retrived_dict[imgName.get()])):
			file_name = "human-baseline/images-128/" + retrived_dict[imgName.get()][i] + ".png"
			load = Image.open(file_name) # pass name
			render = ImageTk.PhotoImage(load)
			img = tkinter.Label(image=render)
			img.image = render
			if i >= 5:
				samp_x = 10 + (150*(i%5))
				samp_y = 300
			else:
				samp_x = 10 + (150*i)
				samp_y = 150
			img.place(x=samp_x, y=samp_y)
		counter.set(counter.get() + 1)
	else:
		final_ = tkinter.Label(text="Done. Stop Hitting that button now!").place(x=350,y=300)
		print("Final Result: ", str(r_k_.get()-1)+"/"+str(len(mod_img_array)))
		pass_.config(state="disabled")
		corr.config(state="disabled")

def correct():
	pass_.config(state="active")
	corr.config(text="Correct")
	if r_k_.get() < len(mod_img_array):
		r_k_.set(r_k_.get() + 1)
		res = tkinter.Label(text="Result: "+str(r_k_.get()-1)+"/"+str(len(mod_img_array))).place(x=1000, y=30)
		onClick()


tkinter.Label(root, textvariable=imgName).pack()
pass_ = tkinter.Button(root, text="Pass", command=onClick, fg="dark green", bg = "white", state="disabled")
pass_.place(x=250,y=500)
corr = tkinter.Button(root, text="Start", command=correct, fg="dark green", bg = "white")
corr.place(x=1000, y=50)
root.mainloop()

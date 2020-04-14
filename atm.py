from PIL import Image, ImageTk
from tkinter import *
import threading
import time
import cv2
import subprocess
from pynput.keyboard import Key, Listener

class App(threading.Thread):

	pass_key = False

	def __init__(self, tk_root):
		self.root = tk_root
		self.pass_key = False
		threading.Thread.__init__(self)
		self.start()

	def run(self):
		loop_active = True
		while loop_active:
			with Listener(on_release = self.on_release) as listener:
				listener.join()
			
			if self.pass_key:
				loop_active = False
				self.root.quit()
				GUI()

	def on_release(self, key):
		if key == Key.space:
			self.pass_key = True
			return False


class ATM:
	def __init__(self, vs):
		# camera
		self.vs = vs
		self.load = None
		self.render = None
		self.frame = None
		self.check = None
		# thread
		self.thread = None
		self.stopEvent = None
		# UI
		self.pin = ""
		self.amt = ""
		self.onAmount = False
		self.root = Tk()
		w = str(  int(self.root.winfo_screenwidth()/2) - 400)
		h = str( int(self.root.winfo_screenheight()/2) - 350)
		self.root.geometry("800x700+"+w+"+"+h)
		self.root.wm_title("Delhi Bank")
		self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

		self.left = Frame(self.root, width=500, height=700)
		self.right = Frame(self.root, width=300, height=700)
		self.left.pack(side=LEFT)
		self.right.pack(side=RIGHT)

		self.first = Frame(self.left)
		self.second = Frame(self.left)
		self.third = Frame(self.left)
		self.forth = Frame(self.left)

		self.reset()

		self.btn0 = None
		self.btn1 = None
		self.btn2 = None
		self.btn3 = None
		self.btn4 = None
		self.btn5 = None
		self.btn6 = None
		self.btn7 = None
		self.btn8 = None
		self.btn9 = None
		self.btns = None
		self.btnh = None

		self.stopEvent = threading.Event()
		self.thread = threading.Thread(target=self.videoLoop, args=())
		self.thread.start()

		
	def reset(self):
		# Right frame
		self.panel = None
		instruction = """Instruction how to use\n\nMove your head in direction of \nrequired movement of pointer.\n\nTilt your in either direction to \nselect an option."""
		self.inst = Label(self.right, text=instruction, anchor=CENTER, width=300, height=400)
		self.inst.pack()

		# Left frame
		self.title  = Label(self.left, text="Delhi Bank", width=45, font="Times 16 bold", height=8)
		self.value  = Label(self.left, text="", width="18", height="4")
		self.text   = Label(self.left, text="Enter your 4 digit pin", width="40", height="4", font="Times 13 bold")
		self.title.pack()

		self.cashWithdraw      = Button(self.left,text="Cash Withdrawal",height="6",width="20")
		self.transfer          = Button(self.left,text="Transfer",height="6",width="20")
		self.changeCardSetting = Button(self.left,text="Change Card Setting",height="6",width="20")
		self.balanceEnquiry    = Button(self.left,text="Balance Inquiry",height="6",width="20")
		self.cashWithdraw.bind("<Button-1>", self.withdrawal)
		self.transfer.bind("<Button-1>", self.transfer)
		self.changeCardSetting.bind("<Button-1>", self.cardSetting)
		self.balanceEnquiry.bind("<Button-1>", self.balEnquiry)
		self.cashWithdraw.pack()
		self.transfer.pack()
		self.changeCardSetting.pack()
		self.balanceEnquiry.pack()


	def videoLoop(self):
		try:
			while not self.stopEvent.is_set():
				self.check, self.frame = self.vs.read()
				self.frame = cv2.resize(self.frame, (300,300))
				self.load = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
				self.load = Image.fromarray(self.load)
				print("YES1")
				self.render = ImageTk.PhotoImage(self.load)
				print("YES2")
				if self.panel is None:
					print("YES3")
					self.panel = Label(image=self.render)
					self.panel.image = self.render
					self.panel.pack(side="left", padx=10, pady=10)
				else:
					print("YES4")
					self.panel.configure(image=self.render)
					self.panel.image = self.render

		except:
			print("error")
			self.stopEvent.set()
			self.vs.release()
			self.load = Image.open("B.jpg")
			width, height = self.load.size
			self.load = self.load.resize((300, 300))
			self.render = ImageTk.PhotoImage(self.load)
			self.panel = Label(image=self.render)
			self.panel.image = self.render
			self.panel.pack()


	def onClose(self):
		time.sleep(10.0)
		print("Closing...")
		self.stopEvent.set()
		self.vs.release()
		self.root.quit()

	def collectMoney(self):
		self.first.destroy()
		self.second.destroy()
		self.third.destroy()
		self.forth.destroy()
		self.text["text"] = "Collect Your Money!!"
		time.sleep(7.0)
		self.onClose()
		Starting()

	def amountScreen(self):
		self.amt = ""
		self.pin = ""
		self.text["text"]="Enter amount"
		self.onAmount = True
		self.value["text"]=""
		self.btns["command"] = self.collectMoney


	def pinChange(self, event, no):
		if self.onAmount:
			self.amt = self.value["text"]
			length = len(self.amt)

			if no != "Back":
				self.amt = self.amt + no
				self.value["text"] = self.amt
			else:
				self.amt = self.amt[:length-1]
				self.value["text"] = self.amt
			print("Amount : " + self.amt)

		else:
			self.pin = self.value["text"]
			length = len(self.pin)

			if length < 4:
				self.pin = self.pin + no
				self.value["text"] = self.pin
			if no == "Back":
				self.pin = self.pin[:length-1]
				self.value["text"] = self.pin
			print("Pin : " + self.pin)

	def withdrawal(self, event):
		self.onAmount = False
		self.cashWithdraw.destroy()
		self.transfer.destroy()
		self.changeCardSetting.destroy()
		self.balanceEnquiry.destroy()

		self.text.pack()
		self.value.pack()

		self.btn0 = Button(self.forth, text=0, height="5", width="7")
		self.btn1 = Button(self.first, text=1, height="5", width="7")
		self.btn2 = Button(self.first, text=2, height="5", width="7")
		self.btn3 = Button(self.first, text=3, height="5", width="7")
		self.btn4 = Button(self.second, text=4, height="5", width="7")
		self.btn5 = Button(self.second, text=5, height="5", width="7")
		self.btn6 = Button(self.second, text=6, height="5", width="7")
		self.btn7 = Button(self.third, text=7, height="5", width="7")
		self.btn8 = Button(self.third, text=8, height="5", width="7")
		self.btn9 = Button(self.third, text=9, height="5", width="7")
		self.btns = Button(self.forth, text="Next", height="5", width="7", command=self.amountScreen)
		self.btnh = Button(self.forth, text="<--", height="5", width="7")

		self.btn0.bind("<Button-1>", lambda event : self.pinChange(event, "0"))
		self.btn1.bind("<Button-1>", lambda event : self.pinChange(event, "1"))
		self.btn2.bind("<Button-1>", lambda event : self.pinChange(event, "2"))
		self.btn3.bind("<Button-1>", lambda event : self.pinChange(event, "3"))
		self.btn4.bind("<Button-1>", lambda event : self.pinChange(event, "4"))
		self.btn5.bind("<Button-1>", lambda event : self.pinChange(event, "5"))
		self.btn6.bind("<Button-1>", lambda event : self.pinChange(event, "6"))
		self.btn7.bind("<Button-1>", lambda event : self.pinChange(event, "7"))
		self.btn8.bind("<Button-1>", lambda event : self.pinChange(event, "8"))
		self.btn9.bind("<Button-1>", lambda event : self.pinChange(event, "9"))
		self.btnh.bind("<Button-1>", lambda event : self.pinChange(event, "Back"))

		self.btn1.pack(side = LEFT)
		self.btn2.pack(side = LEFT)
		self.btn3.pack(side = LEFT)
		self.btn4.pack(side = LEFT)
		self.btn5.pack(side = LEFT)
		self.btn6.pack(side = LEFT)
		self.btn7.pack(side = LEFT)
		self.btn8.pack(side = LEFT)
		self.btn9.pack(side = LEFT)
		self.btns.pack(side = LEFT)
		self.btn0.pack(side = LEFT)
		self.btnh.pack(side = LEFT)

		self.first.pack()
		self.second.pack()
		self.third.pack()
		self.forth.pack()


	def transfer(event):
		print("Transfer")
		pass

	def cardSetting(event):
		pass

	def balEnquiry(event):
		pass


def GUI():
	print("Warming up camera...")
	vs = cv2.VideoCapture(0)
	time.sleep(2.0)
	pba = ATM(vs)
	pba.root.mainloop()


#  Starting Screen

def Starting():
	out = subprocess.Popen(['python3', 'mouse.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	root = Tk()
	root.wm_title("Delhi Bank")
	w = str(  int(root.winfo_screenwidth()/2) - 400)
	h = str( int(root.winfo_screenheight()/2) - 350)
	root.geometry("800x700+"+w+"+"+h)
	APP = App(root)

	now = Label(root, text=" For now press space to continue!!", font="Times 15")
	insert = Label(root, text=" Please Insert your card....", font="Times 30 bold")
	insert.pack(fill=X, pady=315)
	now.pack(fill=X)
	root.mainloop()
	root.quit()


if __name__ == '__main__':
	Starting()
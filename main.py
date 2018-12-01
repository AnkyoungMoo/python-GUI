import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox as msg

class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None

    def show_tip(self, tip_text):
        "Display text in a tooltip window"
        if self.tip_window or not tip_text:
            return

        x, y, _cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)

        tw.wm_geometry("+%d+%d" % (x, y))

        label = tk.Label(tw, text=tip_text, justify=tk.LEFT,
                    background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                    font=("tohoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

def create_ToolTip(widget, text):
    toolTip = ToolTip(widget)

    def enter(event):
        toolTip.show_tip(text)
    def leave(event):
        toolTip.hide_tip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

# window instance 생성
win = tk.Tk()

# 타이틀 설정
win.title("과자 자판기")

snackList = []

# 메뉴를 winow에 적용
menu_bar = Menu(win)
win.config(menu=menu_bar)

# 기본 메뉴 생성
basic_menu = Menu(menu_bar, tearoff=0)
basic_menu.add_command(label='메뉴 추가 요청')
basic_menu.add_command(label='메뉴 삭제 요청')
basic_menu.add_separator()
basic_menu.add_command(label='관리자 전화번호')
menu_bar.add_cascade(label='메뉴', menu=basic_menu)

# 잔고 확인 함수
def moneyCheck():
    msg.showwarning('현재 잔고 확인', '현재 잔고는 [0]원 입니다.')

# 가지고 있는 과자 확인 함수
def ownSnack():
    tempString = ''
    for i in range(len(snackList)):
        tempString += (snackList[i] + '과자\n')

    msg.showinfo('가지고 있는 과자 확인', tempString)

# 사용자 메뉴 생성
user_menu = Menu(menu_bar, tearoff=0)
user_menu.add_command(label='잔고 확인', command=moneyCheck)
user_menu.add_command(label='가지고 있는 과자 확인', command=ownSnack)
menu_bar.add_cascade(label='사용자', menu=user_menu)

# window instance 대신에 사용할 mighfy Frame 생성
mighfy = ttk.LabelFrame(win, text='자판기')
mighfy.grid(column=0, row=0)

## 과자의 종류를 담는 배열
snacks = ['새우', '감자', '오징어', '버터', '딸기', '오렌지']

## 구매버튼을 클릭했을 때 동작을 구성한 콜백 함수
def purchase():
    index = radioVar.get()
    snackList.append(snacks[index])

    messageLabel.configure(text=snacks[index] + ' 과자를 샀다!')
    
# 무엇을 구매했는지를 알려주기 위한 Label
messageLabel = ttk.Label(mighfy, text="Click the Purchase!")
messageLabel.grid(column=0, row=3)

# 구매 버튼 생성
purchaseButton = ttk.Button(mighfy, text="Purchase!", command=purchase)
purchaseButton.grid(column=3, row=3)

# 라디오 버튼에 바인딩할 정수타입의 변수
radioVar = tk.IntVar()

radioVar.set(99)

# 2중 loop를 이용하여 라디오 버튼 생성
for ro in range(2):
    for col in range(3):
        #2차원 배열의 index를 계산
        index = ro + (col + (ro * 2))

        # 라디오 버튼 생성
        currentRadioButton = tk.Radiobutton(mighfy, text=snacks[index], variable=radioVar, value=index)
        currentRadioButton.grid(column=col, row=ro, sticky=tk.W)
        
        create_ToolTip(currentRadioButton, snacks[index] + '과자입니다.')

# for loop를 이용하여 컴포넌트들을 모두 정렬
for child in mighfy.winfo_children():
    child.grid_configure(sticky='E')
    

# 메인 루프 시작
win.mainloop()


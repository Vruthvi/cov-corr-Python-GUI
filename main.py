import customtkinter as tk
import pandas as pd
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import seaborn as sns

root=tk.CTk()
root.geometry("800x700")
root.title("Covariance and Correlation Matrix for a Dataset")
tk.set_appearance_mode("dark")
tk.set_default_color_theme("blue")

frame1=tk.CTkFrame(root,fg_color="transparent")
frame1.pack(side="top",anchor="center",pady=14)

frame2=tk.CTkFrame(root,fg_color="transparent")
frame2.pack(side="top",anchor="center",pady=14)

container_frame = tk.CTkFrame(root, fg_color="transparent")
container_frame.pack(side="left", anchor="nw", pady=16, padx=25, fill="both", expand=False)

frame3 = tk.CTkFrame(container_frame, fg_color="transparent")
frame3.pack(side="top", anchor="w", pady=8, padx=5)

frame5 = tk.CTkFrame(container_frame,fg_color="transparent")
frame5.pack(side="bottom", anchor="w", pady=8, padx=5)

frame4=tk.CTkFrame(root,fg_color="transparent") 
frame4.pack(side="top",anchor="center",pady=16)

global data

def button(frame,text,command):
    button=tk.CTkButton(frame,text=text,font=("Arial",16),command=command)
    button.pack(pady=8,padx=5,anchor="w")
    return button

def sub_label(frame,text):
    sub_label=tk.CTkLabel(frame,text=text,font=("Arial",14))
    sub_label.pack(anchor="w")

def load_dataset_file():
    global data
    file_path = filedialog.askopenfilename(
        title="Open CSV File",
        filetypes=[("CSV Files", "*.csv")]
    )
    if file_path:
        try:
            for widget in frame2.winfo_children():
                if isinstance(widget, tk.CTkLabel):
                    widget.destroy()
                    
            for widget in frame4.winfo_children():
                widget.destroy()
            
            file_label=tk.CTkLabel(frame2,text=(f"Loaded : ' {file_path} '"),font=("Arial",16,"bold"))
            file_label.pack(side="left",pady=2,padx=5)
            data=pd.read_csv(file_path)
            cat1=data.columns
            cat2=data.columns
            first_col.set("No Data Selected")
            second_col.set("No Data Selected")
            first_col.configure(values=list(cat1))
            second_col.configure(values=list(cat2))
                 
        except Exception as e:
            file_error=tk.CTkLabel(frame2,text=e,font=("Arial",16))
            file_error.pack(pady=5)
    
def get_scatter():
    global data
    col1=first_col.get()
    col2=second_col.get()

    fig, ax = plt.subplots(figsize=(15, 8))
    ax.scatter(data[col1], data[col2], alpha=0.7, color="teal")
    ax.set_title(f"Scatter Plot: {col1} vs {col2}")
    ax.set_xlabel(col1)
    ax.set_ylabel(col2)
    ax.grid()

    for widget in frame4.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame4)
    canvas.draw()
    toolbar = NavigationToolbar2Tk(canvas, frame4)
    toolbar.update()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    toolbar.pack()

def get_heatmap():
    global data
    data_numeric = data.apply(pd.to_numeric, errors='coerce')
    data_numeric = data_numeric.dropna(axis=1, how='all')
    corr_matrix = data_numeric.corr()

    fig, ax = plt.subplots(figsize=(15, 8))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
    ax.set_title("Correlation Heatmap")

    for widget in frame4.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame4)
    canvas.draw()
    toolbar=NavigationToolbar2Tk(canvas,frame4)
    toolbar.update()
    toolbar.pack()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def create_table(matrix, frame):
    for widget in frame.winfo_children():
        widget.destroy()

    canvas = tk.CTkCanvas(frame, borderwidth=0, width=950,height=550,bg="black")
    scroll_y = tk.CTkScrollbar(frame, orientation="vertical", command=canvas.yview)
    scroll_x = tk.CTkScrollbar(frame, orientation="horizontal", command=canvas.xview)
    
    matrix_frame = tk.CTkFrame(canvas,fg_color="black")

    canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=matrix_frame, anchor="nw")

    for j, col in enumerate([''] + matrix.columns.tolist()):
        label = tk.CTkLabel(matrix_frame, text=col, font=("Arial", 13, "bold"),text_color="white", padx=5, pady=5)
        label.grid(row=0, column=j, sticky="nsew", padx=1, pady=2)

    for i, index in enumerate(matrix.index.tolist()):
        for j, value in enumerate([index] + matrix.loc[index].tolist()):
            label = tk.CTkLabel(matrix_frame, text=value, font=("Arial", 13),text_color="white", padx=5, pady=5)
            label.grid(row=i+1, column=j, sticky="nsew", padx=1, pady=3)

    for i in range(len(matrix.columns) + 1):
        matrix_frame.grid_columnconfigure(i, weight=1)
    for i in range(len(matrix.index) + 1):
        matrix_frame.grid_rowconfigure(i, weight=1)

    matrix_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def get_covariance():
    global data
    data_numeric = data.apply(pd.to_numeric, errors='coerce').dropna(axis=1, how='all')
    cov_matrix = data.cov(numeric_only=True)
    create_table(cov_matrix, frame4)

def get_correlation():
    global data
    # data_numeric = data.apply(pd.to_numeric, errors='coerce').dropna(axis=1, how='all')
    # corr_matrix = data_numeric.corr()
    corr_matrix = data.corr(numeric_only=True)
    create_table(corr_matrix, frame4)

def change_theme():
    if tk.get_appearance_mode().lower()=="dark":
        tk.set_appearance_mode("light")
        theme_btn.configure(fg_color="black",hover_color="black",text_color="white")
    else:
        tk.set_appearance_mode("dark")
        theme_btn.configure(fg_color="white",hover_color="white",text_color="black")

head_label=tk.CTkLabel(frame1,text="Covariance and Correlation Matrix for a Dataset",font=("Times New Roman bold",22))
head_label.pack()

load_btn=button(frame2,"Load Dataset",load_dataset_file)
load_btn.pack(side="left")

sub_label(frame3,"Select the First Column:")
first_col=tk.CTkOptionMenu(frame3,values=["No Data Selected"],font=("Arial",16))
first_col.pack(pady=5,anchor="w")

sub_label(frame3,"Select the Second Column:")
second_col=tk.CTkOptionMenu(frame3,values=["No Data Selected"],font=("Arial",16))
second_col.pack(pady=5,anchor="w")

matrix=tk.CTkLabel(frame4,text="",font=("Arial bold",16))
matrix.pack(side="left",anchor="ne")

sub_label(frame3,"Select the Operations Below:")

button(frame3,"Get Scatter",get_scatter)

button(frame3,"Get Heatmap",get_heatmap)

button(frame3,"Get Covariance Matrix",get_covariance)

button(frame3,"Get Correlation Matrix",get_correlation)

quit_btn=button(frame5,"Quit",command=root.destroy)
quit_btn.pack(side="bottom",anchor="se")
quit_btn.configure(fg_color="red",hover_color="red")

theme_btn=button(frame5,"Change Theme",command=change_theme)
theme_btn.pack(anchor="sw",side="bottom")
theme_btn.configure(fg_color="white",text_color="black",hover_color="white")



root.mainloop()
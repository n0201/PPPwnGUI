import customtkinter as tk
import psutil
import subprocess
import threading
import os

stage2_selected = False

class App(tk.CTk):
    def __init__(self):
        super().__init__()
        
        global stage2_selected

        self.title("PPPwn GUI - n0201")
        self.geometry("350x350")

        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure((0, 1), weight=1)

        self.label_file = tk.CTkEntry(master=self, placeholder_text="No file selected")
        self.label_file.configure(state="disabled")
        self.label_file.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        def get_file():
            global stage2_selected
            stage2_selected = True
            filename = tk.filedialog.askopenfilename()
            self.label_file.configure(state="normal")
            self.label_file.delete(0, tk.END)
            self.label_file.insert(0, filename)
        
        self.choose_button = tk.CTkButton(self, fg_color="transparent", border_width=2, command=get_file, text="choose stage2.bin")
        self.choose_button.grid(row=0, column=1, padx=20, pady=20, sticky="ew")

        interfaces = psutil.net_if_addrs().keys()
        output_list = list(interfaces)

        self.placeholder_label = tk.CTkLabel(self, text="")
        self.placeholder_label.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

        self.optionmenu_1 = tk.CTkOptionMenu(self, dynamic_resizing=True,
                                                        values=output_list)
        self.optionmenu_1.set("choose interface")
        self.optionmenu_1.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

        self.optionmenu_2 = tk.CTkOptionMenu(self, dynamic_resizing=True,
                                                        values=["900", "950", "1000", "1050", "1100"])
        self.optionmenu_2.set("choose firmware")
        self.optionmenu_2.grid(row=2, column=1, padx=20, pady=20, sticky="ew")

        def exploit_window():
            p = subprocess.Popen("python pppwn\pppwn.py --interface=\""+self.optionmenu_1.get()+"\" --fw="+self.optionmenu_2.get()+" --stage2=\""+self.label_file.get()+"\" --stage1=pppwn\stage1\stage1_"+self.optionmenu_2.get()+".bin", stdout=subprocess.PIPE, shell=True, universal_newlines=True, encoding="utf-8")

            out_window = tk.CTkToplevel(self)
            out_window.title("Jailbreak output")
            out_window.geometry("450x350")
            textbox = tk.CTkTextbox(out_window)
            textbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            while True:
                realtime_output = p.stdout.readline()

                if realtime_output == '' and p.poll() is not None:
                    break

                if realtime_output:
                    textbox.insert(tk.END, realtime_output)
                    self.update()


        def run_exploit():
            if stage2_selected == True:
                threading.Thread(exploit_window()).start()
            else:
                error_window = tk.CTkToplevel(self)
                error_window.title("ERROR")
                error_window.geometry("350x100")
                tk.CTkLabel(error_window, text ="Did you choose the \"stage2.bin\" file?").pack()

        self.exploit_button = tk.CTkButton(self, text="Run exploit", command=run_exploit)
        self.exploit_button.grid(row=3, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

        self.credits_label = tk.CTkLabel(self, text="UI was made with ❤ from n0201 on git")
        self.credits_label.grid(row=4, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

if __name__ == "__main__":
    app = App()
    app.mainloop()
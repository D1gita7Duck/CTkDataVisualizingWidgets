import customtkinter as ctk
import calendar
from datetime import datetime
import CTkToolTip.CTkToolTip.ctk_tooltip as tt


class CTkCalendar(ctk.CTkFrame):
    def __init__(self, master,
                 today_fg_color=None,
                 today_text_color=None,
                 width=300,
                 height=300,
                 fg_color=None,
                 corner_radius=8,
                 border_width=None,
                 border_color=None,
                 bg_color="transparent",
                 background_corner_colors=None,
                 date_highlight_color = None,
                 title_bar_fg_color=None,
                 title_bar_border_width=None,
                 title_bar_border_color=None,
                 title_bar_corner_radius=None,
                 title_bar_text_color=None,
                 title_bar_button_fg_color=None,
                 title_bar_button_hover_color=None,
                 title_bar_button_text_color=None,
                 title_bar_button_border_width=None,
                 title_bar_button_border_color=None,
                 calendar_fg_color=None,
                 calendar_border_width=None,
                 calendar_border_color=None,
                 calendar_corner_radius=None,
                 calendar_text_color=None,
                 calendar_text_fg_color=None,
                 calendar_days_fg_color=None,
                 calendar_dates_state="normal",
                 calendar_dates_command=None,
                 calendar_monday_first = False,
                 calendar_btns_pad=1,
                 show_tooltips : bool = True):
        """
        Calendar widget to display certain month, each day is rendered as Button.\n
        If you do not define today_fg_color, today_text_color and date_highlight_color it will be rendered as other days.\n
        Default format for a week is Sun ... Sat. Can be changed to Mon ... Sun by passing calendar_monday_first=True\n
        """
        super().__init__(master=master,
                         width=width,
                         height=height,
                         fg_color=fg_color,
                         corner_radius=corner_radius,
                         border_width=border_width,
                         border_color=border_color,
                         bg_color=bg_color,
                         background_corner_colors=background_corner_colors)

        # data
        self.today_text_color = today_text_color
        self.today_fg_color = today_fg_color
        self.date_highlight_color = date_highlight_color
        self.highlighted_btn : ctk.CTkButton = None
        self.today = self.current_date()
        self.day, self.month, self.year = self.today[:]
        self.months_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        self.labels_by_date = dict()
        self.month_var = ctk.StringVar(value=calendar.month_name[self.month][0:3])
        self.year_var = ctk.StringVar(value=self.year)
        self.show_tooltips = show_tooltips

        # data for title bar
        self.title_bar_fg_color = title_bar_fg_color
        self.title_bar_border_width = title_bar_border_width
        self.title_bar_border_color = title_bar_border_color
        self.title_bar_text_color = title_bar_text_color
        self.title_bar_button_fg_color = title_bar_button_fg_color
        self.title_bar_button_hover_color = title_bar_button_hover_color
        self.title_bar_button_text_color = title_bar_button_text_color
        self.title_bar_button_border_width = title_bar_button_border_width
        self.title_bar_button_border_color = title_bar_button_border_color
        self.title_bar_corner_radius = title_bar_corner_radius

        # data for calendar frame
        self.calendar_fg_color = calendar_fg_color
        self.calendar_border_width = calendar_border_width
        self.calendar_border_color = calendar_border_color
        self.calendar_corner_radius = calendar_corner_radius
        self.calendar_text_fg_color = calendar_text_fg_color
        self.calendar_text_color = calendar_text_color
        self.calendar_days_fg_color = calendar_days_fg_color
        self.calendar_dates_state = calendar_dates_state
        self.calendar_dates_command = calendar_dates_command
        self.calendar_btns_pad = calendar_btns_pad
        self.calendar_monday_first = calendar_monday_first

        # creating header and calendar frames
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent", width=width, height=height)
        self.content_frame.pack(expand=True, fill="both", padx=corner_radius/3, pady=corner_radius/3)
        self.setup_header_frame()
        self.create_calendar_frame()
        self.create_bindings()

        if self.show_tooltips:
            self.create_tooltips()

    # setting up the header frame
    def setup_header_frame(self):
        self.header_frame = ctk.CTkFrame(self.content_frame, fg_color=self.title_bar_fg_color,
                                    corner_radius=self.title_bar_corner_radius,
                                    border_color=self.title_bar_border_color, border_width=self.title_bar_border_width)
        
        self.header_frame.month_option_menu = ctk.CTkOptionMenu(master=self.header_frame,
                                              width=30,
                                              height=30,
                                              values=self.months_list,
                                              variable=self.month_var,
                                              command=self.change_month_from)
        self.header_frame.month_option_menu.pack(side="left", padx=(10,15))

        self.header_frame.previous_year_btn = ctk.CTkButton(self.header_frame,
                                          text="<",
                                          width=25,
                                          fg_color=self.title_bar_button_fg_color,
                                          hover_color=self.title_bar_button_hover_color,
                                          border_color=self.title_bar_button_border_color,
                                          border_width=self.title_bar_button_border_width,
                                          font=ctk.CTkFont("Arial", 11, "bold"),
                                          command=lambda: self.change_month(-12))
        self.header_frame.previous_year_btn.pack(side="left", padx=(5,5))

        self.header_frame.year_entry = ctk.CTkEntry(master=self.header_frame, width=45, height=30, textvariable=self.year_var)
        self.header_frame.year_entry.pack(side="left", padx=(0,5))
        
        self.header_frame.next_year_btn = ctk.CTkButton(self.header_frame, text=">", width=25, fg_color=self.title_bar_button_fg_color,
                      hover_color=self.title_bar_button_hover_color, border_color=self.title_bar_button_border_color,
                      border_width=self.title_bar_button_border_width, font=ctk.CTkFont("Arial", 11, "bold"),
                      command=lambda: self.change_month(12))
        self.header_frame.next_year_btn.pack(side="left", padx=(0, 10))

        self.header_frame.today_btn = ctk.CTkButton(self.header_frame, text="Today", width=60, fg_color=self.title_bar_button_fg_color,
                      hover_color=self.title_bar_button_hover_color, border_color=self.title_bar_button_border_color,
                      border_width=self.title_bar_button_border_width, font=ctk.CTkFont("Arial", 13, "bold"),
                      command=self.go_to_today)
        self.header_frame.today_btn.pack(side="right", padx=(10,10))

        self.header_frame.place(relx=0.5, rely=0.02, anchor="n", relheight=0.18, relwidth=0.95)

    def create_calendar_frame(self):
        # "updating" frames
        calendar_frame = ctk.CTkFrame(self.content_frame, fg_color=self.calendar_fg_color,
                                      corner_radius=self.calendar_corner_radius,
                                      border_width=self.calendar_border_width, border_color=self.calendar_border_color)
        current_month = calendar.monthcalendar(self.year, self.month)

        # grid
        calendar_frame.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform="b")
        rows = tuple([i for i in range(len(current_month)+1)])
        calendar_frame.rowconfigure(rows, weight=1, uniform="b")

        # labels for dates
        if self.calendar_monday_first:
            # labels for days of the week
            self.setup_days_of_week_label(calendar_frame, row=0, monday_first = True)

            for row in range(len(current_month)):
                for column in range(7):
                    if current_month[row][column] != 0:
                        self.setup_button_normal(calendar_frame, current_month[row][column], row+1, column)
        else:
            # labels for days of the week
            self.setup_days_of_week_label(calendar_frame, row=0, monday_first = False)
            formatted_month = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
            
            for date_row in current_month[3:]:
                for t in date_row:
                    if (t == 0) : break
                    max_month_date = t
                else:
                    continue
                break
            i=0
            while (i<7):
                if (current_month[0][i] == 1):
                    break
                i += 1
            i = (i+1)%7

            row = 0
            column = i
            date = 1
            while (row<5):
                column %= 7
                while (column<7):
                    if (date > max_month_date):
                        break
                    formatted_month[row][column] = date
                    date += 1
                    column += 1
                else:
                    row += 1
                    continue
                break

            # print(formatted_month)
            for row in range(len(formatted_month)):
                for column in range(7):
                    if formatted_month[row][column] != 0:
                        self.setup_button_normal(calendar_frame, formatted_month[row][column], row+1, column)

        calendar_frame.place(relx=0.5, rely=0.97, anchor="s", relheight=0.75, relwidth=0.95)

    def change_month(self, amount):
        self.month += amount
        if self.month < 1:
            self.year -= ((12 + (-amount) - 1) //12)
            self.month = 12 - ((-self.month)%12)
            self.day = 1
        elif self.month > 12:
            self.year += (amount//12) if (amount//12) > 0 else 1
            self.month =  12 if (self.month%12 == 0) else self.month%12
            self.day = 1

        self.month_var.set(calendar.month_name[self.month][0:3])
        self.year_var.set(str(self.year))

        self.create_calendar_frame()

    def change_month_from(self, month : str):
        self.month_var.set(month)
        self.month = self.months_list.index(month) + 1
        self.create_calendar_frame()
    
    def change_year_from(self, event = None):
        if int(self.year_var.get()) < 1:
            raise ValueError("Given year doesn't exist even though calendar module provides it")
        self.year = int(self.year_var.get())
        self.create_calendar_frame()
    
    def go_to_today(self):
        self.month, self.year = self.current_date()[1:]
        self.month_var.set(calendar.month_name[self.month][0:3])
        self.year_var.set(str(self.year))
        self.create_calendar_frame()

    def go_to_today2(self):
        today_month, today_year = self.current_date()[1:]
        # print(today_month, today_year, self.month, self.year, end=' ** ')
        del_month = today_month-self.month
        del_year = self.year - today_year
        delta = ((del_year*12)-(del_month))
        self.change_month(-delta)

    def current_date(self) -> tuple[int, int, int]:
        date = str(datetime.now()).split()
        year, month, day = date[0].split("-")
        return int(day), int(month), int(year)

    def date_is_today(self, date: tuple) -> bool:
        if date[2] == self.today[2] and date[1] == self.today[1] and date[0] == self.today[0]:
            return True
        return False

    def on_date_click(self, button : ctk.CTkButton, btn_state : str, date : int):
        if btn_state != "disabled":
            if self.highlighted_btn is not None:
                self.highlighted_btn.configure(fg_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"])
            if self.date_highlight_color is not None:
                button.configure(fg_color = self.date_highlight_color)
            self.highlighted_btn = button
            if self.calendar_dates_command is not None:
                self.calendar_dates_command(date, self.month, self.year)

    # creating normal date labels for normal calendar
    def setup_button_normal(self, frame, day, row, column):
        if self.today_fg_color is not None and self.date_is_today((day, self.month, self.year)):
            btn = ctk.CTkButton(frame, text=str(day), corner_radius=5,
                         fg_color=self.today_fg_color, font=ctk.CTkFont("Arial", 11),
                         text_color=self.today_text_color, state=self.calendar_dates_state,
                         command=lambda : self.on_date_click(btn, self.calendar_dates_state, day))
            btn.grid(row=row, column=column, sticky="nsew", padx=self.calendar_btns_pad, pady=self.calendar_btns_pad)
            

        else:
            btn = ctk.CTkButton(frame, text=str(day), corner_radius=5,
                         fg_color=self.calendar_text_fg_color, font=ctk.CTkFont("Arial", 11),
                         text_color=self.calendar_text_color, state=self.calendar_dates_state,
                         command=lambda : self.on_date_click(btn, self.calendar_dates_state, day))
            btn.grid(row=row, column=column, sticky="nsew", padx=self.calendar_btns_pad, pady=self.calendar_btns_pad)

    def setup_days_of_week_label(self, frame, row : int, monday_first : bool):
        if monday_first:
            self.days_of_week = ("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su")
        else:
            self.days_of_week = ("Su", "Mo", "Tu", "We", "Th", "Fr", "Sa")
        for column in range(7):
            ctk.CTkLabel(frame, text=str(self.days_of_week[column]), corner_radius=5,
                            fg_color=self.calendar_days_fg_color, font=ctk.CTkFont("Arial", 11),
                            text_color=self.calendar_text_color).grid(row=row, column=column, sticky="nsew",
                                                                    padx=self.calendar_btns_pad,
                                                                    pady=self.calendar_btns_pad)
    
    def create_bindings(self):
        self.master.bind("<1>", lambda event: event.widget.focus_set(), add=True)
        self.header_frame.year_entry.bind("<Return>", self.change_year_from)

    def create_tooltips(self):
        tt.CTkToolTip(widget=self.header_frame.month_option_menu, message="Choose Month", delay=0.1)
        tt.CTkToolTip(widget=self.header_frame.previous_year_btn, message="Previous Year", delay=0.1)
        tt.CTkToolTip(widget=self.header_frame.year_entry, message="Input Year and Press Enter", delay=0.1)
        tt.CTkToolTip(widget=self.header_frame.next_year_btn, message="Next Year", delay=0.1)
        tt.CTkToolTip(widget=self.header_frame.today_btn, message="Go to Today", delay=0.1)
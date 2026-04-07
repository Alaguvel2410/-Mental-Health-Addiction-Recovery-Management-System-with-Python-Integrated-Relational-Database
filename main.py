import tkinter as tk
from tkinter import messagebox
from user import register_user
from assessment import create_assessment, get_questions, get_options, save_response
from result import get_result
from database import check_admin, get_connection
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ─── MAIN WINDOW ───
root = tk.Tk()
root.title("Addiction Recovery System")
root.geometry("1100x700")
root.configure(bg="#1a1a2e")

questions = []
options = []
current_question = 0
assessment_id = None
selected_option = None

# ─── COLOR THEME ───
BG = "#1a1a2e"
CARD = "#16213e"
ACCENT = "#0f3460"
BTN1 = "#e94560"
BTN2 = "#0f3460"
WHITE = "#ffffff"
YELLOW = "#f5a623"
GREEN = "#4cd964"
GRAY = "#aaaaaa"

# ─── FRAMES ───
frame_register = tk.Frame(root, bg=BG)
frame_questions = tk.Frame(root, bg=BG)
frame_result = tk.Frame(root, bg=BG)
frame_admin_login = tk.Frame(root, bg=BG)
frame_analysis = tk.Frame(root, bg=BG)


# ─── HELPER FUNCTIONS ───
def make_label(frame, text, size=13, color=WHITE, bold=False):
    font = ("Arial", size, "bold") if bold else ("Arial", size)
    tk.Label(frame, text=text, font=font, bg=BG, fg=color).pack(pady=5)


def make_entry(frame, show=None):
    e = tk.Entry(frame, width=30, font=("Arial", 13), bg=CARD, fg=WHITE,
                 insertbackground=WHITE, relief="flat", bd=8,
                 show=show if show else "")
    e.pack(pady=8)
    return e


def make_button(frame, text, command, color=BTN1):
    tk.Button(frame, text=text, command=command,
              font=("Arial", 13, "bold"), bg=color, fg=WHITE,
              width=22, height=2, relief="flat", cursor="hand2").pack(pady=8)


# ─── REGISTRATION SCREEN ───
def show_register():
    frame_questions.pack_forget()
    frame_result.pack_forget()
    frame_admin_login.pack_forget()
    frame_analysis.pack_forget()
    frame_register.pack(fill="both", expand=True)


def submit_register():
    name = entry_name.get()
    age = entry_age.get()
    ph_no = entry_phone.get()
    addiction = entry_addiction.get()
    if not name or not age or not ph_no or not addiction:
        messagebox.showerror("Error", "Please fill all fields!")
        return
    user_id = register_user(name, int(age), ph_no, addiction)
    global assessment_id
    assessment_id = create_assessment(user_id)
    show_questions()

# Registration Widgets
tk.Label(frame_register, text="🧠 Addiction Recovery System",
         font=("Arial", 20, "bold"), bg=BG, fg=YELLOW).pack(pady=30)
tk.Label(frame_register, text="User Registration",
         font=("Arial", 15, "bold"), bg=BG, fg=WHITE).pack(pady=5)
tk.Label(frame_register, text="Name:", font=("Arial", 13), bg=BG, fg=GRAY).pack()
entry_name = make_entry(frame_register)
tk.Label(frame_register, text="Age:", font=("Arial", 13), bg=BG, fg=GRAY).pack()
entry_age = make_entry(frame_register)
tk.Label(frame_register, text="Phone Number:", font=("Arial", 13), bg=BG, fg=GRAY).pack()
entry_phone = make_entry(frame_register)
tk.Label(frame_register, text="Type of Addiction:", font=("Arial", 13), bg=BG, fg=GRAY).pack()
entry_addiction = make_entry(frame_register)
make_button(frame_register, "▶ Start Assessment", submit_register, BTN1)
make_button(frame_register, "🔐 Admin Login", lambda: show_admin_login(), BTN2)


# ─── QUESTIONS SCREEN ───
def show_questions():
    global questions, options, current_question, selected_option
    questions = get_questions()
    options = get_options()
    current_question = 0
    selected_option = tk.IntVar()
    frame_register.pack_forget()
    frame_result.pack_forget()
    frame_questions.pack(fill="both", expand=True)
    load_question()


def load_question():
    for widget in frame_questions.winfo_children():
        widget.destroy()
    global selected_option
    selected_option = tk.IntVar()
    q_number = current_question + 1
    q_text = questions[current_question][1]
    q_id = questions[current_question][0]

    tk.Label(frame_questions, text="🧠 Addiction Recovery System",
             font=("Arial", 20, "bold"), bg=BG, fg=YELLOW).pack(pady=20)
    tk.Label(frame_questions, text="Question " + str(q_number) + " of " + str(len(questions)),
             font=("Arial", 20, "bold"), bg=BG, fg=GREEN).pack(pady=5)
    tk.Label(frame_questions, text=q_text, wraplength=480,
             font=("Arial", 20), bg=BG, fg=WHITE).pack(pady=15)

    for option in options:
        tk.Radiobutton(
            frame_questions,
            text=option[1],
            variable=selected_option,
            value=option[0],
            font=("Arial", 16, "bold"),
            bg=BG, fg=WHITE,
            selectcolor=ACCENT,
            activebackground=BG,
            activeforeground=YELLOW,
            padx=500, pady=10,
            anchor="w", justify="center"
        ).pack(fill="x", pady=6)

    tk.Button(frame_questions, text="Next →",
              command=lambda: next_question(q_id),
              font=("Arial", 13, "bold"), bg=BTN1, fg=WHITE,
              width=22, height=2, relief="flat", cursor="hand2").pack(pady=25)


def next_question(q_id):
    global current_question
    if selected_option.get() == 0:
        messagebox.showerror("Error", "Please select an option!")
        return
    save_response(assessment_id, q_id, selected_option.get())
    current_question += 1
    if current_question < len(questions):
        load_question()
    else:
        show_result()


# ─── RESULT SCREEN ───
def show_result():
    frame_questions.pack_forget()
    frame_result.pack(fill="both", expand=True)
    for widget in frame_result.winfo_children():
        widget.destroy()
    result = get_result(assessment_id)
    tk.Label(frame_result, text="✅ Assessment Complete!",
             font=("Arial", 20, "bold"), bg=BG, fg=GREEN).pack(pady=25)
    tk.Label(frame_result, text="Total Score : " + str(result[0]) + " / 80",
             font=("Arial", 15, "bold"), bg=BG, fg=YELLOW).pack(pady=10)
    tk.Label(frame_result, text="Addiction Level : " + str(result[1]),
             font=("Arial", 15, "bold"), bg=BG, fg=BTN1).pack(pady=10)
    tk.Label(frame_result, text="💡 Tips : " + str(result[3]),
             wraplength=480, font=("Arial", 13), bg=BG, fg=WHITE).pack(pady=10)
    tk.Label(frame_result,
             text="⚠️ Disclaimer : This is only a self-assessment\n"
                  "test. It is NOT a medical diagnosis.\n"
                  "Please consult a professional counselor\n"
                  "for proper guidance and support.",
             wraplength=480, font=("Arial", 11, "italic"), bg=BG, fg=GRAY).pack(pady=15)
    tk.Button(frame_result, text="🔄 New Assessment",
              command=show_register, font=("Arial", 13, "bold"),
              bg=BTN2, fg=WHITE, width=22, height=2,
              relief="flat", cursor="hand2").pack(pady=20)


# ─── ADMIN LOGIN SCREEN ───
def show_admin_login():
    frame_register.pack_forget()
    frame_analysis.pack_forget()
    frame_admin_login.pack(fill="both", expand=True)


def submit_admin_login():
    username = entry_admin_user.get()
    password = entry_admin_pass.get()
    if check_admin(username, password):
        show_analysis()
    else:
        messagebox.showerror("Error", "Invalid username or password!")


tk.Label(frame_admin_login, text="🔐 Admin Login",
         font=("Arial", 20, "bold"), bg=BG, fg=YELLOW).pack(pady=40)
tk.Label(frame_admin_login, text="Username:", font=("Arial", 13), bg=BG, fg=GRAY).pack()
entry_admin_user = make_entry(frame_admin_login)
tk.Label(frame_admin_login, text="Password:", font=("Arial", 13), bg=BG, fg=GRAY).pack()
entry_admin_pass = make_entry(frame_admin_login, show="*")
make_button(frame_admin_login, "🔓 Login", submit_admin_login, BTN1)
make_button(frame_admin_login, "← Back", show_register, BTN2)


# ─── ANALYSIS SCREEN ───
def show_analysis():
    frame_admin_login.pack_forget()
    frame_analysis.pack(fill="both", expand=True)

    for widget in frame_analysis.winfo_children():
        widget.destroy()

    # ── DASHBOARD LAYOUT — Stats Left | Chart Right ──
    main_container = tk.Frame(frame_analysis, bg=BG)
    main_container.pack(expand=True, fill="both", padx=20, pady=20)

    # ── STATS PANEL — 45% Left Side ──
    left_frame = tk.Frame(main_container, bg=BG, width=499)
    left_frame.pack(side="left", fill="both")
    left_frame.pack_propagate(False)

    canvas = tk.Canvas(left_frame, bg=BG, highlightthickness=0)
    scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=BG)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    content_frame = tk.Frame(scroll_frame, bg=BG)
    content_frame.pack(expand=True)

    # ── CENTER DIVIDER ──
    tk.Frame(main_container, bg=ACCENT, width=2).pack(side="left", fill="y", padx=5)

    # ── CHART PANEL — 55% Right Side ──
    right_frame = tk.Frame(main_container, bg=BG, width=601)
    right_frame.pack(side="right", fill="both", expand=True)
    right_frame.pack_propagate(False)

    # ── Title ──
    tk.Label(content_frame, text="📊 Admin Analysis Dashboard",
             font=("Arial", 20, "bold"), bg=BG, fg=YELLOW).pack(pady=20)

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SET SQL_SAFE_UPDATES=0;")
        except Exception:
            pass

        # ── Stats Container ──
        stats_container = tk.Frame(content_frame, bg=BG)
        stats_container.pack(pady=20)

        # ── Total Users ──
        cursor.execute("SELECT COUNT(*) AS total_users FROM users;")
        total_users_row = cursor.fetchone()
        total_users = total_users_row[0] if total_users_row and total_users_row[0] is not None else 0
        tk.Label(stats_container, text="👥 Total Users : " + str(total_users),
                 font=("Arial", 13, "bold"), bg=BG, fg=GREEN).pack(pady=6)

        # ── Highest Score ──
        cursor.execute("SELECT MAX(total_score) AS highest_score FROM results;")
        high_row = cursor.fetchone()
        high = high_row[0] if high_row and high_row[0] is not None else 0
        tk.Label(stats_container, text="📈 Highest Score : " + str(high) + " / 80",
                 font=("Arial", 13, "bold"), bg=BG, fg=WHITE).pack(pady=6)

        # ── Lowest Score ──
        cursor.execute("SELECT MIN(total_score) AS minimum_score FROM results;")
        low_row = cursor.fetchone()
        low = low_row[0] if low_row and low_row[0] is not None else 0
        tk.Label(stats_container, text="📉 Lowest Score : " + str(low) + " / 80",
                 font=("Arial", 13, "bold"), bg=BG, fg=WHITE).pack(pady=6)

        # ── Average Score ──
        cursor.execute("SELECT AVG(total_score) AS average_score FROM results;")
        avg_row = cursor.fetchone()
        avg = avg_row[0] if avg_row and avg_row[0] is not None else 0.0
        try:
            avg_display = str(round(float(avg), 2))
        except Exception:
            avg_display = "0.00"
        tk.Label(stats_container, text="📊 Average Score : " + avg_display + " / 80",
                 font=("Arial", 13, "bold"), bg=BG, fg=WHITE).pack(pady=6)

        # ── Total Tests Taken ──
        cursor.execute("SELECT COUNT(*) AS total_tests_taken FROM assessment;")
        total_tests_row = cursor.fetchone()
        total_tests = total_tests_row[0] if total_tests_row and total_tests_row[0] is not None else 0
        tk.Label(stats_container, text="📝 Total Tests Taken : " + str(total_tests),
                 font=("Arial", 13, "bold"), bg=BG, fg=WHITE).pack(pady=6)

        # ── Divider ──
        tk.Frame(content_frame, bg=ACCENT, height=2).pack(fill="x", pady=(20, 10))

        # ── Users per Addiction Type ──
        cursor.execute("""
            SELECT type_of_addiction, COUNT(*) AS users 
            FROM users 
            GROUP BY type_of_addiction;
        """)
        addiction_types = cursor.fetchall()
        tk.Label(content_frame, text="🧩 Users per Addiction Type",
                 font=("Arial", 14, "bold"), bg=BG, fg=YELLOW).pack(pady=(10, 6))

        addiction_container = tk.Frame(content_frame, bg=BG)
        addiction_container.pack(pady=10)

        if addiction_types:
            for addiction_type, count in addiction_types:
                at_text = addiction_type if addiction_type is not None else "Unknown"
                row = tk.Frame(addiction_container, bg=CARD, bd=0, relief="flat")
                row.pack(fill="x", pady=4, padx=20, ipadx=10, ipady=6)
                tk.Label(row, text=" " + at_text, font=("Arial", 12, "bold"),
                         bg=CARD, fg=WHITE, anchor="w").pack(side="left")
                tk.Label(row, text=str(count) + " ", font=("Arial", 12, "bold"),
                         bg=CARD, fg=GREEN, anchor="e").pack(side="right")
        else:
            tk.Label(addiction_container, text="No data available",
                     font=("Arial", 12), bg=BG, fg=GRAY).pack(pady=4)

        # ── Divider ──
        tk.Frame(content_frame, bg=ACCENT, height=2).pack(fill="x", pady=(20, 10))

        # ── Addiction Level Distribution ──
        cursor.execute("""
            SELECT addiction_level, COUNT(*) AS number_of_users 
            FROM results 
            GROUP BY addiction_level;
        """)
        addiction_levels = cursor.fetchall()
        tk.Label(content_frame, text="📊 Addiction Level Distribution",
                 font=("Arial", 14, "bold"), bg=BG, fg=YELLOW).pack(pady=(10, 6))

        level_container = tk.Frame(content_frame, bg=BG)
        level_container.pack(pady=10)

        level_colors = {
            "Low Addiction": "#4cd964",
            "Moderate Addiction": "#f5a623",
            "High Addiction": "#e94560",
            "Severe Addiction": "#ff2d55",
        }

        if addiction_levels:
            for level, count in addiction_levels:
                level_text = level if level is not None else "Unknown"
                level_color = level_colors.get(level_text, WHITE)
                row = tk.Frame(level_container, bg=CARD, bd=0, relief="flat")
                row.pack(fill="x", pady=4, padx=20, ipadx=10, ipady=6)
                tk.Label(row, text=" " + level_text, font=("Arial", 12, "bold"),
                         bg=CARD, fg=level_color, anchor="w").pack(side="left")
                tk.Label(row, text=str(count) + " ", font=("Arial", 12, "bold"),
                         bg=CARD, fg=level_color, anchor="e").pack(side="right")
        else:
            tk.Label(level_container, text="No data available",
                     font=("Arial", 12), bg=BG, fg=GRAY).pack(pady=4)

        # ── PIE CHART ON RIGHT SIDE ──
        tk.Label(right_frame, text="🥧 Addiction Level Chart",
                 font=("Arial", 14, "bold"), bg=BG, fg=YELLOW).pack(pady=(20, 10))

        if addiction_levels:
            labels = []
            sizes = []
            pie_colors = []

            color_map = {
                "Low Addiction": "#4cd964",
                "Moderate Addiction": "#f5a623",
                "High Addiction": "#e94560",
                "Severe Addiction": "#ff2d55",
                "No Addiction": "#00b4d8",
            }

            short_labels = {
                "No Addiction": "No\nAddiction",
                "Low Addiction": "Low\nAddiction",
                "Moderate Addiction": "Moderate\nAddiction",
                "High Addiction": "High\nAddiction",
                "Severe Addiction": "Severe\nAddiction",
            }

            for level, count in addiction_levels:
                level_text = level if level is not None else "Unknown"
                labels.append(short_labels.get(level_text, level_text))
                sizes.append(count)
                pie_colors.append(color_map.get(level_text, "#aaaaaa"))

            fig, ax = plt.subplots(figsize=(6, 6))
            fig.patch.set_facecolor("#1a1a2e")
            ax.set_facecolor("#1a1a2e")

            ax.pie(
                sizes,
                labels=labels,
                colors=pie_colors,
                autopct="%1.1f%%",
                startangle=140,
                radius=0.80,
                pctdistance=0.75,
                labeldistance=1.3,
                textprops={"color": "white", "fontsize": 10.2 , "fontweight": "bold"}
            )
            ax.set_title("Addiction Levels", color="white", fontsize=12)

            chart = FigureCanvasTkAgg(fig, master=right_frame)
            chart.draw()
            chart.get_tk_widget().pack(pady=10)
        else:
            tk.Label(right_frame, text="No data for chart",
                     font=("Arial", 12), bg=BG, fg=GRAY).pack(pady=20)

    except Exception as e:
        tk.Label(content_frame, text="⚠️ Error loading analysis. Check database.",
                 font=("Arial", 12, "bold"), bg=BG, fg=BTN1).pack(pady=10)
        print("Error in show_analysis:", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # ── Back Button ──
    tk.Button(content_frame, text="← Back", command=show_admin_login,
              font=("Arial", 13, "bold"), bg=BTN2, fg=WHITE,
              width=22, height=2, relief="flat", cursor="hand2").pack(pady=30)

    def on_configure(event):
        canvas_width = event.width
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(canvas.create_window((0, 0), window=scroll_frame, anchor="nw"), width=canvas_width)

    canvas.bind("<Configure>", on_configure)


# ─── START APP ───
show_register()
root.mainloop()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实例 3.27 位运算与移位可视化教学演示工具
--------------------------------------------------
专为计算机课程教学设计的轻量、直观可视化工具。
主要特性：
1. 纯 Python 原生 tkinter，零第三方依赖，跨平台即开即用。
2. 界面饱满大气，核心展示区超大字号、消除多余留白，适合投影与屏幕演示。
3. 高对比度选项按钮，彻底解决 macOS/Windows 按钮文字发白看不清的问题。
4. 移位实体墙模型支持输入后“确定”、平滑单步/多步动画推移、撞墙丢弃与补位。
5. 底部对照呈现 Python 移位结果和指定位宽内的低位二进制。
"""

import tkinter as tk
from tkinter import ttk, messagebox


def parse_input_number(text: str):
    """智能解析输入字符串为整数（支持 0b, 0x, 0o, 十进制及负数）"""
    s = text.strip()
    if not s:
        return False, 0, "请输入数字"
    
    is_neg = False
    if s.startswith("-"):
        is_neg = True
        s = s[1:].strip()
    elif s.startswith("+"):
        s = s[1:].strip()

    if not s:
        return False, 0, "格式不完整"

    base = 10
    base_name = "十进制"
    raw = s
    lower_s = s.lower()
    if lower_s.startswith("0b"):
        base = 2
        base_name = "二进制"
        raw = s[2:]
    elif lower_s.startswith("0x"):
        base = 16
        base_name = "十六进制"
        raw = s[2:]
    elif lower_s.startswith("0o"):
        base = 8
        base_name = "八进制"
        raw = s[2:]

    try:
        val = int(raw, base)
        if is_neg:
            val = -val
        return True, val, ""
    except ValueError:
        return False, 0, f"无效的{base_name}格式"


def to_twos_complement_bits(val: int, bit_width: int):
    """转换为对应位宽下的二进制位列表（负数取补码）"""
    mask = (1 << bit_width) - 1
    masked_val = val & mask
    bin_str = f"{masked_val:0{bit_width}b}"
    return list(bin_str)


def calculate_shift(val: int, direction: str, steps: int, bit_width: int):
    """返回 Python 移位结果，以及供固定宽度动画展示的低位。"""
    result = val << steps if direction == "left" else val >> steps
    return result, to_twos_complement_bits(result, bit_width)


class SegmentedChoice(tk.Frame):
    """跨平台高对比度选项切换组件（完美规避 macOS Aqua 按钮文字变白问题）"""

    def __init__(self, parent, options, on_change, default_val="&", **kwargs):
        super().__init__(parent, bg="#CFD8DC", relief="solid", bd=1, **kwargs)
        self.options = options
        self.on_change = on_change
        self.selected_val = default_val
        self.item_labels = []

        for text, val in options:
            lbl = tk.Label(
                self, text=text, font=("Arial", 11, "bold"),
                padx=18, pady=6, cursor="hand2"
            )
            lbl.pack(side="left", padx=1, pady=1)
            lbl.bind("<Button-1>", lambda e, v=val: self._select(v))
            self.item_labels.append((lbl, val))

        self._refresh()

    def _select(self, val):
        self.selected_val = val
        self._refresh()
        self.on_change(val)

    def _refresh(self):
        for lbl, val in self.item_labels:
            if val == self.selected_val:
                lbl.config(bg="#1565C0", fg="#FFFFFF", relief="flat")
            else:
                lbl.config(bg="#ECEFF1", fg="#37474F", relief="flat")


class BitwiseVisualizerApp(tk.Tk):
    """主程序窗口"""

    def __init__(self):
        super().__init__()
        self.title("位运算与移位教学演示工具")
        # 尺寸优化为 860x560，布局饱满不局促
        self.geometry("860x560")
        self.minsize(800, 500)

        # 调色盘
        self.colors = {
            "bg": "#F4F6F9",
            "card": "#FFFFFF",
            "primary": "#1976D2",
            "text": "#212121",
            "muted": "#607D8B",
            # 特征位标红
            "red_bg": "#FFEBEE",
            "red_fg": "#D32F2F",
            "red_bd": "#EF5350",
            # 补零绿色
            "green_bg": "#E8F5E9",
            "green_fg": "#2E7D32",
            "green_bd": "#4CAF50",
            # 墙体棕色
            "wall_bg": "#8D6E63",
            "wall_fg": "#FFFFFF",
            "wall_bd": "#5D4037",
            # 撞墙丢弃
            "discard_bg": "#FFF3E0",
            "discard_fg": "#E65100",
            # 常规格子
            "cell_bg": "#ECEFF1",
            "cell_fg": "#263238",
        }

        self.configure(bg=self.colors["bg"])
        self.bit_width_var = tk.IntVar(value=8)

        self._setup_styles()
        self._build_header()
        self._build_notebook()

        self._on_bit_width_changed()

    def _setup_styles(self):
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("TNotebook", background=self.colors["bg"], borderwidth=0)
        style.configure("TNotebook.Tab", font=("Arial", 11, "bold"), padding=[22, 6],
                        background="#CFD8DC", foreground="#37474F")
        style.map("TNotebook.Tab",
                  background=[("selected", "#FFFFFF")],
                  foreground=[("selected", self.colors["primary"])])

    def _build_header(self):
        """顶部简短控制栏"""
        header = tk.Frame(self, bg=self.colors["card"], relief="ridge", bd=1)
        header.pack(side="top", fill="x", padx=12, pady=(10, 4))

        title = tk.Label(header, text="⚡ 位运算与移位教学演示", font=("Arial", 15, "bold"),
                         bg=self.colors["card"], fg=self.colors["text"])
        title.pack(side="left", padx=16, pady=8)

        bw_frame = tk.Frame(header, bg=self.colors["card"])
        bw_frame.pack(side="right", padx=16, pady=8)

        tk.Label(bw_frame, text="演示位宽: ", font=("Arial", 10, "bold"),
                 bg=self.colors["card"], fg=self.colors["text"]).pack(side="left")

        bw_combo = ttk.Combobox(bw_frame, values=["4 位 (半字节)", "8 位 (1 字节)", "16 位 (2 字节)"],
                                state="readonly", width=14)
        bw_combo.current(1)
        bw_combo.pack(side="left")
        bw_combo.bind("<<ComboboxSelected>>", self._on_bw_select)
        self.bw_combo = bw_combo

    def _on_bw_select(self, event=None):
        idx = self.bw_combo.current()
        self.bit_width_var.set(4 if idx == 0 else (8 if idx == 1 else 16))
        self._on_bit_width_changed()

    def _on_bit_width_changed(self):
        self.tab_logic.update_display()
        self.tab_shift.on_confirm()

    def _build_notebook(self):
        container = tk.Frame(self, bg=self.colors["bg"])
        container.pack(fill="both", expand=True, padx=12, pady=4)

        self.notebook = ttk.Notebook(container)
        self.notebook.pack(fill="both", expand=True)

        # Tab 1
        t1 = tk.Frame(self.notebook, bg=self.colors["bg"])
        self.notebook.add(t1, text="  双数逻辑运算 ( & , | , ^ )  ")
        self.tab_logic = TabLogic(t1, self)

        # Tab 2
        t2 = tk.Frame(self.notebook, bg=self.colors["bg"])
        self.notebook.add(t2, text="  移位运算 ( << , >> 实体墙模型 )  ")
        self.tab_shift = TabShift(t2, self)


# =========================================================================
# Tab 1: 双数逻辑运算 (&, |, ^)
# =========================================================================

class TabLogic:
    def __init__(self, parent, app: BitwiseVisualizerApp):
        self.parent = parent
        self.app = app
        self.current_op = "&"

        self._build_ui()
        self.update_display()

    def _build_ui(self):
        # 1. 顶部输入与运算选择整合区
        top_card = tk.Frame(self.parent, bg=self.app.colors["card"], relief="ridge", bd=1)
        top_card.pack(fill="x", padx=4, pady=6)

        ctrl_row = tk.Frame(top_card, bg=self.app.colors["card"])
        ctrl_row.pack(fill="x", padx=16, pady=8)

        # 数 A
        tk.Label(ctrl_row, text="数 A:", font=("Arial", 12, "bold"),
                 bg=self.app.colors["card"], fg=self.app.colors["text"]).pack(side="left", padx=(0, 4))
        self.entry_a = tk.Entry(ctrl_row, font=("Arial", 12), width=10, relief="solid", bd=1, justify="center")
        self.entry_a.insert(0, "5")
        self.entry_a.pack(side="left", padx=(0, 18))
        self.entry_a.bind("<KeyRelease>", lambda e: self.update_display())

        # 数 B
        tk.Label(ctrl_row, text="数 B:", font=("Arial", 12, "bold"),
                 bg=self.app.colors["card"], fg=self.app.colors["text"]).pack(side="left", padx=(0, 4))
        self.entry_b = tk.Entry(ctrl_row, font=("Arial", 12), width=10, relief="solid", bd=1, justify="center")
        self.entry_b.insert(0, "3")
        self.entry_b.pack(side="left", padx=(0, 24))
        self.entry_b.bind("<KeyRelease>", lambda e: self.update_display())

        # 运算符选项切换栏
        tk.Label(ctrl_row, text="运算:", font=("Arial", 11, "bold"),
                 bg=self.app.colors["card"], fg=self.app.colors["text"]).pack(side="left", padx=(0, 6))

        ops = [
            ("& 按位与", "&"),
            ("| 按位或", "|"),
            ("^ 按位异或", "^")
        ]
        self.op_selector = SegmentedChoice(ctrl_row, ops, self._on_op_change, default_val="&")
        self.op_selector.pack(side="left")

        # 2. 核心大尺寸展示卡片（扩展填满中间主要区域）
        self.grid_card = tk.Frame(self.parent, bg=self.app.colors["card"], relief="ridge", bd=1)
        self.grid_card.pack(fill="both", expand=True, padx=4, pady=4)

        # 简要口诀横幅
        self.lbl_rule = tk.Label(self.grid_card, text="", font=("Arial", 12, "bold"),
                                bg="#E3F2FD", fg="#0D47A1", height=2)
        self.lbl_rule.pack(fill="x", padx=12, pady=(10, 4))

        # 居中超大网格容器
        self.grid_container = tk.Frame(self.grid_card, bg=self.app.colors["card"])
        self.grid_container.pack(fill="both", expand=True, padx=12, pady=6)

        # 3. 底部大字号计算结果行
        self.bottom_bar = tk.Frame(self.grid_card, bg="#FAFAFA", relief="groove", bd=1)
        self.bottom_bar.pack(fill="x", padx=12, pady=(4, 12))

        self.lbl_result = tk.Label(self.bottom_bar, text="", font=("Arial", 15, "bold"),
                                   bg="#FAFAFA", fg=self.app.colors["primary"])
        self.lbl_result.pack(side="left", padx=18, pady=10)

        self.lbl_bin_result = tk.Label(self.bottom_bar, text="", font=("Courier New", 14, "bold"),
                                       bg="#FAFAFA", fg=self.app.colors["text"])
        self.lbl_bin_result.pack(side="right", padx=18, pady=10)

    def _on_op_change(self, op):
        self.current_op = op
        self.update_display()

    def update_display(self):
        ok_a, val_a, err_a = parse_input_number(self.entry_a.get())
        ok_b, val_b, err_b = parse_input_number(self.entry_b.get())
        bit_width = self.app.bit_width_var.get()

        if not (ok_a and ok_b):
            self._render_msg("请输入有效的数字 A 和 B（支持十进制、0b、0x）")
            return

        bits_a = to_twos_complement_bits(val_a, bit_width)
        bits_b = to_twos_complement_bits(val_b, bit_width)

        if self.current_op == "&":
            res_val = val_a & val_b
            rule_text = "【按位与 &】：两者都为 1 结果才为 1，将同为 1 的位标红"
            bg_rule, fg_rule = "#FFEBEE", "#C62828"
        elif self.current_op == "|":
            res_val = val_a | val_b
            rule_text = "【按位或 |】：只要有 1 结果就是 1，将有 1 的位标红"
            bg_rule, fg_rule = "#E8F5E9", "#1B5E20"
        else: # "^"
            res_val = val_a ^ val_b
            rule_text = "【按位异或 ^】：两数不同结果为 1，将对应位不同的位标红"
            bg_rule, fg_rule = "#EDE7F6", "#4A148C"

        self.lbl_rule.config(text=rule_text, bg=bg_rule, fg=fg_rule)
        bits_res = to_twos_complement_bits(res_val, bit_width)

        self._render_grid(bits_a, bits_b, bits_res, bit_width)

        self.lbl_result.config(text=f"计算结果:  {val_a}  {self.current_op}  {val_b}  =  {res_val}")
        self.lbl_bin_result.config(text=f"二进制: 0b{''.join(bits_res)}")

    def _render_msg(self, msg):
        for w in self.grid_container.winfo_children():
            w.destroy()
        tk.Label(self.grid_container, text=msg, font=("Arial", 13),
                 fg="#D32F2F", bg=self.app.colors["card"]).pack(expand=True)
        self.lbl_rule.config(text="", bg="#ECEFF1")
        self.lbl_result.config(text="")
        self.lbl_bin_result.config(text="")

    def _render_grid(self, bits_a, bits_b, bits_res, bit_width):
        for w in self.grid_container.winfo_children():
            w.destroy()

        center_frame = tk.Frame(self.grid_container, bg=self.app.colors["card"])
        center_frame.pack(anchor="center", expand=True)

        # 标签列
        labels = ["权位", "数 A", f"数 B ({self.current_op})", "结果"]
        for idx, text in enumerate(labels):
            r = idx if idx < 3 else idx + 1
            lbl = tk.Label(center_frame, text=text, font=("Arial", 12, "bold"),
                           bg=self.app.colors["card"], fg=self.app.colors["muted"],
                           width=11, anchor="e")
            lbl.grid(row=r, column=0, padx=(0, 12), pady=6)

        # 格子宽度高度进一步大幅强化，彻底消除留白
        if bit_width == 4:
            cell_w, cell_h = 100, 72
            num_font = ("Arial", 30, "bold")
        elif bit_width == 8:
            cell_w, cell_h = 68, 64
            num_font = ("Arial", 26, "bold")
        else: # 16位
            cell_w, cell_h = 42, 50
            num_font = ("Arial", 16, "bold")

        for i in range(bit_width):
            bit_idx = bit_width - 1 - i
            b_a = bits_a[i]
            b_b = bits_b[i]
            b_r = bits_res[i]
            col = i + 1

            # 权位标号 (Bit 序号)
            box_h = tk.Frame(center_frame, bg="#ECEFF1", width=cell_w, height=28, relief="groove", bd=1)
            box_h.grid_propagate(False)
            box_h.grid(row=0, column=col, padx=3, pady=3)
            tk.Label(box_h, text=f"B{bit_idx}", font=("Arial", 9, "bold"),
                     bg="#ECEFF1", fg=self.app.colors["muted"]).pack(expand=True)

            # 教学标红判定
            mark_a, mark_b, mark_r = False, False, False
            if self.current_op == "&":
                if b_a == "1" and b_b == "1":
                    mark_a = mark_b = mark_r = True
            elif self.current_op == "|":
                if b_a == "1": mark_a = True
                if b_b == "1": mark_b = True
                if b_a == "1" or b_b == "1": mark_r = True
            elif self.current_op == "^":
                if b_a != b_b:
                    mark_a = mark_b = mark_r = True

            # 数 A 格子
            self._cell(center_frame, b_a, mark_a, cell_w, cell_h, num_font).grid(row=1, column=col, padx=3, pady=4)
            # 数 B 格子
            self._cell(center_frame, b_b, mark_b, cell_w, cell_h, num_font).grid(row=2, column=col, padx=3, pady=4)
            # 竖式分割线
            sep = tk.Frame(center_frame, height=3, bg=self.app.colors["primary"])
            sep.grid(row=3, column=col, sticky="ew", padx=1, pady=3)
            # 结果格子
            self._cell(center_frame, b_r, mark_r, cell_w, cell_h, num_font, is_res=True).grid(row=4, column=col, padx=3, pady=4)

        # 标签列分割线
        sep_lbl = tk.Frame(center_frame, height=3, bg=self.app.colors["primary"])
        sep_lbl.grid(row=3, column=0, sticky="ew", padx=1, pady=3)

    def _cell(self, parent, val, highlight, w, h, font, is_res=False):
        f = tk.Frame(parent, width=w, height=h, relief="solid", bd=1)
        f.grid_propagate(False)
        if highlight:
            bg, fg, bd = self.app.colors["red_bg"], self.app.colors["red_fg"], self.app.colors["red_bd"]
            f.config(bg=bg, highlightbackground=bd, highlightthickness=2)
        else:
            bg = "#FAFAFA" if is_res else self.app.colors["cell_bg"]
            fg = self.app.colors["cell_fg"]
            f.config(bg=bg)
        tk.Label(f, text=val, font=font, bg=bg, fg=fg).pack(expand=True, fill="both")
        return f


# =========================================================================
# Tab 2: 移位运算 (<<, >> 实体墙模型 + 确定载入 + 移动动画)
# =========================================================================

class TabShift:
    """移位演示：支持确定载入、步进移动动画、超大实体墙体及初始与结果对比"""

    def __init__(self, parent, app: BitwiseVisualizerApp):
        self.parent = parent
        self.app = app

        # 状态变量
        self.initial_val = 5
        self.initial_bits = []
        self.current_bits = []
        self.final_val = None
        self.final_bits = None

        self.discarded_bit = None
        self.discard_dir = None
        self.padded_dir = None

        # 动画控制器
        self.is_animating = False
        self.anim_job = None

        self._build_ui()
        self.on_confirm()

    def _build_ui(self):
        # 1. 顶部控制栏：数值 X + 移动位数 + 确定键 + 左移/右移/重置
        top_card = tk.Frame(self.parent, bg=self.app.colors["card"], relief="ridge", bd=1)
        top_card.pack(fill="x", padx=4, pady=6)

        ctrl_row = tk.Frame(top_card, bg=self.app.colors["card"])
        ctrl_row.pack(fill="x", padx=16, pady=8)

        # 输入 X
        tk.Label(ctrl_row, text="输入数值 X:", font=("Arial", 12, "bold"),
                 bg=self.app.colors["card"], fg=self.app.colors["text"]).pack(side="left", padx=(0, 6))

        self.entry_x = tk.Entry(ctrl_row, font=("Arial", 12), width=10, relief="solid", bd=1, justify="center")
        self.entry_x.insert(0, "5")
        self.entry_x.pack(side="left", padx=(0, 16))
        self.entry_x.bind("<Return>", lambda e: self.on_confirm())

        # 移动位数
        tk.Label(ctrl_row, text="移动位数:", font=("Arial", 12, "bold"),
                 bg=self.app.colors["card"], fg=self.app.colors["text"]).pack(side="left", padx=(0, 6))

        self.entry_steps = tk.Entry(ctrl_row, font=("Arial", 12), width=5, relief="solid", bd=1, justify="center")
        self.entry_steps.insert(0, "1")
        self.entry_steps.pack(side="left", padx=(0, 12))
        self.entry_steps.bind("<Return>", lambda e: self.on_confirm())

        # 确定键 (明确载入并显示二进制)
        self.btn_confirm = tk.Button(
            ctrl_row, text="确定", font=("Arial", 11, "bold"),
            bg="#1976D2", fg="#0D47A1", relief="raised", cursor="hand2", padx=12,
            command=self.on_confirm
        )
        self.btn_confirm.pack(side="left", padx=(0, 18))

        # 左移与右移按钮（触发动画）
        self.btn_left = tk.Button(
            ctrl_row, text="⬅️ 左移 (<<)", font=("Arial", 11, "bold"),
            bg="#E3F2FD", fg="#0D47A1", relief="raised", cursor="hand2", padx=12,
            command=lambda: self.start_shift_animation("left")
        )
        self.btn_left.pack(side="left", padx=6)

        self.btn_right = tk.Button(
            ctrl_row, text="➡️ 右移 (>>)", font=("Arial", 11, "bold"),
            bg="#E3F2FD", fg="#0D47A1", relief="raised", cursor="hand2", padx=12,
            command=lambda: self.start_shift_animation("right")
        )
        self.btn_right.pack(side="left", padx=6)

        # 重置按钮
        self.btn_reset = tk.Button(
            ctrl_row, text="🔄 重置", font=("Arial", 11),
            bg="#ECEFF1", fg="#37474F", relief="groove", cursor="hand2", padx=10,
            command=self.reset_number
        )
        self.btn_reset.pack(side="left", padx=6)

        # 2. 中间大尺寸“实体墙 🧱”舞台（占据核心区域）
        self.stage_card = tk.Frame(self.parent, bg=self.app.colors["card"], relief="ridge", bd=1)
        self.stage_card.pack(fill="both", expand=True, padx=4, pady=4)

        self.stage_container = tk.Frame(self.stage_card, bg=self.app.colors["card"])
        self.stage_container.pack(fill="both", expand=True, padx=10, pady=8)

        # 3. 底部详细对照行（显示初始值、二进制以及运算后的十进制和二进制）
        self.bottom_card = tk.Frame(self.stage_card, bg="#FAFAFA", relief="groove", bd=1)
        self.bottom_card.pack(fill="x", padx=12, pady=(4, 12))

        # 第一行：初始值对照
        row1 = tk.Frame(self.bottom_card, bg="#FAFAFA")
        row1.pack(fill="x", padx=16, pady=(8, 2))

        self.lbl_init_dec = tk.Label(row1, text="初始值: -", font=("Arial", 13, "bold"),
                                     bg="#FAFAFA", fg="#1565C0")
        self.lbl_init_dec.pack(side="left")

        self.lbl_init_bin = tk.Label(row1, text="初始二进制: -", font=("Courier New", 12, "bold"),
                                     bg="#FAFAFA", fg=self.app.colors["muted"])
        self.lbl_init_bin.pack(side="right")

        # 第二行：移位运算结果对照
        row2 = tk.Frame(self.bottom_card, bg="#FAFAFA")
        row2.pack(fill="x", padx=16, pady=(2, 8))

        self.lbl_res_dec = tk.Label(row2, text="运算结果: 等待操作（点击上方左移/右移）", font=("Arial", 13, "bold"),
                                    bg="#FAFAFA", fg=self.app.colors["text"])
        self.lbl_res_dec.pack(side="left")

        self.lbl_res_bin = tk.Label(row2, text="", font=("Courier New", 12, "bold"),
                                    bg="#FAFAFA", fg="#2E7D32")
        self.lbl_res_bin.pack(side="right")

    def on_confirm(self):
        """点击确定键：载入数值并直接在下方显示二进制形式"""
        if self.anim_job:
            self.app.after_cancel(self.anim_job)
            self.anim_job = None
        self.is_animating = False
        self._set_buttons_state(True)

        ok, val, err = parse_input_number(self.entry_x.get())
        if not ok:
            messagebox.showwarning("输入提示", f"数值输入有误: {err}")
            return False

        try:
            steps = int(self.entry_steps.get().strip())
            if steps <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("输入提示", "移动位数必须是大于 0 的整数！")
            return False

        bw = self.app.bit_width_var.get()
        self.initial_val = val
        self.initial_bits = to_twos_complement_bits(val, bw)
        self.current_bits = list(self.initial_bits)

        self.discarded_bit = None
        self.discard_dir = None
        self.padded_dir = None
        self.final_val = None
        self.final_bits = None

        self._render_stage()

        # 更新底部初始状态
        self.lbl_init_dec.config(text=f"初始十进制: {val}")
        self.lbl_init_bin.config(text=f"初始低 {bw} 位: 0b{''.join(self.initial_bits)}")

        self.lbl_res_dec.config(text="移位结果: 就绪，点击【⬅️ 左移】或【➡️ 右移】开始推移", fg=self.app.colors["muted"])
        self.lbl_res_bin.config(text="")
        return True

    def start_shift_animation(self, direction):
        """启动平滑移位动画"""
        if self.is_animating:
            return
        # 每次从当前输入重新载入，避免连点时用上次的位串却仍显示初始值。
        if not self.on_confirm():
            return
        steps = int(self.entry_steps.get().strip())

        self.is_animating = True
        self._set_buttons_state(False)

        # 提示准备开始
        dir_name = "左移" if direction == "left" else "右移"
        self.lbl_res_dec.config(
            text=f"开始推移: 即将连续{dir_name} {steps} 位（每步 0.8 秒）...",
            fg="#E65100"
        )

        # 启动分步推移动画：先停顿 250ms 给出视觉准备，每步间隔 800ms（0.8秒）舒缓演进
        self.anim_job = self.app.after(250, lambda: self._animate_step(direction, current_step=1, total_steps=steps))

    def _animate_step(self, direction, current_step, total_steps):
        """执行单步推移并重绘"""
        bw = self.app.bit_width_var.get()
        if direction == "left":
            discarded = self.current_bits[0]
            self.padded_dir = "right"
            dir_name = "左移"
            op_sym = "<<"
        else:
            discarded = self.current_bits[-1]
            self.padded_dir = "left"
            dir_name = "右移"
            op_sym = ">>"

        self.discarded_bit = discarded
        self.discard_dir = direction

        # Python 的负数右移补符号位；墙内只展示结果的低 bw 位。
        cur_dec, self.current_bits = calculate_shift(self.initial_val, direction, current_step, bw)
        self._render_stage()

        # 动画过程中更新底部提示
        self.lbl_res_dec.config(
            text=f"推移中: 正在执行第 {current_step}/{total_steps} 位{dir_name}...",
            fg="#E65100"
        )
        self.lbl_res_bin.config(text=f"当前低 {bw} 位: 0b{''.join(self.current_bits)}")

        if current_step < total_steps:
            # 800毫秒（0.8秒）后执行下一步动画，舒缓平稳，适合课堂教学细致观察
            self.anim_job = self.app.after(800, lambda: self._animate_step(direction, current_step + 1, total_steps))
        else:
            # 动画结束，展示最终结果
            self.is_animating = False
            self.anim_job = None
            self._set_buttons_state(True)

            self.final_val = cur_dec
            self.final_bits = list(self.current_bits)

            # 最终数学结论
            math_tip = f"{self.initial_val} {op_sym} {total_steps} = {cur_dec}"

            self.lbl_res_dec.config(text=f"运算结果: {math_tip}", fg=self.app.colors["primary"])
            self.lbl_res_bin.config(text=f"结果低 {bw} 位: 0b{''.join(self.final_bits)}", fg="#2E7D32")

    def _set_buttons_state(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.btn_left.config(state=state)
        self.btn_right.config(state=state)
        self.btn_confirm.config(state=state)

    def reset_number(self):
        """重置恢复初始状态"""
        self.on_confirm()

    def _render_stage(self):
        """渲染超大实体墙体与居中二进制队列"""
        for w in self.stage_container.winfo_children():
            w.destroy()

        bw = self.app.bit_width_var.get()
        center_stage = tk.Frame(self.stage_container, bg=self.app.colors["card"])
        center_stage.pack(anchor="center", expand=True)

        if bw == 4:
            cell_w, cell_h = 100, 78
            wall_h = 125
            font_num = ("Arial", 30, "bold")
        elif bw == 8:
            cell_w, cell_h = 66, 72
            wall_h = 120
            font_num = ("Arial", 26, "bold")
        else: # 16位
            cell_w, cell_h = 42, 58
            wall_h = 105
            font_num = ("Arial", 16, "bold")

        # --- 1. 左侧撞墙丢弃指示区 ---
        disc_l_frame = tk.Frame(center_stage, bg=self.app.colors["card"], width=95, height=wall_h)
        disc_l_frame.pack_propagate(False)
        disc_l_frame.pack(side="left", padx=(0, 8))

        tk.Label(disc_l_frame, text="撞左墙丢弃", font=("Arial", 10, "bold"),
                 bg=self.app.colors["card"], fg=self.app.colors["muted"]).pack(anchor="s", pady=(6, 2))

        if self.discard_dir == "left" and self.discarded_bit is not None:
            box_l = tk.Frame(disc_l_frame, bg=self.app.colors["discard_bg"], relief="solid", bd=1,
                             highlightbackground="#D84315", highlightthickness=1)
            box_l.pack(fill="both", expand=True, padx=4, pady=4)
            tk.Label(box_l, text=f"💥 {self.discarded_bit}", font=("Arial", 18, "bold"),
                     bg=self.app.colors["discard_bg"], fg="#D84315").pack(expand=True)
            tk.Label(box_l, text="溢出销毁", font=("Arial", 9, "bold"),
                     bg=self.app.colors["discard_bg"], fg="#BF360C").pack(side="bottom", pady=2)
        else:
            tk.Label(disc_l_frame, text="", bg=self.app.colors["card"]).pack(expand=True)

        # --- 2. 实体【左墙 🧱】---
        wall_l = self._build_wall(center_stage, "🧱\n左\n墙", wall_h)
        wall_l.pack(side="left", padx=2)

        # --- 3. 中间二进制格子队列 ---
        q_frame = tk.Frame(center_stage, bg=self.app.colors["card"], relief="groove", bd=2, padx=4, pady=4)
        q_frame.pack(side="left", padx=8)

        for idx in range(bw):
            bit_val = self.current_bits[idx]
            bit_p = bw - 1 - idx

            col_f = tk.Frame(q_frame, bg=self.app.colors["card"])
            col_f.pack(side="left", padx=3)

            # 序号
            tk.Label(col_f, text=f"B{bit_p}", font=("Arial", 9, "bold"),
                     bg=self.app.colors["card"], fg=self.app.colors["muted"]).pack(pady=(0, 2))

            # 方格
            is_new = False
            if self.padded_dir == "right" and idx == (bw - 1):
                is_new = True
            elif self.padded_dir == "left" and idx == 0:
                is_new = True

            box = tk.Frame(col_f, width=cell_w, height=cell_h, relief="solid", bd=1)
            box.pack_propagate(False)
            box.pack()

            if is_new:
                box.config(bg=self.app.colors["green_bg"],
                           highlightbackground=self.app.colors["green_bd"], highlightthickness=2)
                tk.Label(box, text=bit_val, font=font_num,
                         bg=self.app.colors["green_bg"], fg=self.app.colors["green_fg"]).pack(expand=True)
                fill_bit = "1" if self.padded_dir == "left" and self.initial_val < 0 else "0"
                tk.Label(box, text=f"+{fill_bit}补位", font=("Arial", 9, "bold"),
                         bg=self.app.colors["green_bg"], fg=self.app.colors["green_fg"]).pack(side="bottom", pady=2)
            else:
                box.config(bg=self.app.colors["cell_bg"])
                tk.Label(box, text=bit_val, font=font_num,
                         bg=self.app.colors["cell_bg"], fg=self.app.colors["cell_fg"]).pack(expand=True)

        # --- 4. 实体【右墙 🧱】---
        wall_r = self._build_wall(center_stage, "🧱\n右\n墙", wall_h)
        wall_r.pack(side="left", padx=2)

        # --- 5. 右侧撞墙丢弃指示区 ---
        disc_r_frame = tk.Frame(center_stage, bg=self.app.colors["card"], width=95, height=wall_h)
        disc_r_frame.pack_propagate(False)
        disc_r_frame.pack(side="left", padx=(8, 0))

        tk.Label(disc_r_frame, text="撞右墙丢弃", font=("Arial", 10, "bold"),
                 bg=self.app.colors["card"], fg=self.app.colors["muted"]).pack(anchor="s", pady=(6, 2))

        if self.discard_dir == "right" and self.discarded_bit is not None:
            box_r = tk.Frame(disc_r_frame, bg=self.app.colors["discard_bg"], relief="solid", bd=1,
                             highlightbackground="#D84315", highlightthickness=1)
            box_r.pack(fill="both", expand=True, padx=4, pady=4)
            tk.Label(box_r, text=f"💥 {self.discarded_bit}", font=("Arial", 18, "bold"),
                     bg=self.app.colors["discard_bg"], fg="#D84315").pack(expand=True)
            tk.Label(box_r, text="溢出销毁", font=("Arial", 9, "bold"),
                     bg=self.app.colors["discard_bg"], fg="#BF360C").pack(side="bottom", pady=2)
        else:
            tk.Label(disc_r_frame, text="", bg=self.app.colors["card"]).pack(expand=True)

    def _build_wall(self, parent, text, height):
        wall = tk.Frame(parent, width=42, height=height, bg=self.app.colors["wall_bg"],
                        relief="raised", bd=3, highlightbackground=self.app.colors["wall_bd"], highlightthickness=1)
        wall.pack_propagate(False)
        tk.Label(wall, text=text, font=("Arial", 11, "bold"),
                 bg=self.app.colors["wall_bg"], fg=self.app.colors["wall_fg"]).pack(expand=True)
        return wall


def main():
    app = BitwiseVisualizerApp()
    app.mainloop()

if __name__ == "__main__":
    main()

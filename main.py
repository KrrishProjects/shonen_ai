import threading
import flet as ft
from google import genai

API_KEY = "AIzaSyC2lxp24-81u9HWkLYJ4cV4JcdXIE3CTiU"

client = genai.Client(api_key=API_KEY)


def ask_ai(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text or "No response received."


def main(page: ft.Page):
    page.title = "Shonen AI"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0b0f19"
    page.padding = 0

    chat_sessions = {}
    current_chat = ["Chat 1"]

    messages = ft.Column(
        spacing=16,
        scroll="auto",
        expand=True,
    )

    history_column = ft.Column(
        spacing=8,
        scroll="auto",
    )

    def create_bubble(text, is_user=False):
        return ft.Row(
            alignment=ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START,
            controls=[
                ft.Container(
                    content=ft.Markdown(
                        text,
                        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                        code_theme="atom-one-dark",
                        selectable=True,
                    ),
                    bgcolor="#2563eb" if is_user else "#1e293b",
                    padding=14,
                    border_radius=18,
                    width=300,
                )
            ],
        )

    def load_chat(chat_name):
        current_chat[0] = chat_name
        messages.controls.clear()

        if chat_name in chat_sessions:
            for item in chat_sessions[chat_name]:
                messages.controls.append(item)

        page.update()

    def add_history_button(chat_name):
        history_column.controls.append(
            ft.IconButton(
                icon=ft.Icons.CHAT_BUBBLE_OUTLINE,
                icon_color="white",
                tooltip=chat_name,
                on_click=lambda e, name=chat_name: load_chat(name),
            )
        )

    def new_chat(e=None):
        chat_name = f"Chat {len(chat_sessions) + 1}"
        chat_sessions[chat_name] = []
        current_chat[0] = chat_name

        add_history_button(chat_name)

        messages.controls.clear()
        page.update()

    chat_sessions["Chat 1"] = []
    add_history_button("Chat 1")

    input_box = ft.TextField(
        hint_text="Ask Shonen AI...",
        border_color="transparent",
        bgcolor="#111827",
        color="white",
        cursor_color="white",
        border_radius=28,
        expand=True,
        text_size=15,
        on_submit=lambda e: send_message(e),
    )

    send_button = ft.IconButton(
        icon=ft.Icons.ARROW_UPWARD_ROUNDED,
        icon_color="white",
        bgcolor="#2563eb",
    )

    def finish_ai_response(prompt, typing_indicator):
        try:
            answer = ask_ai(prompt)
        except Exception as ex:
            answer = f"Error: {ex}"

        if typing_indicator in messages.controls:
            messages.controls.remove(typing_indicator)

        ai_bubble = create_bubble(answer)
        messages.controls.append(ai_bubble)

        chat_sessions[current_chat[0]] = messages.controls.copy()

        input_box.disabled = False
        send_button.disabled = False

        page.update()

    def send_message(e):
        prompt = input_box.value.strip()

        if not prompt:
            return

        user_bubble = create_bubble(prompt, True)
        messages.controls.append(user_bubble)

        input_box.value = ""
        input_box.disabled = True
        send_button.disabled = True

        chat_sessions[current_chat[0]] = messages.controls.copy()

        typing_indicator = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            controls=[
                ft.Container(
                    content=ft.Text(
                        "Shonen AI is thinking...",
                        color="gray",
                        italic=True,
                    ),
                    bgcolor="#111827",
                    padding=12,
                    border_radius=18,
                )
            ],
        )

        messages.controls.append(typing_indicator)
        page.update()

        threading.Thread(
            target=finish_ai_response,
            args=(prompt, typing_indicator),
            daemon=True,
        ).start()

    send_button.on_click = send_message

    sidebar = ft.Container(
        width=76,
        bgcolor="#0f172a",
        padding=8,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    ft.Icons.AUTO_AWESOME,
                    color="#60a5fa",
                    size=32,
                ),
                ft.Container(height=16),
                ft.IconButton(
                    icon=ft.Icons.ADD,
                    icon_color="white",
                    bgcolor="#2563eb",
                    tooltip="New Chat",
                    on_click=new_chat,
                ),
                ft.Divider(color="#1e293b"),
                history_column,
            ],
        ),
    )

    top_bar = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(
                    "Shonen AI",
                    size=28,
                    weight="bold",
                    color="white",
                ),
            ],
        ),
        padding=18,
    )

    bottom_bar = ft.Container(
        content=ft.Row(
            controls=[
                input_box,
                send_button,
            ],
        ),
        padding=12,
        bgcolor="#0f172a",
        border_radius=28,
    )

    chat_area = ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[
                "#0b0f19",
                "#111827",
                "#172554",
            ],
        ),
        content=ft.Column(
            controls=[
                top_bar,
                ft.Container(
                    content=messages,
                    expand=True,
                    padding=16,
                ),
                bottom_bar,
            ],
            expand=True,
        ),
    )

    page.add(
        ft.Row(
            controls=[
                sidebar,
                chat_area,
            ],
            expand=True,
            spacing=0,
        )
    )


ft.app(target=main)

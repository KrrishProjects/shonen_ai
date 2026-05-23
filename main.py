import flet as ft
from google import genai

API_KEY = "AIzaSyC2lxp24-81u9HWkLYJ4cV4JcdXIE3CTiU"


def ask_ai(prompt):
    client = genai.Client(api_key=API_KEY)

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

    messages = ft.Column(
        spacing=12,
        expand=True,
        scroll="auto",
    )

    input_box = ft.TextField(
        hint_text="Ask Shonen AI...",
        expand=True,
        bgcolor="#111827",
        color="white",
        border_color="#334155",
        border_radius=20,
    )

    def add_message(text, user=False):
        messages.controls.append(
            ft.Row(
                alignment=ft.MainAxisAlignment.END if user else ft.MainAxisAlignment.START,
                controls=[
                    ft.Container(
                        content=ft.Text(
                            text,
                            color="white",
                            size=15,
                            selectable=True,
                        ),
                        bgcolor="#2563eb" if user else "#1e293b",
                        padding=12,
                        border_radius=16,
                        width=300,
                    )
                ],
            )
        )
        page.update()

    def send_message(e=None):
        prompt = input_box.value.strip()

        if not prompt:
            return

        input_box.value = ""
        add_message(prompt, True)

        loading = ft.Text(
            "Shonen AI is thinking...",
            color="gray",
            italic=True,
        )

        messages.controls.append(loading)
        page.update()

        try:
            answer = ask_ai(prompt)
        except Exception as ex:
            answer = "Error: " + str(ex)

        if loading in messages.controls:
            messages.controls.remove(loading)

        add_message(answer, False)

    send_button = ft.IconButton(
        icon=ft.Icons.SEND,
        icon_color="white",
        bgcolor="#2563eb",
        on_click=send_message,
    )

    sidebar = ft.Container(
        width=70,
        bgcolor="#0f172a",
        padding=10,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    ft.Icons.AUTO_AWESOME,
                    color="#60a5fa",
                    size=30,
                ),
                ft.Container(height=20),
                ft.IconButton(
                    icon=ft.Icons.ADD,
                    icon_color="white",
                    bgcolor="#2563eb",
                    tooltip="New Chat",
                    on_click=lambda e: messages.controls.clear() or page.update(),
                ),
            ],
        ),
    )

    top_bar = ft.Container(
        bgcolor="#0b0f19",
        padding=16,
        content=ft.Text(
            "Shonen AI",
            color="white",
            size=26,
            weight="bold",
        ),
    )

    bottom_bar = ft.Container(
        bgcolor="#0f172a",
        padding=12,
        content=ft.Row(
            controls=[
                input_box,
                send_button,
            ]
        ),
    )

    chat_panel = ft.Container(
        expand=True,
        bgcolor="#0b0f19",
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[
                top_bar,
                ft.Container(
                    content=messages,
                    expand=True,
                    padding=14,
                ),
                bottom_bar,
            ],
        ),
    )

    page.add(
        ft.Row(
            expand=True,
            spacing=0,
            controls=[
                sidebar,
                chat_panel,
            ],
        )
    )


ft.app(target=main)

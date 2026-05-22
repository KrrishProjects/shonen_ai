import flet as ft
from google import genai

API_KEY = "AIzaSyBR8O2jdWyToJMVzV9NJo0BrLUJJyYZSPI"

client = genai.Client(api_key=API_KEY)


def ask_ai(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def main(page: ft.Page):
    page.title = "Shonen AI"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0f0f0f"
    page.padding = 20
    page.scroll = "auto"

    chat = ft.Column(expand=True, scroll="auto")

    user_input = ft.TextField(
        hint_text="Ask Shonen AI...",
        expand=True,
        border_radius=15,
        bgcolor="#1e1e1e",
        color="white",
        border_color="#333333",
    )

    def send_message(e):
        prompt = user_input.value.strip()

        if not prompt:
            return

        chat.controls.append(
            ft.Container(
                content=ft.Text(
                    f"You: {prompt}",
                    color="white",
                    size=16,
                ),
                bgcolor="#1f1f1f",
                padding=10,
                border_radius=12,
            )
        )

        page.update()

        try:
            answer = ask_ai(prompt)

        except Exception as ex:
            answer = f"Error: {ex}"

        chat.controls.append(
            ft.Container(
                content=ft.Text(
                    f"Shonen AI: {answer}",
                    color="white",
                    size=16,
                ),
                bgcolor="#2b2b2b",
                padding=10,
                border_radius=12,
            )
        )

        user_input.value = ""
        page.update()

    send_btn = ft.IconButton(
        icon=ft.Icons.SEND,
        icon_color="orange",
        on_click=send_message,
    )

    page.add(
        ft.Text(
            "Shonen AI",
            size=32,
            weight="bold",
            color="white",
        ),
        ft.Container(chat, expand=True),
        ft.Row(
            [
                user_input,
                send_btn,
            ]
        ),
    )


ft.run(main)

import flet as ft
from google import genai
from PIL import Image

API_KEY = "AIzaSyBR8O2jdWyToJMVzV9NJo0BrLUJJyYZSPI"

client = genai.Client(api_key=API_KEY)


def ask_ai(prompt, image_path=None):
    if image_path:
        img = Image.open(image_path)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                prompt,
                img,
            ],
        )
    else:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

    return response.text


def main(page: ft.Page):
    page.title = "Shonen AI"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0b0f19"
    page.padding = 0

    chat_sessions = {}
    current_chat = ["Chat 1"]
    selected_image = {"path": None}

    messages = ft.Column(
        spacing=20,
        scroll="auto",
        expand=True,
    )

    history_column = ft.Column(
        spacing=10,
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
                    padding=15,
                    border_radius=20,
                    width=320,
                )
            ],
        )

    def create_image_user_bubble(text, image_path):
        image_controls = []

        if image_path:
            image_controls.append(
                ft.Image(
                    src=image_path,
                    width=220,
                    height=160,
                )
            )

        image_controls.append(
            ft.Markdown(
                text,
                extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                code_theme="atom-one-dark",
                selectable=True,
            )
        )

        return ft.Row(
            alignment=ft.MainAxisAlignment.END,
            controls=[
                ft.Container(
                    content=ft.Column(
                        spacing=10,
                        controls=image_controls,
                    ),
                    bgcolor="#2563eb",
                    padding=15,
                    border_radius=20,
                    width=320,
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

    def new_chat(e):
        chat_name = f"Chat {len(chat_sessions) + 1}"

        chat_sessions[chat_name] = []
        current_chat[0] = chat_name
        selected_image["path"] = None

        history_column.controls.append(
            ft.TextButton(
                content=ft.Text(
                    chat_name,
                    color="white",
                ),
                on_click=lambda e, name=chat_name: load_chat(name),
            )
        )

        messages.controls.clear()
        page.update()

    def on_dialog_result(e):
        if e.files:
            file = e.files[0]

            selected_image["path"] = file.path if file.path else None

            if selected_image["path"]:
                messages.controls.append(
                    ft.Container(
                        content=ft.Column(
                            spacing=10,
                            controls=[
                                ft.Text(
                                    "📷 Image selected",
                                    color="gray",
                                    size=13,
                                ),
                                ft.Image(
                                    src=selected_image["path"],
                                    width=220,
                                    height=160,
                                ),
                            ],
                        ),
                        bgcolor="#111827",
                        padding=12,
                        border_radius=18,
                    )
                )
            else:
                messages.controls.append(
                    ft.Container(
                        content=ft.Text(
                            "📷 Image selected. Preview may not be available in web mode.",
                            color="gray",
                            size=13,
                        ),
                        bgcolor="#111827",
                        padding=12,
                        border_radius=18,
                    )
                )

            page.update()


    input_box = ft.TextField(
        hint_text="Ask Shonen AI...",
        border_color="transparent",
        bgcolor="#111827",
        color="white",
        cursor_color="white",
        border_radius=30,
        expand=True,
        text_size=16,
    )

    def send_message(e):
        prompt = input_box.value.strip()

        if not prompt and not selected_image["path"]:
            return

        if not prompt and selected_image["path"]:
            prompt = "Describe this image."

        image_path = selected_image["path"]

        if image_path:
            user_bubble = create_image_user_bubble(prompt, image_path)
        else:
            user_bubble = create_bubble(prompt, True)

        messages.controls.append(user_bubble)

        input_box.value = ""
        chat_sessions[current_chat[0]] = messages.controls.copy()

        typing_indicator = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            controls=[
                ft.Container(
                    content=ft.Text(
                        "Shonen AI is typing...",
                        color="gray",
                        italic=True,
                    ),
                    bgcolor="#111827",
                    padding=12,
                    border_radius=20,
                )
            ],
        )

        messages.controls.append(typing_indicator)
        page.update()

        try:
            answer = ask_ai(prompt, image_path)

        except Exception as ex:
            answer = f"Error: {ex}"

        if typing_indicator in messages.controls:
            messages.controls.remove(typing_indicator)

        ai_bubble = create_bubble(answer)
        messages.controls.append(ai_bubble)

        chat_sessions[current_chat[0]] = messages.controls.copy()

        selected_image["path"] = None

        page.update()

    sidebar = ft.Container(
        width=90,
        bgcolor="#0f172a",
        padding=10,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    ft.Icons.AUTO_AWESOME,
                    color="#60a5fa",
                    size=35,
                ),
                ft.Container(height=20),
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
            ]
        ),
        padding=20,
    )

    bottom_bar = ft.Container(
        content=ft.Row(
            controls=[
ft.IconButton(
    icon=ft.Icons.IMAGE,
    icon_color="gray",
    tooltip="Image upload coming soon",
),
                input_box,
                ft.IconButton(
                    icon=ft.Icons.ARROW_UPWARD_ROUNDED,
                    icon_color="white",
                    bgcolor="#2563eb",
                    on_click=send_message,
                ),
            ]
        ),
        padding=15,
        bgcolor="#0f172a",
        border_radius=30,
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
                    padding=20,
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
        )
    )


ft.app(target=main)

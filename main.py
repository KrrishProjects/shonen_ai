import flet as ft


def main(page: ft.Page):
    page.title = "Shonen AI"
    page.bgcolor = "#0b0f19"
    page.padding = 30

    page.add(
        ft.Column(
            controls=[
                ft.Text(
                    "Shonen AI",
                    size=32,
                    color="white",
                    weight="bold",
                ),
                ft.Text(
                    "Android test build is working.",
                    size=18,
                    color="white",
                ),
            ]
        )
    )


ft.app(target=main)

# Idle Tutor Tycoon

This repository contains the code for *Idle Tutor Tycoon*, a Python/PyGame based idle/tycoon style game built as part of the 2025 Major Work for HSC Software Engineering.

## Prerequisites

- **Python 3.8+** – the game has been tested with Python 3.11.
- **Pip** – Python package manager used to install dependencies.

## Installing Dependencies

The game relies on a few third‑party libraries:

- [`pygame-ce`](https://pypi.org/project/pygame-ce/) – handling graphics, input and sound.
- [`ntplib`](https://pypi.org/project/ntplib/) – synchronising timestamps for save files.
- [`emoji`](https://pypi.org/project/emoji/) – only imported in the code, but not strictly required by gameplay.

Install them using pip:

```bash
pip install pygame-ce ntplib emoji
```

Creating a virtual environment is recommended but optional:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

## Project Structure

```
assets/          Game art, fonts and sounds
savestates/      Save file storage (`save_data.json`)
main.py          Entry point for the game
*.py             Game logic, UI and helper modules
```

The `assets` folder must remain in the same directory as `main.py` so that images, fonts and sounds can be loaded correctly. The game automatically writes progress to `savestates/save_data.json` on exit.

## Running the Game

1. Clone or download this repository.
2. Ensure the dependencies above are installed.
3. From the repository root, run:

```bash
python main.py
```

The game window should open and you can start playing. Progress will be saved when you exit.

## Troubleshooting

- **Missing modules** – If Python reports a module cannot be found (`ModuleNotFoundError`), double‑check the dependencies were installed in the environment you are using.
- **Audio issues** – PyGame tries to initialise the mixer module on start up. Ensure your system has working audio drivers if you encounter errors.
- **Save file location** – If the `savestates` folder is missing, create it manually or run the game once so it can generate `savestates/save_data.json`.

## License

This project was developed for educational purposes. Refer to the repository for asset sources and further information.

